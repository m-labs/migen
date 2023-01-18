# EEM FMC Carrier

# Copyright (c) 2022 Jakub Matyas
# Warsaw Univeristy of Technology <jakub.matyas.stud@pw.edu.pl>
# Copyright (c) 2022 Paweł Kulik
# Creotech Instruments S.A. <pawel.kulik@creotech.pl>
# SPDX-License-Identifier: BSD-2-Clause

from migen.build.generic_platform import IOStandard, Pins, Subsignal, Misc
from migen.build.xilinx import XilinxPlatform

# IOs ----------------------------------------------------------------------------------------------

_ios = [
    ("gpio_int", 0, Pins("T20"), IOStandard("LVCMOS25")),
    ("i2c_mux_rst_n", 0, Pins("R14"), IOStandard("LVCMOS25")),
    ("fan_pwm", 0, Pins("N15"), IOStandard("LVCMOS25")),
    ("servmod", 0, Pins("P14"), IOStandard("LVCMOS25")),
    ("pgood_fmc", 0, Pins("P20"), IOStandard("LVCMOS25")),
    ("pg_m2c", 0, Pins("M17"), IOStandard("LVCMOS15")),

    ("serial", 0,
        Subsignal("rx", Pins("U22")),  # FPGA input, schematics TxD_2V5
        Subsignal("tx", Pins("U21")),  # FPGA output, schematics RxD_2V5
        IOStandard("LVCMOS25")
    ),

    ("gtp_clk", 0,
        Subsignal("p", Pins("F10")),
        Subsignal("n", Pins("E10"))
        # IOStandard("LVDS_25")
    ),

    ("fpga_i2c", 0,
        Subsignal("scl", Pins("V22")),
        Subsignal("sda", Pins("T21")),
        IOStandard("LVCMOS25")
    ),

    # FMC
    ("fmc_clk_m2c", 0,
        Subsignal("p", Pins("C18")),
        Subsignal("n", Pins("C19")),
        IOStandard("LVDS_25")
    ),
    ("fmc_clk_m2c", 1,
        Subsignal("p", Pins("D17")),
        Subsignal("n", Pins("C17")),
        IOStandard("LVDS_25")
    ),
    ("fmc_clk_bdir", 0,
        Subsignal("p", Pins("Y18")),
        Subsignal("n", Pins("Y19")),
        IOStandard("LVDS_25")
    ),
    ("fmc_clk_bdir", 1,
        Subsignal("p", Pins("W19")),
        Subsignal("n", Pins("W20")),
        IOStandard("LVDS_25")
    ),

    ("shared_bus", 0,
        Subsignal("dir", Pins("F21 D20 E22 F15 D21")),
        Subsignal("vadj", Pins("G22 E21 G21 D14 D22")),
        IOStandard("LVCMOS25")
    ),
    ("gtp3_sel", 0, Pins("F4"), IOStandard("LVCMOS25")),


    ("ddram", 0,
        Subsignal("a", Pins(
            "H14 G13 J22 H13 H17 G16 K21 G15 "
            "H18 J21 J16 H20 K22 H22 G20"),
            IOStandard("SSTL15")),
        Subsignal("ba", Pins("H19 J20 H15"), IOStandard("SSTL15")),
        Subsignal("ras_n", Pins("J15"), IOStandard("SSTL15")),
        Subsignal("cas_n", Pins("J14"), IOStandard("SSTL15")),
        Subsignal("we_n", Pins("L21"), IOStandard("SSTL15")),
        Subsignal("dm", Pins("M13 K19"), IOStandard("SSTL15")),
        Subsignal("dq", Pins(
            "L13 L14 M16 K16 K14 L16 M15 L15 "
            "M20 M18 L18 L20 N18 N20 N19 L19"),
            IOStandard("SSTL15"),
            Misc("IN_TERM=UNTUNED_SPLIT_50")),
        Subsignal("dqs_p", Pins("K17 N22"), IOStandard("DIFF_SSTL15")),
        Subsignal("dqs_n", Pins("J17 M22"), IOStandard("DIFF_SSTL15")),
        Subsignal("clk_p", Pins("G17"), IOStandard("DIFF_SSTL15")),
        Subsignal("clk_n", Pins("G18"), IOStandard("DIFF_SSTL15")),
        Subsignal("cke", Pins("M21"), IOStandard("SSTL15")),
        Subsignal("odt", Pins("J19"), IOStandard("SSTL15")),
        Subsignal("reset_n", Pins("K18"), IOStandard("LVCMOS15")),
        Misc("SLEW=FAST"),
    ),

    ("spiflash1x", 0,
        Subsignal("cs_n", Pins("T19")),
        Subsignal("dq", Pins("P22 R22 P21 R21")),
        # "clk" is on CCLK
        IOStandard("LVCMOS25")
    ),

    ("spiflash2x", 0,
        Subsignal("cs_n", Pins("T19")),
        Subsignal("dq", Pins("P22 R22")),
        Subsignal("wp", Pins("P21")),
        Subsignal("hold", Pins("R21")),
        # "clk" is on CCLK
        IOStandard("LVCMOS25")
    ),

]

