from migen.build.generic_platform import *
from migen.build.lattice import LatticePlatform
from collections import defaultdict


_io = [
       ("clk25", 0, Pins("K9"), IOStandard("LVCMOS33")),

       ("user_led", 0, Pins("H3"), IOStandard("LVCMOS33")),

       ("serial", 0,
        Subsignal("rx", Pins("T11")),
        Subsignal("tx", Pins("M13"), Misc("PULLUP")),
        Subsignal("rts", Pins("T10"), Misc("PULLUP")),
        Subsignal("cts", Pins("M15"), Misc("PULLUP")),
        IOStandard("LVCMOS33"),
        ),

       ("serial", 1,
        Subsignal("rx", Pins("T13")),
        Subsignal("tx", Pins("M11"), Misc("PULLUP")),
        Subsignal("rts", Pins("B16"), Misc("PULLUP")),
        Subsignal("cts", Pins("A6"), Misc("PULLUP")),
        IOStandard("LVCMOS33"),
        ),

       ("bb_uart1", 0,
        Subsignal("rx", Pins("T3")),
        Subsignal("tx", Pins("R5"), Misc("PULLUP")),
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
        Subsignal("rst", Pins("B2")),
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

    ("stm32", {
        "PA0": "A2",
        "PA1": "P14",
        "PA2": "B8",
        "PA3": "L13",
        "PA7": "N12",
        "PA8": "M9",
        "PA9": "P10",
        "PA10": "R10",
        "PA15": "B14",

        "PB0": "A1",
        "PB1": "G12",
        "PB2": "B6",
        "PB6": "A7",
        "PB10": "C3",
        "PB11": "F7",
        "PB12": "B13",
        "PB13": "B12",
        "PB15": "A11",

        "PC0": "L14",
        "PC1": "M14",
        "PC2": "A9",
        "PC3": "M16",
        "PC4": "N16",
        "PC5": "P16",
        "PC6": "B10",
        "PC7": "B15",
        "PC8": "H16",
        "PC9": "J10",
        "PC10": "J16",
        "PC11": "J15",
        "PC12": "K12",

        "PD0": "T9",
        "PD1": "N9",
        "PD2": "K13",
        "PD7": "L12",
        "PD11": "E5",
        "PD12": "D5",
        "PD13": "C5",

        "PE0": "D3",
        "PE2": "P15",
        "PE3": "N10",
        "PE4": "R15",
        "PE5": "T15",
        "PE6": "M8",
        "PE7": "E6",
        "PE8": "D6",
        "PE9": "F12",
        "PE10": "A5",
        "PE11": "G11",
        "PE12": "B4",
        "PE13": "F11",
        "PE14": "C4",
        "PE15": "B3",

        "PF7": "L9",
        "PF8": "L10",
        "PF9": "P9",
        "PF14": "B9",

        "PG0": "M7",
        "PG1": "P8",
        "PG2": "K14",
        "PG3": "K15",
    }),

    ("bb", {
        "CLKOUT2": "R9",

        "GPIO0_7": "R14",

        "GPIO1_16": "A16",
        "GPIO1_17": "R3",
        "GPIO1_29": "D11",
        "GPIO1_31": "D14",

        "GPIO2_6": "D16",
        "GPIO2_7": "C16",
        "GPIO2_8": "E16",
        "GPIO2_9": "D15",
        "GPIO2_11": "F15",
        "GPIO2_13": "F16",
        "GPIO2_22": "C11",
        "GPIO2_23": "C10",
        "GPIO2_24": "E10",
        "GPIO2_25": "D4",

        "GPIO3_19": "P4",
        "GPIO3_21": "R4",

        "GPMC_A2": "T7",
        "GPMC_A3": "T1",
        "GPMC_A14": "F9",
        "GPMC_A15": "B7",
        "GPMC_AD0": "C12",
        "GPMC_AD1": "E11",
        "GPMC_AD2": "J12",
        "GPMC_AD3": "J11",
        "GPMC_AD4": "C13",
        "GPMC_AD5": "C14",
        "GPMC_AD6": "J14",
        "GPMC_AD7": "J13",
        "GPMC_AD8": "E13",
        "GPMC_AD9": "G13",
        "GPMC_AD10": "G14",
        "GPMC_AD11": "G10",
        "GPMC_AD12": "E14",
        "GPMC_AD13": "H14",
        "GPMC_AD14": "F14",
        "GPMC_AD15": "F13",
        "GPMC_ADVN": "H12",
        "GPMC_BE0N": "G16",
        "GPMC_CLK": "H11",
        "GPMC_CSN1": "D13",
        "GPMC_OEN": "H13",
        "GPMC_WE1N": "G15",
    }),

    ("esp32", {
        "IO2": "D9",
        "IO4": "D7",
        "IO22": "C7",
        "IO34": "E9",
        "IO35": "C9",
    }),

    ("orange_pi", {
       "PG06": "A15",
    }),
]


for eem, ios in _connectors:
    if eem.startswith("eem"):
        pins = defaultdict(list)
        for j in range(8):
            res_name = "{}:d{}_{}".format(eem, j, "cc_" if j == 0 else "")
            # platform.request("eem{k}", j) -> Record n:p (1 bit Signals)
            _io.append((eem, j,
                        *[Subsignal(p, Pins("{}{}".format(res_name, p)))
                          for p in "np"],
                        IOStandard("LVDS25E")))
            for p in "np":
                # FIXME: break up EEMs for yosys/nextpnr not to get confused
                # platform.request("eem{k}_n", j) -> Signal(1)
                _io.append(("{}_{}".format(eem, p), j,
                            Pins("{}{}".format(res_name, p))))
                pins[p].append("{}{}".format(res_name, p))

        # platform.request("eem", k) -> Record n:p (8 bits)
        _io.append(("eem", int(eem[-1]),
                    *[Subsignal(p, Pins(" ".join(pins[p]))) for p in "np"],
                    IOStandard("LVDS25E")))


class Platform(LatticePlatform):
    default_clk_name = "clk25"
    default_clk_period = 40.

    def __init__(self):
        LatticePlatform.__init__(self, "ice40-hx8k-ct256",
                                 _io, _connectors,
                                 toolchain="icestorm")
