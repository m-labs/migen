from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform

_io_v1_0 = [
    ("user_led", 0, Pins("T16"), IOStandard("LVCMOS25")),  # LED_USER1

    ("clk50", 0, Pins("W19"), IOStandard("LVCMOS25")),

    ("serial", 0,
        Subsignal("rx", Pins("N13")),  # FPGA input, schematics TxD_2V5
        Subsignal("tx", Pins("N17")),  # FPGA output, schematics RxD_2V5
        IOStandard("LVCMOS25")
    ),

    ("clk_sel", 0, Pins("F21"), IOStandard("LVCMOS25")),

    ("vusb_present", 0, Pins("M17"), IOStandard("LVCMOS25")),

    ("sfp_ctl", 0,
        Subsignal("mod_def1", Pins("U7")),
        Subsignal("mod_def2", Pins("T3")),
        Subsignal("los", Pins("P15")),
        Subsignal("mod_present", Pins("U16")),
        Subsignal("rate_select", Pins("N15")),
        Subsignal("tx_disable", Pins("R14")),
        Subsignal("tx_fault", Pins("N14")),
        Subsignal("led", Pins("P16")),
        IOStandard("LVCMOS25")
    ),
    ("sfp_ctl", 1,
        Subsignal("mod_def1", Pins("P17")),
        Subsignal("mod_def2", Pins("U18")),
        Subsignal("los", Pins("R18")),
        Subsignal("mod_present", Pins("W20")),
        Subsignal("rate_select", Pins("T18")),
        Subsignal("tx_disable", Pins("R17")),
        Subsignal("tx_fault", Pins("U17")),
        Subsignal("led", Pins("R19")),
        IOStandard("LVCMOS25")
    ),
    ("sfp_ctl", 2,
        Subsignal("mod_def1", Pins("P14")),
        Subsignal("mod_def2", Pins("P20")),
        Subsignal("los", Pins("V22")),
        Subsignal("mod_present", Pins("T21")),
        Subsignal("rate_select", Pins("T20")),
        Subsignal("tx_disable", Pins("U21")),
        Subsignal("tx_fault", Pins("R16")),
        Subsignal("led", Pins("P19")),
        IOStandard("LVCMOS25")
    ),
]


_io_v1_1 = [
    ("user_led", 0, Pins("N17"), IOStandard("LVCMOS25")),  # LED_USER1
    ("user_led", 1, Pins("V22"), IOStandard("LVCMOS25")),  # LED_USER2
    ("user_led", 2, Pins("T21"), IOStandard("LVCMOS25")),  # LED_USER3

    ("serial", 0,
        Subsignal("rx", Pins("M17")),  # FPGA input, schematics TxD_2V5
        Subsignal("tx", Pins("T16")),  # FPGA output, schematics RxD_2V5
        IOStandard("LVCMOS25")
    ),

    ("vusb_present", 0, Pins("N13"), IOStandard("LVCMOS25")),

    ("sfp_ctl", 0,
        Subsignal("los", Pins("N15")),
        Subsignal("mod_present_n", Pins("P16")),
        Subsignal("rate_select", Pins("R14")),
        Subsignal("rate_select1", Pins("P15")),
        Subsignal("tx_disable", Pins("N14")),
        Subsignal("tx_fault", Pins("U7")),
        Subsignal("led", Pins("U16")),
        IOStandard("LVCMOS25")
    ),

    ("sfp_ctl", 1,
        Subsignal("los", Pins("T18")),
        Subsignal("mod_present_n", Pins("P17")),
        Subsignal("rate_select", Pins("U18")),
        Subsignal("rate_select1", Pins("R18")),
        Subsignal("tx_disable", Pins("R17")),
        Subsignal("tx_fault", Pins("U17")),
        Subsignal("led", Pins("R19")),
        IOStandard("LVCMOS25")
    ),

    ("sfp_ctl", 2,
        Subsignal("los", Pins("R16")),
        Subsignal("mod_present_n", Pins("T20")),
        Subsignal("rate_select", Pins("P14")),
        Subsignal("rate_select1", Pins("U21")),
        Subsignal("tx_disable", Pins("P20")),
        Subsignal("tx_fault", Pins("P19")),
        Subsignal("led", Pins("W20")),
        IOStandard("LVCMOS25")
    ),
]


