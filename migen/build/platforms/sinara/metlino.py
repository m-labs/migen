from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform


_io = [
    ("user_led", 0, Pins("J24"), IOStandard("LVCMOS33")), # sfp0_led1
    ("user_led", 1, Pins("J25"), IOStandard("LVCMOS33")), # sfp0_led2
    ("user_led", 2, Pins("L25"), IOStandard("LVCMOS33")), # sfp1_led1
    ("user_led", 3, Pins("K25"), IOStandard("LVCMOS33")), # sfp1_led2

    ("clk50", 0, Pins("N24"), IOStandard("LVCMOS33")),

    ("serial", 0,
        Subsignal("tx", Pins("K20")),
        Subsignal("rx", Pins("K22")),
        IOStandard("LVCMOS33")
    ),

    ("i2c", 0,
        Subsignal("scl", Pins("N21")),
        Subsignal("sda", Pins("M21")),
        IOStandard("LVCMOS33")
    ),

    # this is the second SPI flash (not containing the bitstream)
    # clock is shared with the bitstream flash and needs to be accessed
    # through STARTUPE3
    ("spiflash", 0,
        Subsignal("cs_n", Pins("G26")),
        Subsignal("dq", Pins("M20 L20 R21 R22")),
        IOStandard("LVCMOS33")
    ),

    ("ddram", 0,
        Subsignal("a", Pins(
            "AE17 AL17 AG16 AG17 AD16 AH14 AD15 AK15",
            "AF14 AF15 AL18 AL15 AE18 AJ15 AG14"),
            IOStandard("SSTL15_DCI")),
        Subsignal("ba", Pins("AF17 AD19 AD18"), IOStandard("SSTL15_DCI")),
        Subsignal("ras_n", Pins("AH19"), IOStandard("SSTL15_DCI")),
        Subsignal("cas_n", Pins("AK18"), IOStandard("SSTL15_DCI")),
        Subsignal("we_n", Pins("AG19"), IOStandard("SSTL15_DCI")),
        Subsignal("cs_n", Pins("AF18"), IOStandard("SSTL15_DCI")),
        Subsignal("dm", Pins("AD21 AE25 AJ21 AM21 AH26 AN26 AJ29 AL32"),
            IOStandard("SSTL15_DCI"),
            Misc("DATA_RATE=DDR")),
        Subsignal("dq", Pins(
            "AE23 AG20 AF22 AF20 AE22 AD20 AG22 AE20",
            "AJ24 AG24 AJ23 AF23 AH23 AF24 AH22 AG25",
            "AL22 AL25 AM20 AK23 AK22 AL24 AL20 AL23",
            "AM24 AN23 AN24 AP23 AP25 AN22 AP24 AM22",
            "AH28 AK26 AK28 AM27 AJ28 AH27 AK27 AM26",
            "AL30 AP29 AM30 AN28 AL29 AP28 AM29 AN27",
            "AH31 AH32 AJ34 AK31 AJ31 AJ30 AH34 AK32",
            "AN33 AP33 AM34 AP31 AM32 AN31 AL34 AN32"),
            IOStandard("SSTL15_DCI"),
            Misc("ODT=RTT_40"),
            Misc("DATA_RATE=DDR")),
        Subsignal("dqs_p", Pins("AG21 AH24 AJ20 AP20 AL27 AN29 AH33 AN34"),
            IOStandard("DIFF_SSTL15_DCI"),
            Misc("ODT=RTT_40"),
            Misc("DATA_RATE=DDR")),
        Subsignal("dqs_n", Pins("AH21 AJ25 AK20 AP21 AL28 AP30 AJ33 AP34"),
            IOStandard("DIFF_SSTL15_DCI"),
            Misc("ODT=RTT_40"),
            Misc("DATA_RATE=DDR")),
        Subsignal("clk_p", Pins("AE16"), IOStandard("DIFF_SSTL15_DCI"), Misc("DATA_RATE=DDR")),
        Subsignal("clk_n", Pins("AE15"), IOStandard("DIFF_SSTL15_DCI"), Misc("DATA_RATE=DDR")),
        Subsignal("cke", Pins("AL19"), IOStandard("SSTL15_DCI")),
        Subsignal("odt", Pins("AJ18"), IOStandard("SSTL15_DCI")),
        Subsignal("reset_n", Pins("AJ14"), IOStandard("SSTL15")),
        Misc("SLEW=FAST"),
        Misc("OUTPUT_IMPEDANCE=RDRV_40_40")
    ),

    ("gth_clk200", 0,
        Subsignal("p", Pins("K6")),
        Subsignal("n", Pins("K5"))
    ),
    ("port0", 0,
        Subsignal("txp", Pins("B6")),
        Subsignal("txn", Pins("B5")),
        Subsignal("rxp", Pins("A4")),
        Subsignal("rxn", Pins("A3"))
    ),
    ("sfp", 0,
        Subsignal("txp", Pins("D6")),
        Subsignal("txn", Pins("D5")),
        Subsignal("rxp", Pins("D2")),
        Subsignal("rxn", Pins("D1"))
    ),
    ("sfp", 1,
        Subsignal("txp", Pins("C4")),
        Subsignal("txn", Pins("C3")),
        Subsignal("rxp", Pins("B2")),
        Subsignal("rxn", Pins("B1"))
    ),
    ("sfp", 2,
        Subsignal("txp", Pins("F6")),
        Subsignal("txn", Pins("F5")),
        Subsignal("rxp", Pins("E4")),
        Subsignal("rxn", Pins("E3"))
    ),

    ("input_clk_sel", 0, Pins("AK11"), IOStandard("LVCMOS33")),
    ("filtered_clk_sel", 0, Pins("AN12"), IOStandard("LVCMOS33")),
    ("si5324", 0,
        Subsignal("rst_n", Pins("AL13"), IOStandard("LVCMOS33")),
        Subsignal("int", Pins("AK13"), IOStandard("LVCMOS33"))
    ),
    ("cdr_clk_clean", 0,
        Subsignal("p", Pins("V6")),
        Subsignal("n", Pins("V5"))
    ),
    ("mch_fabric_d", 0,
        Subsignal("txp", Pins("AN4")),
        Subsignal("txn", Pins("AN3")),
        Subsignal("rxp", Pins("AP2")),
        Subsignal("rxn", Pins("AP1"))
    ),
    ("mch_fabric_d", 1,
        Subsignal("txp", Pins("AL4")),
        Subsignal("txn", Pins("AL3")),
        Subsignal("rxp", Pins("AK2")),
        Subsignal("rxn", Pins("AK1"))
    ),
    ("mch_fabric_d", 2,
        Subsignal("txp", Pins("AH6")),
        Subsignal("txn", Pins("AH5")),
        Subsignal("rxp", Pins("AH2")),
        Subsignal("rxn", Pins("AH1"))
    ),
    ("mch_fabric_d", 3,
        Subsignal("txp", Pins("AE4")),
        Subsignal("txn", Pins("AE3")),
        Subsignal("rxp", Pins("AD2")),
        Subsignal("rxn", Pins("AD1"))
    ),
    ("mch_fabric_d", 4,
        Subsignal("txp", Pins("AA4")),
        Subsignal("txn", Pins("AA3")),
        Subsignal("rxp", Pins("Y2")),
        Subsignal("rxn", Pins("Y1"))
    ),
    ("mch_fabric_d", 5,
        Subsignal("txp", Pins("U4")),
        Subsignal("txn", Pins("U3")),
        Subsignal("rxp", Pins("T2")),
        Subsignal("rxn", Pins("T1"))
    ),
    ("mch_fabric_d", 6,
        Subsignal("txp", Pins("AM6")),
        Subsignal("txn", Pins("AM5")),
        Subsignal("rxp", Pins("AM2")),
        Subsignal("rxn", Pins("AM1"))
    ),
    ("mch_fabric_d", 7,
        Subsignal("txp", Pins("AK6")),
        Subsignal("txn", Pins("AK5")),
        Subsignal("rxp", Pins("AJ4")),
        Subsignal("rxn", Pins("AJ3"))
    ),
    ("mch_fabric_d", 8,
        Subsignal("txp", Pins("AG4")),
        Subsignal("txn", Pins("AG3")),
        Subsignal("rxp", Pins("AF2")),
        Subsignal("rxn", Pins("AF1"))
    ),
    ("mch_fabric_d", 9,
        Subsignal("txp", Pins("AC4")),
        Subsignal("txn", Pins("AC3")),
        Subsignal("rxp", Pins("AB2")),
        Subsignal("rxn", Pins("AB1"))
    ),
    ("mch_fabric_d", 10,
        Subsignal("txp", Pins("W4")),
        Subsignal("txn", Pins("W3")),
        Subsignal("rxp", Pins("V2")),
        Subsignal("rxn", Pins("V1"))
    ),
    ("mch_fabric_d", 11,
        Subsignal("txp", Pins("R4")),
        Subsignal("txn", Pins("R3")),
        Subsignal("rxp", Pins("P2")),
        Subsignal("rxn", Pins("P1"))
    ),

    ("ddmtd_main_dcxo_oe", 0, Pins("AM11"), IOStandard("LVCMOS33")),
    ("ddmtd_main_dcxo_i2c", 0,
        Subsignal("scl", Pins("AN11")),
        Subsignal("sda", Pins("AN13")),
        IOStandard("LVCMOS33")),
    ("ddmtd_helper_dcxo_oe", 0, Pins("AK12"), IOStandard("LVCMOS33")),
    ("ddmtd_helper_dcxo_i2c", 0,
        Subsignal("scl", Pins("AL12")),
        Subsignal("sda", Pins("AM12")),
        IOStandard("LVCMOS33")),
    ("ddmtd_helper_clk", 0,
        Subsignal("p", Pins("E18")),
        Subsignal("n", Pins("E17")),
        IOStandard("LVDS"), Misc("DIFF_TERM_ADV=TERM_100")
    ),
]


