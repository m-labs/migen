from migen.build.generic_platform import *
from migen.build.lattice import LatticePlatform
from migen.build.lattice.programmer import IceBurnProgrammer


_io = [
    ("user_led", 0, Pins("59"), IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("56"), IOStandard("LVCMOS33")),
    ("user_led", 2, Pins("53"), IOStandard("LVCMOS33")),
    ("user_led", 3, Pins("51"), IOStandard("LVCMOS33")),

    ("user_btn", 0, Pins("60"), IOStandard("LVCMOS33")),
    ("user_btn", 1, Pins("57"), IOStandard("LVCMOS33")),
    ("user_btn", 2, Pins("54"), IOStandard("LVCMOS33")),
    ("user_btn", 3, Pins("52"), IOStandard("LVCMOS33")),

    ("clk3p3", 0, Pins("13"), IOStandard("LVCMOS33"))
]


class Platform(LatticePlatform):
    default_clk_name = "clk3p3"
    default_clk_period = 303.0303

    def __init__(self):
        LatticePlatform.__init__(self, "ice40-hx1k-vq100", _io,
                                 toolchain="icestorm")

    def create_programmer(self, iceburn_path="./iCEburn.py"):
        return IceBurnProgrammer(iceburn_path)
