from migen.build.generic_platform import *
from migen.build.altera import AlteraPlatform
from migen.build.altera.programmer import USBBlaster


_io = [
    ("clk12", 0, Pins("H6"), IOStandard("3.3-V LVTTL")),

    ("user_led", 0, Pins("A8"), IOStandard("3.3-V LVTTL")),
    ("user_led", 1, Pins("A9"), IOStandard("3.3-V LVTTL")),
    ("user_led", 2, Pins("A11"), IOStandard("3.3-V LVTTL")),
    ("user_led", 3, Pins("A10"), IOStandard("3.3-V LVTTL")),
    ("user_led", 4, Pins("B10"), IOStandard("3.3-V LVTTL")),
    ("user_led", 5, Pins("C9"), IOStandard("3.3-V LVTTL")),
    ("user_led", 6, Pins("C10"), IOStandard("3.3-V LVTTL")),
    ("user_led", 7, Pins("D8"), IOStandard("3.3-V LVTTL")),

    ("sw", 0, Pins("E6"), IOStandard("3.3-V LVTTL")),

    ("serial", 0,
        Subsignal("tx", Pins("B4"), IOStandard("3.3-V LVTTL")),
        Subsignal("rx", Pins("A4"), IOStandard("3.3-V LVTTL")),
        Subsignal("rts", Pins("A6"), IOStandard("3.3-V LVTTL")),
        Subsignal("cts", Pins("B5"), IOStandard("3.3-V LVTTL")),
        Subsignal("dtr", Pins("A7"), IOStandard("3.3-V LVTTL")),
        Subsignal("dsr", Pins("B6"), IOStandard("3.3-V LVTTL"))
    ),

    ("sdram_clock", 0, Pins("M9"), IOStandard("3.3-V LVTTL")),
    ("sdram", 0,
        Subsignal("a", Pins("K6 M5 N5 J8 N10 M11 N9 L10 M13 N8 N4 M10 L11 M12")),
        Subsignal("ba", Pins("N6 K8")),
        Subsignal("cs_n", Pins("M4")),
        Subsignal("cke", Pins("M8")),
        Subsignal("ras_n", Pins("M7")),
        Subsignal("cas_n", Pins("N7")),
        Subsignal("we_n", Pins("K7")),
        Subsignal("dq", Pins("D11 G10 F10 F9 E10 D9 G9 F8 F13 E12 E13 D12 C12 B12 B13 A12")),
        Subsignal("dm", Pins("E9 F12")),
        IOStandard("3.3-V LVTTL")
    ),

    ("accelerometer", 0,
        Subsignal("int1", Pins("J5")),
        Subsignal("int1", Pins("L4")),
        Subsignal("mosi", Pins("J7")),
        Subsignal("miso", Pins("K5")),
        Subsignal("clk", Pins("J6")),
        Subsignal("cs_n", Pins("L5")),
        IOStandard("3.3-V LVTTL")
    ),

    ("spiflash", 0,
        Subsignal("cs_n", Pins("B3")),
        Subsignal("clk", Pins("A3")),
        Subsignal("dio0", Pins("A2")),
        Subsignal("dio1", Pins("B2")),
        Subsignal("dio2", Pins("C4")),
        Subsignal("dio3", Pins("B9")),
        IOStandard("3.3-V LVTTL")
    ),

    # J1 connector
    ("gpio_0", 0,
        Pins("D3 E1 C2 C1 D1 E3 F1 E4 H8 K10 H5 H4 J1 J2"),
        IOStandard("3.3-V LVTTL")
    ),

    # J2 connector
    ("gpio_1", 0,
        Pins("L12 J12 J13 K11 K12 J10 H10 H13 G12 B11 G13"),
        IOStandard("3.3-V LVTTL")
    ),

    ("pmod", 0,
        Subsignal("d", Pins("F15 F16 C17 C18 F14 G14 D17 D18")),
        IOStandard("3.3-V LVTTL")
    )
]


class Platform(AlteraPlatform):
    default_clk_name = "clk12"
    default_clk_period = 83.333
    create_rbf = False

    def __init__(self):
        AlteraPlatform.__init__(self, "10M08SAU169C8G", _io)

    def create_programmer(self):
        return USBBlaster()
