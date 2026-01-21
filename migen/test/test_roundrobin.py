import unittest
from itertools import count

from migen import *
from migen.genlib.roundrobin import RoundRobin, SP_TIMESLICE
from migen.test.support import SimCase

class RoundRobinCase(SimCase, unittest.TestCase):
    class TestBench(Module):
        def __init__(self):
            self.submodules.dut = RoundRobin(n=2, switch_policy=SP_TIMESLICE, max_cycles=8)

    def test_grant_switch(self, vcd=True):
        def gen():
            expected_grants = [0]*10 + [1]*10 + [0]*10
            observed_grants = []
            for cycle in count():
                if cycle == 0:
                    yield self.tb.dut.request[0].eq(1)
                    yield self.tb.dut.request[1].eq(1)
                    yield
                elif cycle == 31:
                    break
                else:
                    grant = (yield self.tb.dut.grant)
                    transok = (yield self.tb.dut.transok)

                    observed_grants.append(grant)
                    if(yield self.tb.dut.transok[grant]):
                        self.assertLessEqual((yield self.tb.dut.counter), 9)

                    if(yield self.tb.dut.transok[grant]):
                        yield self.tb.dut.transok[grant].eq(0)
                    else:
                        yield self.tb.dut.transok[grant].eq(1)
                    yield
                    
            self.assertEqual(observed_grants, expected_grants)


        if vcd:
            self.run_with(gen(), vcd_name='roundrobin.vcd')
        else:
            self.run_with(gen())
