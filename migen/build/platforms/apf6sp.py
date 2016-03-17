""" Platform definitions for apf6sp board by Armadeus System """
from migen import *
from migen.fhdl import *
from migen.build.generic_platform import *
from migen.build.altera import AlteraPlatform

_io = [("pcie_x1", 0,
        Subsignal("clk_p", Pins("V4"), IOStandard("1.5-V PCML")),
        Subsignal("clk_n", Pins("U4"), IOStandard("1.5-V PCML")),
        Subsignal("rx_p", Pins("AA2"), IOStandard("1.5-V PCML")),
        Subsignal("rx_n", Pins("AA1"), IOStandard("1.5-V PCML")),
        Subsignal("tx_p", Pins("Y4"), IOStandard("1.5-V PCML")),
        Subsignal("tx_n", Pins("Y3"), IOStandard("1.5-V PCML")),
        Subsignal("perst", Pins("R17"), IOStandard("2.5 V")),
        Subsignal("npor", Pins("R16"), IOStandard("2.5 V"))),

       ("pcie_clk", 0,
        Subsignal("p", Pins("V4"), IOStandard("1.5-V PCML")),
        Subsignal("n", Pins("U4"), IOStandard("1.5-V PCML"))),

       ("ddram", 0,
        Subsignal("a", Pins("C11 B11 A8 A7 " +
                            "D11 E11 F8 E7 " +
                            "D9 D8 B6 B5 C8 " +
                            "B8 H6"), IOStandard("SSTL-135")),

        Subsignal("ba", Pins("C6 C10 C9"), IOStandard("SSTL-135")),

        Subsignal("ras_n", Pins("A9"), IOStandard("SSTL-135")),
        Subsignal("cas_n", Pins("A10"), IOStandard("SSTL-135")),
        Subsignal("cs_n", Pins("H8"), IOStandard("SSTL-135")),
        Subsignal("we_n", Pins("E6"), IOStandard("SSTL-135")),

        Subsignal("dm", Pins("A15 C19 C21 F12 " +
                             "E12 B12 B13 C13 " +
                             "D13 C14 A14 E14 " +
                             "F15 B18 A17 C15 " +
                             "C16 B16 C18 D17 " +
                             "E16 A20 A22 E17 " +
                             "D18 B20 C20"), IOStandard("SSTL-135")),

        Subsignal("dqs_n",
                  Pins("G8 H12 G14"),
                  IOStandard("SSTL-135")),

        Subsignal("dqs",
                  Pins("H9 G12 G15"),
                  IOStandard("SSTL-135")),

        Subsignal("ck", Pins("J9"), IOStandard("SSTL-135")),
        Subsignal("ck_n", Pins("J8"), IOStandard("SSTL-135")),
        Subsignal("cke", Pins("B15"), IOStandard("SSTL-135")),
        Subsignal("odt", Pins("A13"), IOStandard("SSTL-135")),

        Subsignal("reset_n", Pins("B22"), IOStandard("SSTL-135")),
        Subsignal("oct_rzqin", Pins("A12"), IOStandard("SSTL-135")))]

