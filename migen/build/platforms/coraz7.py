from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform


# https://github.com/Digilent/Cora-Z7-10-base-linux/blob/master/src/constraints/Cora-Z7-10-Master.xdc
_io = [
    # FIXME: Though the named IOStandard is specified by the official
    # constraints file, Vivado demands this pin to be of a pair with
    # differential signaling.
    #("clk125", 0, Pins("H16"), IOStandard("LVCMOS33")),

    # LED0: B, G, R
    ("user_led", 0, Pins("L15 G17 N15"), IOStandard("LVCMOS33")),
    # LED1: B, G, R
    ("user_led", 1, Pins("G14 L14 M15"), IOStandard("LVCMOS33")),

    ("user_btn", 0, Pins("D20"), IOStandard("LVCMOS33")),
    ("user_btn", 1, Pins("D19"), IOStandard("LVCMOS33")),

    ("i2c", 0,
        Subsignal("sda", Pins("P15")),
        Subsignal("scl", Pins("P16")),
        IOStandard("LVCMOS33"),
    ),
    ("spi", 0,
        Subsignal("miso", Pins("W15")),
        Subsignal("mosi", Pins("T12")),
        Subsignal("clk", Pins("H15")),
        Subsignal("cs_n", Pins("F16")),
        IOStandard("LVCMOS33"),
    ),
]

_connectors = [
    ("pmoda", "Y18 Y19 Y16 Y17 U18 U19 W18 W19"),
    ("pmodb", "W14 Y14 T11 T10 V16 W16 V12 W13"),
    ("crypto_sda", "J15"),
    ("user_dio", "L19 M19 N20 P20 P19 R19 T20 T19 U20 V20 W20 K19"),
    ("ck_io", "U14 V13 T14 T15 V17 V18 R17 R14 N18 M18 U15 K18 J18 G15 R16 U12 U13 V15 T16 U17 T17 R18 P18 N17 M17 L17 H17 H18 G18 L20"),
]

DEVICE_VARIANTS = {
    "07s": "xc7z007s-clg400-1",
    "10": "xc7z010-clg400-1",
}

# Digilent Cora Z7-07S, and Z7-10
class Platform(XilinxPlatform):
    # default_clk_name = "sys_clk"
    # default_clk_period = 20

    def __init__(self, device_variant="10"):
        device = DEVICE_VARIANTS[device_variant]
        XilinxPlatform.__init__(self, device, _io, _connectors, toolchain="vivado")
