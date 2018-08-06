import bisect

from migen import *
from migen.build.generic_platform import *
from migen.build.lattice import LatticePlatform

_connectors = [
    # Pins 1-22
    ("GPIO", "13 14 16 17 20 21 23 25 26 27 28 4 5 8 9 10 11 12"),
]


# Default peripherals.
# Only on AX.
led = [
    ("user_led", 0, Pins("GPIO:0"), IOStandard("LVCMOS33"))
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
    # within +/-5%. These numbers were extracted from
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
        freq_str = "{:.2f}".format(self.nearest_freq(period))
        self.specials += Instance("OSCH",
                                  p_NOM_FREQ=freq_str,
                                  i_STDBY=C(0),
                                  o_OSC=out
                                  )

    def nearest_freq(self, period):
        target_freq = 1000.0/period

        # A None match is defined to not be in range. Handles special cases
        # described below.
        def in_range(actual, err=0.05):
            return abs((target_freq - actual)/target_freq) <= err if actual else False

        # Agreed-upon algorithm:
        # https://github.com/m-labs/migen/pull/111#discussion_r189687411
        i = bisect.bisect_right(self.supported_freqs, target_freq)

        # Special case: desired freq was < 2.08, but could still within +5%
        lo_match = self.supported_freqs[i-1] if i else None

        # Special case: desired freq was > 133.00, but could still within -5%
        hi_match = self.supported_freqs[i] if i < len(self.supported_freqs) else None

        if in_range(lo_match):
            selected_freq = lo_match
        elif in_range(hi_match):
            selected_freq = hi_match
        else:
            raise ValueError("Clock period out of range (-/+5%) for internal oscillator.")

        return selected_freq


class OschRouting(Module):
    def __init__(self):
        self.osch_used = False  # Only one default clock,
        # even if > 1 OSCH is possible, so run only once.
        self.mach_clk_sig = Signal()

    def mk_clk(self, name, clk_period):
        if not self.osch_used:
            self.mach_clk_sig.name_override = name
            self.submodules.mclk = MachClock(clk_period, self.mach_clk_sig)
            self.osch_used = True
        else:
            raise ConstraintError
        return self.mach_clk_sig


class Platform(LatticePlatform):
    default_clk_name = "osch_clk"
    default_clk_period = 1000.0/15.6

    def __init__(self):
        self.osch_clk_period = 1000.0/15.65
        self.osch_routing = OschRouting()    # Internal oscillator routing.
        # Routed during self.do_finalize().
        LatticePlatform.__init__(self, "LCMXO2-1200HC-4SG32C", [],
                                 _connectors, toolchain="diamond")

    # MachXO2 has an internal clock, which is not exposed as an I/O.
    # To get access to it, we handle a request for the clock specially.
    def request(self, *args, **kwargs):
        try:
            sig = GenericPlatform.request(self, *args, **kwargs)
        except ConstraintError:
            if args[0] == "osch_clk":
                # Do not add to self.constraint_manager.matched because we
                # don't want this signal to become part of the UCF.
                sig = self.osch_routing.mk_clk("osch_clk",
                                               self.osch_clk_period)
        return sig

    def do_finalize(self, f, *args, **kwargs):
        # Still add clock to period constraints even though it is not a pin.
        # The constraint reflects the actual frequency chosen plus 5% as a
        # worst case, per MachXO2 oscillator tolerances (+/- 5%, which is
        # unrelated to the +/- 5% error in the frequency selection algorithm).
        # This approach is specified by Lattice:
        # http://www.latticesemi.com/en/Support/AnswerDatabase/4/0/7/4072
        #
        # If the higher of the two closest frequencies to desired was chosen,
        # the constraint will be up to 10% higher than the desired frequency
        # due to the combination of oscillator tolerance and the frequency
        # selection algorithm. If the lower closest frequency was chosen, the
        # constraint will be up to 5% higher than the desired frequency.
        if self.osch_routing.osch_used and hasattr(self, "osch_clk_period"):
            adjusted_freq = 1.05 * \
                self.osch_routing.mclk.nearest_freq(self.osch_clk_period)
            self.add_internal_clock_constraint(self.osch_routing.mach_clk_sig,
                                               1000.0/adjusted_freq)

        # And lastly, add the oscillator routing so the correct primitive
        # is instantiated.
        f += self.osch_routing.get_fragment()

        # Handle cases where OSCH is either not used or not default.
        if self.default_clk_name != "osch_clk":
            GenericPlatform.do_finalize(self, f, *args, **kwargs)

    def set_osch_period(self, period):
        # osch_clk_period is the variable used to set the OSCH period.
        # If default_clk_name == "osch_clk", default_clk_period should _also_
        # be set to osch_clk_period for consistency with the rest of Migen,
        # which may look for a class variable called default_clk_name.
        self.osch_clk_period = period

        if self.default_clk_name == "osch_clk":
            self.default_clk_period = period

    def add_internal_clock_constraint(self, clk, period):
        # Normally clocks are routed from I/O pins and are thus treated as
        # PORTs. However, for internally generated clocks, they need to be
        # specified as NETs.
        self.add_platform_command("""FREQUENCY NET "{{clk}}" {freq} MHz;""".format(freq=float(1/period)*1000, clk="clk"), clk=clk)