_connector = [
    ("HIROSE",
     {"CLKIN0": "T10",
      "CLKIN_1N": "R9",
      "CLKIN_1P": "P9",
      "CLKIN_2N": "R15",
      "CLKIN_2P": "T15",
      "CLKOUT0": "R10",
      "CLKOUT_1N": "G17",
      "CLKOUT_1P": "G18",
      "CLKOUT_2N": "AB22",
      "CLKOUT_2P": "AA22",
      "D0": "M10",
      "D1": "K15",
      "D2": "L9",
      "D3": "L15",
      "LVDS_RX_N0": "AA9",
      "LVDS_RX_P0": "Y9",
      "LVDS_RX_N1": "U10",
      "LVDS_RX_P1": "U11",
      "LVDS_RX_N2": "U8",
      "LVDS_RX_P2": "V9",
      "LVDS_RX_N3": "U12",
      "LVDS_RX_P3": "T12",
      "LVDS_RX_N4": "W13",
      "LVDS_RX_P4": "V13",
      "LVDS_RX_N5": "W12",
      "LVDS_RX_P5": "Y12",
      "LVDS_RX_N6": "Y14",
      "LVDS_RX_P6": "W14",
      "LVDS_RX_N7": "U16",
      "LVDS_RX_P7": "U17",
      "LVDS_RX_N8": "Y16",
      "LVDS_RX_P8": "Y17",
      "LVDS_RX_N9": "W16",
      "LVDS_RX_P9": "W17",
      "LVDS_RX_N10": "V18",
      "LVDS_RX_P10": "W18",
      "LVDS_RX_N11": "V19",
      "LVDS_RX_P11": "V20",
      "LVDS_RX_N12": "T18",
      "LVDS_RX_P12": "T17",
      "LVDS_RX_N13": "J18",
      "LVDS_RX_P13": "J17",
      "LVDS_RX_N14": "K19",
      "LVDS_RX_P14": "L18",
      "LVDS_RX_N15": "L20",
      "LVDS_RX_P15": "L19",
      "LVDS_RX_N16": "P19",
      "LVDS_RX_P16": "R19",
      "LVDS_TX_N0": "W11",
      "LVDS_TX_P0": "Y11",
      "LVDS_TX_N1": "R12",
      "LVDS_TX_P1": "T13",
      "LVDS_TX_N2": "AA13",
      "LVDS_TX_P2": "AB13",
      "LVDS_TX_N3": "AB10",
      "LVDS_TX_P3": "AB11",
      "LVDS_TX_N4": "Y10",
      "LVDS_TX_P4": "AA10",
      "LVDS_TX_N5": "AA15",
      "LVDS_TX_P5": "Y15",
      "LVDS_TX_N6": "AB15",
      "LVDS_TX_P6": "AB16",
      "LVDS_TX_N7": "R11",
      "LVDS_TX_P7": "P12",
      "LVDS_TX_N8": "AA17",
      "LVDS_TX_P8": "AB17",
      "LVDS_TX_N9": "AB18",
      "LVDS_TX_P9": "AA18",
      "LVDS_TX_N10": "AA19",
      "LVDS_TX_P10": "Y19",
      "LVDS_TX_N11": "R21",
      "LVDS_TX_P11": "R20",
      "LVDS_TX_N12": "AB20",
      "LVDS_TX_P12": "AB21",
      "LVDS_TX_N13": "AA20",
      "LVDS_TX_P13": "Y20",
      "LVDS_TX_N14": "U21",
      "LVDS_TX_P14": "U22",
      "LVDS_TX_N15": "R22",
      "LVDS_TX_P15": "T22",
      "LVDS_TX_N16": "G21",
      "LVDS_TX_P16": "G22",
      "XCVR_RX_N0": "W1",
      "XCVR_RX_P0": "W2",
      "XCVR_RX_N1": "R1",
      "XCVR_RX_P1": "R2",
      "XCVR_RX_N2": "L1",
      "XCVR_RX_P2": "L2",
      "XCVR_TX_N0": "U1",
      "XCVR_TX_P0": "U2",
      "XCVR_TX_N1": "N1",
      "XCVR_TX_P1": "N2",
      "XCVR_TX_N2": "J1",
      "XCVR_TX_P2": "J2",
     }
    )]

class Platform(AlteraPlatform):
    """ Apf6sp platform """
    default_clk_name = "pcie_clk"
    default_clk_period = 8

    def __init__(self, toolchain="quartus"):
        AlteraPlatform.__init__(self, "5CGXFC4C7U19C8", _io, _connector)


