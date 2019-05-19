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
        Subsignal("p", Pins("Y6")),
        Subsignal("n", Pins("Y5"))
    ),
    ("port0", 0,
        Subsignal("txp", Pins("B6")),
        Subsignal("txn", Pins("B5")),
        Subsignal("rxp", Pins("A4")),
        Subsignal("rxn", Pins("A3"))
    ),

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
]


class Platform(XilinxPlatform):
    default_clk_name = "clk50"
    default_clk_period = 20.0

    def __init__(self):
        XilinxPlatform.__init__(self, "xcku040-ffva1156-1-c", _io, toolchain="vivado")
        self.toolchain.bitstream_commands.extend([
            "set_property BITSTREAM.CONFIG.OVERTEMPSHUTDOWN Enable [current_design]",
            "set_property BITSTREAM.GENERAL.COMPRESS True [current_design]",
            "set_property BITSTREAM.CONFIG.CONFIGRATE 33 [current_design]",
            "set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]",
            "set_property CFGBVS VCCO [current_design]",
            "set_property CONFIG_VOLTAGE 3.3 [current_design]",
            ])
