from migen import *
from migen.build.xilinx.common import XilinxMultiReg
from migen.build.xilinx.vivado import XilinxVivadoToolchain
from migen.fhdl import verilog
from migen.genlib.cdc import *

if __name__ == "__main__":
    ps = PulseSynchronizer("from", "to")
    v = verilog.convert(ps, {ps.i, ps.o},
            special_overrides={MultiReg: XilinxMultiReg},
            attr_translate=XilinxVivadoToolchain.attr_translate)
    print(v)
