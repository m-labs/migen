import unittest
import importlib
import pkgutil
import tempfile

from migen import *
from migen.genlib.cdc import MultiReg
import migen.build.platforms


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
                # Roach has no default clock, so expect failure/skip.
                if name == "roach":
                    pass
                else:
                    plat = importlib.import_module(mod).Platform()
                    m = TestModulePlatform(plat)
                    with tempfile.TemporaryDirectory(name) as temp_dir:
                        plat.build(m, run=False, build_name=name,
                                   build_dir=temp_dir)
