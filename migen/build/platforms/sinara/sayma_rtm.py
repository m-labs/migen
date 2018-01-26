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
        Subsignal("miso", Pins("D9"), Misc("PULLDOWN=TRUE")),
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
        Subsignal("miso", Pins("R13"), Misc("PULLDOWN=TRUE")),
        IOStandard("LVCMOS25")
    ),
    ("ad9154_txen", 0, Pins("V16 U16"), IOStandard("LVCMOS25")),
    ("ad9154_spi", 1,
        Subsignal("clk", Pins("J15")),
        Subsignal("cs_n", Pins("K18")),
        Subsignal("mosi", Pins("J18")),
        Subsignal("miso", Pins("J16"), Misc("PULLDOWN=TRUE")),
        IOStandard("LVCMOS25")
    ),
    ("ad9154_txen", 1, Pins("L17 L14"), IOStandard("LVCMOS25")),

    # Allaki
    ("allaki0_rfsw0", 1, Pins("R2"), IOStandard("LVCMOS25")),
    ("allaki0_rfsw1", 1, Pins("N4"), IOStandard("LVCMOS25")),
    ("allaki1_rfsw0", 1, Pins("R5"), IOStandard("LVCMOS25")),
    ("allaki1_rfsw1", 1, Pins("V4"), IOStandard("LVCMOS25")),
    ("allaki2_rfsw0", 1, Pins("B15"), IOStandard("LVCMOS25")),
    ("allaki2_rfsw1", 1, Pins("B12"), IOStandard("LVCMOS25")),
    ("allaki3_rfsw0", 1, Pins("L4"), IOStandard("LVCMOS25")),
    ("allaki3_rfsw1", 1, Pins("J4"), IOStandard("LVCMOS25")),

    ("allaki0_att0", 1,
        Subsignal("le", Pins("U2")),
        Subsignal("sin", Pins("T4")),
        Subsignal("clk", Pins("V3")),
        Subsignal("rst_n", Pins("R3")),
        IOStandard("LVCMOS25")
    ),
    ("allaki0_att1", 1,
        Subsignal("le", Pins("P1")),
        Subsignal("sin", Pins("P3")),
        Subsignal("clk", Pins("N3")),
        Subsignal("rst_n", Pins("M4")),
        IOStandard("LVCMOS25")
    ),
    ("allaki1_att0", 1,
        Subsignal("le", Pins("U7")),
        Subsignal("sin", Pins("R6")),
        Subsignal("clk", Pins("V8")),
        Subsignal("rst_n", Pins("R7")),
        IOStandard("LVCMOS25")
    ),
    ("allaki1_att1", 1,
        Subsignal("le", Pins("T3")),
        Subsignal("sin", Pins("U5")),
        Subsignal("clk", Pins("P6")),
        Subsignal("rst_n", Pins("U4")),
        IOStandard("LVCMOS25")
    ),
    ("allaki2_att0", 1,
        Subsignal("le", Pins("C13")),
        Subsignal("sin", Pins("E16")),
        Subsignal("clk", Pins("D14")),
        Subsignal("rst_n", Pins("A15")),
        IOStandard("LVCMOS25")
    ),
    ("allaki2_att1", 1,
        Subsignal("le", Pins("D11")),
        Subsignal("sin", Pins("C14")),
        Subsignal("clk", Pins("A12")),
        Subsignal("rst_n", Pins("C12")),
        IOStandard("LVCMOS25")
    ),
    ("allaki3_att0", 1,
        Subsignal("le", Pins("M2")),
        Subsignal("sin", Pins("N1")),
        Subsignal("clk", Pins("M6")),
        Subsignal("rst_n", Pins("L5")),
        IOStandard("LVCMOS25")
    ),
    ("allaki3_att1", 1,
        Subsignal("le", Pins("K5")),
        Subsignal("sin", Pins("L2")),
        Subsignal("clk", Pins("K2")),
        Subsignal("rst_n", Pins("J5")),
        IOStandard("LVCMOS25")
    ),
]


class Platform(XilinxPlatform):
    default_clk_name = "clk50"
    default_clk_period = 20.0

    def __init__(self):
        XilinxPlatform.__init__(self, "xc7a15t-csg325-1", _io, toolchain="vivado")
