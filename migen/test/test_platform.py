import os
import unittest
import importlib
import pkgutil
import tempfile

from migen import *
from migen.genlib.cdc import MultiReg
from migen.build.lattice import diamond, icestorm, trellis
from migen.build.altera import quartus
from migen.build.xilinx import ise, vivado
import migen.build.platforms


def _toolchain_var(plat):
    if isinstance(plat.toolchain, diamond.LatticeDiamondToolchain):
        return "MIGEN_HAS_DIAMOND"
    elif isinstance(plat.toolchain, icestorm.LatticeIceStormToolchain):
        return "MIGEN_HAS_ICESTORM"
    elif isinstance(plat.toolchain, trellis.LatticeTrellisToolchain):
        return "MIGEN_HAS_TRELLIS"
    elif isinstance(plat.toolchain, quartus.AlteraQuartusToolchain):
        return "MIGEN_HAS_QUARTUS"
    elif isinstance(plat.toolchain, ise.XilinxISEToolchain):
        return "MIGEN_HAS_ISE"
    elif isinstance(plat.toolchain, vivado.XilinxVivadoToolchain):
        return "MIGEN_HAS_VIVADO"
    else:
        raise ValueError("Unrecognized toolchain {} for {}"
                         .format(type(plat.toolchain), type(plat)))


def _find_platforms(mod_root):
    def mk_name(mod, child):
        return ".".join([mod.__name__, child])

    imports = []
    for _, name, is_mod in pkgutil.walk_packages(mod_root.__path__):
        if is_mod:
            new_root = importlib.import_module(mk_name(mod_root, name))
            imports.extend(_find_platforms(new_root))
        else:
            imports.append((mk_name(mod_root, name), name))
    return imports


class TestModulePlatform(Module):
    def __init__(self, plat):
        # FIXME: Somehow incorporate plat.request() into this.
        inp = Signal()
        out = Signal()

        self.specials += MultiReg(inp, out)


class TestExamplesPlatform(unittest.TestCase):
    def test_platforms(self):
        for mod, name in _find_platforms(migen.build.platforms):
            with self.subTest(mod=mod, name=name):
                run_toolchain_var = "MIGEN_RUN_TOOLCHAIN_{}".format(
                                    name.upper())

                plat = importlib.import_module(mod).Platform()
                has_toolchain_var = _toolchain_var(plat)
                if not os.getenv(has_toolchain_var, False):
                    raise unittest.SkipTest("{} not set for {}."
                                            .format(has_toolchain_var, name))

                m = TestModulePlatform(plat)
                with tempfile.TemporaryDirectory(name) as temp_dir:
                    do_build = os.getenv(run_toolchain_var, False)
                    if not do_build:
                        print("{} not set, not running toolchain for {}."
                              .format(run_toolchain_var, name))
                    plat.build(m, build_name=name, build_dir=temp_dir,
                               run=do_build)
