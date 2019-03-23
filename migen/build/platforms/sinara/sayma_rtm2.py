from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform


_io = [
    ("clk50", 0, Pins("T14"), IOStandard("LVCMOS33")),

    ("serial", 0,
        Subsignal("tx", Pins("T17")),
        Subsignal("rx", Pins("U17")),
        IOStandard("LVCMOS33")
    ),

    ("amc_rtm_serwb", 0,
        Subsignal("clk_p", Pins("P4"), Misc("DIFF_TERM=TRUE")), # LVDS26_CC_P
        Subsignal("clk_n", Pins("P3"), Misc("DIFF_TERM=TRUE")), # LVDS26_CC_N
        Subsignal("tx_p", Pins("V3")),  # LVDS27_P
        Subsignal("tx_n", Pins("V2")),  # LVDS27_N
        Subsignal("rx_p", Pins("U2"), Misc("DIFF_TERM=TRUE")),  # LVDS25_P
        Subsignal("rx_n", Pins("U1"), Misc("DIFF_TERM=TRUE")),  # LVDS25_N
        IOStandard("LVDS_25")
    ),

    # HMC clocking chips (830 and 7043)
    ("hmc_spi", 0,
        Subsignal("clk", Pins("T18"), Misc("PULLDOWN=TRUE")),
        # cs[0]=830 cs[1]=7043
        # Watch out for the HMC830 SPI mode peculiarity. PULLDOWN CS here
        # so that toggling the SPI core offline will make edges.
        Subsignal("cs_n", Pins("K16 R17"), Misc("PULLDOWN=TRUE")),
        Subsignal("mosi", Pins("R18"), Misc("PULLDOWN=TRUE")),
        Subsignal("miso", Pins("J15"), Misc("PULLDOWN=TRUE")),
        IOStandard("LVCMOS33")
    ),
    ("hmc7043_reset", 0, Pins("J18"), IOStandard("LVCMOS33")),
    ("hmc7043_gpo", 0, Pins("L14"), IOStandard("LVCMOS33")),

    ("rtm_fpga_sysref", 0,
        Subsignal("p", Pins("R3")),
        Subsignal("n", Pins("T2")),
        IOStandard("LVDS_25"), Misc("DIFF_TERM=TRUE")
    ),
    ("rtm_fpga_sysref", 1,
        Subsignal("p", Pins("R5")),
        Subsignal("n", Pins("T5")),
        IOStandard("LVDS_25"), Misc("DIFF_TERM=TRUE")
    ),

    # clock mux
    ("clk_src_ext_sel", 0, Pins("R6"), IOStandard("LVCMOS25")),

    # DACs
    ("ad9154_spi", 0,
        Subsignal("clk", Pins("V4"), Misc("PULLDOWN=TRUE")),
        Subsignal("cs_n", Pins("U4"), Misc("PULLUP=TRUE")),
        Subsignal("mosi", Pins("P6"), Misc("PULLDOWN=TRUE")),
        Subsignal("miso", Pins("P5"), Misc("PULLDOWN=TRUE")),
        IOStandard("LVCMOS25")
    ),
    ("ad9154_txen", 0, Pins("U6 U5"), IOStandard("LVCMOS25")),
    ("ad9154_rst_n", 0, Pins("T3"), IOStandard("LVCMOS25")),
    ("ad9154_spi", 1,
        Subsignal("clk", Pins("K2"), Misc("PULLDOWN=TRUE")),
        Subsignal("cs_n", Pins("J4"), Misc("PULLUP=TRUE")),
        Subsignal("mosi", Pins("K1"), Misc("PULLDOWN=TRUE")),
        Subsignal("miso", Pins("K3"), Misc("PULLDOWN=TRUE")),
        IOStandard("LVCMOS25")
    ),
    ("ad9154_txen", 1, Pins("L2 L4"), IOStandard("LVCMOS25")),
    ("ad9154_rst_n", 1, Pins("J5"), IOStandard("LVCMOS25")),

    ("i2c", 0,
        Subsignal("scl", Pins("P16")),
        Subsignal("sda", Pins("P15")),
        IOStandard("LVCMOS33")
    ),

    ("si5324", 0,
        Subsignal("rst_n", Pins("C14"), IOStandard("LVCMOS25")),
        Subsignal("int", Pins("V6"), IOStandard("LVCMOS25"))
    ),
    ("si5324_clkin", 0,
        Subsignal("p", Pins("M2")),
        Subsignal("n", Pins("M1")),
        IOStandard("LVDS_25"),
    ),
    ("cdr_clk_clean", 0,
        Subsignal("p", Pins("B6")),
        Subsignal("n", Pins("B5"))
    ),
    ("cdr_clk_clean_fabric", 0,
        Subsignal("p", Pins("R2")),
        Subsignal("n", Pins("R1")),
        IOStandard("LVDS_25"), Misc("DIFF_TERM=TRUE")
    ),
    ("rtm_amc_link", 0,
        Subsignal("txp", Pins("H2")),
        Subsignal("txn", Pins("H1")),
        Subsignal("rxp", Pins("E4")),
        Subsignal("rxn", Pins("E3"))
    ),
    # SATA connector J13
    ("sata", 0,
        Subsignal("txp", Pins("B2")),
        Subsignal("txn", Pins("B1")),
        Subsignal("rxp", Pins("G4")),
        Subsignal("rxn", Pins("G3"))
    ),

    # Bogus AFE pins for testing (TODO)
    ("allaki0_rfsw0", 0, Pins("E18"), IOStandard("LVCMOS25")),
    ("allaki0_rfsw1", 0, Pins("F17"), IOStandard("LVCMOS25")),
]

class Platform(XilinxPlatform):
    default_clk_name = "clk50"
    default_clk_period = 20.0

    def __init__(self, larger=False):
        chip = "xc7a50t-csg325-3" if larger else "xc7a35t-csg325-3"
        XilinxPlatform.__init__(self, chip, _io,
                                toolchain="vivado", name="sayma_rtm")
        self.toolchain.bitstream_commands.extend([
            "set_property BITSTREAM.CONFIG.OVERTEMPPOWERDOWN Enable [current_design]",
            "set_property BITSTREAM.GENERAL.COMPRESS True [current_design]",
            "set_property CFGBVS VCCO [current_design]",
            "set_property CONFIG_VOLTAGE 3.3 [current_design]",
        ])

