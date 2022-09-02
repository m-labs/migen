#
# Based on board definition included in LiteX-Boards by 
#     Florent Kermarrec <florent@enjoy-digital.fr>
#
# Copyright (c) 2018-2019 Florent Kermarrec <florent@enjoy-digital.fr>
# Copyright (c) 2022-2022 Mikolaj Sowinski <msowinski@technosystem.com.pl>
# SPDX-License-Identifier: BSD-2-Clause

from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform


_io = [
    # Clk / Rst
   ("clk200", 0,
        Subsignal("p", Pins("AD12"), IOStandard("LVDS")),
        Subsignal("n", Pins("AD11"), IOStandard("LVDS"))
    ),
    ("cpu_reset_n", 0, Pins("R19"), IOStandard("LVCMOS33")),

    # Leds
    ("user_led", 0, Pins("T28"), IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("V19"), IOStandard("LVCMOS33")),
    ("user_led", 2, Pins("U30"), IOStandard("LVCMOS33")),
    ("user_led", 3, Pins("U29"), IOStandard("LVCMOS33")),
    ("user_led", 4, Pins("V20"), IOStandard("LVCMOS33")),
    ("user_led", 5, Pins("V26"), IOStandard("LVCMOS33")),
    ("user_led", 6, Pins("W24"), IOStandard("LVCMOS33")),
    ("user_led", 7, Pins("W23"), IOStandard("LVCMOS33")),

    # Buttons
    ("user_btn_c", 0, Pins("E18"), IOStandard("LVCMOS33")),
    ("user_btn_d", 0, Pins("M19"), IOStandard("LVCMOS33")),
    ("user_btn_l", 0, Pins("M20"), IOStandard("LVCMOS33")),
    ("user_btn_r", 0, Pins("C19"), IOStandard("LVCMOS33")),
    ("user_btn_u", 0, Pins("B19"), IOStandard("LVCMOS33")),

    # Switches
    ("user_sw", 0, Pins("G19"), IOStandard("LVCMOS12")),
    ("user_sw", 1, Pins("G25"), IOStandard("LVCMOS12")),
    ("user_sw", 2, Pins("H24"), IOStandard("LVCMOS12")),
    ("user_sw", 3, Pins("K19"), IOStandard("LVCMOS12")),
    ("user_sw", 4, Pins("N19"), IOStandard("LVCMOS12")),
    ("user_sw", 5, Pins("P19"), IOStandard("LVCMOS12")),
    ("user_sw", 6, Pins("P26"), IOStandard("LVCMOS33")),
    ("user_sw", 7, Pins("P27"), IOStandard("LVCMOS33")),

    # Serial
    ("serial", 0,
        Subsignal("tx", Pins("Y23")),
        Subsignal("rx", Pins("Y20")),
        IOStandard("LVCMOS33")
    ),

    # SPI Flash
    ("spiflash", 0,  # clock needs to be accessed through STARTUPE2
        Subsignal("cs_n", Pins("U19")),
        # Subsignal("dq", Pins("P24", "R25", "R20", "R21")),
        Subsignal("mosi", Pins("P24")),
        Subsignal("miso", Pins("R25")),
        IOStandard("LVCMOS33")
    ),

    # USB FIFO
    ("usb_fifo", 0, # Can be used when FT2232H's Channel A configured to ASYNC FIFO 245 mode
        Subsignal("data",  Pins("AD27 W27 W28 W29 Y29 Y28 AA28 AA26")),
        Subsignal("rxf_n", Pins("AB29")),
        Subsignal("txe_n", Pins("AA25")),
        Subsignal("rd_n",  Pins("AB25")),
        Subsignal("wr_n",  Pins("AC27")),
        Subsignal("siwua", Pins("AB28")),
        Subsignal("oe_n",  Pins("AC30")),
        Misc("SLEW=FAST"),
        Drive(8),
        IOStandard("LVCMOS33"),
    ),

    # SDCard
    ("spisdcard", 0,
        Subsignal("rst",  Pins("AE24")),
        Subsignal("clk",  Pins("R28")),
        Subsignal("cs_n", Pins("T30"), Misc("PULLUP True")),
        Subsignal("mosi", Pins("R29"), Misc("PULLUP True")),
        Subsignal("miso", Pins("R26"), Misc("PULLUP True")),
        Misc("SLEW=FAST"),
        IOStandard("LVCMOS33")
    ),
    ("sdcard", 0,
        Subsignal("rst",  Pins("AE24"),            Misc("PULLUP True")),
        Subsignal("data", Pins("R26 R30 P29 T30"), Misc("PULLUP True")),
        Subsignal("cmd",  Pins("R29"),             Misc("PULLUP True")),
        Subsignal("clk",  Pins("R28")),
        Subsignal("cd",   Pins("P28")),
        Misc("SLEW=FAST"),
        IOStandard("LVCMOS33")
    ),


    # DDR3 SDRAM
    ("ddram", 0,
        Subsignal("a", Pins(
            "AC12 AE8 AD8 AC10 AD9  AA13 AA10 AA11",
            "Y10  Y11 AB8  AA8 AB12 AA12 AH9"),
            IOStandard("SSTL15")),
        Subsignal("ba",    Pins("AE9 AB10 AC11"), IOStandard("SSTL15")),
        Subsignal("ras_n", Pins("AE11"), IOStandard("SSTL15")),
        Subsignal("cas_n", Pins("AF11"), IOStandard("SSTL15")),
        Subsignal("we_n",  Pins("AG13"), IOStandard("SSTL15")),
        Subsignal("cs_n",  Pins("AH12"), IOStandard("SSTL15")),
        Subsignal("dm", Pins("AD4 AF3 AH4 AF8"),
            IOStandard("SSTL15")),
        Subsignal("dq", Pins(
            "AD3 AC2 AC1 AC5 AC4 AD6 AE6 AC7",
            "AF2 AE1 AF1 AE4 AE3 AE5 AF5 AF6",
            "AJ4 AH6 AH5 AH2 AJ2 AJ1 AK1 AJ3",
            "AF7 AG7 AJ6 AK6 AJ8 AK8 AK5 AK4"),
            IOStandard("SSTL15_T_DCI")),
        Subsignal("dqs_p", Pins("AD2 AG4 AG2 AH7"),
            IOStandard("DIFF_SSTL15")),
        Subsignal("dqs_n", Pins("AD1 AG3 AH1 AJ7"),
            IOStandard("DIFF_SSTL15")),
        Subsignal("clk_p", Pins("AB9"), IOStandard("DIFF_SSTL15")),
        Subsignal("clk_n", Pins("AC9"), IOStandard("DIFF_SSTL15")),
        Subsignal("cke",   Pins("AJ9"), IOStandard("SSTL15")),
        Subsignal("odt",   Pins("AK9"), IOStandard("SSTL15")),
        Subsignal("reset_n", Pins("AG5"), IOStandard("LVCMOS15")),
        Misc("SLEW=FAST"),
        Misc("VCCAUX_IO=HIGH")
    ),

    # RGMII Ethernet
    ("eth_clocks", 0,
        Subsignal("tx", Pins("AE10")),
        Subsignal("rx", Pins("AG10")),
        IOStandard("LVCMOS15")
    ),
    ("eth", 0,
        Subsignal("rst_n",   Pins("AH24"), IOStandard("LVCMOS33")),
        Subsignal("int_n",   Pins("AK16"), IOStandard("LVCMOS18")),
        Subsignal("mdio",    Pins("AG12"), IOStandard("LVCMOS15")),
        Subsignal("mdc",     Pins("AF12"), IOStandard("LVCMOS15")),
        Subsignal("rx_ctl",  Pins("AH11"), IOStandard("LVCMOS15")),
        Subsignal("rx_data", Pins("AJ14 AH14 AK13 AJ13"), IOStandard("LVCMOS15")),
        Subsignal("tx_ctl",  Pins(" AK14"), IOStandard("LVCMOS15")),
        Subsignal("tx_data", Pins("AJ12 AK11 AJ11 AK10"), IOStandard("LVCMOS15")),
    ),
]


