import os
import struct
import re
import subprocess
import sys
import ctypes


def language_by_filename(name):
    extension = name.rsplit(".")[-1]
    if extension in ["v", "vh", "vo"]:
        return "verilog"
    if extension in ["vhd", "vhdl", "vho"]:
        return "vhdl"
    return None


def write_to_file(filename, contents, force_unix=False):
    newline = None
    if force_unix:
        newline = "\n"
    with open(filename, "w", newline=newline) as f:
        f.write(contents)


def sub_rules(line, rules, max_matches=1):
    for pattern, color in rules:
        line, matches = re.subn(pattern, color, line, max_matches)
        max_matches -= matches
        if not max_matches:
            break
    return line


def subprocess_call_filtered(command, rules, *, max_matches=1, **kwargs):
    with subprocess.Popen(command, stdout=subprocess.PIPE,
                          universal_newlines=True, bufsize=1,
                          **kwargs) as proc:
        with open(proc.stdout.fileno(), errors="ignore", closefd=False) as stdout:
            for line in stdout:
                print(sub_rules(line, rules, max_matches), end="")
        return proc.wait()
