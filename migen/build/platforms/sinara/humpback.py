from migen.build.generic_platform import *
from migen.build.lattice import LatticePlatform


_io = [
       ("clk25", 0, Pins("K9"), IOStandard("LVCMOS33")),

       ("user_led", 0, Pins("H3"), IOStandard("LVCMOS33")),

       ("serial", 0,
        Subsignal("rx", Pins("M13")),
        Subsignal("tx", Pins("T11"), Misc("PULLUP")),
        Subsignal("cts", Pins("T10"), Misc("PULLUP")),
        Subsignal("rts", Pins("M15"), Misc("PULLUP")),
        IOStandard("LVCMOS33"),
        ),

       ("serial", 1,
        Subsignal("rx", Pins("M11")),
        Subsignal("tx", Pins("T13"), Misc("PULLUP")),
        Subsignal("cts", Pins("B16"), Misc("PULLUP")),
        Subsignal("rts", Pins("A6"), Misc("PULLUP")),
        IOStandard("LVCMOS33"),
        ),

       ("spi", 0,
        Subsignal("cs_n", Pins("R2")),
        Subsignal("miso", Pins("T2")),
        Subsignal("mosi", Pins("N5")),
        Subsignal("clk", Pins("C8")),
        IOStandard("LVCMOS33"),
        ),

       ("i2c", 0,
        Subsignal("sda", Pins("T16"), Misc("PULLUP")),
        Subsignal("scl", Pins("M12"), Misc("PULLUP")),
        IOStandard("LVCMOS33"),
        ),
]


_io += [("sw", i, Pins(p), IOStandard("LVCMOS33"))
        for i, p in enumerate(
            "L16 K16 L11 T14 P7 N7 T8 P6 N6 T6 R6 P5".split())]


_connectors = [
    ("eem0", {
        "d0_cc_n": "H1",
        "d0_cc_p": "J3",
        "d1_n": "B1",
        "d1_p": "F5",
        "d2_n": "C2",
        "d2_p": "C1",
        "d3_n": "D2",
        "d3_p": "F4",
        "d4_n": "D1",
        "d4_p": "G5",
        "d5_n": "E3",
        "d5_p": "G4",
        "d6_n": "E2",
        "d6_p": "H5",
        "d7_n": "F3",
        "d7_p": "G3",
    }),

    ("eem1", {
        "d0_cc_n": "L3",
        "d0_cc_p": "L6",
        "d1_n": "F1",
        "d1_p": "H6",
        "d2_n": "G2",
        "d2_p": "H4",
        "d3_n": "H2",
        "d3_p": "J4",
        "d4_n": "J1",
        "d4_p": "J2",
        "d5_n": "K3",
        "d5_p": "K1",
        "d6_n": "L1",
        "d6_p": "L4",
        "d7_n": "M1",
        "d7_p": "K4",
    }),

    ("eem2", {
        "d0_cc_n": "G1",
        "d0_cc_p": "J5",
        "d1_n": "M2",
        "d1_p": "K5",
        "d2_n": "N2",
        "d2_p": "L7",
        "d3_n": "M3",
        "d3_p": "M6",
        "d4_n": "N3",
        "d4_p": "L5",
        "d5_n": "M4",
        "d5_p": "P1",
        "d6_n": "M5",
        "d6_p": "P2",
        "d7_n": "N4",
        "d7_p": "R1",
    }),
]


class Platform(LatticePlatform):
    default_clk_name = "clk25"
    default_clk_period = 40.

    def __init__(self):
        LatticePlatform.__init__(self, "ice40-hx8k-ct256",
                                 _io, _connectors,
                                 toolchain="icestorm")