# via VHDCI carrier v1.1
_connectors = [
    ("eem0", {
        "d0_cc_n": "D25",
        "d0_cc_p": "E25",
        "d1_n": "C22",
        "d1_p": "C21",
        "d2_n": "D21",
        "d2_p": "D20",
        "d3_n": "F25",
        "d3_p": "G24",
        "d4_n": "B22",
        "d4_p": "B21",
        "d5_n": "C23",
        "d5_p": "D23",
        "d6_n": "A24",
        "d6_p": "B24",
        "d7_n": "E21",
        "d7_p": "E20",
    }),

    ("eem1", {
        "d0_cc_n": "E23",
        "d0_cc_p": "E22",
        "d1_n": "A28",
        "d1_p": "A27",
        "d2_n": "F24",
        "d2_p": "F23",
        "d3_n": "A29",
        "d3_p": "B29",
        "d4_n": "B27",
        "d4_p": "C27",
        "d5_n": "A20",
        "d5_p": "B20",
        "d6_n": "C28",
        "d6_p": "D28",
        "d7_n": "D26",
        "d7_p": "E26",
    }),

    ("eem2", {
        "d0_cc_n": "C24",
        "d0_cc_p": "D24",
        "d1_n": "A25",
        "d1_p": "B25",
        "d2_n": "B26",
        "d2_p": "C26",
        "d3_n": "D29",
        "d3_p": "E28",
        "d4_n": "F20",
        "d4_p": "G20",
        "d5_n": "E27",
        "d5_p": "F27",
        "d6_n": "F22",
        "d6_p": "G22",
        "d7_n": "G21",
        "d7_p": "H21",
    }),

    ("eem3", {
        "d0_cc_n": "AB31",
        "d0_cc_p": "AB30",
        "d1_n": "Y30",
        "d1_p": "W30",
        "d2_n": "Y32",
        "d2_p": "Y31",
        "d3_n": "W31",
        "d3_p": "V31",
        "d4_n": "Y33",
        "d4_p": "W33",
        "d5_n": "W34",
        "d5_p": "V33",
        "d6_n": "AD33",
        "d6_p": "AC33",
        "d7_n": "V34",
        "d7_p": "U34",
    }),

    ("eem4", {
        "d0_cc_n": "W24",
        "d0_cc_p": "W23",
        "d1_n": "U25",
        "d1_p": "U24",
        "d2_n": "W29",
        "d2_p": "V29",
        "d3_n": "V28",
        "d3_p": "V27",
        "d4_n": "AD31",
        "d4_p": "AD30",
        "d5_n": "AG30",
        "d5_p": "AF30",
        "d6_n": "Y28",
        "d6_p": "W28",
        "d7_n": "U27",
        "d7_p": "U26",
    }),

    ("eem5", {
        "d0_cc_n": "AA25",
        "d0_cc_p": "AA24",
        "d1_n": "T23",
        "d1_p": "T22",
        "d2_n": "AD28",
        "d2_p": "AC28",
        "d3_n": "W21",
        "d3_p": "V21",
        "d4_n": "AB20",
        "d4_p": "AA20",
        "d5_n": "AF34",
        "d5_p": "AE33",
        "d6_n": "AC21",
        "d6_p": "AB21",
        "d7_n": "AB29",
        "d7_p": "AA29",
    }),

    ("eem6", {
        "d0_cc_n": "AA23",
        "d0_cc_p": "Y23",
        "d1_n": "AB22",
        "d1_p": "AA22",
        "d2_n": "AF32",
        "d2_p": "AE32",
        "d3_n": "AC23",
        "d3_p": "AC22",
        "d4_n": "AE30",
        "d4_p": "AD29",
        "d5_n": "AG32",
        "d5_p": "AG31",
        "d6_n": "AB32",
        "d6_p": "AA32",
        "d7_n": "AB26",
        "d7_p": "AB25",
    }),

    ("eem7", {
        "d0_cc_n": "AC32",
        "d0_cc_p": "AC31",
        "d1_n": "AD34",
        "d1_p": "AC34",
        "d2_n": "AG29",
        "d2_p": "AF29",
        "d3_n": "AB27",
        "d3_p": "AA27",
        "d4_n": "AC27",
        "d4_p": "AC26",
        "d5_n": "AF27",
        "d5_p": "AE27",
        "d6_n": "AG34",
        "d6_p": "AF33",
        "d7_n": "AF28",
        "d7_p": "AE28",
    }),
]


class Platform(XilinxPlatform):
    default_clk_name = "clk50"
    default_clk_period = 20.0

    def __init__(self):
        XilinxPlatform.__init__(self, "xcku040-ffva1156-1-c", _io, _connectors, toolchain="vivado")
        self.toolchain.bitstream_commands.extend([
            "set_property BITSTREAM.CONFIG.OVERTEMPSHUTDOWN Enable [current_design]",
            "set_property BITSTREAM.GENERAL.COMPRESS True [current_design]",
            "set_property BITSTREAM.CONFIG.CONFIGRATE 33 [current_design]",
            "set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]",
            "set_property CFGBVS VCCO [current_design]",
            "set_property CONFIG_VOLTAGE 3.3 [current_design]",
            ])
