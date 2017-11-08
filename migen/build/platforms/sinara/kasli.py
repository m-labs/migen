from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform


_io = [
    ("user_led", 0, Pins("T16"), IOStandard("LVCMOS25")),  # LED_USER1

    ("clk50", 0, Pins("W19"), IOStandard("LVCMOS25")),

    ("clk_fpgaio", 0,
        Subsignal("p", Pins("Y18")),
        Subsignal("n", Pins("Y19")),
        IOStandard("LVDS25"),
    ),

    ("clk_rec", 0,
        Subsignal("p", Pins("U20")),
        Subsignal("n", Pins("V20")),
        IOStandard("LVDS25"),
    ),

    ("serial", 0,
        Subsignal("tx", Pins("N13")),
        Subsignal("rx", Pins("N17")),
        IOStandard("LVCMOS25")
    ),

    ("clk_sel", 0, Pins("F21"), IOStandard("LVCMOS25")),
    
    ("vusb_present", 0, Pins("M17"), IOStandard("LVCMOS25")),

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

    ("clk_gtp", 0,
        Subsignal("p", Pins("F6")),
        Subsignal("n", Pins("E6")),
    ),

    ("clk125_gtp", 0,
        Subsignal("p", Pins("F10")),
        Subsignal("n", Pins("E10")),
    ),

    ("sfp_gtp", 0,
        Subsignal("txp", Pins("B4")),
        Subsignal("txn", Pins("A4")),
        Subsignal("rxp", Pins("B8")),
        Subsignal("rxn", Pins("A8")),
    ),
    ("sfp", 0,
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

    ("sfp_gtp", 1,
        Subsignal("txp", Pins("D5")),
        Subsignal("txn", Pins("C5")),
        Subsignal("rxp", Pins("D11")),
        Subsignal("rxn", Pins("C11")),
    ),
    ("sfp", 1,
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

    ("sfp_gtp", 2,
        Subsignal("txp", Pins("B6")),
        Subsignal("txn", Pins("A6")),
        Subsignal("rxp", Pins("B10")),
        Subsignal("rxn", Pins("A10")),
    ),
    ("sfp", 2,
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

    ("sata_gtp", 0,
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
    ("EEM0", {
        "D0_CC_P": "R4",
        "D0_CC_N": "T4",
        "D1_P": "R3",
        "D1_N": "R2",
        "D2_P": "T1",
        "D2_N": "U1",
        "D3_P": "U2",
        "D3_N": "V2",
        "D4_P": "W1",
        "D4_N": "Y1",
        "D5_P": "W2",
        "D6_P": "Y2",
        "D6_N": "AA1",
        "D5_N": "AB1",
        "D7_P": "Y4",
        "D7_N": "AA4",
    }),

    # ...
]


class Platform(XilinxPlatform):
    default_clk_name = "clk50"
    default_clk_period = 20.0

    def __init__(self):
        XilinxPlatform.__init__(
                self, "xc7a100t-fgg484-2", _io, _connectors,
                toolchain="vivado")
