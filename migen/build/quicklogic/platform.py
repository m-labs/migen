import os
import shutil

from migen.build.generic_platform import GenericPlatform
from migen.build.quicklogic import quicklogic

class QuicklogicPlatform(GenericPlatform):
    bitstream_ext = ".bit"

    def __init__(self, *args, toolchain="quicklogic", **kwargs):
        GenericPlatform.__init__(self, *args, **kwargs)
        self.edifs = set()
        self.ips = set()

        self.board_type = "ql-eos-s3_wlcsp"
        if self.device == "chandalar":
            self.part = "PD64"
        elif self.device == "quickfeather":
            self.part = "PU64"
        else:
            raise ValueError("Unknown device")

        if toolchain == "quicklogic":
            self.toolchain = quicklogic.QuicklogicToolchain()
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
        return GenericPlatform.get_verilog(self, *args,
            attr_translate=self.toolchain.attr_translate, **kwargs)

    def get_edif(self, fragment, **kwargs):
        return GenericPlatform.get_edif(self, fragment, "UNISIMS", "Quicklogic", self.device, **kwargs)

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

    def do_finalize(self, fragment, *args, **kwargs):
        super().do_finalize(fragment, *args, **kwargs)
