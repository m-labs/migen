from migen.build.generic_platform import Subsignal, Pins, IOStandard
from migen.build.lattice import LatticePlatform
from migen.build.lattice.programmer import MyStormProgrammer


_io = [
    ("sram", 0,
        Subsignal("adr", Pins("137 138 139 141 142 42 43 44 73 74 75 76 115",
                              "116 117 118 119 78 62")),
        Subsignal("dat", Pins("135 134 130 128 125 124 122 121 61 60 56 55 52",
                              "49 48 47")),
        Subsignal("oe", Pins("45")),
        Subsignal("we", Pins("120")),
        Subsignal("cs", Pins("136")),
        IOStandard("LVCMOS33"),
    ),

    ("clk100", 0, Pins("129"), IOStandard("LVCMOS33")),

    ("mmc", 0,
        Subsignal("dat", Pins("63 64 39 38")),
        Subsignal("cmd", Pins("41")),
        Subsignal("clk", Pins("37")),
        IOStandard("LVCMOS33"),
    ),

    ("serial", 0,
        Subsignal("rx", Pins("88")),
        Subsignal("tx", Pins("85")),
        Subsignal("rts", Pins("91")),
        Subsignal("cts", Pins("94")),
        IOStandard("LVCMOS33"),
    ),

    ("user_btn", 0, Pins("63"), IOStandard("LVCMOS33")),
    ("user_btn", 1, Pins("64"), IOStandard("LVCMOS33")),

    ("user_sw", 0, Pins("37"), IOStandard("LVCMOS33")),
    ("user_sw", 1, Pins("38"), IOStandard("LVCMOS33")),
    ("user_sw", 2, Pins("39"), IOStandard("LVCMOS33")),
    ("user_sw", 3, Pins("41"), IOStandard("LVCMOS33")),

    ("user_led", 0, Pins("71"), IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("67"), IOStandard("LVCMOS33")),
    ("user_led", 2, Pins("68"), IOStandard("LVCMOS33")),
    ("user_led", 3, Pins("70"), IOStandard("LVCMOS33")),

    ("done", 0, Pins("52"), IOStandard("LVCMOS33")),
    ("dbg1", 0, Pins("49"), IOStandard("LVCMOS33")),
    ("greset", 0, Pins("128"), IOStandard("LVCMOS33")),
]

_connectors = [
    ("pmod0", "94 91 88 85"),
    ("pmod1", "95 93 90 87"),
    ("pmod2", "105 102 99 97"),
    ("pmod3", "104 101 98 96"),
    ("pmod4", "143 114 112 107"),
    ("pmod5", "144 113 110 106"),
    ("pmod6", "10 9 2 1"),
    ("pmod7", "8 7 4 3"),
    ("pmod8", "20 19 16 15"),
    ("pmod9", "18 17 12 11"),
    ("pmod10", "34 33 22 21"),
    ("pmod11", "32 31 26 25"),
    ("pmod12", "29 28 24 23"),
    ("pmod13", "71 67 68 70"),
]


class Platform(LatticePlatform):
    default_clk_name = "clk100"
    default_clk_period = 10

    def __init__(self):
        LatticePlatform.__init__(self, "ice40-hx8k-tq144:4k",
                                 _io, _connectors, toolchain="icestorm")

    def create_programmer(self, serial_port="/dev/ttyACM0"):
        return MyStormProgrammer(serial_port)
