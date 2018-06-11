# This file is Copyright (c) 2018 William D. Jones <thor0505@comcast.net>
# This file is Copyright (c) 2018 Caleb Jamison <cbjamo@gmail.com>
# License: BSD

from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform, XC3SProg, VivadoProgrammer

_io = [
    ("user_led", 0, Pins("H5"), IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("J5"), IOStandard("LVCMOS33")),
    ("user_led", 2, Pins("T9"), IOStandard("LVCMOS33")),
    ("user_led", 3, Pins("T10"), IOStandard("LVCMOS33")),

    ("rgb_led", 0,
        Subsignal("r", Pins("G6")),
        Subsignal("g", Pins("F6")),
        Subsignal("b", Pins("E1")),
        IOStandard("LVCMOS33"),
    ),

    ("rgb_led", 1,
        Subsignal("r", Pins("G3")),
        Subsignal("g", Pins("J4")),
        Subsignal("b", Pins("G4")),
        IOStandard("LVCMOS33"),
    ),

    ("rgb_led", 2,
        Subsignal("r", Pins("J3")),
        Subsignal("g", Pins("J2")),
        Subsignal("b", Pins("H4")),
        IOStandard("LVCMOS33"),
    ),

    ("rgb_led", 3,
        Subsignal("r", Pins("K1")),
        Subsignal("g", Pins("H6")),
        Subsignal("b", Pins("K2")),
        IOStandard("LVCMOS33"),
    ),

    ("user_sw", 0, Pins("A8"), IOStandard("LVCMOS33")),
    ("user_sw", 1, Pins("C11"), IOStandard("LVCMOS33")),
    ("user_sw", 2, Pins("C10"), IOStandard("LVCMOS33")),
    ("user_sw", 3, Pins("A10"), IOStandard("LVCMOS33")),

    ("user_btn", 0, Pins("D9"), IOStandard("LVCMOS33")),
    ("user_btn", 1, Pins("C9"), IOStandard("LVCMOS33")),
    ("user_btn", 2, Pins("B9"), IOStandard("LVCMOS33")),
    ("user_btn", 3, Pins("B8"), IOStandard("LVCMOS33")),

    ("clk100", 0, Pins("E3"), IOStandard("LVCMOS33")), # Double Check IOStandard

    ("cpu_reset", 0, Pins("C2"), IOStandard("LVCMOS33")),

    ("serial", 0,
        Subsignal("tx", Pins("D10")),
        Subsignal("rx", Pins("A9")),
        IOStandard("LVCMOS33")),

    ("spi", 0,
        Subsignal("clk", Pins("F1")),
        Subsignal("cs_n", Pins("C1")),
        Subsignal("mosi", Pins("H1")),
        Subsignal("miso", Pins("G1")),
        IOStandard("LVCMOS33"),
    ),

    ("i2c", 0,
        Subsignal("scl", Pins("L18")),
        Subsignal("sda", Pins("M18")),
        Subsignal("scl_pup", Pins("A14")),
        Subsignal("sda_pup", Pins("A13")),
        IOStandard("LVCMOS33"),
    ),


    ("spiflash_4x", 0,  # clock needs to be accessed through STARTUPE2
        Subsignal("cs_n", Pins("L13")),
        Subsignal("dq", Pins("K17", "K18", "L14", "M14")),
        IOStandard("LVCMOS33")
    ),
    ("spiflash_1x", 0,  # clock needs to be accessed through STARTUPE2
        Subsignal("cs_n", Pins("L13")),
        Subsignal("mosi", Pins("K17")),
        Subsignal("miso", Pins("K18")),
        Subsignal("wp", Pins("L14")),
        Subsignal("hold", Pins("M14")),
        IOStandard("LVCMOS33"),
    ),

    ("ddram", 0,
        Subsignal("a", Pins(
            "R2 M6 N4 T1 N6 R7 V6 U7 R8 V7 R6 U6 T6 T8"),
            IOStandard("SSTL135")),
        Subsignal("ba", Pins("R1 P4 P2"), IOStandard("SSTL135")),
        Subsignal("ras_n", Pins("P3"), IOStandard("SSTL135")),
        Subsignal("cas_n", Pins("M4"), IOStandard("SSTL135")),
        Subsignal("we_n", Pins("P5"), IOStandard("SSTL135")),
        Subsignal("cs_n", Pins("U8"), IOStandard("SSTL135")),
        Subsignal("dm", Pins("L1 U1"), IOStandard("SSTL135")),
        Subsignal("dq", Pins(
            "K5 L3 K3 L6 M3 M1 L4 M2 V4 T5 U4 V5 V1 T3 U3 R3"),
            IOStandard("SSTL135"),
            Misc("IN_TERM=UNTUNED_SPLIT_40")),
        Subsignal("dqs_p", Pins("N2 U2"), IOStandard("DIFF_SSTL135")),
        Subsignal("dqs_n", Pins("N1 V2"), IOStandard("DIFF_SSTL135")),
        Subsignal("clk_p", Pins("U9"), IOStandard("DIFF_SSTL135")),
        Subsignal("clk_n", Pins("V9"), IOStandard("DIFF_SSTL135")),
        Subsignal("cke", Pins("N5"), IOStandard("SSTL135")),
        Subsignal("odt", Pins("R5"), IOStandard("SSTL135")),
        Subsignal("reset_n", Pins("K6"), IOStandard("SSTL135")),
        Misc("SLEW=FAST"),
    ),

    ("eth_clocks", 0,
        Subsignal("tx", Pins("H16")),
        Subsignal("rx", Pins("F15")),
        Subsignal("ref_clk", Pins("G18")), # FIXME this is missing in the litex version
        IOStandard("LVCMOS33"),
    ),
    ("eth", 0,
        Subsignal("rst_n", Pins("C16")),
        Subsignal("mdio", Pins("K13")),
        Subsignal("mdc", Pins("F16")),
        Subsignal("dv", Pins("G16")),
        Subsignal("rx_er", Pins("C17")),
        Subsignal("rx_data", Pins("D18 E17 E18 G17")),
        Subsignal("tx_en", Pins("H15")),
        Subsignal("tx_data", Pins("H14 J14 J13 H17")),
        Subsignal("col", Pins("D17")),
        Subsignal("crs", Pins("G14")),
        IOStandard("LVCMOS33"),
    ),
]

