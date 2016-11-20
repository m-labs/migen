# This file is Copyright (c) 2016 Ivan Uvarov <flashcactus@ya.ru>
# License: BSD
#
# Note: This file maps only the buttons, switches, LEDs and GPIO headers;
# the actual devboard has much more than that.

from migen.build.generic_platform import *
from migen.build.altera import AlteraPlatform
from migen.build.altera.programmer import USBBlaster


_io = [
    ("clk50", 0, Pins("M9"), IOStandard("3.3-V LVTTL")),
    ("clk50", 1, Pins("H13"), IOStandard("3.3-V LVTTL")),
    ("clk50", 2, Pins("E10"), IOStandard("3.3-V LVTTL")),
    ("clk50", 3, Pins("V15"), IOStandard("3.3-V LVTTL")),

    ("user_led", 0, Pins("AA2"), IOStandard("3.3-V LVTTL")),
    ("user_led", 1, Pins("AA1"), IOStandard("3.3-V LVTTL")),
    ("user_led", 2, Pins("W2"), IOStandard("3.3-V LVTTL")),
    ("user_led", 3, Pins("Y3"), IOStandard("3.3-V LVTTL")),
    ("user_led", 4, Pins("N2"), IOStandard("3.3-V LVTTL")),
    ("user_led", 5, Pins("N1"), IOStandard("3.3-V LVTTL")),
    ("user_led", 6, Pins("U2"), IOStandard("3.3-V LVTTL")),
    ("user_led", 7, Pins("U1"), IOStandard("3.3-V LVTTL")),
    ("user_led", 8, Pins("L2"), IOStandard("3.3-V LVTTL")),
    ("user_led", 9, Pins("L1"), IOStandard("3.3-V LVTTL")),


    ("seven_seg", 0, Pins("U21 V21 W22 W21 Y22 Y21 AA22"), IOStandard("3.3-V LVTTL")),
    ("seven_seg", 1, Pins("AA20 AB20 AA19 AA18 AB18 AA17 U22"), IOStandard("3.3-V LVTTL")),
    ("seven_seg", 2, Pins("Y19 AB17 AA10 Y14 V14 AB22 AB21"), IOStandard("3.3-V LVTTL")),
    ("seven_seg", 3, Pins("Y16 W16 Y17 V16 U17 V18 V19"), IOStandard("3.3-V LVTTL")),
    ("seven_seg", 4, Pins("U20 Y20 V20 U16 U15 Y15 P9"), IOStandard("3.3-V LVTTL")),
    ("seven_seg", 5, Pins("N9 M8 T14 P14 C1 C2 W19"), IOStandard("3.3-V LVTTL")),


    ("key", 0, Pins("U7"), IOStandard("3.3-V LVTTL")),
    ("key", 1, Pins("W9"), IOStandard("3.3-V LVTTL")),
    ("key", 2, Pins("M7"), IOStandard("3.3-V LVTTL")),
    ("key", 3, Pins("M6"), IOStandard("3.3-V LVTTL")),

    ("sw", 0, Pins("U13"), IOStandard("3.3-V LVTTL")),
    ("sw", 1, Pins("V13"), IOStandard("3.3-V LVTTL")),
    ("sw", 2, Pins("T13"), IOStandard("3.3-V LVTTL")),
    ("sw", 3, Pins("T12"), IOStandard("3.3-V LVTTL")),
    ("sw", 4, Pins("AA15"), IOStandard("3.3-V LVTTL")),
    ("sw", 5, Pins("AB15"), IOStandard("3.3-V LVTTL")),
    ("sw", 6, Pins("AA14"), IOStandard("3.3-V LVTTL")),
    ("sw", 7, Pins("AA13"), IOStandard("3.3-V LVTTL")),
    ("sw", 8, Pins("AB13"), IOStandard("3.3-V LVTTL")),
    ("sw", 9, Pins("AB12"), IOStandard("3.3-V LVTTL")),


    ("gpio_0", 0,
        Pins("N16 B16 M16 C16 D17 K20 K21 K22 M20 M21 N21 R22 R21 T22 N20 N19 M22 P19 L22 P17 P16 M18 L18 L17 L19 K17 K19 P18 R15 R17 R16 T20 T19 T18 T17 T15"),
        IOStandard("3.3-V LVTTL")
    ),
    ("gpio_1", 0,
        Pins("H16 A12 H15 B12 A13 B13 C13 D13 G18 G17 H18 J18 J19 G11 H10 J11 H14 A15 J13 L8 A14 B15 C15 E14 E15 E16 F14 F15 F13 F12 G16 G15 G13 G12 J17 K16"),
        IOStandard("3.3-V LVTTL")
    ),
]


class Platform(AlteraPlatform):
    default_clk_name = "clk50"
    default_clk_period = 20

    def __init__(self):
        AlteraPlatform.__init__(self, "5CEBA4F23C7", _io)

    def create_programmer(self):
        return USBBlaster()
