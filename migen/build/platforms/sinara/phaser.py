from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform

_ios = [
    ("user_led", 0, Pins("V5"), IOStandard("LVCMOS33")),  # LED0
    ("user_led", 1, Pins("U6"), IOStandard("LVCMOS33")),  # LED1
    ("user_led", 2, Pins("AA3"), IOStandard("LVCMOS33")),  # LED2
    ("user_led", 3, Pins("W4"), IOStandard("LVCMOS33")),  # LED3
    ("user_led", 4, Pins("AA4"), IOStandard("LVCMOS33")),  # LED4
    ("user_led", 5, Pins("W5"), IOStandard("LVCMOS33")),  # LED5

    ("test_point", 0, Pins("N15"), IOStandard("LVCMOS25")),  # TP0
    ("test_point", 1, Pins("P15"), IOStandard("LVCMOS25")),  # TP1
    ("test_point", 2, Pins("N13"), IOStandard("LVCMOS25")),  # TP2
    ("test_point", 3, Pins("P16"), IOStandard("LVCMOS25")),  # TP3
    ("test_point", 4, Pins("N14"), IOStandard("LVCMOS25")),  # TP4
    ("test_point", 5, Pins("R16"), IOStandard("LVCMOS25")),  # TP5

    ("clk_sel", 0, Pins("T20"), IOStandard("LVCMOS25")),  # SMA_CLK_SEL

    ("hw_variant", 0, Pins("N19"), IOStandard("LVCMOS25")),  # ASSY_VARIANT
    ("hw_rev", 0, Pins("N18 M17 M15 M16"), IOStandard("LVCMOS25")),  # HW_REV

    ("fan_pwm", 0, Pins("AB7"), IOStandard("LVCMOS33")),

    ("i2c", 0,  # EEM0_I2C
        Subsignal("scl", Pins("AB1")),
        Subsignal("sda", Pins("AA1")),
        IOStandard("LVCMOS33")
    ),
    ("i2c", 1,  # EEM1_I2C
        Subsignal("scl", Pins("Y2")),
        Subsignal("sda", Pins("Y3")),
        IOStandard("LVCMOS33")
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

    ("clk_gtp", 0,
        Subsignal("p", Pins("F6")),
        Subsignal("n", Pins("E6")),
    ),

    ("mgt", 0,
        Subsignal("txp", Pins("B4")),
        Subsignal("txn", Pins("A4")),
        Subsignal("rxp", Pins("B8")),
        Subsignal("rxn", Pins("A8")),
    ),
    ("mgt", 1,
        Subsignal("txp", Pins("D5")),
        Subsignal("txn", Pins("C5")),
        Subsignal("rxp", Pins("D11")),
        Subsignal("rxn", Pins("C11")),
    ),
    ("mgt", 2,
        Subsignal("txp", Pins("B6")),
        Subsignal("txn", Pins("A6")),
        Subsignal("rxp", Pins("B10")),
        Subsignal("rxn", Pins("A10")),
    ),
    ("mgt", 3,
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
        Misc("SLEW=FAST")
    ),

    ("adc_ctrl", 0,
        Subsignal("term_stat", Pins("W6 Y6")),
        Subsignal("gain0", Pins("AB5 AA5")),
        Subsignal("gain1", Pins("AA6 AB6")),
        IOStandard("LVCMOS33")
    ),

    # cnv, sdob, sck: p-n swapped on pcb
    ("adc", 0,
        Subsignal("sck_n", Pins("N22")),
        Subsignal("sck_p", Pins("M22")),
        Subsignal("clkout_n", Pins("K19"), Misc("DIFF_TERM=TRUE")),
        Subsignal("clkout_p", Pins("K18"), Misc("DIFF_TERM=TRUE")),
        Subsignal("cnvn_n", Pins("J22")),
        Subsignal("cnvn_p", Pins("H22")),
        Subsignal("sdo_n", Pins("K22 M21"), Misc("DIFF_TERM=TRUE")),
        Subsignal("sdo_p", Pins("K21 L21"), Misc("DIFF_TERM=TRUE")),
        IOStandard("LVDS_25")
    ),

    ("trf_ctrl", 0,
        Subsignal("ps", Pins("U1")),
        Subsignal("ld", Pins("U2")),
        IOStandard("LVCMOS33")
    ),

    ("trf_spi", 0,
        Subsignal("clk", Pins("U3")),
        Subsignal("miso", Pins("V9")),  # RDBK
        Subsignal("mosi", Pins("T3")),  # DATA
        Subsignal("cs_n", Pins("T1")),  # LE
        IOStandard("LVCMOS33")
    ),

    ("trf_ctrl", 1,
        Subsignal("ps", Pins("W7")),
        Subsignal("ld", Pins("V2")),
        IOStandard("LVCMOS33")
    ),

    ("trf_spi", 1,
        Subsignal("clk", Pins("Y1")),
        Subsignal("miso", Pins("V7")),  # RDBK
        Subsignal("mosi", Pins("W1")),  # DATA
        Subsignal("cs_n", Pins("W2")),  # LE
        IOStandard("LVCMOS33")
    ),

    ("att_rstn", 0, Pins("T4"), IOStandard("LVCMOS33")),

    ("att_spi", 0,
        Subsignal("clk", Pins("R4")),
        Subsignal("miso", Pins("T5")),  # S_OUT
        Subsignal("mosi", Pins("R2")),  # S_IN
        Subsignal("cs_n", Pins("R3")),  # LE
        IOStandard("LVCMOS33")
    ),

    ("att_rstn", 1, Pins("V3"), IOStandard("LVCMOS33")),

    ("att_spi", 1,
        Subsignal("clk", Pins("T6")),
        Subsignal("miso", Pins("V4")),  # S_OUT
        Subsignal("mosi", Pins("U5")),  # S_IN
        Subsignal("cs_n", Pins("R6")),  # LE
        IOStandard("LVCMOS33")
    ),

    ("dac_ctrl", 0,
        Subsignal("alarm", Pins("AB8")),
        Subsignal("resetb", Pins("Y7")),
        Subsignal("sleep", Pins("Y8")),
        Subsignal("txena", Pins("V8")),
        IOStandard("LVCMOS33")
    ),

    ("dac_spi", 0,
        Subsignal("clk", Pins("U7")),  # SCLK
        Subsignal("miso", Pins("AA8")),  # SDO
        Subsignal("mosi", Pins("W9")),  # SDIO
        Subsignal("cs_n", Pins("Y9")),  # SDENB
        IOStandard("LVCMOS33")
    ),

    # A3, B8: p-n swapped on pcb
    ("dac_data", 0,
        Subsignal("data_a_n", Pins(
            "F20 D19 E18 C22 C17 A19 E17 D21 "
            "D16 C19 B18 D15 E14 F14 B16 C15")),
        Subsignal("data_a_p", Pins(
            "F19 E19 F18 B22 D17 A18 F16 E21 "
            "E16 C18 B17 D14 E13 F13 B15 C14")),
        Subsignal("data_b_n", Pins(
            "G16 M20 G20 H19 H18 L18 J21 H15 "
            "L16 L15 K14 J17 H14 L20 G13 L13")),
        Subsignal("data_b_p", Pins(
            "G15 N20 H20 J19 H17 M18 J20 J15 "
            "K16 L14 K13 K17 J14 L19 H13 M13")),
        Subsignal("data_clk_n", Pins("D22")),
        Subsignal("data_clk_p", Pins("E22")),
        Subsignal("ostr_n", Pins("B13")),
        Subsignal("ostr_p", Pins("C13")),
        Subsignal("istr_parityab_n", Pins("G22")),
        Subsignal("istr_parityab_p", Pins("G21")),
        Subsignal("paritycd_n", Pins("G18")),
        Subsignal("paritycd_p", Pins("G17")),
        Subsignal("sync_n", Pins("A14")),
        Subsignal("sync_p", Pins("A13")),
        IOStandard("LVDS_25")
    ),
]

_connectors = [
    ("eem0", {
        "d0_cc_n": "W20",
        "d0_cc_p": "W19",
        "d1_n": "U21",
        "d1_p": "T21",
        "d2_n": "W22",
        "d2_p": "W21",
        "d3_n": "T18",
        "d3_p": "R18",
        "d4_n": "V20",
        "d4_p": "U20",
        "d5_n": "R19",
        "d5_p": "P19",
        "d6_n": "V19",
        "d6_p": "V18",
        "d7_n": "W17",
        "d7_p": "V17",
    }),
    ("eem1", {
        "d0_cc_n": "Y19",
        "d0_cc_p": "Y18",
        "d1_n": "AB20",
        "d1_p": "AA19",
        "d2_n": "AA21",
        "d2_p": "AA20",
        "d3_n": "AB18",
        "d3_p": "AA18",
        "d4_n": "AB22",
        "d4_p": "AB21",
        "d5_n": "Y22",
        "d5_p": "Y21",
        "d6_n": "U18",
        "d6_p": "U17",
        "d7_n": "R14",
        "d7_p": "P14",
    }),
]


_extensions = [
    ("eem", i, IOStandard("LVDS_25")) + tuple([
        Subsignal("data{}_{}".format(j, p), Pins(
            "eem{}:d{}{}_{}".format(i, j, "_cc" if j == 0 else "", p)))
                for j in range(8) for p in "pn"])
    for i in range(2)
]


class Platform(XilinxPlatform):
    userid = 0xffffffff
    def __init__(self):
        XilinxPlatform.__init__(
                self, "xc7a100t-fgg484-2", _ios, _connectors,
                toolchain="vivado")
        self.add_extension(_extensions)
        self.add_platform_command(
                "set_property INTERNAL_VREF 0.750 [get_iobanks 35]")
        self.toolchain.bitstream_commands.extend([
            "set_property BITSTREAM.CONFIG.OVERTEMPPOWERDOWN "
                "Enable [current_design]",
            "set_property BITSTREAM.GENERAL.COMPRESS True [current_design]",
            "set_property BITSTREAM.CONFIG.CONFIGRATE 33 [current_design]",
            "set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]",
            "set_property BITSTREAM.CONFIG.USR_ACCESS "
                "TIMESTAMP [current_design]",
            "set_property BITSTREAM.CONFIG.USERID "
                "\"{:#010x}\" [current_design]".format(self.userid),
            "set_property CFGBVS VCCO [current_design]",
            "set_property CONFIG_VOLTAGE 2.5 [current_design]",
        ])