_connectors = [
    ("pmoda", 0, "G13 B11 A11 D12 D13 B18 A18 K16"),
    ("pmodb", 0, "E15 E16 D15 C15 J17 J18 K15 J15"),
    ("pmodc", 0, "U12 V12 V10 V11 U14 V14 T13 U13"),
    ("pmodd", 0, "D4 D3 F4 F3 E2 D2 H2 G2"),
    ("ck_io", 0, "V15 U16 P14 T11 R12 T14 T15 T16 N15 M16 V17 U18 R17 P17",
                "F5 D8 C7 E7 D7 D5 B7 B6 E6 E5 A4 A3",
                "U11 V16 M13 R10 R11 R13 R15 P15 R16 N16 N14 U17 T18 R18 P18 N17")
]


class Platform(XilinxPlatform):
    default_clk_name = "clk100"
    default_clk_period = 10.0

    def __init__(self, toolchain="vivado", programmer="vivado"):
        XilinxPlatform.__init__(self, "XC7A35TICSG324-1L", _io,
                                toolchain=toolchain)
        self.toolchain.bitstream_commands = \
            ["set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]"]
        self.toolchain.additional_commands = \
            ["write_cfgmem -force -format bin -interface spix4 -size 16 "
             "-loadbit \"up 0x0 {build_name}.bit\" -file {build_name}.bin"]
        self.programmer = programmer
        self.add_platform_command("set_property INTERNAL_VREF 0.675 [get_iobanks 34]")

    def create_programmer(self):
        if self.programmer == "xc3sprog":
            return XC3SProg("nexys4")
        elif self.programmer == "vivado":
            return VivadoProgrammer(flash_part="n25q128-3.3v-spi-x1_x2_x4")
        else:
            raise ValueError("{} programmer is not supported"
                             .format(self.programmer))
