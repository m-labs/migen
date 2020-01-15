from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform


_io = [
    ("clk125_gtp", 0,
        Subsignal("p", Pins("D6")),
        Subsignal("n", Pins("D5")),
    ),

    ("serial", 0,
        Subsignal("tx", Pins("U17")),
        Subsignal("rx", Pins("T17")),
        IOStandard("LVCMOS33")
    ),

    # HMC clocking chips (830 and 7043)
    ("hmc830_pwr_en", 0, Pins("V7"), IOStandard("LVCMOS25")),
    ("hmc7043_out_en", 0, Pins("V8"), IOStandard("LVCMOS25")),
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
        Subsignal("scl", Pins("P15")),
        Subsignal("sda", Pins("P16")),
        IOStandard("LVCMOS33")
    ),

    ("filtered_clk_sel", 0, Pins("M5"), IOStandard("LVCMOS25")),
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
    ("ddmtd_main_dcxo_oe", 0, Pins("N6"), IOStandard("LVCMOS25")),
    ("ddmtd_main_dcxo_i2c", 0,
        Subsignal("scl", Pins("P14")),
        Subsignal("sda", Pins("U15")),
        IOStandard("LVCMOS33")),
    ("ddmtd_helper_dcxo_oe", 0, Pins("M6"), IOStandard("LVCMOS25")),
    ("ddmtd_helper_dcxo_i2c", 0,
        Subsignal("scl", Pins("T15")),
        Subsignal("sda", Pins("R16")),
        IOStandard("LVCMOS33")),
    ("ddmtd_helper_clk", 0,
        Subsignal("p", Pins("N3")),
        Subsignal("n", Pins("N2")),
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

    # NOTE: AFE pins here are numbered after DAC channels and NOT signal indices
    # See: https://github.com/sinara-hw/BaseMod/issues/29
    # AFE0 pins
    ("basemod0_rfsw", 0, Pins("U16"), IOStandard("LVCMOS33")),
    ("basemod0_rfsw", 1, Pins("U14"), IOStandard("LVCMOS33")),
    ("basemod0_rfsw", 2, Pins("V14"), IOStandard("LVCMOS33")),
    ("basemod0_rfsw", 3, Pins("V12"), IOStandard("LVCMOS33")),
    ("basemod0_att", 0,
        Subsignal("le", Pins("V17")),
        Subsignal("miso", Pins("V13 V9 U11 U9")),
        Subsignal("mosi", Pins("R13 T12 U12 V11")),
        Subsignal("clk", Pins("V16")),
        Subsignal("rst_n", Pins("T13")),
        IOStandard("LVCMOS33")
    ),

    # AFE0 ADC amp
    ("basemod0_adc_amp_a0", 0, Pins("H16"), IOStandard("LVCMOS25")),
    ("basemod0_adc_amp_a0", 1, Pins("C17"), IOStandard("LVCMOS25")),
    ("basemod0_adc_amp_a0", 2, Pins("E17"), IOStandard("LVCMOS25")),
    ("basemod0_adc_amp_a0", 3, Pins("G14"), IOStandard("LVCMOS25")),
    ("basemod0_adc_amp_a1", 0, Pins("G16"), IOStandard("LVCMOS25")),
    ("basemod0_adc_amp_a1", 1, Pins("C18"), IOStandard("LVCMOS25")),
    ("basemod0_adc_amp_a1", 2, Pins("D18"), IOStandard("LVCMOS25")),
    ("basemod0_adc_amp_a1", 3, Pins("F14"), IOStandard("LVCMOS25")),

    # AFE1 pins
    ("basemod1_rfsw", 0, Pins("J16"), IOStandard("LVCMOS33")),
    ("basemod1_rfsw", 1, Pins("K15"), IOStandard("LVCMOS33")),
    ("basemod1_rfsw", 2, Pins("L15"), IOStandard("LVCMOS33")),
    ("basemod1_rfsw", 3, Pins("M15"), IOStandard("LVCMOS33")),
    ("basemod1_att", 0,
        Subsignal("le", Pins("K17")),
        Subsignal("miso", Pins("M16 N18 N14 N17")),
        Subsignal("mosi", Pins("L18 M17 M14 N16")),
        Subsignal("clk", Pins("K18")),
        Subsignal("rst_n", Pins("J14")),
        IOStandard("LVCMOS33")
    ),

    # AFE1 ADC amp
    ("basemod1_adc_amp_a0", 0, Pins("D8"), IOStandard("LVCMOS25")),
    ("basemod1_adc_amp_a0", 1, Pins("D9"), IOStandard("LVCMOS25")),
    ("basemod1_adc_amp_a0", 2, Pins("B9"), IOStandard("LVCMOS25")),
    ("basemod1_adc_amp_a0", 3, Pins("C11"), IOStandard("LVCMOS25")),
    ("basemod1_adc_amp_a1", 0, Pins("C8"), IOStandard("LVCMOS25")),
    ("basemod1_adc_amp_a1", 1, Pins("C9"), IOStandard("LVCMOS25")),
    ("basemod1_adc_amp_a1", 2, Pins("A9"), IOStandard("LVCMOS25")),
    ("basemod1_adc_amp_a1", 3, Pins("B11"), IOStandard("LVCMOS25")),

    # Header I/O
    ("header_gpio", 0, Pins("B17"), IOStandard("LVCMOS25")),
    ("header_gpio", 1, Pins("C16"), IOStandard("LVCMOS25")),
    ("header_gpio", 2, Pins("A17"), IOStandard("LVCMOS25")),
    ("header_gpio", 3, Pins("B16"), IOStandard("LVCMOS25")),
    ("header_gpio", 4, Pins("D16"), IOStandard("LVCMOS25")),
    ("header_gpio", 5, Pins("E16"), IOStandard("LVCMOS25")),
    ("header_gpio", 6, Pins("A15"), IOStandard("LVCMOS25")),
    ("header_gpio", 7, Pins("B14"), IOStandard("LVCMOS25")),
    ("header_gpio", 8, Pins("C13"), IOStandard("LVCMOS25")),
    ("header_gpio", 9, Pins("D13"), IOStandard("LVCMOS25")),
]

class Platform(XilinxPlatform):
    default_clk_name = "clk50"
    default_clk_period = 20.0

    def __init__(self):
        chip = "xc7a50t-csg325-3"
        XilinxPlatform.__init__(self, chip, _io,
                                toolchain="vivado", name="sayma_rtm")
        self.toolchain.bitstream_commands.extend([
            "set_property BITSTREAM.CONFIG.OVERTEMPPOWERDOWN Enable [current_design]",
            "set_property BITSTREAM.GENERAL.COMPRESS True [current_design]",
            "set_property CFGBVS VCCO [current_design]",
            "set_property CONFIG_VOLTAGE 3.3 [current_design]",
        ])