_connectors = [
    ("fmc1", {
        "DP0_C2M_P":     "Y2",
        "DP0_C2M_N":     "Y1",
        "DP0_M2C_P":     "AA4",
        "DP0_M2C_N":     "AA3",
        "GBTCLK0_M2C_P": "L8",
        "GBTCLK0_M2C_N": "L7",

        "HA00_CC_N": "K29",
        "HA00_CC_P": "K28",
        "HA01_CC_N": "L28",
        "HA01_CC_P": "M28",
        "HA02_N": "P22",
        "HA02_P": "P21",
        "HA03_N": "N26",
        "HA03_P": "N25",
        "HA04_N": "M25",
        "HA04_P": "M24",
        "HA05_N": "H29",
        "HA05_P": "J29",
        "HA06_N": "N30",
        "HA06_P": "N29",
        "HA07_N": "M30",
        "HA07_P": "M29",
        "HA08_N": "J28",
        "HA08_P": "J27",
        "HA09_N": "K30",
        "HA09_P": "L30",
        "HA10_N": "N22",
        "HA10_P": "N21",
        "HA11_N": "N24",
        "HA11_P": "P23",
        "HA12_N": "L27",
        "HA12_P": "L26",
        "HA13_N": "J26",
        "HA13_P": "K26",
        "HA14_N": "M27",
        "HA14_P": "N27",
        "HA15_N": "J22",
        "HA15_P": "J21",
        "HA16_N": "M23",
        "HA16_P": "M22",
        "HA17_CC_N": "B25",
        "HA17_CC_P": "C25",
        "HA18_N": "D19",
        "HA18_P": "E19",
        "HA19_N": "F30",
        "HA19_P": "G29",
        "HA20_N": "F27",
        "HA20_P": "G27",
        "HA21_N": "F28",
        "HA21_P": "G28",
        "HA22_N": "C21",
        "HA22_P": "D21",
        "HA23_N": "F18",
        "HA23_P": "G18",

        "HB00_CC_N": "F13",
        "HB00_CC_P": "G13",
        "HB01_N": "G15",
        "HB01_P": "H15",
        "HB02_N": "K15",
        "HB02_P": "L15",
        "HB03_N": "G14",
        "HB03_P": "H14",
        "HB04_N": "H16",
        "HB04_P": "J16",
        "HB05_N": "K16",
        "HB05_P": "L16",
        "HB06_CC_N": "E13",
        "HB06_CC_P": "F12",
        "HB07_N": "A13",
        "HB07_P": "B13",
        "HB08_N": "J14",
        "HB08_P": "K14",
        "HB09_N": "B15",
        "HB09_P": "C15",
        "HB10_N": "J12",
        "HB10_P": "J11",
        "HB11_N": "C11",
        "HB11_P": "D11",
        "HB12_N": "A12",
        "HB12_P": "A11",
        "HB13_N": "B12",
        "HB13_P": "C12",
        "HB14_N": "H12",
        "HB14_P": "H11",
        "HB15_N": "L13",
        "HB15_P": "L12",
        "HB16_N": "J13",
        "HB16_P": "K13",
        "HB17_CC_N": "D13",
        "HB17_CC_P": "D12",
        "HB18_N": "E15",
        "HB18_P": "E14",
        "HB19_N": "E11",
        "HB19_P": "F11",
        "HB20_N": "A15",
        "HB20_P": "B14",
        "HB21_N": "C14",
        "HB21_P": "D14",

        "LA00_CC_N": "C27",
        "LA00_CC_P": "D27",
        "LA01_CC_N": "C26",
        "LA01_CC_P": "D26",
        "LA02_N": "G30",
        "LA02_P": "H30",
        "LA03_N": "E30",
        "LA03_P": "E29",
        "LA04_N": "H27",
        "LA04_P": "H26",
        "LA05_N": "A30",
        "LA05_P": "B30",
        "LA06_N": "C30",
        "LA06_P": "D29",
        "LA07_N": "E25",
        "LA07_P": "F25",
        "LA08_N": "B29",
        "LA08_P": "C29",
        "LA09_N": "A28",
        "LA09_P": "B28",
        "LA10_N": "A27",
        "LA10_P": "B27",
        "LA11_N": "A26",
        "LA11_P": "A25",
        "LA12_N": "E26",
        "LA12_P": "F26",
        "LA13_N": "D24",
        "LA13_P": "E24",
        "LA14_N": "B24",
        "LA14_P": "C24",
        "LA15_N": "A23",
        "LA15_P": "B23",
        "LA16_N": "D23",
        "LA16_P": "E23",
        "LA17_CC_N": "E21",
        "LA17_CC_P": "F21",
        "LA18_CC_N": "D18",
        "LA18_CC_P": "D17",
        "LA19_N": "H22",
        "LA19_P": "H21",
        "LA20_N": "F22",
        "LA20_P": "G22",
        "LA21_N": "L18",
        "LA21_P": "L17",
        "LA22_N": "H17",
        "LA22_P": "J17",
        "LA23_N": "F17",
        "LA23_P": "G17",
        "LA24_N": "G20",
        "LA24_P": "H20",
        "LA25_N": "C22",
        "LA25_P": "D22",
        "LA26_N": "A22",
        "LA26_P": "B22",
        "LA27_N": "A21",
        "LA27_P": "A20",
        "LA28_N": "H19",
        "LA28_P": "J19",
        "LA29_N": "A18",
        "LA29_P": "B18",
        "LA30_N": "A17",
        "LA30_P": "A16",
        "LA31_N": "B17",
        "LA31_P": "C17",
        "LA32_N": "J18",
        "LA32_P": "K18",
        "LA33_N": "C16",
        "LA33_P": "D16",
        }
    ),
]


class Platform(XilinxPlatform):
    default_clk_name = "clk200"
    default_clk_period = 5.0

    def __init__(self):
        XilinxPlatform.__init__(self, "xc7k325t-ffg900-2", _io, _connectors,
            toolchain="vivado")
        self.toolchain.bitstream_commands.extend([
            "set_property BITSTREAM.CONFIG.OVERTEMPPOWERDOWN Enable [current_design]",
            "set_property BITSTREAM.GENERAL.COMPRESS TRUE [current_design]",
            "set_property CONFIG_MODE SPIx1 [current_design]",
            "set_property CFGBVS VCCO [current_design]",
            "set_property CONFIG_VOLTAGE 3.3 [current_design]",
            "set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 1 [current_design]"
        ])

    def do_finalize(self, fragment):
        XilinxPlatform.do_finalize(self, fragment)
        try:
            self.add_period_constraint(self.lookup_request("clk200").p, 5.0)
        except ValueError:
            pass
        try:
            self.add_period_constraint(self.lookup_request("eth_clocks").rx, 8.0)
        except ValueError:
            pass
        try:
            self.add_period_constraint(self.lookup_request("eth_clocks").tx, 8.0)
        except ValueError:
            pass
