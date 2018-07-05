from itertools import count
import tempfile
import os
from collections import OrderedDict
import shutil

from migen.fhdl.namer import build_namespace


def vcd_codes():
    codechars = [chr(i) for i in range(33, 127)]
    for n in count():
        q, r = divmod(n, len(codechars))
        code = codechars[r]
        while q > 0:
            q, r = divmod(q, len(codechars))
            code = codechars[r] + code
        yield code


class VCDWriter:
    def __init__(self, filename):
        self.filename = filename
        self.buffer_file = tempfile.TemporaryFile(
            dir=os.path.dirname(filename), mode="w+")
        self.codegen = vcd_codes()
        self.codes = OrderedDict()
        self.signal_values = dict()
        self.t = 0

    def _get_code(self, signal):
        try:
            code = self.codes[signal]
        except KeyError:
            code = next(self.codegen)
            self.codes[signal] = code
        return code

    def _write_primitive_value(self, f, signal, value):
        l = len(signal)
        if value < 0:
            value += 2**l
        if l > 1:
            fmtstr = "b{:0" + str(l) + "b} {}\n"
        else:
            fmtstr = "{}{}\n"
        code = self._get_code(signal)
        f.write(fmtstr.format(value, code))

    def _write_enum_value(self, f, signal, value):
        val = "b"
        for c in signal._enumeration[value].encode():
            val += "{:08b}".format(c)
        code = self._get_code(signal)
        f.write("{} {}\n".format(val, code))

    def _write_value(self, f, signal, value):
        if hasattr(signal, "_enumeration"):
            self._write_enum_value(self.buffer_file, signal, value)
        else:
            self._write_primitive_value(self.buffer_file, signal, value)

    def set(self, signal, value):
        if signal not in self.signal_values or self.signal_values[signal] != value:
            self._write_value(self.buffer_file, signal, value)
            self.signal_values[signal] = value

    def delay(self, delay):
        self.t += delay
        self.buffer_file.write("#{}\n".format(self.t))

    def close(self):
        out = open(self.filename, "w")
        try:
            ns = build_namespace(self.codes.keys())
            for signal, code in self.codes.items():
                name = ns.get_name(signal)
                if hasattr(signal, "_enumeration"):
                    size = max([len(v) for v in signal._enumeration.values()])*8
                else:
                    size = len(signal)
                out.write("$var wire {size} {code} {name} $end\n"
                          .format(name=name, code=code, size=size))
            out.write("$dumpvars\n")
            for signal in self.codes.keys():
                self._write_value(out, signal, signal.reset.value)
            out.write("$end\n")
            out.write("#0\n")

            self.buffer_file.seek(0)
            shutil.copyfileobj(self.buffer_file, out)
            self.buffer_file.close()
        finally:
            out.close()


class DummyVCDWriter:
    def set(self, signal, value):
        pass

    def delay(self, delay):
        pass

    def close(self):
        pass
