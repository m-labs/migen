from migen.build.generic_platform import *
from migen.build.lattice import LatticePlatform
from migen.build.lattice.programmer import IceStormProgrammer


_io = [
    ("user_led", 0, Pins("39"), IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("40"), IOStandard("LVCMOS33")),
    ("user_led", 2, Pins("41"), IOStandard("LVCMOS33")),

    ("user_sw", 0, Pins("23"), IOStandard("LVCMOS33")),
    ("user_sw", 1, Pins("25"), IOStandard("LVCMOS33")),
    ("user_sw", 2, Pins("34"), IOStandard("LVCMOS33")),
    ("user_sw", 3, Pins("43"), IOStandard("LVCMOS33")),

    ("clk12", 0, Pins("35"), IOStandard("LVCMOS33"))
]


class Platform(LatticePlatform):
    default_clk_name = "clk12"
    default_clk_period = 83.333

    def __init__(self):
        LatticePlatform.__init__(self, "ice40-up5k-sg48", _io,
                                 toolchain="icestorm")

    def create_programmer(self):
        return IceStormProgrammer()
