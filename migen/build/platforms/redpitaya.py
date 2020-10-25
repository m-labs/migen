# From redpid, copyright 2014-2020 Robert Jordens <jordens@gmail.com>
# https://github.com/quartiq/redpid
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform

_io = [
    ("user_led", i, Pins(p), IOStandard("LVCMOS33"),
     Drive(4), Misc("SLEW SLOW")) for i, p in enumerate(
        "F16 F17 G15 H15 K14 G14 J15 J14".split())
]

_io += [
    ("clk125", 0,
        Subsignal("p", Pins("U18")),
        Subsignal("n", Pins("U19")),
        IOStandard("DIFF_HSTL_I_18")
    ),

    ("adc", 0,
        Subsignal("clk", Pins("N20 P20"), Misc("SLEW=FAST"), Drive(8)),
        Subsignal("cdcs", Pins("V18"), Misc("SLEW=FAST"), Drive(8)),
        Subsignal("data_a", Pins("V17 U17 Y17 W16 Y16 W15 W14 Y14 "
                                 "W13 V12 V13 T14 T15 V15 T16 V16"),
                  ),
        Subsignal("data_b", Pins("T17 R16 R18 P16 P18 N17 R19 T20 "
                                 "T19 U20 V20 W20 W19 Y19 W18 Y18"),
                  ),
        IOStandard("LVCMOS18")
    ),

    ("dac", 0,
        Subsignal("data", Pins("M19 M20 L19 L20 K19 J19 J20 H20 "
                               "G19 G20 F19 F20 D20 D19"),
                  Misc("SLEW=SLOW"), Drive(4)),
        Subsignal("wrt", Pins("M17"), Drive(8), Misc("SLEW=FAST")),
        Subsignal("sel", Pins("N16"), Drive(8), Misc("SLEW=FAST")),
        Subsignal("rst", Pins("N15"), Drive(8), Misc("SLEW=FAST")),
        Subsignal("clk", Pins("M18"), Drive(8), Misc("SLEW=FAST")),
        IOStandard("LVCMOS33")
    ),

    ("pwm", 0, Pins("T10"), IOStandard("LVCMOS18"),
        Drive(12), Misc("SLEW=FAST")),
    ("pwm", 1, Pins("T11"), IOStandard("LVCMOS18"),
        Drive(12), Misc("SLEW=FAST")),
    ("pwm", 2, Pins("P15"), IOStandard("LVCMOS18"),
        Drive(12), Misc("SLEW=FAST")),
    ("pwm", 3, Pins("U13"), IOStandard("LVCMOS18"),
        Drive(12), Misc("SLEW=FAST")),

    ("xadc", 0,
        Subsignal("p", Pins("C20 E17 B19 E18 K9")),
        Subsignal("n", Pins("B20 D18 A20 E19 L10")),
        IOStandard("LVCMOS33")
    ),

    ("exp", 0,
        Subsignal("p", Pins("G17 H16 J18 K17 L14 L16 K16 M14")),
        Subsignal("n", Pins("G18 H17 H18 K18 L15 L17 J16 M15")),
        IOStandard("LVCMOS33"),
    ),

    ("sata", 0,
        Subsignal("rx_p", Pins("T12")),
        Subsignal("rx_n", Pins("U12")),
        Subsignal("tx_p", Pins("U14")),
        Subsignal("tx_n", Pins("U15")),
        IOStandard("DIFF_SSTL18_I")
    ),

    ("sata", 1,
        Subsignal("rx_p", Pins("P14")),
        Subsignal("rx_n", Pins("R14")),
        Subsignal("tx_p", Pins("N18")),
        Subsignal("tx_n", Pins("P19")),
        IOStandard("DIFF_SSTL18_I")
    ),
]


class Platform(XilinxPlatform):
    def __init__(self):
        XilinxPlatform.__init__(self, "xc7z010-clg400-1", _io,
            toolchain="vivado")
