import bisect

from migen import *
from migen.build.generic_platform import *
from migen.build.lattice import LatticePlatform

_io = [
]

_connectors = [
    # Pins 1-22
    ("GPIO", "13 14 16 17 20 21 23 25 26 27 28 4 5 8 9 10 11 12"),
]


# Default peripherals.
# Only on AX.
led = [
    ("user_led", 0, Pins("GPIO:0"))
]

serial = [
    ("serial", 0,
        Subsignal("tx", Pins("GPIO:2")),
        Subsignal("rx", Pins("GPIO:3")),
        IOStandard("LVCMOS33")
     )
]


class MachClock(Module):
    # Diamond will complain that the frequency of the oscillator doesn't match
    # if it doesn't match one of the below frequencies. Since we tend to deal
    # with periods in nanoseconds, choose the closest frequency (in MHz)
    # without going over. These numbers were extracted from
    # "MachXO2 sysCLOCK PLL Design and Usage Guide"
    supported_freqs = [
        2.08, 2.15, 2.22, 2.29, 2.38, 2.46, 2.56, 2.66, 2.77, 2.89,
        3.02, 3.17, 3.33, 3.50, 3.69, 3.91, 4.16, 4.29, 4.43, 4.59,
        4.75, 4.93, 5.12, 5.32, 5.54, 5.78, 6.05, 6.33, 6.65, 7.00,
        7.39, 7.82, 8.31, 8.58, 8.87, 9.17, 9.50, 9.85, 10.23, 10.64,
        11.08, 11.57, 12.09, 12.67, 13.30, 14.00, 14.78, 15.65, 15.65, 16.63,
        17.73, 19.00, 20.46, 22.17, 24.18, 26.60, 29.56, 33.25, 38.00, 44.33,
        53.20, 66.50, 88.67, 133.00
    ]

    def __init__(self, period, out):
        self.specials += Instance("OSCH",
                                  p_NOM_FREQ=str(self.nearest_freq(period)),
                                  i_STDBY=C(0),
                                  o_OSC=out
                                  )

    def nearest_freq(self, period):
        i = bisect.bisect_right(self.supported_freqs, 1000.0/period)
        if i:
            return self.supported_freqs[i-1]
        raise ValueError("Clock period out of range for internal oscillator.")


class Platform(LatticePlatform):
    default_clk_name = "osch_clk"
    default_clk_period = 62.5

    def __init__(self):
        self.osch_used = False  # There may be > 1 osch,
        # but there's only one default clk.
        self.osch_routing = Module()    # Internal oscillator routing.
        # Routed during self.do_finalize().
        LatticePlatform.__init__(self, "LCMXO2-1200HC-4SG32C", _io,
                                 _connectors, toolchain="diamond")

    # MachXO2 has an internal clock, which is not exposed as an I/O.
    # To get access to it, we handle a request for the clock specially.
    def request(self, *args, **kwargs):
        try:
            sig = GenericPlatform.request(self, *args, **kwargs)
        except ConstraintError:
            # Do not add to self.constraint_manager.matched because we
            # don't want this signal to become part of the UCF.
            if (args[0] == "osch_clk") and not self.osch_used:
                self.mach_clk_sig = Signal(name_override=args[0])
                self.osch_routing.submodules += \
                    MachClock(self.default_clk_period, self.mach_clk_sig)
                sig = self.mach_clk_sig
                self.osch_used = True
            else:
                raise
        return sig

    def do_finalize(self, f, *args, **kwargs):
        # Still add clock to period constraints even though it is not a pin.
        if self.osch_used and hasattr(self, "default_clk_period"):
            self.add_period_constraint(self.mach_clk_sig,
                                       self.default_clk_period)

        # And lastly, add the oscillator routing so the correct primitive
        # is instantiated.
        f += self.osch_routing.get_fragment()