# Connectors ---------------------------------------------------------------------------------------

_connectors = [
    ("fmc0", {
        # LPC
        "LA33_N": "T15",
        "LA32_N": "AB17",
        "LA31_N": "Y14",
        "LA30_N": "U16",
        "LA29_N": "AA16",
        "LA28_N": "AB15",
        "LA27_N": "AB13",
        "LA26_N": "AA14",
        "LA25_N": "Y12",
        "LA24_N": "W16",
        "LA23_N": "AA11",
        "LA22_N": "AB12",
        "LA21_N": "W10",
        "LA20_N": "V15",
        "LA19_N": "AB10",
        "LA18_CC_N": "W12",
        "LA17_CC_N": "V14",
        "LA16_N": "F14",
        "LA15_N": "E14",
        "LA14_N": "B13",
        "LA13_N": "A14",
        "LA12_N": "D16",
        "LA11_N": "A20",
        "LA10_N": "C15",
        "LA09_N": "F20",
        "LA08_N": "A21",
        "LA07_N": "A19",
        "LA06_N": "B16",
        "LA05_N": "A16",
        "LA04_N": "B22",
        "LA03_N": "E18",
        "LA02_N": "E17",
        "LA01_CC_N": "D19",
        "LA00_CC_N": "B18",
        "LA33_P": "T14",
        "LA32_P": "AB16",
        "LA31_P": "W14",
        "LA30_P": "T16",
        "LA29_P": "Y16",
        "LA28_P": "AA15",
        "LA27_P": "AA13",
        "LA26_P": "Y13",
        "LA25_P": "Y11",
        "LA24_P": "W15",
        "LA23_P": "AA10",
        "LA22_P": "AB11",
        "LA21_P": "V10",
        "LA20_P": "U15",
        "LA19_P": "AA9",
        "LA18_CC_P": "W11",
        "LA17_CC_P": "V13",
        "LA16_P": "F13",
        "LA15_P": "E13",
        "LA14_P": "C13",
        "LA13_P": "A13",
        "LA12_P": "E16",
        "LA11_P": "B20",
        "LA10_P": "C14",
        "LA09_P": "F19",
        "LA08_P": "B21",
        "LA07_P": "A18",
        "LA06_P": "B15",
        "LA05_P": "A15",
        "LA04_P": "C22",
        "LA03_P": "F18",
        "LA02_P": "F16",
        "LA01_CC_P": "E19",
        "LA00_CC_P": "B17",
        # DIFF_HSTL_I_DCI_18
        "GBTCLK0_M2C_P": "F6",
        "GBTCLK0_M2C_N": "E6",
        "DP0_M2C_P": "B8",
        "DP0_M2C_N": "A8",
        "DP0_C2M_P": "B4",
        "DP0_C2M_N": "A4",
        # "HPC"
        # HA[23:0]
        "HA23_N": "P4",
        "HA22_N": "N5",
        "HA21_N": "N3",
        "HA20_N": "H5",
        "HA19_N": "P1",
        "HA18_CC_N": "K3",
        "HA17_CC_N": "G4",
        "HA16_N": "G2",
        "HA15_N": "J2",
        "HA14_N": "N2",
        "HA13_N": "A1",
        "HA12_N": "E3",
        "HA11_N": "D1",
        "HA10_N": "F1",
        "HA09_N": "M5",
        "HA08_N": "B2",
        "HA07_N": "M2",
        "HA06_N": "D2",
        "HA05_N": "J6",
        "HA04_N": "L4",
        "HA03_N": "J1",
        "HA02_N": "L1",
        "HA01_CC_N": "G3",
        "HA00_CC_N": "J4",
        "HA23_P": "P5",
        "HA22_P": "P6",
        "HA21_P": "N4",
        "HA20_P": "J5",
        "HA19_P": "R1",
        "HA18_CC_P": "L3",
        "HA17_CC_P": "H4",
        "HA16_P": "H2",
        "HA15_P": "K2",
        "HA14_P": "P2",
        "HA13_P": "B1",
        "HA12_P": "F3",
        "HA11_P": "E1",
        "HA10_P": "G1",
        "HA09_P": "M6",
        "HA08_P": "C2",
        "HA07_P": "M3",
        "HA06_P": "E2",
        "HA05_P": "K6",
        "HA04_P": "L5",
        "HA03_P": "K1",
        "HA02_P": "M1",
        "HA01_CC_P": "H3",
        "HA00_CC_P": "K4",
        # HB[21:0]
        "HB21_N": "AB8",
        "HB20_N": "AA6",
        "HB19_N": "AB1",
        "HB18_N": "AB6",
        "HB17_CC_N": "AA4",
        "HB16_N": "Y9",
        "HB15_N": "AB5",
        "HB14_N": "V2",
        "HB13_N": "Y1",
        "HB12_N": "AA3",
        "HB11_N": "Y2",
        "HB10_N": "AB2",
        "HB09_N": "Y7",
        "HB08_N": "V8",
        "HB07_N": "W5",
        "HB06_CC_N": "W4",
        "HB05_N": "V5",
        "HB04_N": "U1",
        "HB03_N": "R2",
        "HB02_N": "T6",
        "HB01_N": "T4",
        "HB00_CC_N": "U5",
        "HB21_P": "AA8",
        "HB20_P": "Y6",
        "HB19_P": "AA1",
        "HB18_P": "AB7",
        "HB17_CC_P": "Y4",
        "HB16_P": "W9",
        "HB15_P": "AA5",
        "HB14_P": "U2",
        "HB13_P": "W1",
        "HB12_P": "Y3",
        "HB11_P": "W2",
        "HB10_P": "AB3",
        "HB09_P": "Y8",
        "HB08_P": "V9",
        "HB07_P": "W6",
        "HB06_CC_P": "V4",
        "HB05_P": "U6",
        "HB04_P": "T1",
        "HB03_P": "R3",
        "HB02_P": "R6",
        "HB01_P": "R4",
        "HB00_CC_P": "T5",
        # DIFF_HSTL_I_DCI_18
        "GBTCLK1_M2C_P": "",
        "GBTCLK1_M2C_N": "",
        ## Mezzanine 2 Carrier
        "DP1_M2C_P": "D11",
        "DP1_M2C_N": "C11",
        "DP2_M2C_P": "B10",
        "DP2_M2C_N": "A10",
        "DP3_M2C_P": "D9",
        "DP3_M2C_N": "C9",
        # "DP4_M2C_P": "",          # Artix 7 in 484 package has only 4 GTP channels; see: https://github.com/sinara-hw/EEM_FMC_Carrier/discussions/2
        # "DP4_M2C_N": "",
        # "DP5_M2C_P": "",
        # "DP5_M2C_N": "",
        # "DP6_M2C_P": "",
        # "DP6_M2C_N": "",
        # "DP7_M2C_P": "",
        # "DP7_M2C_N": "",
        # "DP8_M2C_P": "",
        # "DP8_M2C_N": "",
        # "DP9_M2C_P": "",
        # "DP9_M2C_N": "",
        ## Carrier 2 Mezzanine
        "DP1_C2M_P": "D5",
        "DP1_C2M_N": "C5",
        "DP2_C2M_P": "B6",
        "DP2_C2M_N": "A6",
        "DP3_C2M_P": "D7",
        "DP3_C2M_N": "C7",
        # "DP4_C2M_P": "",
        # "DP4_C2M_N": "",
        # "DP5_C2M_P": "",
        # "DP5_C2M_N": "",
        # "DP6_C2M_P": "",
        # "DP6_C2M_N": "",
        # "DP7_C2M_P": "",
        # "DP7_C2M_N": "",
        # "DP8_C2M_P": "",
        # "DP8_C2M_N": "",
        # "DP9_C2M_P": "",
        # "DP9_C2M_N": "",
    }),
    ("eem0", {
        "d0_cc_n": "V19",
        "d0_cc_p": "V18",
        "d1_n": "R17",
        "d1_p": "P16",
        "d2_n": "T18",
        "d2_p": "R18",
        "d3_n": "W17",
        "d3_p": "V17",
        "d4_n": "R19",
        "d4_p": "P19",
        "d5_n": "R16",
        "d5_p": "P15",
        "d6_n": "U18",
        "d6_p": "U17",
        "d7_n": "AA21",
        "d7_p": "AA20",
    }),
    ("eem1", {
        "d0_cc_n": "V20",
        "d0_cc_p": "U20",
        "d1_n": "P17",
        "d1_p": "N17",
        "d2_n": "N14",
        "d2_p": "N13",
        "d3_n": "Y22",
        "d3_p": "Y21",
        "d4_n": "W22",
        "d4_p": "W21",
        "d5_n": "AB22",
        "d5_p": "AB21",
        "d6_n": "AB20",
        "d6_p": "AA19",
        "d7_n": "AB18",
        "d7_p": "AA18",
    }),
]

