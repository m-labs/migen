from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform


_io = [
    ("clk50", 0, Pins("E15"), IOStandard("LVCMOS25")),

    ("serial", 0,
        Subsignal("tx", Pins("C16")),
        Subsignal("rx", Pins("B17")),
        IOStandard("LVCMOS25")
    ),

    ("amc_rtm_serwb", 0,
        Subsignal("clk_p", Pins("R18")), # rtm_fpga_usr_io_p
        Subsignal("clk_n", Pins("T18")), # rtm_fpga_usr_io_n
        Subsignal("tx_p", Pins("T17")),  # rtm_fpga_lvds2_p
        Subsignal("tx_n", Pins("U17")),  # rtm_fpga_lvds2_n
        Subsignal("rx_p", Pins("R16")),  # rtm_fpga_lvds1_p
        Subsignal("rx_n", Pins("R17")),  # rtm_fpga_lvds1_n
        IOStandard("LVDS_25")
    ),

    # HMC clocking chips (830 and 7043)
    ("hmc_spi", 0,
        Subsignal("clk", Pins("A17")),
        Subsignal("mosi", Pins("B16")),
        Subsignal("miso", Pins("D9"), Misc("PULLDOWN")),
        # cs[0]=830 cs[1]=7043
        Subsignal("cs_n", Pins("C8 D16")),
        IOStandard("LVCMOS25")
    ),
    ("hmc7043_reset", 0, Pins("E17"), IOStandard("LVCMOS25")),

    # clock mux
    ("clk_src_ext_sel", 0, Pins("P15"), IOStandard("LVCMOS25")),
    ("ref_clk_src_sel", 0, Pins("J14"), IOStandard("LVCMOS25")),
    ("dac_clk_src_sel", 0, Pins("P16"), IOStandard("LVCMOS25")),

    # DACs
    ("ad9154_rst_n", 0, Pins("U15"), IOStandard("LVCMOS25")),
    ("ad9154_spi", 0,
        Subsignal("clk", Pins("T13")),
        Subsignal("cs_n", Pins("U14")),
        Subsignal("mosi", Pins("V17")),
        Subsignal("miso", Pins("R13"), Misc("PULLDOWN")),
        IOStandard("LVCMOS25")
    ),
    ("ad9154_txen", 0, Pins("V16 U16"), IOStandard("LVCMOS25")),
    ("ad9154_spi", 1,
        Subsignal("clk", Pins("J15")),
        Subsignal("cs_n", Pins("K18")),
        Subsignal("mosi", Pins("J18")),
        Subsignal("miso", Pins("J16"), Misc("PULLDOWN")),
        IOStandard("LVCMOS25")
    ),
    ("ad9154_txen", 1, Pins("L17 L14"), IOStandard("LVCMOS25")),
]


class Platform(XilinxPlatform):
    default_clk_name = "clk50"
    default_clk_period = 20.0

    def __init__(self):
        XilinxPlatform.__init__(self, "xc7a15t-csg325-1", _io, toolchain="vivado")
