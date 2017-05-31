from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform
from migen.build.xilinx.programmer import Adept



_io = [
    ("clk100", 0, Pins("V12"), IOStandard("LVCMOS33")),

    ("serial", 0,
        Subsignal("tx", Pins("N17")),
        Subsignal("rx", Pins("N18")),

        IOStandard("LVCMOS33"),
        Misc("SLEW=FAST")
    ),

    ("joystick", 0,
        Subsignal("L", Pins("C4")),
        Subsignal("R", Pins("D9")),
        Subsignal("U", Pins("A8")),
        Subsignal("D", Pins("C9")),
        Subsignal("S", Pins("B8")),

        Misc("PULLUP"),
        IOStandard("LVCMOS33")
    ),

    ("dipswitch", 0, Pins("T10"), IOStandard("LVCMOS33"), Misc("PULLUP")),
    ("dipswitch", 1, Pins("T9"), IOStandard("LVCMOS33"), Misc("PULLUP")),
    ("dipswitch", 2, Pins("V9"), IOStandard("LVCMOS33"), Misc("PULLUP")),
    ("dipswitch", 3, Pins("M8"), IOStandard("LVCMOS33"), Misc("PULLUP")),
    ("dipswitch", 4, Pins("N8"), IOStandard("LVCMOS33"), Misc("PULLUP")),
    ("dipswitch", 5, Pins("U8"), IOStandard("LVCMOS33"), Misc("PULLUP")),
    ("dipswitch", 6, Pins("V8"), IOStandard("LVCMOS33"), Misc("PULLUP")),
    ("dipswitch", 7, Pins("T5"), IOStandard("LVCMOS33"), Misc("PULLUP")),

    ("user_led", 0, Pins("U16"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 1, Pins("V16"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 2, Pins("U15"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 3, Pins("V15"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 4, Pins("M11"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 5, Pins("N11"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 6, Pins("R11"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 7, Pins("T11"), IOStandard("LVCMOS33"), Drive(8)),


    ("sevenseg", 0,
        Subsignal("segment7", Pins("T17")),  # A
        Subsignal("segment6", Pins("T18")),  # B
        Subsignal("segment5", Pins("U17")),  # C
        Subsignal("segment4", Pins("U18")),  # D
        Subsignal("segment3", Pins("M14")),  # E
        Subsignal("segment2", Pins("N14")),  # F
        Subsignal("segment1", Pins("L14")),  # G
        Subsignal("segment0", Pins("M13")),  # Dot
        Subsignal("enable0", Pins("P17")),   # EN0
        Subsignal("enable1", Pins("P18")),   # EN1
        Subsignal("enable2", Pins("N15")),   # EN2
        Subsignal("enable3", Pins("N16")),    # EN3

        IOStandard("LVCMOS33")
    ),


    ("vga_out", 0,
        Subsignal("hsync", Pins("N6")),
        Subsignal("vsync", Pins("P7")),
        Subsignal("r", Pins("U7 V7 N7")),
        Subsignal("g", Pins("P8 T6 V6")),
        Subsignal("b", Pins("R7 T7")),

        IOStandard("LVCMOS33"),
        Misc("SLEW=FAST")
    ),

    ("ethernet", 0,
        Subsignal("PhyRstn", Pins("P3")),
        Subsignal("PhyCrs", Pins("N3")),
        Subsignal("PhyCol", Pins("P4")),
        Subsignal("PhyClk25Mhz", Pins("N4")),

        Subsignal("PhyTxd", Pins("U2 U1 T2 T1")),
        Subsignal("PhyTxEn", Pins("L2")),
        Subsignal("PhyTxClk", Pins("L5")),
        Subsignal("PhyTxEr", Pins("P2")),

        Subsignal("PhyRxd", Pins("P1 N2 N1 M3")),
        Subsignal("PhyRxDv", Pins("L1")),
        Subsignal("PhyRxEr", Pins("M1")),
        Subsignal("PhyRxClk", Pins("H4")),

        Subsignal("PhyMdc", Pins("M5")),
        Subsignal("PhyMdio", Pins("L6")),

        IOStandard("LVCMOS33"),
        Misc("SLEW=FAST")

     ),

     ("usb-hid", 0, 
        Subsignal("PS2KeyboardData", Pins("J13")),
        Subsignal("PS2KeyboardClk", Pins("L12")),

        Subsignal("PS2MouseData", Pins("K14")),
        Subsignal("PS2MouseClk", Pins("L13")),

        Subsignal("PicGpio", Pins("L16 H17")),

        IOStandard("LVCMOS33"),
        Misc("SLEW=FAST")
     ),

     ("usb", 0, 
        Subsignal("EppAstb", Pins("H1")),
        Subsignal("EppDstb", Pins("K4")),
        Subsignal("EppWait", Pins("C2")),
        Subsignal("EppDB", Pins("E1 F4 F3 D2 D1 H7 G6 E4")),
        Subsignal("UsbClk", Pins("H2")),
        Subsignal("UsbDir", Pins("F6")),

        Subsignal("UsbWR", Pins("C1")),
        Subsignal("UsbOE", Pins("H6")),

        Subsignal("UsbAdr", Pins("H5 E3")),

        Subsignal("UsbPktend", Pins("D3")),

        Subsignal("UsbFlag", Pins("F5")),
        Subsignal("UsbMode", Pins("F1")),

        IOStandard("LVCMOS33"),
        Misc("SLEW=FAST")
     ),

     ("memory", 0, 
        Subsignal("MemOE", Pins("L18")),
        Subsignal("MemWR", Pins("M16")),
        Subsignal("MemAdv", Pins("H18")),
        Subsignal("MemWait", Pins("V4")),
        Subsignal("MemClk", Pins("R10")),

        Subsignal("RamCS", Pins("L15")),
        Subsignal("RamCRE", Pins("M18")),
        Subsignal("RamUB", Pins("K15")),
        Subsignal("RamLB", Pins("K16")),

        Subsignal("FlashCS", Pins("L17")),
        Subsignal("FlashRp", Pins("T4")),

        Subsignal("QuadSpiFlashCS", Pins("V3")),
        Subsignal("QuadSpiFlashSck", Pins("R15")),

        Subsignal("MemAdr", Pins("K18 K17 J18 J16 G18 G16 H16 H15 H14 H13 F18 F17 K13 K12 E18 E16 G13 H12 D18 D17 G14 F14 C18 C17 F16 F15")),

        Subsignal("QuadSpiFlashDB", Pins("T13")),
        Subsignal("MemDB", Pins("R13 T14 V14 U5 V5 R3 T3 R5 N5 P6 P12 U13 V13 U10 R8 T8")),
        
        IOStandard("LVCMOS33"),
        Misc("SLEW=FAST")
     )
]

_connectors = [
    ("VHDCI", "B2 A2 D6 C6 B3 A3 B4 A4 C5 A5 B6 A6 C7 A7 D8 C8 B9 A9 D11 C11 C10 A10 G9 F9 B11 A11 B12 A12 C13 A13 B14 A14 F13 E13 C15 A15 D14 C14 B16 A16"),
    ("JA", "T12 V12 N10 P11 M10 N9 U11 V11"),
    ("JB", "K2 K1 L4 L3 J3 J1 K3 K5"),
    ("JC", "H3 L7 K6 G3 G1 J7 J6 F2"),
    ("JD", "G11 F10 F11 E11 D12 C12 F12 E12")
]


class Platform(XilinxPlatform):
    default_clk_name = "clk100"
    default_clk_period = 10

    def __init__(self):
        XilinxPlatform.__init__(self, "xc6slx16-csg324", _io, _connectors)

    def create_programmer(self):
        return Adept("Nexys3", 0)
