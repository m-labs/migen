from migen.build.generic_platform import Pins, IOStandard, Subsignal
from migen.build.altera import AlteraPlatform
from migen.build.altera.programmer import USBBlaster


_io = [
    ("clk1_50", 0, Pins("V11"), IOStandard("3.3-V LVTTL")),
    ("clk2_50", 0, Pins("Y13"), IOStandard("3.3-V LVTTL")),
    ("clk3_50", 0, Pins("E11"), IOStandard("3.3-V LVTTL")),

    ("user_led", 0, Pins("W15"), IOStandard("3.3-V LVTTL")),
    ("user_led", 1, Pins("AA24"), IOStandard("3.3-V LVTTL")),
    ("user_led", 2, Pins("V16"), IOStandard("3.3-V LVTTL")),
    ("user_led", 3, Pins("V15"), IOStandard("3.3-V LVTTL")),
    ("user_led", 4, Pins("AF26"), IOStandard("3.3-V LVTTL")),
    ("user_led", 5, Pins("AE26"), IOStandard("3.3-V LVTTL")),
    ("user_led", 6, Pins("Y16"), IOStandard("3.3-V LVTTL")),
    ("user_led", 7, Pins("AA23"), IOStandard("3.3-V LVTTL")),

    ("key", 0, Pins("AH17"), IOStandard("3.3-V LVTTL")),
    ("key", 1, Pins("AH16"), IOStandard("3.3-V LVTTL")),

    ("sw", 0, Pins("L10"), IOStandard("3.3-V LVTTL")),
    ("sw", 1, Pins("L9"), IOStandard("3.3-V LVTTL")),
    ("sw", 2, Pins("H6"), IOStandard("3.3-V LVTTL")),
    ("sw", 3, Pins("H5"), IOStandard("3.3-V LVTTL")),

    ("epcs", 0,
        Subsignal("data0", Pins("AD7")),
        Subsignal("data1", Pins("AC6")),
        Subsignal("data2", Pins("AC5")),
        Subsignal("data3", Pins("AB6")),
        Subsignal("dclk", Pins("AA8")),
        Subsignal("ncso", Pins("AA6")),
        IOStandard("3.3-V LVTTL")
    ),

    ("adc", 0,
        Subsignal("convst", Pins("U9")),
        Subsignal("sck", Pins("V10")),
        Subsignal("sdi", Pins("AC4")),
        Subsignal("sdo", Pins("AD4")),
        IOStandard("3.3-V LVTTL")
    ),

    ("gpio_0", 0,
        Pins("V12 AF7 W12 AF8 Y8 AB4 W8 Y4 Y5 U11 T8 T12 AH5 AH6 AH4 AG5 AH3",
             "AH2 AF4 AG6 AF5 AE4 T13 T11 AE7 AF6 AF9 AE8 AD10 AE9 AD11 AF10",
             "AD12 AE11 AF11 AE12"),
        IOStandard("3.3-V LVTTL")
    ),

    ("gpio_1", 0,
        Pins("Y15 AG28 AA15 AH27 AG26 AH24 AF23 AE22 AF21 AG20 AG19 AF20",
             "AC23 AG18 AH26 AA19 AG24 AF25 AH23 AG23 AE19 AF18 AD19 AE20",
             "AE24 AD20 AF22 AH22 AH19 AH21 AG21 AH18 AD23 AE23 AA18 AC22"),
        IOStandard("3.3-V LVTTL")
    ),

    ("arduino", 0,
        Subsignal("gpio",
            Pins("AG13 AF13 AG10 AG9 U14 U13 AG8 AH8 AF17 AE15 AF15 AG16 AH11",
                 "AH12 AH9 AG11")),
        Subsignal("reset", Pins("AH7")),
        IOStandard("3.3-V LVTTL")
    ),

    ("hps", 0,
        Subsignal("key", Pins("J18"), IOStandard("3.3-V LVTTL")),
        Subsignal("led", Pins("A20"), IOStandard("3.3-V LVTTL")),

        Subsignal("eth",
            Subsignal("tx_en", Pins("A12")),
            Subsignal("tx_data", Pins("A16 J14 A15 D17")),
            Subsignal("rx_dv", Pins("J13")),
            Subsignal("rx_data", Pins("A14 A11 C15 A9")),
            Subsignal("reset_n", Pins("B4")),
            Subsignal("mdio", Pins("E16")),
            Subsignal("mdc", Pins("A13")),
            Subsignal("int_n", Pins("B14")),
            IOStandard("3.3-V LVTTL")
        ),

        Subsignal("eth_clocks",
            Subsignal("rx", Pins("J12")),
            Subsignal("gtx", Pins("J15")),
            IOStandard("3.3-V LVTTL")
        ),

        Subsignal("serial",
            Subsignal("rx", Pins("A22")),
            Subsignal("tx", Pins("B21")),
            Subsignal("conv_usb_n", Pins("C6")),
            IOStandard("3.3-V LVTTL")
        ),

        Subsignal("sd",
            Subsignal("clk", Pins("B8")),
            Subsignal("cmd", Pins("D14")),
            Subsignal("data", Pins("C13 B6 B11 B9")),
            IOStandard("3.3-V LVTTL")
        ),

        Subsignal("usb",
            Subsignal("clkout", Pins("G4")),
            Subsignal("data", Pins("C10 F5 C9 C4 C8 D4 C7 F4")),
            Subsignal("dir", Pins("E5")),
            Subsignal("nxt", Pins("D5")),
            Subsignal("reset", Pins("H12")),
            Subsignal("stp", Pins("C5")),
            IOStandard("3.3-V LVTTL")
        ),

        Subsignal("gsensor_int", Pins("A17"), IOStandard("3.3-V LVTTL")),
        Subsignal("i2c0",
            Subsignal("sclk", Pins("C18")),
            Subsignal("sdat", Pins("A19")),
            IOStandard("3.3-V LVTTL")
        ),

        Subsignal("ltc_gpio", Pins("H13"), IOStandard("3.3-V LVTTL")),
        Subsignal("i2c1",
            Subsignal("sclk", Pins("B21")),
            Subsignal("sdat", Pins("A21")),
            IOStandard("3.3-V LVTTL")
        ),
        Subsignal("spim",
            Subsignal("clk", Pins("C19")),
            Subsignal("miso", Pins("B19")),
            Subsignal("mosi", Pins("B16")),
            Subsignal("ss", Pins("C16")),
            IOStandard("3.3-V LVTTL")
        ),

        Subsignal("ddram",
            Subsignal("a",
                      Pins("C28 B28 E26 D26 J21 J20 C26 B26",
                           "F26 F25 A24 B24 D24 C24 G23"),
                      IOStandard("SSTL-15 Class I")),
            Subsignal("ba", Pins("A27 H25 G25"),
                      IOStandard("SSTL-15 Class I")),
            Subsignal("cas_n", Pins("A26"),
                      IOStandard("SSTL-15 Class I")),
            Subsignal("cke", Pins("L28"),
                      IOStandard("SSTL-15 Class I")),
            Subsignal("ck_n", Pins("N20"),
                      IOStandard("Differential 1.5-V SSTL Class I")),
            Subsignal("ck_p", Pins("N21"),
                      IOStandard("Differential 1.5-V SSTL Class I")),
            Subsignal("cs_n", Pins("L21"),
                      IOStandard("SSTL-15 Class I")),
            Subsignal("dm", Pins("G28 P28 W28 AB28"),
                      IOStandard("SSTL-15 Class I")),
            Subsignal("dq",
                      Pins("J25 J24 E28 D27 J26 K26 G27 F28 K25 L25 J27",
                           "J28 M27 M26 M28 N28 N24 N25 T28 U28 N26 N27",
                           "R27 V27 R26 R25 AA28 W26 R24 T24 Y27 AA27"),
                      IOStandard("SSTL-15 Class I")),
            Subsignal("dqs_n", Pins("R16 R18 T18 T20"),
                      IOStandard("Differential 1.5-V SSTL Class I")),
            Subsignal("dqs_p", Pins("R17 R19 T19 U19"),
                      IOStandard("Differential 1.5-V SSTL Class I")),
            Subsignal("odt", Pins("D28"), IOStandard("SSTL-15 Class I")),
            Subsignal("ras_n", Pins("A25"), IOStandard("SSTL-15 Class I")),
            Subsignal("reset_n", Pins("V28"), IOStandard("SSTL-15 Class I")),
            Subsignal("we_n", Pins("E25"), IOStandard("SSTL-15 Class I")),
            Subsignal("rzq", Pins("D25"), IOStandard("SSTL-15 Class I"))),
    ),
]


class Platform(AlteraPlatform):
    default_clk_name = "clk1_50"
    default_clk_period = 20

    def __init__(self):
        AlteraPlatform.__init__(self, "5CSEMA4U23C6", _io)

    def create_programmer(self):
        return USBBlaster(cable_name="DE-SoC", device_id=2)