class PciePllClockedModule(Module):
    """ This function add the pcie PLL as main clock for modules.
    See http://www.armadeus.com/wiki/index.php?title=IMX6-CycloneV_interface_description#Clocking_without_PCIe
    for the explainations
    """

    def __init__(self, platform):
        cd_sys = ClockDomain(name="cd_sys", reset_less=True)
        self.clock_domains += cd_sys

        pcie_clk = platform.request("pcie_clk")
        pci_clk_sig = Signal()

        self.specials += Instance("ALT_INBUF_DIFF", name="ibuf_diff",
                                  i_i=pcie_clk.p,
                                  i_ibar=pcie_clk.n,
                                  o_o=pci_clk_sig)
        self.specials += Instance("altera_pll",
                        i_rst=0,
                        o_outclk=cd_sys.clk,
                        i_refclk=pci_clk_sig,

                        p_fractional_vco_multiplier="false",
                        p_reference_clock_frequency="125.0 MHz",
                        p_operation_mode="direct",
                        p_number_of_clocks=Instance.PreformattedParam("1"),
                        p_output_clock_frequency0="62.500000 MHz",
                        p_phase_shift0="0 ps",
                        p_duty_cycle0=Instance.PreformattedParam("50"),
                        p_output_clock_frequency1="0 MHz",
                        p_phase_shift1="0 ps",
                        p_duty_cycle1=Instance.PreformattedParam("50"),
                        p_output_clock_frequency2="0 MHz",
                        p_phase_shift2="0 ps",
                        p_duty_cycle2=Instance.PreformattedParam("50"),
                        p_output_clock_frequency3="0 MHz",
                        p_phase_shift3="0 ps",
                        p_duty_cycle3=Instance.PreformattedParam("50"),
                        p_output_clock_frequency4="0 MHz",
                        p_phase_shift4="0 ps",
                        p_duty_cycle4=Instance.PreformattedParam("50"),
                        p_output_clock_frequency5="0 MHz",
                        p_phase_shift5="0 ps",
                        p_duty_cycle5=Instance.PreformattedParam("50"),
                        p_output_clock_frequency6="0 MHz",
                        p_phase_shift6="0 ps",
                        p_duty_cycle6=Instance.PreformattedParam("50"),
                        p_output_clock_frequency7="0 MHz",
                        p_phase_shift7="0 ps",
                        p_duty_cycle7=Instance.PreformattedParam("50"),
                        p_output_clock_frequency8="0 MHz",
                        p_phase_shift8="0 ps",
                        p_duty_cycle8=Instance.PreformattedParam("50"),
                        p_output_clock_frequency9="0 MHz",
                        p_phase_shift9="0 ps",
                        p_duty_cycle9=Instance.PreformattedParam("50"),
                        p_output_clock_frequency10="0 MHz",
                        p_phase_shift10="0 ps",
                        p_duty_cycle10=Instance.PreformattedParam("50"),
                        p_output_clock_frequency11="0 MHz",
                        p_phase_shift11="0 ps",
                        p_duty_cycle11=Instance.PreformattedParam("50"),
                        p_output_clock_frequency12="0 MHz",
                        p_phase_shift12="0 ps",
                        p_duty_cycle12=Instance.PreformattedParam("50"),
                        p_output_clock_frequency13="0 MHz",
                        p_phase_shift13="0 ps",
                        p_duty_cycle13=Instance.PreformattedParam("50"),
                        p_output_clock_frequency14="0 MHz",
                        p_phase_shift14="0 ps",
                        p_duty_cycle14=Instance.PreformattedParam("50"),
                        p_output_clock_frequency15="0 MHz",
                        p_phase_shift15="0 ps",
                        p_duty_cycle15=Instance.PreformattedParam("50"),
                        p_output_clock_frequency16="0 MHz",
                        p_phase_shift16="0 ps",
                        p_duty_cycle16=Instance.PreformattedParam("50"),
                        p_output_clock_frequency17="0 MHz",
                        p_phase_shift17="0 ps",
                        p_pll_subtype="General",
                        p_pll_type="General",
                        p_duty_cycle17=Instance.PreformattedParam("50"))
