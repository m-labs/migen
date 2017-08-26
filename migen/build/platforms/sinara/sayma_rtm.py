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
        Subsignal("mosi", Pins("B16"), Misc("PULLDOWN")),
        Subsignal("miso", Pins("D9")),
        # cs[0]=830 cs[1]=7043
        Subsignal("cs_n", Pins("C8 D16")),
        IOStandard("LVCMOS25")
    ),
    ("hmc7043_reset", 0, Pins("E17"), IOStandard("LVCMOS25")),
]


class Platform(XilinxPlatform):
    default_clk_name = "clk50"
    default_clk_period = 20.0

    def __init__(self):
        XilinxPlatform.__init__(self, "xc7a15t-csg325-1", _io, toolchain="vivado")
