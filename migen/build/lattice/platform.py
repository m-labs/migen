from migen.build.generic_platform import GenericPlatform
from migen.build.lattice import common, diamond, icestorm


class LatticePlatform(GenericPlatform):
    bitstream_ext = ".bit"

    def __init__(self, *args, toolchain="diamond", **kwargs):
        GenericPlatform.__init__(self, *args, **kwargs)
        if toolchain == "diamond":
            self.toolchain = diamond.LatticeDiamondToolchain()
        elif toolchain == "icestorm":
            self.bitstream_ext = ".bin"
            self.toolchain = icestorm.LatticeIceStormToolchain()
        else:
            raise ValueError("Unknown toolchain")

    def get_verilog(self, *args, special_overrides=dict(), **kwargs):
        so = dict(common.lattice_special_overrides)
        so.update(special_overrides)
        if isinstance(self.toolchain, diamond.LatticeDiamondToolchain):
            return GenericPlatform.get_verilog(self, *args, special_overrides=so, **kwargs)
        elif isinstance(self.toolchain, icestorm.LatticeIceStormToolchain):
            return GenericPlatform.get_verilog(self, *args, special_overrides=so,
                attr_translate=self.toolchain.attr_translate, **kwargs)
        else:
            raise ValueError("Unknown toolchain")

    def build(self, *args, **kwargs):
        return self.toolchain.build(self, *args, **kwargs)

    def add_period_constraint(self, clk, period):
        if hasattr(clk, "p"):
            clk = clk.p
        self.toolchain.add_period_constraint(self, clk, period)
