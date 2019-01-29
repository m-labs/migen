from migen import *
from migen.build.generic_platform import *
from migen.build.lattice import LatticePlatform
from migen.build.lattice.programmer import IceStormProgrammer


_io = [
    ("rgb_led", 0,
        Subsignal("r", Pins("41")),
        Subsignal("g", Pins("40")),
        Subsignal("b", Pins("39")),
        IOStandard("LVCMOS33")
    ),
]

spiflash = [
    # Only usable in PROG FLASH mode - see JP2 header 
    ("spiflash", 0,
        Subsignal("cs_n", Pins("16"), IOStandard("LVCMOS33")),
        Subsignal("clk", Pins("15"), IOStandard("LVCMOS33")),
        Subsignal("mosi", Pins("14"), IOStandard("LVCMOS33")),
        Subsignal("miso", Pins("17"), IOStandard("LVCMOS33")),
    ),
]


_connectors = [

    # JP5's pinout is all Free, except 1 (3.3V) and 2 (GND).
    #         3  4  5  6  7  8  9 10 11 12 13 14 15 16
    ("JP5", "23 25 26 27 32 35 31 37 34 43 36 42 38 28"),
    
    #         1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
    ("JP6", "12 21 13 19 18 11  9  6 44  4  3 48 45 47 46  2"),
]

class MachClock(Module):
    def __init__(self, period, out):
        self.specials += Instance("SB_HFOSC",
                                  i_CLKHFPU=C(1),
                                  i_CLKHFEN=C(1),
                                  o_CLKHF=out
                                  )

class HfoscRouting(Module):
    def __init__(self):
        self.hfosc_used = False  # Only one default clock,
        self.mach_clk_sig = Signal()

    def mk_clk(self, name, clk_period):
        if not self.hfosc_used:
            self.mach_clk_sig.name_override = name
            self.submodules.mclk = MachClock(clk_period, self.mach_clk_sig)
            self.hfosc_used = True
        else:
            raise ConstraintError
        return self.mach_clk_sig

class Platform(LatticePlatform):
    default_clk_name = "sb_hfosc"
    default_clk_period = 48
    
    def __init__(self):
        self.sb_hfosc_routing = HfoscRouting()    # Internal oscillator routing.
        LatticePlatform.__init__(self, "ice40-up5k-sg48", _io, _connectors,
                                 toolchain="icestorm")
        
    def request(self, *args, **kwargs):
        try:
            sig = GenericPlatform.request(self, *args, **kwargs)
        except ConstraintError:
            # ICE40UP5K  internal clock
            if args[0] == "sb_hfosc":
                # Do not add to self.constraint_manager.matched because we
                # don't want this signal to become part of the UCF.
                sig = self.sb_hfosc_routing.mk_clk("sb_hfosc", 48)
        return sig

    def do_finalize(self, f, *args, **kwargs):
        f += self.sb_hfosc_routing.get_fragment()

        # Handle cases where hfosc is default not default.
        if self.default_clk_name != "sb_hfosc":
            GenericPlatform.do_finalize(self, f, *args, **kwargs)

        if self.default_clk_name == "sb_hfosc":
            self.default_clk_period = 48
