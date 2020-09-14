# This file is Copyright (c) 2020 Antmicro <www.antmicro.com>

from migen.build.generic_platform import *
from migen.build.quicklogic import QuicklogicPlatform, JLinkProgrammer, OpenOCD

_io = [
        ("rgb_led", 0,
            Subsignal("r", Pins("34")),
            Subsignal("g", Pins("39")),
            Subsignal("b", Pins("38")),
            IOStandard("LVCMOS33"),
        ),
        ("i2c", 0,
            Subsignal("scl", Pins("4")),
            Subsignal("sda", Pins("5")),
            IOStandard("LVCMOS33"),
        ),
        ("accel", 0,
            Subsignal("int", Pins("2")),
            IOStandard("LVCMOS33"),
        ),
        ("user_btn", 0, Pins("62"), IOStandard("LVCMOS33")),
        ("serial_debug", 0,
            Subsignal("clk", Pins("54")),
            Subsignal("data", Pins("53")),
            IOStandard("LVCMOS33"),
        ),
        ("spi", 0,
            Subsignal("clk", Pins("20")),
            Subsignal("mosi", Pins("16")),
            Subsignal("miso", Pins("17")),
            IOStandard("LVCMOS33"),
        ),
        ("serial", 0,
            Subsignal("tx", Pins("8")),
            Subsignal("rx", Pins("9")),
            IOStandard("LVCMOS33"),
        ),
]

_connectors = [
        ("J2", "28 22 21 37 36 42 40 7"),
        ("J3", "6 55 31 25 47 41"),
        ("J8", "27 26 33 32 23 57 56 3 64 63 61 59"),
]

class Platform(QuicklogicPlatform):
    default_clk_name = "IO_CLK"
    default_clk_period = 10.00

    def __init__(self, programmer="jlink"):
        QuicklogicPlatform.__init__(self, "quickfeather", _io, _connectors,
                                 toolchain="quicklogic")
        self.programmer = programmer

    def create_programmer(self):
        if self.programmer is "jlink":
            return JLinkProgrammer()
        elif self.programmer is "openocd":
            return OpenOCD()
        else:
            raise ValueError("{} programmer is not supported"
                             .format(self.programmer))
