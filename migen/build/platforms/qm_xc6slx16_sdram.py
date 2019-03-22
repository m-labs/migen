from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform


_io = [
    ("user_led", 1, Pins("T9"), IOStandard("LVCMOS33"), Drive(24), Misc("SLEW=QUIETIO")),
    ("user_led", 3, Pins("R9"), IOStandard("LVCMOS33"), Drive(24), Misc("SLEW=QUIETIO")),

    ("clk50", 0, Pins("A10"), IOStandard("LVCMOS33")),

    ("serial", 0,
        Subsignal("tx", Pins("P12"), IOStandard("LVCMOS33"), Misc("SLEW=SLOW")),
        Subsignal("rx", Pins("M11"), IOStandard("LVCMOS33"), Misc("PULLUP"))
    ),

    ("spiflash", 0,
        Subsignal("cs_n", Pins("T3")),
        Subsignal("clk", Pins("R11")),
        Subsignal("mosi", Pins("T10")),
        Subsignal("miso", Pins("P10"), Misc("PULLUP")),
        IOStandard("LVCMOS33"), Misc("SLEW=FAST")
    ),

    ("sdram_clock", 0, Pins("H1"), IOStandard("LVCMOS33"), Misc("SLEW=FAST")),
    ("sdram", 0,
        Subsignal("a", Pins("L4 M3 M4 N3 R2 R1 P2 P1 N1 M1 L3 L1 K1")),
        Subsignal("ba", Pins("K3 K2")),
        Subsignal("cs_n", Pins("J3")),
        Subsignal("cke", Pins("J1")),
        Subsignal("ras_n", Pins("J4")),
        Subsignal("cas_n", Pins("H3")),
        Subsignal("we_n", Pins("G3")),
        Subsignal("dq", Pins("A3 A2 B3 B2 C3 C2 D3 E3 G1 F1 F2 E1 E2 D1 C1 B1")),
        Subsignal("dm", Pins("F3 H2")),
        IOStandard("LVCMOS33"), Misc("SLEW=FAST")
    )
]

_connectors = [
    ("U7", "- - - - - - - E12 E13 B15 B16 C15 C16 D14 D16 E15 E16 F15 F16 G11 F12 " +
    "F14 F13 G16 G14 H15 H16 G12 H11 H13 H14 J14 J16 J11 J12 K14 J13 K15 K16 " +
    "L16 L14 K11 K12 M15 M16 N14 N16 M13 M14 L12 L13 P15 P16 R15 R16 R14 T15 " +
    "T13 T14 T12 R12"),
    ("U8", "- - - - - - - A14 B14 C13 A13 B12 A12 C11 A11 B10 A9 C9 A8 B8 A7 C7 A6 " +
     "B6 A5 B5 A4 E10 C10 E11 F10 F9 D9 C8 D8 E7 E6 F7 C6 D6 M6 P4 N5 P5 N6 M7 " +
     "P6 N8 L7 P9 T4 T5 R5 T6 T7 N9 M9 M10 P11 P12 M11"), #P12 M11 used as serial
]


class Platform(XilinxPlatform):
    default_clk_name = "clk50"
    default_clk_period = 50

    def __init__(self):
        XilinxPlatform.__init__(self, "xc6slx16-ftg256", _io, _connectors)

