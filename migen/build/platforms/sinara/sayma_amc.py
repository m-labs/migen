from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform


_io = [
    ("user_led", 0, Pins("AG9"), IOStandard("LVCMOS33")),  # sfp1_led1
    ("user_led", 1, Pins("AJ10"), IOStandard("LVCMOS33")), # sfp1_led2
    ("user_led", 2, Pins("AJ13"), IOStandard("LVCMOS33")), # sfp2_led1
    ("user_led", 3, Pins("AE13"), IOStandard("LVCMOS33")), # sfp2_led2

    ("clk50", 0, Pins("AF9"), IOStandard("LVCMOS33")),

    ("serial", 0,
        Subsignal("tx", Pins("AK8")),
        Subsignal("rx", Pins("AL8")),
        IOStandard("LVCMOS33")
    ),
    ("serial", 1,
        Subsignal("tx", Pins("M27")),
        Subsignal("rx", Pins("L27")),
        IOStandard("LVCMOS33")
    ),
    ("serial_rtm", 0,
        Subsignal("tx", Pins("G27")),
        Subsignal("rx", Pins("H27")),
        IOStandard("LVCMOS33")
    ),

    ("i2c", 0,
        Subsignal("scl", Pins("N21")),
        Subsignal("sda", Pins("M21")),
        IOStandard("LVCMOS33")
    ),

    ("rtm_fpga_cfg", 0,
        Subsignal("cclk", Pins("J25")),
        Subsignal("din", Pins("K26")),
        Subsignal("done", Pins("K27"), Misc("PULLUP=TRUE")),
        Subsignal("init_b", Pins("G25"), Misc("PULLUP=TRUE")),
        Subsignal("program_b", Pins("G26"), Misc("PULLUP=TRUE")),
        IOStandard("LVCMOS33")
    ),

    # this is the second SPI flash (not containing the bitstream)
    # clock is shared with the bitstream flash and needs to be accessed
    # through STARTUPE3
    ("spiflash", 0,
        Subsignal("cs_n", Pins("K21")),
        Subsignal("dq", Pins("M20 L20 R21 R22")),
        IOStandard("LVCMOS33")
    ),

    ("ddram_32", 1,
        Subsignal("a", Pins(
            "E15 D15 J16 K18 H16 K17 K16 J15",
            "K15 D14 D18 G15 L18 G14 L15"),
            IOStandard("SSTL15_DCI")),
        Subsignal("ba", Pins("L19 H17 G16"), IOStandard("SSTL15_DCI")),
        Subsignal("ras_n", Pins("E18"), IOStandard("SSTL15_DCI")),
        Subsignal("cas_n", Pins("E16"), IOStandard("SSTL15_DCI")),
        Subsignal("we_n", Pins("D16"), IOStandard("SSTL15_DCI")),
        Subsignal("cs_n", Pins("G19"), IOStandard("SSTL15_DCI")),
        Subsignal("dm", Pins("F27 E26 D23 G24"),
            IOStandard("SSTL15_DCI"),
            Misc("DATA_RATE=DDR")),
        Subsignal("dq", Pins(
            "C28 B27 A27 C27 D28 E28 A28 D29",
            "D25 C26 E25 B25 C24 A25 D24 B26",
            "B20 D21 B22 E23 E22 D20 B21 A20",
            "F23 H21 F24 G21 F22 E21 G22 E20"),
            IOStandard("SSTL15_DCI"),
            Misc("ODT=RTT_40"),
            Misc("DATA_RATE=DDR")),
        Subsignal("dqs_p", Pins("B29 B24 C21 G20"),
            IOStandard("DIFF_SSTL15_DCI"),
            Misc("ODT=RTT_40"),
            Misc("DATA_RATE=DDR")),
        Subsignal("dqs_n", Pins("A29 A24 C22 F20"),
            IOStandard("DIFF_SSTL15_DCI"),
            Misc("ODT=RTT_40"),
            Misc("DATA_RATE=DDR")),
        Subsignal("clk_p", Pins("J19"), IOStandard("DIFF_SSTL15_DCI"), Misc("DATA_RATE=DDR")),
        Subsignal("clk_n", Pins("J18"), IOStandard("DIFF_SSTL15_DCI"), Misc("DATA_RATE=DDR")),
        Subsignal("cke", Pins("H18"), IOStandard("SSTL15_DCI")),
        Subsignal("odt", Pins("F19"), IOStandard("SSTL15_DCI")),
        Subsignal("reset_n", Pins("F14"), IOStandard("SSTL15")),
        Misc("SLEW=FAST"),
        Misc("OUTPUT_IMPEDANCE=RDRV_40_40")
    ),

    ("ddram_64", 0,
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

    ("eth_clocks", 0,
        Subsignal("tx", Pins("M22")),
        Subsignal("rx", Pins("AG11")),
        IOStandard("LVCMOS33"), Misc("SLEW=FAST"), Drive(16)
    ),
    ("eth", 0,
        Subsignal("rx_ctl", Pins("T24")),
        Subsignal("rx_data", Pins("R23 P23 R25 R26")),
        Subsignal("tx_ctl", Pins("N22")),
        Subsignal("tx_data", Pins("K20 K22 P20 P21")),
        Subsignal("mdc", Pins("T27")),
        Subsignal("mdio", Pins("R27")),
        IOStandard("LVCMOS33"), Misc("SLEW=FAST"), Drive(16)
    ),

    ("sma_io", 0,
        Subsignal("level", Pins("K23")),
        Subsignal("direction", Pins("K25")),
        IOStandard("LVCMOS33")
    ),
    ("sma_io", 1,
        Subsignal("level", Pins("L25")),
        Subsignal("direction", Pins("L23")),
        IOStandard("LVCMOS33")
    ),

    ("amc_rtm_serwb", 0,
        Subsignal("clk", Pins("J8")), # rtm_fpga_usr_io_p
        Subsignal("tx", Pins("A13")), # rtm_fpga_lvds1_p
        Subsignal("rx", Pins("C12")), # rtm_fpga_lvds2_p
        IOStandard("LVCMOS18")
    ),

    ("si5324", 0,
        Subsignal("rst_n", Pins("L24"), IOStandard("LVCMOS33")),
        Subsignal("int", Pins("L22"), IOStandard("LVCMOS33"))
    ),
    ("si5324_clkin", 0,
        Subsignal("p", Pins("D13")),
        Subsignal("n", Pins("C13")),
        IOStandard("LVDS"),
    ),
    ("cdr_clk_clean", 0,
        Subsignal("p", Pins("AF6")),
        Subsignal("n", Pins("AF5"))
    ),
    ("cdr_clk_clean_fabric", 0,
        Subsignal("p", Pins("H12")),
        Subsignal("n", Pins("G12")),
        IOStandard("LVDS"), Misc("DIFF_TERM_ADV=TERM_100")
    ),
    ("gth_clk200", 0,
        Subsignal("p", Pins("AD6")),
        Subsignal("n", Pins("AD5"))
    ),

    ("sfp", 0,
        Subsignal("txp", Pins("AN4")),
        Subsignal("txn", Pins("AN3")),
        Subsignal("rxp", Pins("AP2")),
        Subsignal("rxn", Pins("AP1"))
    ),
    ("sfp_tx_disable", 0, Pins("AP11"), IOStandard("LVCMOS33")),
    ("sfp", 1,
        Subsignal("txp", Pins("AM6")),
        Subsignal("txn", Pins("AM5")),
        Subsignal("rxp", Pins("AM2")),
        Subsignal("rxn", Pins("AM1"))
    ),
    ("sfp_tx_disable", 1, Pins("AM12"), IOStandard("LVCMOS33")),
    # Master SATA connector J11
    ("sata", 0,
        Subsignal("txp", Pins("AL4")),
        Subsignal("txn", Pins("AL3")),
        Subsignal("rxp", Pins("AK2")),
        Subsignal("rxn", Pins("AK1"))
    ),

    # AD9154 DACs
    ("dac_refclk", 0,
        Subsignal("p", Pins("V6")),
        Subsignal("n", Pins("V5")),
    ),
    ("dac_refclk", 1,
        Subsignal("p", Pins("P6")),
        Subsignal("n", Pins("P5")),
    ),
    ("dac_sysref", 0,
        Subsignal("p", Pins("B10")),
        Subsignal("n", Pins("A10")),
        IOStandard("LVDS"), Misc("DIFF_TERM_ADV=TERM_100")
    ),
    ("dac_sync", 0,
        Subsignal("p", Pins("L8")),
        Subsignal("n", Pins("K8")),
        IOStandard("LVDS"), Misc("DIFF_TERM_ADV=TERM_100")
    ),
    ("dac_sync", 1,
        Subsignal("p", Pins("J9")),
        Subsignal("n", Pins("H9")),
        IOStandard("LVDS"), Misc("DIFF_TERM_ADV=TERM_100")
    ),
    ("dac_jesd", 0,
        Subsignal("txp", Pins("R4 U4 W4 AA4 AC4 AE4 AG4 AH6")),
        Subsignal("txn", Pins("R3 U3 W3 AA3 AC3 AE3 AG3 AH5"))
    ),
    ("dac_jesd", 1,
        Subsignal("txp", Pins("B6 C4 D6 F6 G4 J4 L4 N4")),
        Subsignal("txn", Pins("B5 C3 D5 F5 G3 J3 L3 N3"))
    ),

    # Raw RTM GTH pairs.
    # Those can be clocked by the Si5324 and used for DRTIO.
    ("rtm_gth", 0,
        Subsignal("txp", Pins("AH6")),
        Subsignal("txn", Pins("AH5")),
        Subsignal("rxp", Pins("AH2")),
        Subsignal("rxn", Pins("AH1")),
    ),
    ("rtm_gth", 1,
        Subsignal("txp", Pins("AG4")),
        Subsignal("txn", Pins("AG3")),
        Subsignal("rxp", Pins("AF2")),
        Subsignal("rxn", Pins("AF1")),
    ),
    ("rtm_gth", 2,
        Subsignal("txp", Pins("AE4")),
        Subsignal("txn", Pins("AE3")),
        Subsignal("rxp", Pins("AD2")),
        Subsignal("rxn", Pins("AD1")),
    ),
    ("rtm_gth", 3,
        Subsignal("txp", Pins("AC4")),
        Subsignal("txn", Pins("AC3")),
        Subsignal("rxp", Pins("AB2")),
        Subsignal("rxn", Pins("AB1")),
    ),
    ("rtm_gth", 4,
        Subsignal("txp", Pins("AA4")),
        Subsignal("txn", Pins("AA3")),
        Subsignal("rxp", Pins("Y2")),
        Subsignal("rxn", Pins("Y1")),
    ),
    ("rtm_gth", 5,
        Subsignal("txp", Pins("W4")),
        Subsignal("txn", Pins("W3")),
        Subsignal("rxp", Pins("V2")),
        Subsignal("rxn", Pins("V1")),
    ),
    ("rtm_gth", 6,
        Subsignal("txp", Pins("U4")),
        Subsignal("txn", Pins("U3")),
        Subsignal("rxp", Pins("T2")),
        Subsignal("rxn", Pins("T1")),
    ),
    ("rtm_gth", 7,
        Subsignal("txp", Pins("R4")),
        Subsignal("txn", Pins("R3")),
        Subsignal("rxp", Pins("P2")),
        Subsignal("rxn", Pins("P1")),
    ),

    ("adc_sysref", 0,
        Subsignal("p", Pins("C11")),
        Subsignal("n", Pins("B11")),
        IOStandard("LVDS"), Misc("DIFF_TERM_ADV=TERM_100")
    ),
    ("aux_clk", 0,
        Subsignal("p", Pins("AF10")),
        Subsignal("n", Pins("AG10")),
        IOStandard("LVDS_25")
    ),

    # has 100R external termination resistor
    ("sysclk1_300", 0,
        Subsignal("p", Pins("F18")),
        Subsignal("n", Pins("F17")),
        IOStandard("DIFF_SSTL15_DCI"), Misc("OUTPUT_IMPEDANCE=RDRV_40_40")
    ),

]


_connectors = [
    ("LPC", {
        "LA33_N": "V28",
        "LA32_N": "U25",
        "LA31_N": "Y28",
        "LA30_N": "U27",
        "LA29_N": "W29",
        "LA28_N": "W26",
        "LA27_N": "AB26",
        "LA26_N": "AB22",
        "LA25_N": "AB20",
        "LA24_N": "AC23",
        "LA23_N": "AC21",
        "LA22_N": "U22",
        "LA21_N": "W21",
        "LA20_N": "T23",
        "LA19_N": "V23",
        "LA18_CC_N": "Y25",
        "LA17_CC_N": "W24",
        "LA16_N": "Y30",
        "LA15_N": "Y32",
        "LA14_N": "V34",
        "LA13_N": "Y33",
        "LA12_N": "W31",
        "LA11_N": "AB29",
        "LA10_N": "AB34",
        "LA09_N": "AF32",
        "LA08_N": "AD31",
        "LA07_N": "AD33",
        "LA06_N": "AD34",
        "LA05_N": "AF34",
        "LA04_N": "AG32",
        "LA03_N": "W34",
        "LA02_N": "AG34",
        "LA01_CC_N": "AB31",
        "LA00_CC_N": "AB32",
        "LA33_P": "V27",
        "LA32_P": "U24",
        "LA31_P": "W28",
        "LA30_P": "U26",
        "LA29_P": "V29",
        "LA28_P": "V26",
        "LA27_P": "AB25",
        "LA26_P": "AA22",
        "LA25_P": "AA20",
        "LA24_P": "AC22",
        "LA23_P": "AB21",
        "LA22_P": "U21",
        "LA21_P": "V21",
        "LA20_P": "T22",
        "LA19_P": "V22",
        "LA18_CC_P": "W25",
        "LA17_CC_P": "W23",
        "LA16_P": "W30",
        "LA15_P": "Y31",
        "LA14_P": "U34",
        "LA13_P": "W33",
        "LA12_P": "V31",
        "LA11_P": "AA29",
        "LA10_P": "AA34",
        "LA09_P": "AE32",
        "LA08_P": "AD30",
        "LA07_P": "AC33",
        "LA06_P": "AC34",
        "LA05_P": "AE33",
        "LA04_P": "AG31",
        "LA03_P": "V33",
        "LA02_P": "AF33",
        "LA01_CC_P": "AB30",
        "LA00_CC_P": "AA32",
        # LVDS
        "CLK0_M2C_N": "AA25",
        "CLK0_M2C_P": "AA24",
        "CLK1_M2C_N": "AA23",
        "CLK1_M2C_P": "Y23",
        # DIFF_HSTL_I_DCI_18
        "GBTCLK0_M2C_P": "AC31",
        "GBTCLK0_M2C_N": "AC32",
        "DP0_M2C_P": "AE27",
        "DP0_M2C_N": "AF27",
        "DP0_C2M_P": "AE28",
        "DP0_C2M_N": "AF28",
    }),
]


class Platform(XilinxPlatform):
    default_clk_name = "clk50"
    default_clk_period = 20.0

    def __init__(self):
        XilinxPlatform.__init__(
                self, "xcku040-ffva1156-1-c", _io, _connectors,
                toolchain="vivado")
        self.toolchain.bitstream_commands.extend([
            # FIXME: enable this when the XADC reference wiring is fixed
            # "set_property BITSTREAM.CONFIG.OVERTEMPPOWERDOWN Enable [current_design]",
            "set_property BITSTREAM.GENERAL.COMPRESS True [current_design]",
            "set_property BITSTREAM.CONFIG.CONFIGRATE 33 [current_design]",
            "set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]",
            "set_property CFGBVS VCCO [current_design]",
            "set_property CONFIG_VOLTAGE 3.3 [current_design]",
            ])

    # We do not contrain Ethernet clocks here, since we do not know
    # if they are RGMII (125MHz) or MII (25MHz)
