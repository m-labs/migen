import unittest
import os
import tempfile

from migen.sim.vcd import VCDWriter


class VcdWriter(unittest.TestCase):

    def get_file_path(self, dir):
        return os.path.join(dir, self.id() + ".vcd")

    def check_expectation(self, filename, expectation):
        self.vcd.close()
        with open(filename, 'r') as f:
            self.assertMultiLineEqual(expectation, f.read())

    def test_empty(self):

        expected_content = (
            "$dumpvars\n"
            "$end\n"
            "#0\n"
        )

        with tempfile.TemporaryDirectory() as dir:
            filename = self.get_file_path(dir)
            self.vcd = VCDWriter(filename)
            self.check_expectation(filename, expected_content)

    def test_module_name(self):

        expected_content = (
            "$scope module name1 $end\n"
            "$enddefinitions $end\n"
            "$dumpvars\n"
            "$end\n"
            "#0\n"
        )

        with tempfile.TemporaryDirectory() as dir:
            filename = self.get_file_path(dir)
            self.vcd = VCDWriter(filename, module_name="name1")
            self.check_expectation(filename, expected_content)
