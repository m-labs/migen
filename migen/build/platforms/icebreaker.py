from migen.build.generic_platform import *
from migen.build.lattice import LatticePlatform
from migen.build.lattice.programmer import IceStormProgrammer


_io = [
    ("user_led_n",    0, Pins("11"), IOStandard("LVCMOS33")),
    ("user_led_n",    1, Pins("37"), IOStandard("LVCMOS33")),
    ("user_ledr_n",   0, Pins("11"), IOStandard("LVCMOS33")),
    ("user_ledg_n",   0, Pins("37"), IOStandard("LVCMOS33")),
    ("user_button_n", 0, Pins("10"), IOStandard("LVCMOS33")),

    ("serial", 0,
        Subsignal("rx", Pins("6")),
        Subsignal("tx", Pins("9"), Misc("PULLUP")),
        IOStandard("LVCMOS33")
    ),

    ("spiflash", 0,
        Subsignal("cs_n",      Pins("16"), IOStandard("LVCMOS33")),
        Subsignal("clk",       Pins("15"), IOStandard("LVCMOS33")),
        Subsignal("si",        Pins("17"), IOStandard("LVCMOS33")),
        Subsignal("so",        Pins("14"), IOStandard("LVCMOS33")),
        Subsignal("wp_n",      Pins("12"), IOStandard("LVCMOS33")),
        Subsignal("hld_rst_n", Pins("13"), IOStandard("LVCMOS33")),
    ),

    ("spiflash4x", 0,
        Subsignal("cs_n", Pins("16"), IOStandard("LVCMOS33")),
        Subsignal("clk",  Pins("15"), IOStandard("LVCMOS33")),
        Subsignal("dq",   Pins("14 17 12 13"), IOStandard("LVCMOS33")),
    ),

    ("break_off_pmod", 0,
        Subsignal("btn", Pins("20 19 18"), IOStandard("LVCMOS33")),
        Subsignal("ledr", Pins("26"), IOStandard("LVCMOS33")),
        Subsignal("ledg", Pins("27 25 23 21"), IOStandard("LVCMOS33")),
    ),

    ("clk12", 0, Pins("35"), IOStandard("LVCMOS33"))
]

_connectors = [
    ("PMOD1A", "4 2 47 45 3 48 46 44"),
    ("PMOD1B", "43 38 34 31 42 36 32 28"),
    ("PMOD2",  "27 25 21 19 26 23 20 18")
]


class Platform(LatticePlatform):
    default_clk_name = "clk12"
    default_clk_period = 83.333

    def __init__(self):
        LatticePlatform.__init__(self, "ice40-up5k-sg48", _io, _connectors,
                                 toolchain="icestorm")

    def create_programmer(self):
        return IceStormProgrammer()
