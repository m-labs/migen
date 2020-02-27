from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform


# https://github.com/Digilent/Cora-Z7-10-base-linux/blob/master/src/constraints/Cora-Z7-10-Master.xdc
_io = [
    ("sys_clk", 0, Pins("H16"), IOStandard("LVCMOS33")),

    # LED0: B, G, R
    ("user_led", 0, Pins("L15 G17 N15"), IOStandard("LVCMOS33")),
    # LED1: B, G, R
    ("user_led", 1, Pins("G14 L14 M15"), IOStandard("LVCMOS33")),

    ("user_btn", 0, Pins("D20"), IOStandard("LVCMOS33")),
    ("user_btn", 1, Pins("D19"), IOStandard("LVCMOS33")),

    # A
    ("pmod", 0, Pins("Y18 Y19 Y16 Y17 U18 U19 W18 W19"), IOStandard("LVCMOS33")),
    # B
    ("pmod", 1, Pins("W14 Y14 T11 T10 V16 W16 V12 W13"), IOStandard("LVCMOS33")),

    ("crypto_sda", 0, Pins("J15"), IOStandard("LVCMOS33")),

    ("user_dio", 1, Pins("L19"), IOStandard("LVCMOS33")),
    ("user_dio", 2, Pins("M19"), IOStandard("LVCMOS33")),
    ("user_dio", 3, Pins("N20"), IOStandard("LVCMOS33")),
    ("user_dio", 4, Pins("P20"), IOStandard("LVCMOS33")),
    ("user_dio", 5, Pins("P19"), IOStandard("LVCMOS33")),
    ("user_dio", 6, Pins("R19"), IOStandard("LVCMOS33")),
    ("user_dio", 7, Pins("T20"), IOStandard("LVCMOS33")),
    ("user_dio", 8, Pins("T19"), IOStandard("LVCMOS33")),
    ("user_dio", 9, Pins("U20"), IOStandard("LVCMOS33")),
    ("user_dio", 10, Pins("V20"), IOStandard("LVCMOS33")),
    ("user_dio", 11, Pins("W20"), IOStandard("LVCMOS33")),
    ("user_dio", 12, Pins("K19"), IOStandard("LVCMOS33")),
]


class Platform(XilinxPlatform):
    default_clk_name = "sys_clk"
    default_clk_period = 8

    def __init__(self):
        XilinxPlatform.__init__(self, "xc7z007s-clg400-1", _io, toolchain="vivado")