_io_common = [
    ("i2c", 0,
        Subsignal("scl", Pins("J16")),
        Subsignal("sda", Pins("F15")),
        IOStandard("LVCMOS25")
    ),

    ("spiflash", 0,
        Subsignal("cs_n", Pins("T19")),
        Subsignal("dq", Pins("P22 R22 P21 R21")),
        # "clk" is on CCLK
        IOStandard("LVCMOS25")
    ),
    ("spiflash2x", 0,
        Subsignal("cs_n", Pins("T19")),
        Subsignal("dq", Pins("P22 R22")),
        Subsignal("wp", Pins("P21")),
        Subsignal("hold", Pins("R21")),
        # "clk" is on CCLK
        IOStandard("LVCMOS25")
    ),

    ("clk125_gtp", 0,
        Subsignal("p", Pins("F10")),
        Subsignal("n", Pins("E10")),
    ),

    ("si5324_clkin", 0,
        Subsignal("p", Pins("U20")),
        Subsignal("n", Pins("V20")),
        IOStandard("LVDS_25"),
    ),

    ("si5324_clkout", 0,
        Subsignal("p", Pins("F6")),
        Subsignal("n", Pins("E6")),
    ),

    ("si5324_clkout_fabric", 0,
        Subsignal("p", Pins("Y18")),
        Subsignal("n", Pins("Y19")),
        IOStandard("LVDS_25"),
    ),

    ("sfp", 0,
        Subsignal("txp", Pins("B4")),
        Subsignal("txn", Pins("A4")),
        Subsignal("rxp", Pins("B8")),
        Subsignal("rxn", Pins("A8")),
    ),
    ("sfp", 1,
        Subsignal("txp", Pins("D5")),
        Subsignal("txn", Pins("C5")),
        Subsignal("rxp", Pins("D11")),
        Subsignal("rxn", Pins("C11")),
    ),
    ("sfp", 2,
        Subsignal("txp", Pins("B6")),
        Subsignal("txn", Pins("A6")),
        Subsignal("rxp", Pins("B10")),
        Subsignal("rxn", Pins("A10")),
    ),
    ("sata", 0,
        Subsignal("txp", Pins("D7")),
        Subsignal("txn", Pins("C7")),
        Subsignal("rxp", Pins("D9")),
        Subsignal("rxn", Pins("C9")),
    ),

    ("ddram", 0,
        Subsignal("a", Pins(
            "L6 M5 P6 K6 M1 M3 N2 M6 "
            "P1 P2 L4 N5 L3 R1 N3"),
            IOStandard("SSTL15")),
        Subsignal("ba", Pins("L5 M2 N4"), IOStandard("SSTL15")),
        Subsignal("ras_n", Pins("J4"), IOStandard("SSTL15")),
        Subsignal("cas_n", Pins("J6"), IOStandard("SSTL15")),
        Subsignal("we_n", Pins("K3"), IOStandard("SSTL15")),
        # Subsignal("cs_n", Pins(""), IOStandard("SSTL15")),
        Subsignal("dm", Pins("G2 E2"), IOStandard("SSTL15")),
        Subsignal("dq", Pins(
            "G3 J1 H4 H5 H2 K1 H3 J5 "
            "G1 B1 F1 F3 C2 A1 D2 B2"),
            IOStandard("SSTL15"),
            Misc("IN_TERM=UNTUNED_SPLIT_50")),
        Subsignal("dqs_p", Pins("K2 E1"), IOStandard("DIFF_SSTL15")),
        Subsignal("dqs_n", Pins("J2 D1"), IOStandard("DIFF_SSTL15")),
        Subsignal("clk_p", Pins("P5"), IOStandard("DIFF_SSTL15")),
        Subsignal("clk_n", Pins("P4"), IOStandard("DIFF_SSTL15")),
        Subsignal("cke", Pins("L1"), IOStandard("SSTL15")),
        Subsignal("odt", Pins("K4"), IOStandard("SSTL15")),
        Subsignal("reset_n", Pins("G4"), IOStandard("LVCMOS15")),
        Misc("SLEW=FAST"),
    ),
]


