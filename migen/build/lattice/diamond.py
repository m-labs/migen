# This file is Copyright (c) 2015 Florent Kermarrec <florent@enjoy-digital.fr>
# License: BSD

import os
import sys
import subprocess
import shutil

from migen.fhdl.structure import _Fragment
from migen.fhdl.verilog import DummyAttrTranslate

from migen.build.generic_platform import *
from migen.build import tools
from migen.build.lattice import common


def _format_constraint(c):
    if isinstance(c, Pins):
        return ("LOCATE COMP ", " SITE " + "\"" + c.identifiers[0] + "\"")
    elif isinstance(c, IOStandard):
        return ("IOBUF PORT ", " IO_TYPE=" + c.name)
    elif isinstance(c, Misc):
        return c.misc


def _format_lpf(signame, pin, others, resname):
    fmt_c = [_format_constraint(c) for c in ([Pins(pin)] + others)]
    r = ""
    for pre, suf in fmt_c:
        r += pre + "\"" + signame + "\"" + suf + ";\n"
    return r


def _build_lpf(named_sc, named_pc):
    r = "BLOCK RESETPATHS;\n"
    r += "BLOCK ASYNCPATHS;\n"
    for sig, pins, others, resname in named_sc:
        if len(pins) > 1:
            for i, p in enumerate(pins):
                r += _format_lpf(sig + "[" + str(i) + "]", p, others, resname)
        else:
            r += _format_lpf(sig, pins[0], others, resname)
    if named_pc:
        r += "\n" + "\n\n".join(named_pc)
    return r


def _build_files(device, sources, vincpaths, build_name):
    tcl = []
    tcl.append("prj_project new -name \"{}\" -impl \"implementation\" -dev {} -synthesis \"synplify\"".format(build_name, device))
    for path in vincpaths:
        tcl.append("prj_impl option {include path} {\"" + path + "\"}")
    for filename, language, library in sources:
        tcl.append("prj_src add \"" + filename + "\" -work " + library)
    tcl.append("prj_run Synthesis -impl implementation -forceOne")
    tcl.append("prj_run Translate -impl implementation")
    tcl.append("prj_run Map -impl implementation")
    tcl.append("prj_run PAR -impl implementation")
    tcl.append("prj_run Export -impl implementation -task Bitgen")
    tcl.append("prj_run Export -impl implementation -task Jedecgen")
    tools.write_to_file(build_name + ".tcl", "\n".join(tcl))


def _run_diamond(build_name, source, ver=None):
    if sys.platform == "win32" or sys.platform == "cygwin":
        build_script_contents = "REM Autogenerated by Migen\n"
        build_script_contents = "pnmainc " + build_name + ".tcl\n"
        build_script_file = "build_" + build_name + ".bat"
        tools.write_to_file(build_script_file, build_script_contents)
        r = subprocess.call([build_script_file])
        shutil.copy(os.path.join("implementation", build_name + "_implementation.bit"), build_name + ".bit")
        shutil.copy(os.path.join("implementation", build_name + "_implementation.jed"), build_name + ".jed")
    else:
        raise NotImplementedError

    if r != 0:
        raise OSError("Subprocess failed")


class LatticeDiamondToolchain:
    attr_translate = DummyAttrTranslate()

    def build(self, platform, fragment, build_dir="build", build_name="top",
              toolchain_path="/opt/Diamond", run=True):
        os.makedirs(build_dir, exist_ok=True)
        cwd = os.getcwd()
        os.chdir(build_dir)

        if not isinstance(fragment, _Fragment):
            fragment = fragment.get_fragment()
        platform.finalize(fragment)

        v_output = platform.get_verilog(fragment)
        named_sc, named_pc = platform.resolve_signals(v_output.ns)
        v_file = build_name + ".v"
        v_output.write(v_file)
        sources = platform.sources | {(v_file, "verilog", "work")}
        _build_files(platform.device, sources, platform.verilog_include_paths, build_name)

        tools.write_to_file(build_name + ".lpf", _build_lpf(named_sc, named_pc))

        if run:
            _run_diamond(build_name, toolchain_path)

        os.chdir(cwd)

        return v_output.ns

    def add_period_constraint(self, platform, clk, period):
        # TODO: handle differential clk
        platform.add_platform_command("""FREQUENCY PORT "{clk}" {freq} MHz;""".format(freq=str(float(1/period)*1000), clk="{clk}"), clk=clk)
