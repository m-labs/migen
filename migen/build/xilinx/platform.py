import os
import shutil

from migen.build.generic_platform import GenericPlatform
from migen.build.xilinx import common, vivado, ise


class XilinxPlatform(GenericPlatform):
    bitstream_ext = ".bit"

    def __init__(self, *args, toolchain="ise", **kwargs):
        GenericPlatform.__init__(self, *args, **kwargs)
        self.edifs = set()
        self.ips = set()
        if toolchain == "ise":
            self.toolchain = ise.XilinxISEToolchain()
        elif toolchain == "vivado":
            self.toolchain = vivado.XilinxVivadoToolchain()
        else:
            raise ValueError("Unknown toolchain")

    def add_edif(self, filename):
        self.edifs.add((os.path.abspath(filename)))

    def add_ip(self, filename):
        self.ips.add((os.path.abspath(filename)))

    def copy_ips(self, build_dir, subdir="ip"):
        copied_ips = set()

        target = os.path.join(build_dir, subdir)
        os.makedirs(target, exist_ok=True)
        for filename in self.ips:
            path = os.path.join(subdir, os.path.basename(filename))
            dest = os.path.join(build_dir, path)
            shutil.copyfile(filename, dest)
            copied_ips.add(path)

        return copied_ips

    def get_verilog(self, *args, special_overrides=dict(), **kwargs):
        so = dict(common.xilinx_special_overrides)
        if self.device[:3] == "xc6":
            so.update(common.xilinx_s6_special_overrides)
        if self.device[:3] == "xc7":
            so.update(common.xilinx_s7_special_overrides)
        if self.device[:4] == "xcku":
            so.update(common.xilinx_ku_special_overrides)
        so.update(special_overrides)
        return GenericPlatform.get_verilog(self, *args,
            special_overrides=so, attr_translate=self.toolchain.attr_translate, **kwargs)

    def get_edif(self, fragment, **kwargs):
        return GenericPlatform.get_edif(self, fragment, "UNISIMS", "Xilinx", self.device, **kwargs)

    def build(self, *args, **kwargs):
        return self.toolchain.build(self, *args, **kwargs)

    def add_period_constraint(self, clk, period):
        if hasattr(clk, "p"):
            clk = clk.p
        self.toolchain.add_period_constraint(self, clk, period)

    def add_false_path_constraint(self, from_, to):
        if hasattr(from_, "p"):
            from_ = from_.p
        if hasattr(to, "p"):
            to = to.p
        self.toolchain.add_false_path_constraint(self, from_, to)