_connectors = [
    ("eem0", {
        "d0_cc_n": "T4",
        "d0_cc_p": "R4",
        "d1_n": "R2",
        "d1_p": "R3",
        "d2_n": "U1",
        "d2_p": "T1",
        "d3_n": "V2",
        "d3_p": "U2",
        "d4_n": "Y1",
        "d4_p": "W1",
        "d5_n": "Y2",
        "d5_p": "W2",
        "d6_n": "AB1",
        "d6_p": "AA1",
        "d7_n": "AA4",
        "d7_p": "Y4",
    }),

    ("eem1", {
        "d0_cc_n": "U5",
        "d0_cc_p": "T5",
        "d1_n": "W7",
        "d1_p": "V7",
        "d2_n": "V3",
        "d2_p": "U3",
        "d3_n": "V8",
        "d3_p": "V9",
        "d4_n": "AB2",
        "d4_p": "AB3",
        "d5_n": "T6",
        "d5_p": "R6",
        "d6_n": "V5",
        "d6_p": "U6",
        "d7_n": "AB5",
        "d7_p": "AA5",
    }),

    ("eem2", {
        "d0_cc_n": "W4",
        "d0_cc_p": "V4",
        "d1_n": "AA3",
        "d1_p": "Y3",
        "d2_n": "W5",
        "d2_p": "W6",
        "d3_n": "Y7",
        "d3_p": "Y8",
        "d4_n": "AA6",
        "d4_p": "Y6",
        "d5_n": "AB6",
        "d5_p": "AB7",
        "d6_n": "AB8",
        "d6_p": "AA8",
        "d7_n": "Y9",
        "d7_p": "W9",
    }),

    ("eem3", {
        "d0_cc_n": "L20",
        "d0_cc_p": "L19",
        "d1_n": "L13",
        "d1_p": "M13",
        "d2_n": "M20",
        "d2_p": "N20",
        "d3_n": "K14",
        "d3_p": "K13",
        "d4_n": "L15",
        "d4_p": "L14",
        "d5_n": "M16",
        "d5_p": "M15",
        "d6_n": "L18",
        "d6_p": "M18",
        "d7_n": "N19",
        "d7_p": "N18",
    }),

    ("eem4", {
        "d0_cc_n": "V19",
        "d0_cc_p": "V18",
        "d1_n": "Y22",
        "d1_p": "Y21",
        "d2_n": "W17",
        "d2_p": "V17",
        "d3_n": "W22",
        "d3_p": "W21",
        "d4_n": "AB18",
        "d4_p": "AA18",
        "d5_n": "AB20",
        "d5_p": "AA19",
        "d6_n": "AA21",
        "d6_p": "AA20",
        "d7_n": "AB22",
        "d7_p": "AB21",
    }),

    ("eem5", {
        "d0_cc_n": "K19",
        "d0_cc_p": "K18",
        "d1_n": "H15",
        "d1_p": "J15",
        "d2_n": "K22",
        "d2_p": "K21",
        "d3_n": "M22",
        "d3_p": "N22",
        "d4_n": "G18",
        "d4_p": "G17",
        "d5_n": "J21",
        "d5_p": "J20",
        "d6_n": "L21",
        "d6_p": "M21",
        "d7_n": "K16",
        "d7_p": "L16",
    }),

    ("eem6", {
        "d0_cc_n": "H19",
        "d0_cc_p": "J19",
        "d1_n": "H18",
        "d1_p": "H17",
        "d2_n": "G20",
        "d2_p": "H20",
        "d3_n": "J17",
        "d3_p": "K17",
        "d4_n": "H14",
        "d4_p": "J14",
        "d5_n": "H22",
        "d5_p": "J22",
        "d6_n": "G13",
        "d6_p": "H13",
        "d7_n": "G16",
        "d7_p": "G15",
    }),

    ("eem7", {
        "d0_cc_n": "D19",
        "d0_cc_p": "E19",
        "d1_n": "G22",
        "d1_p": "G21",
        "d2_n": "F20",
        "d2_p": "F19",
        "d3_n": "F14",
        "d3_p": "F13",
        "d4_n": "E14",
        "d4_p": "E13",
        "d5_n": "D15",
        "d5_p": "D14",
        "d6_n": "E18",
        "d6_p": "F18",
        "d7_n": "E17",
        "d7_p": "F16",
    }),

    ("eem8", {
        "d0_cc_n": "C17",
        "d0_cc_p": "D17",
        "d1_n": "A16",
        "d1_p": "A15",
        "d2_n": "A14",
        "d2_p": "A13",
        "d3_n": "A19",
        "d3_p": "A18",
        "d4_n": "B13",
        "d4_p": "C13",
        "d5_n": "C15",
        "d5_p": "C14",
        "d6_n": "A20",
        "d6_p": "B20",
        "d7_n": "B16",
        "d7_p": "B15",
    }),

    ("eem9", {
        "d0_cc_n": "C19",
        "d0_cc_p": "C18",
        "d1_n": "A21",
        "d1_p": "B21",
        "d2_n": "D16",
        "d2_p": "E16",
        "d3_n": "B18",
        "d3_p": "B17",
        "d4_n": "C20",
        "d4_p": "D20",
        "d5_n": "D22",
        "d5_p": "E22",
        "d6_n": "B22",
        "d6_p": "C22",
        "d7_n": "D21",
        "d7_p": "E21",
    }),

    ("eem10", {
        "d0_cc_n": "V14",
        "d0_cc_p": "V13",
        "d1_n": "AA16",
        "d1_p": "Y16",
        "d2_n": "AB17",
        "d2_p": "AB16",
        "d3_n": "AB13",
        "d3_p": "AA13",
        "d4_n": "AA14",
        "d4_p": "Y13",
        "d5_n": "AB15",
        "d5_p": "AA15",
        "d6_n": "W16",
        "d6_p": "W15",
        "d7_n": "T15",
        "d7_p": "T14",
    }),

    ("eem11", {
        "d0_cc_n": "W12",
        "d0_cc_p": "W11",
        "d1_n": "V15",
        "d1_p": "U15",
        "d2_n": "Y14",
        "d2_p": "W14",
        "d3_n": "W10",
        "d3_p": "V10",
        "d4_n": "Y12",
        "d4_p": "Y11",
        "d5_n": "AB12",
        "d5_p": "AB11",
        "d6_n": "AA11",
        "d6_p": "AA10",
        "d7_n": "AB10",
        "d7_p": "AA9",
    }),
]


