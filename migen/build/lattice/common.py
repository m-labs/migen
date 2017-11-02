from migen.fhdl.module import Module
from migen.fhdl.specials import Instance
from migen.genlib.io import *
from migen.genlib.resetsync import AsyncResetSynchronizer


class DiamondAsyncResetSynchronizerImpl(Module):
    def __init__(self, cd, async_reset):
        rst1 = Signal()
        self.specials += [
            Instance("FD1S3BX", i_D=0, i_PD=async_reset,
                i_CK=cd.clk, o_Q=rst1),
            Instance("FD1S3BX", i_D=rst1, i_PD=async_reset,
                i_CK=cd.clk, o_Q=cd.rst)
        ]


class DiamondAsyncResetSynchronizer:
    @staticmethod
    def lower(dr):
        return DiamondAsyncResetSynchronizerImpl(dr.cd, dr.async_reset)


class DiamondDDROutputImpl(Module):
    def __init__(self, i1, i2, o, clk):
        self.specials += Instance("ODDRXD1",
                synthesis_directive="ODDRAPPS=\"SCLK_ALIGNED\"",
                i_SCLK=clk,
                i_DA=i1, i_DB=i2, o_Q=o,
        )


class DiamondDDROutput:
    @staticmethod
    def lower(dr):
        return DiamondDDROutputImpl(dr.i1, dr.i2, dr.o, dr.clk)

diamond_special_overrides = {
    AsyncResetSynchronizer: DiamondAsyncResetSynchronizer,
    DDROutput: DiamondDDROutput
}


icestorm_special_overrides = {

}
