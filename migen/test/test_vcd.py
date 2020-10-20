import unittest
import os

from migen.sim.vcd import VCDWriter


class VcdWriter(unittest.TestCase):

    def setUp(self):
        self.filename = self.id() + ".vcd"

    def tearDown(self):
        self.vcd.close()
        with open(self.filename, 'r') as f:
            self.assertMultiLineEqual(self.expected_file, f.read())
        os.remove(self.filename)

    def test_empty(self):

        self.vcd = VCDWriter(self.filename)

        self.expected_file = (
            "$dumpvars\n"
            "$end\n"
            "#0\n"
        )

    def test_module_name(self):

        self.vcd = VCDWriter(self.filename, module_name="name1")

        self.expected_file = (
            "$scope module name1 $end\n"
            "$enddefinitions $end\n"
            "$dumpvars\n"
            "$end\n"
            "#0\n"
        )

    def test_timescale(self):

        self.vcd = VCDWriter(self.filename, timescale="1ps")

        self.expected_file = (
            "$timescale 1ps $end\n"
            "$enddefinitions $end\n"
            "$dumpvars\n"
            "$end\n"
            "#0\n"
        )