class Platform(XilinxPlatform):
    default_clk_name = "clk50"
    default_clk_period = 20.0
    userid = 0xffffffff

    def __init__(self, hw_rev="v1.0"):
        if hw_rev == "v1.0":
            io_rev = _io_v1_0
        elif hw_rev == "v1.1":
            io_rev = _io_v1_1
        else:
            raise ValueError("Unknown hardware revision", hw_rev)

        XilinxPlatform.__init__(
                self, "xc7a100t-fgg484-2", _io_common + io_rev, _connectors,
                toolchain="vivado")
        self.add_platform_command(
                "set_property INTERNAL_VREF 0.750 [get_iobanks 35]")
        self.toolchain.bitstream_commands.extend([
            # NOTE: disable this on Kasli/v1.0 boards where the XADC reference
            # has not been fixed.
            "set_property BITSTREAM.CONFIG.OVERTEMPPOWERDOWN Enable [current_design]",
            "set_property BITSTREAM.GENERAL.COMPRESS True [current_design]",
            "set_property BITSTREAM.CONFIG.CONFIGRATE 33 [current_design]",
            "set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 2 [current_design]",
            "set_property BITSTREAM.CONFIG.USR_ACCESS TIMESTAMP [current_design]",
            "set_property BITSTREAM.CONFIG.USERID \"{:#010x}\" [current_design]".format(self.userid),
            "set_property CFGBVS VCCO [current_design]",
            "set_property CONFIG_VOLTAGE 2.5 [current_design]",
            ])
