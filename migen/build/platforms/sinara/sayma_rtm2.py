from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform


_io = [
    ("clk50", 0, Pins("R2"), IOStandard("LVCMOS25")),

    ("serial", 0,
        Subsignal("tx", Pins("C16")),
        Subsignal("rx", Pins("B17")),
        IOStandard("LVCMOS33")
    ),

    ("amc_rtm_serwb", 0,
        Subsignal("clk_p", Pins("P14"), Misc("DIFF_TERM=TRUE")), # LVDS26_CC_P
        Subsignal("clk_n", Pins("R15"), Misc("DIFF_TERM=TRUE")), # LVDS26_CC_N
        Subsignal("tx_p", Pins("T17")),  # LVDS27_P
        Subsignal("tx_n", Pins("U17")),  # LVDS27_N
        Subsignal("rx_p", Pins("R18"), Misc("DIFF_TERM=TRUE")),  # LVDS25_P
        Subsignal("rx_n", Pins("T18"), Misc("DIFF_TERM=TRUE")),  # LVDS25_N
        IOStandard("LVDS_25")
    ),

    # HMC clocking chips (830 and 7043)
    ("hmc_spi", 0,
        Subsignal("clk", Pins("A17"), Misc("PULLDOWN=TRUE")),
        # cs[0]=830 cs[1]=7043
        # Watch out for the HMC830 SPI mode peculiarity. PULLDOWN CS here
        # so that toggling the SPI core offline will make edges.
        #TODO Subsignal("cs_n", Pins("C8 D16"), Misc("PULLDOWN=TRUE")),
        Subsignal("mosi", Pins("B16"), Misc("PULLDOWN=TRUE")),
        Subsignal("miso", Pins("D9"), Misc("PULLDOWN=TRUE")),
        IOStandard("LVCMOS33")
    ),
    ("hmc7043_reset", 0, Pins("E17"), IOStandard("LVCMOS33")),
    ("hmc7043_gpo", 0, Pins("D8"), IOStandard("LVCMOS33")),

    # clock mux
    ("clk_src_ext_sel", 0, Pins("D16"), IOStandard("LVCMOS33")),

    # DACs
    ("ad9154_spi", 0,
        Subsignal("clk", Pins("V17"), Misc("PULLDOWN=TRUE")),
        Subsignal("cs_n", Pins("V16"), Misc("PULLUP=TRUE")),
        Subsignal("mosi", Pins("R13"), Misc("PULLDOWN=TRUE")),
        Subsignal("miso", Pins("T13"), Misc("PULLDOWN=TRUE")),
        IOStandard("LVCMOS25")
    ),
    ("ad9154_txen", 0, Pins("U14 V14"), IOStandard("LVCMOS25")),
    ("ad9154_rst_n", 0, Pins("U16"), IOStandard("LVCMOS25")),
    ("ad9154_spi", 1,
        Subsignal("clk", Pins("J16"), Misc("PULLDOWN=TRUE")),
        Subsignal("cs_n", Pins("J15"), Misc("PULLUP=TRUE")),
        Subsignal("mosi", Pins("K18"), Misc("PULLDOWN=TRUE")),
        Subsignal("miso", Pins("K17"), Misc("PULLDOWN=TRUE")),
        IOStandard("LVCMOS25")
    ),
    ("ad9154_txen", 1, Pins("L18 J14"), IOStandard("LVCMOS25")),
    ("ad9154_rst_n", 1, Pins("K16"), IOStandard("LVCMOS25")),

    ("i2c", 0,
        Subsignal("scl", Pins("D13")),
        Subsignal("sda", Pins("C13")),
        IOStandard("LVCMOS33")
    ),

    ("si5324", 0,
        Subsignal("rst_n", Pins("C9"), IOStandard("LVCMOS33")),
        Subsignal("int", Pins("D15"), IOStandard("LVCMOS33"))
    ),
    ("si5324_clkin", 0,
        Subsignal("p", Pins("M16")),
        Subsignal("n", Pins("M17")),
        IOStandard("LVDS_25"),
    ),
    # TODO: rename, this will be muxed with the WR PLL
    ("si5324_clkout", 0,
        Subsignal("p", Pins("B6")),
        Subsignal("n", Pins("B5"))
    ),
    ("si5324_clkout_fabric", 0,
        Subsignal("p", Pins("T14")),
        Subsignal("n", Pins("T15")),
        IOStandard("LVDS_25")
    ),
    # Slave SATA connector J14
    ("sata", 0,
        Subsignal("txp", Pins("D2")),
        Subsignal("txn", Pins("D1")),
        Subsignal("rxp", Pins("C4")),
        Subsignal("rxn", Pins("C3"))
    ),
]

class Platform(XilinxPlatform):
    default_clk_name = "clk50"
    default_clk_period = 20.0

    def __init__(self, larger=False):
        chip = "xc7a50t-csg325-1" if larger else "xc7a15t-csg325-1"
        XilinxPlatform.__init__(self, chip, _io,
                                toolchain="vivado", name="sayma_rtm")
        self.toolchain.bitstream_commands.extend([
            "set_property BITSTREAM.CONFIG.OVERTEMPPOWERDOWN Enable [current_design]",
            "set_property BITSTREAM.GENERAL.COMPRESS True [current_design]",
            "set_property CFGBVS VCCO [current_design]",
            "set_property CONFIG_VOLTAGE 3.3 [current_design]",
        ])