_extensions = [
    ("eem", i, IOStandard("LVDS_25")) + tuple([
        Subsignal("d{}{}_{}".format(j, "_cc" if j == 0 else "", p), Pins(
            "eem{}:d{}{}_{}".format(i, j, "_cc" if j == 0 else "", p)))
                for j in range(8) for p in "pn"])
    for i in range(2)
]

# Platform -----------------------------------------------------------------------------------------

class Platform(XilinxPlatform):
    userid = 0xffffffff

    def __init__(self):
        XilinxPlatform.__init__(
            self, "xc7a100t-fgg484-3", _ios, _connectors,
            toolchain="vivado")
        self.add_extension(_extensions)

        # https://support.xilinx.com/s/article/42036?language=en_US
        self.add_platform_command(
                "set_property INTERNAL_VREF 0.750 [get_iobanks 15]")

        self.add_platform_command(
            "set_property BITSTREAM.CONFIG.OVERTEMPPOWERDOWN Enable [current_design] \n \
            set_property BITSTREAM.GENERAL.COMPRESS True [current_design] \n \
            set_property BITSTREAM.CONFIG.CONFIGRATE 33 [current_design] \n\
            set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 2 [current_design] \n\
            set_property BITSTREAM.CONFIG.USR_ACCESS TIMESTAMP [current_design] \n\
            set_property CFGBVS VCCO [current_design] \n\
            set_property CONFIG_VOLTAGE 2.5 [current_design]"
        )

    def create_programmer(self):
        raise NotImplementedError
