from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform


_io = [
    ("clk50", 0, Pins("E15"), IOStandard("LVCMOS33")),

    ("serial", 0,
        Subsignal("tx", Pins("C16")),
        Subsignal("rx", Pins("B17")),
        IOStandard("LVCMOS33")
    ),

    ("amc_rtm_serwb", 0,
        Subsignal("clk", Pins("R18")), # rtm_fpga_usr_io_p
        Subsignal("tx", Pins("T17")),  # rtm_fpga_lvds2_p
        Subsignal("rx", Pins("R16")),  # rtm_fpga_lvds1_p
        IOStandard("LVCMOS18")
    ),

    # HMC clocking chips (830 and 7043)
    ("hmc_spi", 0,
        Subsignal("clk", Pins("A17"), Misc("PULLDOWN=TRUE")),
        # cs[0]=830 cs[1]=7043
        # Watch out for the HMC830 SPI mode peculiarity. PULLDOWN CS here
        # so that toggling the SPI core offline will make edges.
        Subsignal("cs_n", Pins("C8 D16"), Misc("PULLDOWN=TRUE")),
        Subsignal("mosi", Pins("B16"), Misc("PULLDOWN=TRUE")),
        Subsignal("miso", Pins("D9"), Misc("PULLDOWN=TRUE")),
        IOStandard("LVCMOS33")
    ),
    ("hmc7043_reset", 0, Pins("E17"), IOStandard("LVCMOS33")),
    ("hmc7043_gpo", 0, Pins("D8"), IOStandard("LVCMOS33")),

    # clock mux
    ("clk_src_ext_sel", 0, Pins("P15"), IOStandard("LVCMOS18")),
    ("ref_clk_src_sel", 0, Pins("J14"), IOStandard("LVCMOS18")),
    ("dac_clk_src_sel", 0, Pins("P16"), IOStandard("LVCMOS18")),
    ("ref_lo_clk_sel", 0, Pins("L18"), IOStandard("LVCMOS18")),

    # DACs
    ("ad9154_rst_n", 0, Pins("U15"), IOStandard("LVCMOS18")),
    ("ad9154_spi", 0,
        Subsignal("clk", Pins("T13"), Misc("PULLDOWN=TRUE")),
        Subsignal("cs_n", Pins("U14"), Misc("PULLUP=TRUE")),
        Subsignal("mosi", Pins("V17"), Misc("PULLDOWN=TRUE")),
        Subsignal("miso", Pins("R13"), Misc("PULLDOWN=TRUE")),
        IOStandard("LVCMOS18")
    ),
    ("ad9154_txen", 0, Pins("V16 U16"), IOStandard("LVCMOS18")),
    ("ad9154_spi", 1,
        Subsignal("clk", Pins("J15"), Misc("PULLDOWN=TRUE")),
        Subsignal("cs_n", Pins("K18"), Misc("PULLUP=TRUE")),
        Subsignal("mosi", Pins("J18"), Misc("PULLDOWN=TRUE")),
        Subsignal("miso", Pins("J16"), Misc("PULLDOWN=TRUE")),
        IOStandard("LVCMOS18")
    ),
    ("ad9154_txen", 1, Pins("L17 L14"), IOStandard("LVCMOS18")),

    # Allaki
    ("allaki0_rfsw0", 1, Pins("R2"), IOStandard("LVCMOS33")),
    ("allaki0_rfsw1", 1, Pins("N4"), IOStandard("LVCMOS33")),
    ("allaki1_rfsw0", 1, Pins("R5"), IOStandard("LVCMOS33")),
    ("allaki1_rfsw1", 1, Pins("V4"), IOStandard("LVCMOS33")),
    ("allaki2_rfsw0", 1, Pins("B15"), IOStandard("LVCMOS33")),
    ("allaki2_rfsw1", 1, Pins("B12"), IOStandard("LVCMOS33")),
    ("allaki3_rfsw0", 1, Pins("L4"), IOStandard("LVCMOS33")),
    ("allaki3_rfsw1", 1, Pins("J4"), IOStandard("LVCMOS33")),

    ("allaki0_att0", 1,
        Subsignal("le", Pins("U2")),
        Subsignal("sin", Pins("T4")),
        Subsignal("clk", Pins("V3")),
        Subsignal("rst_n", Pins("R3")),
        IOStandard("LVCMOS33")
    ),
    ("allaki0_att1", 1,
        Subsignal("le", Pins("P1")),
        Subsignal("sin", Pins("P3")),
        Subsignal("clk", Pins("N3")),
        Subsignal("rst_n", Pins("M4")),
        IOStandard("LVCMOS33")
    ),
    ("allaki1_att0", 1,
        Subsignal("le", Pins("U7")),
        Subsignal("sin", Pins("R6")),
        Subsignal("clk", Pins("V8")),
        Subsignal("rst_n", Pins("R7")),
        IOStandard("LVCMOS33")
    ),
    ("allaki1_att1", 1,
        Subsignal("le", Pins("T3")),
        Subsignal("sin", Pins("U5")),
        Subsignal("clk", Pins("P6")),
        Subsignal("rst_n", Pins("U4")),
        IOStandard("LVCMOS33")
    ),
    ("allaki2_att0", 1,
        Subsignal("le", Pins("C13")),
        Subsignal("sin", Pins("E16")),
        Subsignal("clk", Pins("D14")),
        Subsignal("rst_n", Pins("A15")),
        IOStandard("LVCMOS33")
    ),
    ("allaki2_att1", 1,
        Subsignal("le", Pins("D11")),
        Subsignal("sin", Pins("C14")),
        Subsignal("clk", Pins("A12")),
        Subsignal("rst_n", Pins("C12")),
        IOStandard("LVCMOS33")
    ),
    ("allaki3_att0", 1,
        Subsignal("le", Pins("M2")),
        Subsignal("sin", Pins("N1")),
        Subsignal("clk", Pins("M6")),
        Subsignal("rst_n", Pins("L5")),
        IOStandard("LVCMOS33")
    ),
    ("allaki3_att1", 1,
        Subsignal("le", Pins("K5")),
        Subsignal("sin", Pins("L2")),
        Subsignal("clk", Pins("K2")),
        Subsignal("rst_n", Pins("J5")),
        IOStandard("LVCMOS33")
    ),
]

_connectors = [
    ("clk_mez", {
        "gpio_{}".format(num): pin for num, pin in enumerate(
             "D18 C17 C18 G17 F18 H16 G15 G15"
             "F15 G14 F14 H17 H18 F17 H14 E18".split())}),
]


class Platform(XilinxPlatform):
    default_clk_name = "clk50"
    default_clk_period = 20.0

    def __init__(self):
        XilinxPlatform.__init__(self, "xc7a15t-csg325-1", _io, _connectors,
                                toolchain="vivado")
        self.toolchain.bitstream_commands.extend([
            # FIXME: enable this when the XADC reference wiring is fixed
            # "set_property BITSTREAM.CONFIG.OVERTEMPPOWERDOWN Enable [current_design]",
            "set_property BITSTREAM.GENERAL.COMPRESS True [current_design]",
            "set_property CFGBVS VCCO [current_design]",
            "set_property CONFIG_VOLTAGE 3.3 [current_design]",
        ])
