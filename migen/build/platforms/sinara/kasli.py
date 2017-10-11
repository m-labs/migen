from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform


_io = [
    ("user_led", 0, Pins("Y19"), IOStandard("LVCMOS25")),  # LED_USER1

    ("clk50", 0, Pins("Y18"), IOStandard("LVCMOS25")),

    ("clk_fpgaio", 0,
        Subsignal("p", Pins("W19")),
        Subsignal("n", Pins("W20")),
        IOStandard("LVDS25"),
    ),

    ("clk_rec", 0,
        Subsignal("p", Pins("U20")),
        Subsignal("n", Pins("V20")),
        IOStandard("LVDS25"),
    ),

    ("serial", 0,
        Subsignal("tx", Pins("V22")),
        Subsignal("rx", Pins("P16")),
        IOStandard("LVCMOS25")
    ),

    ("clk_sel", 0, Pins("W22"), IOStandard("LVCMOS25")),

    ("i2c", 0,
        Subsignal("scl", Pins("U21")),
        Subsignal("sda", Pins("T21")),
        IOStandard("LVCMOS25")
    ),

    ("spiflash", 0,
        Subsignal("cs_n", Pins("T19")),
        Subsignal("dq", Pins("P22 R22 P21 R21")),
        IOStandard("LVCMOS25")
    ),

    ("clk_gtp", 0,
        Subsignal("p", Pins("F6")),
        Subsignal("n", Pins("E6")),
    ),

    # ("clk125_gtp", 0,
    #     Subsignal("p", Pins("F10")),
    #     Subsignal("n", Pins("E10")),
    # ),

    ("sfp_gtp", 0,
        Subsignal("txp", Pins("B4")),
        Subsignal("txn", Pins("A4")),
        Subsignal("rxp", Pins("B8")),
        Subsignal("rxn", Pins("A8")),
    ),
    ("sfp", 0,
        Subsignal("mod_def1", Pins("T3")),
        Subsignal("mod_def2", Pins("U7")),
        Subsignal("los", Pins("U17")),
        Subsignal("mod_present", Pins("U18")),
        Subsignal("rate_select", Pins("P14")),
        Subsignal("tx_disable", Pins("R14")),
        Subsignal("tx_fault", Pins("R18")),
        Subsignal("led", Pins("N17")),
        IOStandard("LVCMOS25")
    ),

    ("sfp_gtp", 1,
        Subsignal("txp", Pins("D5")),
        Subsignal("txn", Pins("C5")),
        Subsignal("rxp", Pins("D11")),
        Subsignal("rxn", Pins("C11")),
    ),
    ("sfp", 1,
        # ...
        Subsignal("led", Pins("T18")),
        IOStandard("LVCMOS25")
    ),

    ("sfp_gtp", 2,
        Subsignal("txp", Pins("B6")),
        Subsignal("txn", Pins("A6")),
        Subsignal("rxp", Pins("B10")),
        Subsignal("rxn", Pins("A10")),
    ),
    ("sfp", 2,
        # ...
        Subsignal("led", Pins("P20")),
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
            "K2 G2 F3 J5 E2 H5 J2 K1 "
            "D1 E1 D2 A1 C2 B1 F4"),
            IOStandard("SSTL15")),
        Subsignal("ba", Pins("H2 J1 G1"), IOStandard("SSTL15")),
        Subsignal("ras_n", Pins("K4"), IOStandard("SSTL15")),
        Subsignal("cas_n", Pins("G4"), IOStandard("SSTL15")),
        Subsignal("we_n", Pins("F1"), IOStandard("SSTL15")),
        # Subsignal("cs_n", Pins(""), IOStandard("SSTL15")),
        Subsignal("dm", Pins("J4 N4"), IOStandard("SSTL15")),
        Subsignal("dq", Pins(
            "L4 L5 J6 K6 K3 L3 M2 M3 "
            "P1 R1 N2 P2 M5 M6 N5 P6"),
            IOStandard("SSTL15"),
            Misc("IN_TERM=UNTUNED_SPLIT_50")),
        Subsignal("dqs_p", Pins("M1 P5"), IOStandard("DIFF_SSTL15")),
        Subsignal("dqs_n", Pins("L1 P4"), IOStandard("DIFF_SSTL15")),
        Subsignal("clk_p", Pins("H3"), IOStandard("DIFF_SSTL15")),
        Subsignal("clk_n", Pins("G3"), IOStandard("DIFF_SSTL15")),
        Subsignal("cke", Pins("B2"), IOStandard("SSTL15")),
        Subsignal("odt", Pins("H4"), IOStandard("SSTL15")),
        Subsignal("reset_n", Pins("L6"), IOStandard("LVCMOS15")),
        Misc("SLEW=FAST"),
    ),
]


_connectors = [
    ("EEM0", {
        "D0_CC_P": "V4",
        "D0_CC_N": "W4",
        "D1_P": "T1",
        "D1_N": "U1",
        "D2_P": "U2",
        "D2_N": "V2",
        "D3_P": "R3",
        "D3_N": "R2",
        "D4_P": "W2",
        "D4_N": "Y2",
        "D5_P": "W1",
        "D6_P": "Y1",
        "D6_N": "U3",
        "D5_N": "V3",
        "D7_P": "AA1",
        "D7_N": "AB1",
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
