import os
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
        def mkdir_and_build_source(plat, mod, name):
            # Test should not fail if toolchain doesn't exist,
            # which will happen if source=True (the default).
            cwd = os.getcwd()
            try:
                print("{}: Building with source=True.".format(mod))
                mkdir_and_build(plat, name, source=True)
            except FileNotFoundError as e:
                # If build fails, make sure we return to our
                # original directory; mkdir_and_build() will
                # purge the build_dir as part of cleanup.
                os.chdir(cwd)
                print("{}: Toolchain not installed. Building with source=False."
                      .format(mod))
                # Platform will be finalized during first run,
                # so get a fresh instance for both iterations.
                plat = importlib.import_module(mod).Platform()
                mkdir_and_build(plat, name, source=False)

        def mkdir_and_build(plat, name, **kwargs):
            m = TestModulePlatform(plat)
            with tempfile.TemporaryDirectory(name) as temp_dir:
                plat.build(m, run=False, build_name=name,
                           build_dir=temp_dir, **kwargs)

        for mod, name in _find_platforms(migen.build.platforms):
            with self.subTest(mod=mod, name=name):
                # Roach has no default clock, so expect failure/skip.
                if name == "roach":
                    print("{}: Skipping build.".format(mod))
                else:
                    plat = importlib.import_module(mod).Platform()

                    if plat.toolchain.supports_sourcing:
                        mkdir_and_build_source(plat, mod, name)
                    else:
                        # Toolchain doesn't support a looking for a script
                        # setting up an environment (the "source" argument).
                        # The test will not fail just because the toolchain
                        # path doesn't exist.
                        print("{}: Build does not require sourcing."
                              .format(mod))
                        mkdir_and_build(plat, name)
