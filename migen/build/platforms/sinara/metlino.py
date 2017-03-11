from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform


_io = [
    ("clk50", 0, Pins("N24"), IOStandard("LVCMOS33")),

    ("serial", 0,
        Subsignal("tx", Pins("K20")),
        Subsignal("rx", Pins("K22")),
        IOStandard("LVCMOS33")
    ),

    ("ddram", 0,
        Subsignal("a", Pins(
            "AE17 AH17 AE18 AJ15 AG16 AL17 AK18 AG17 AF18 AH19 AF15 AD19 AJ14 AG19 AH16"),
            IOStandard("SSTL15")),
        Subsignal("ba", Pins("AF17 AL15 AK15"), IOStandard("SSTL15")),
        Subsignal("ras_n", Pins("AF14"), IOStandard("SSTL15")),
        Subsignal("cas_n", Pins("AG14"), IOStandard("SSTL15")),
        Subsignal("we_n", Pins("AD16"), IOStandard("SSTL15")),
        Subsignal("cs_n", Pins("AL19"), IOStandard("SSTL15")),
        Subsignal("dm", Pins("AD21 AE25 AJ21 AM21 AH26 AN26 AJ29 AL32"),
            IOStandard("SSTL15")),
        Subsignal("dq", Pins(
            "AE23 AG20 AF22 AF20 AE22 AD20 AG22 AE20 AJ24 AG24 AJ23 AF23 AH23 AF24 AH22 AG25 AL22 AL25 AM20 AK23 AK22 AL24 AL20 AL23 AM24 AN23 AN24 AP23 AP25 AN22 AP24 AM22 AH28 AK26 AK28 AM27 AJ28 AH27 AK27 AM26 AL30 AP29 AM30 AN28 AL29 AP28 AM29 AN27 AH31 AH32 AJ34 AK31 AJ31 AJ30 AH34 AK32 AN33 AP33 AM34 AP31 AM32 AN31 AL34 AN32"),
            IOStandard("SSTL15_T_DCI")),
        Subsignal("dqs_p", Pins("AG21 AH24 AJ20 AP20 AL27 AN29 AH33 AN34"),
            IOStandard("DIFF_SSTL15")),
        Subsignal("dqs_n", Pins("AH21 AJ25 AK20 AP21 AL28 AP30 AJ33 AP34"),
            IOStandard("DIFF_SSTL15")),
        Subsignal("clk_p", Pins("AE16"), IOStandard("DIFF_SSTL15")),
        Subsignal("clk_n", Pins("AE15"), IOStandard("DIFF_SSTL15")),
        Subsignal("cke", Pins("AD15"), IOStandard("SSTL15")),
        Subsignal("odt", Pins("AJ18"), IOStandard("SSTL15")),
        Subsignal("reset_n", Pins("AL18"), IOStandard("LVCMOS15"))),
]


class Platform(XilinxPlatform):
    default_clk_name = "clk50"
    default_clk_period = 20.0

    def __init__(self):
        XilinxPlatform.__init__(self, "xcku040-ffva1156-1-c", _io, toolchain="vivado")
