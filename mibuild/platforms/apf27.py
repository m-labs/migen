from mibuild.generic_platform import *
from mibuild.xilinx_ise import XilinxISEPlatform, CRG_SE

_io = [
    ("FPGA_RESET", 0, Pins("T9"),  IOStandard("LVCMOS18"), Drive(8)),
    ("FPGA_INITB", 0, Pins("T12"), IOStandard("LVCMOS18"), Drive("8")),
    ("CS4_DTACK", 0, Pins("R3"), IOStandard("LVCMOS18"), Drive("8")),
    ("CS5N", 0, Pins("P10"), IOStandard("LVCMOS18")),
    ("DATA0", 0, Pins("T5"), IOStandard("LVCMOS18"), Drive("8")),
    ("DATA1", 0, Pins("T6"), IOStandard("LVCMOS18"), Drive("8")),
    ("DATA2", 0, Pins("P7"), IOStandard("LVCMOS18"), Drive("8")),
    ("DATA3", 0, Pins("N8"), IOStandard("LVCMOS18"), Drive("8")),
    ("DATA4", 0, Pins("P12"), IOStandard("LVCMOS18"), Drive("8")),
    ("DATA5", 0, Pins("T13"), IOStandard("LVCMOS18"), Drive("8")),
    ("DATA6", 0, Pins("R13"), IOStandard("LVCMOS18"), Drive("8")),
    ("DATA7", 0, Pins("T14"), IOStandard("LVCMOS18"), Drive("8")),
    ("CLK0", 0, Pins("N9"), IOStandard("LVCMOS18")),
    ("EB0N", 0, Pins("P9"), IOStandard("LVCMOS18")),
    ("OEN", 0, Pins("R9"), IOStandard("LVCMOS18")),
    ("ADDR1", 0, Pins("N5"), IOStandard("LVCMOS18")),
    ("ADDR2", 0, Pins("L7"), IOStandard("LVCMOS18")),
    ("ADDR3", 0, Pins("M7"), IOStandard("LVCMOS18")),
    ("ADDR4", 0, Pins("M8"), IOStandard("LVCMOS18")),
    ("ADDR5", 0, Pins("L8"), IOStandard("LVCMOS18")),
    ("ADDR6", 0, Pins("L9"), IOStandard("LVCMOS18")),
    ("ADDR7", 0, Pins("L10"), IOStandard("LVCMOS18")),
    ("ADDR8", 0, Pins("M11"), IOStandard("LVCMOS18")),
    ("DATA8", 0, Pins("P5"), IOStandard("LVCMOS18"), Drive("8")),
    ("DATA9", 0, Pins("N6"), IOStandard("LVCMOS18"), Drive("8")),
    ("DATA10", 0, Pins("T3"), IOStandard("LVCMOS18"), Drive("8")),
    ("DATA11", 0, Pins("T11"), IOStandard("LVCMOS18"), Drive("8")),
    ("DATA12", 0, Pins("T4"), IOStandard("LVCMOS18"), Drive("8")),
    ("DATA13", 0, Pins("R5"), IOStandard("LVCMOS18"), Drive("8")),
    ("DATA14", 0, Pins("M10"), IOStandard("LVCMOS18"), Drive("8")),
    ("DATA15", 0, Pins("T10"), IOStandard("LVCMOS18"), Drive("8")),
    ("ADDR9", 0, Pins("P11"), IOStandard("LVCMOS18")),
    ("ADDR10", 0, Pins("N11"), IOStandard("LVCMOS18")),
    ("ADDR11", 0, Pins("N12"), IOStandard("LVCMOS18")),
    ("ADDR12", 0, Pins("P13"), IOStandard("LVCMOS18")),
    ("IO_L01P_0", 0, Pins("D13"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L01N_0", 0, Pins("C13"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L02P_0", 0, Pins("B15"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L02N_0", 0, Pins("B14"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L03P_0", 0, Pins("C12"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L03N_0", 0, Pins("D11"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L04P_0", 0, Pins("A14"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L04N_0", 0, Pins("A13"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L09P_0", 0, Pins("C10"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L09N_0", 0, Pins("D9"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L10P_0", 0, Pins("C9"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L10N_0", 0, Pins("A9"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L11P_0", 0, Pins("C8"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L11N_0", 0, Pins("D8"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L12P_0", 0, Pins("A8"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L12N_0", 0, Pins("B8"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L07P_0", 0, Pins("C11"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L07N_0", 0, Pins("A11"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L08P_0", 0, Pins("B10"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L08N_0", 0, Pins("A10"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L15P_0", 0, Pins("A6"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L15N_0", 0, Pins("B6"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L16P_0", 0, Pins("D7"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L16N_0", 0, Pins("C6"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L17P_0", 0, Pins("A5"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L17N_0", 0, Pins("C5"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L18P_0", 0, Pins("A4"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L18N_0", 0, Pins("B4"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L19P_0", 0, Pins("A3"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L19N_0", 0, Pins("B3"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L01P_3", 0, Pins("C2"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L01N_3", 0, Pins("C1"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L02P_3", 0, Pins("D4"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L02N_3", 0, Pins("D3"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L03P_3", 0, Pins("D1"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L03N_3", 0, Pins("E1"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L08P_3", 0, Pins("F1"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L08N_3", 0, Pins("G1"), IOStandard("LVCMOS33"), Drive("12")),
    ("IP_L04N_3", 0, Pins("F4"), IOStandard("LVCMOS33"), Drive("12")),
    ("IP_L25N_3", 0, Pins("L6"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L11P_3", 0, Pins("G2"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L11N_3", 0, Pins("H1"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L12P_3", 0, Pins("H3"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L12N_3", 0, Pins("J3"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L14P_3", 0, Pins("J2"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L14N_3", 0, Pins("J1"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L15P_3", 0, Pins("K3"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L15N_3", 0, Pins("K1"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L20P_3", 0, Pins("M1"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L20N_3", 0, Pins("N1"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L22P_3", 0, Pins("N2"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L22N_3", 0, Pins("P1"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L23P_3", 0, Pins("R1"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L23N_3", 0, Pins("P2"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L24P_3", 0, Pins("N3"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L24N_3", 0, Pins("M4"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L20P_1", 0, Pins("E14"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L20N_1", 0, Pins("F13"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L22P_1", 0, Pins("D16"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L22N_1", 0, Pins("D15"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L23P_1", 0, Pins("E13"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L23N_1", 0, Pins("D14"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L24P_1", 0, Pins("C16"), IOStandard("LVCMOS33"), Drive("12")),
    ("IO_L24N_1", 0, Pins("C15"), IOStandard("LVCMOS33"), Drive("12"))
    ]


class Platform(XilinxISEPlatform):
    xst_opt = """-ifmt MIXED
-opt_mode SPEED
-register_balancing yes"""

    def __init__(self):
        XilinxISEPlatform.__init__(self, "xc3s200a-ft256-4", _io,
            lambda p: CRG_SE(p, "CLK0", None))

    def do_finalize(self, fragment):
        try:
            self.add_platform_command("""
NET "{CLK0}" TNM_NET = "GRPCLK0";
TIMESPEC "TSCLK0" = PERIOD "GRPCLK0" 10 ns HIGH 50%;
""", CLK0=self.lookup_request("CLK0"))
        except ConstraintError:
            pass
