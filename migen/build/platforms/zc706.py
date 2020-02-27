from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform


_io = [
    ("clk200", 0,
     Subsignal("p", Pins("H9"), IOStandard("DIFF_SSTL15")),
     Subsignal("n", Pins("G9"), IOStandard("DIFF_SSTL15"))
    ),

    ("user_led", 0, Pins("Y21"), IOStandard("LVCMOS25")),
    ("user_led", 1, Pins("G2"), IOStandard("LVCMOS25")),
    ("user_led", 2, Pins("W21"), IOStandard("LVCMOS25")),
    ("user_led", 3, Pins("A17"), IOStandard("LVCMOS25")),

    ("serial", 0,
             Subsignal("tx", Pins("C19")),
             Subsignal("rx", Pins("D18")),
             IOStandard("LVCMOS18")),
]


class Platform(XilinxPlatform):
    default_clk_name = "clk200"
    default_clk_period = 5  # 200 MHz

    def __init__(self):
        XilinxPlatform.__init__(self, "xc7z045-ffg900-1", _io, toolchain="vivado")
