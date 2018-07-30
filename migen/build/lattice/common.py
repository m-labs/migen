from migen.fhdl.module import Module
from migen.fhdl.specials import Instance, Tristate
from migen.fhdl.bitcontainer import value_bits_sign
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
                                  i_DA=i1, i_DB=i2, o_Q=o)


class DiamondDDROutput:
    @staticmethod
    def lower(dr):
        return DiamondDDROutputImpl(dr.i1, dr.i2, dr.o, dr.clk)

diamond_special_overrides = {
    AsyncResetSynchronizer: DiamondAsyncResetSynchronizer,
    DDROutput: DiamondDDROutput
}


class IcestormAsyncResetSynchronizerImpl(Module):
    def __init__(self, cd, async_reset):
        rst1 = Signal()
        self.specials += [
            Instance("SB_DFFS", i_D=0, i_S=async_reset,
                     i_C=cd.clk, o_Q=rst1),
            Instance("SB_DFFS", i_D=rst1, i_S=async_reset,
                     i_C=cd.clk, o_Q=cd.rst)
        ]


class IcestormAsyncResetSynchronizer:
    @staticmethod
    def lower(dr):
        return IcestormAsyncResetSynchronizerImpl(dr.cd, dr.async_reset)


class IcestormTristateImpl(Module):
    def __init__(self, io, o, oe, i):
        nbits, sign = value_bits_sign(io)
        if nbits == 1:
            self.specials += \
                Instance("SB_IO",
                    p_PIN_TYPE=C(0b101001, 6),
                    io_PACKAGE_PIN=io,
                    i_OUTPUT_ENABLE=oe,
                    i_D_OUT_0=o,
                    o_D_IN_0=i,
                )
        else:
            for bit in range(nbits):
                self.specials += \
                    Instance("SB_IO",
                        p_PIN_TYPE=C(0b101001, 6),
                        io_PACKAGE_PIN=io[bit],
                        i_OUTPUT_ENABLE=oe,
                        i_D_OUT_0=o[bit],
                        o_D_IN_0=i[bit],
                    )


class IcestormTristate(Module):
    @staticmethod
    def lower(dr):
        return IcestormTristateImpl(dr.target, dr.o, dr.oe, dr.i)


class IcestormDifferentialOutputImpl(Module):
    def __init__(self, i, o_p, o_n):
        self.specials += Instance("SB_IO",
                                  p_PIN_TYPE=C(0b011000, 6),
                                  p_IO_STANDARD="SB_LVCMOS",
                                  io_PACKAGE_PIN=o_p,
                                  i_D_OUT_0=i)

        self.specials += Instance("SB_IO",
                                  p_PIN_TYPE=C(0b011000, 6),
                                  p_IO_STANDARD="SB_LVCMOS",
                                  io_PACKAGE_PIN=o_n,
                                  i_D_OUT_0=~i)


class IcestormDifferentialOutput:
    @staticmethod
    def lower(dr):
        return IcestormDifferentialOutputImpl(dr.i, dr.o_p, dr.o_n)

icestorm_special_overrides = {
    AsyncResetSynchronizer: IcestormAsyncResetSynchronizer,
    Tristate:               IcestormTristate,
    DifferentialOutput:     IcestormDifferentialOutput
}
