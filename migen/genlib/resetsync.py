from migen.fhdl.structure import *
from migen.fhdl.specials import Special


__all__ = ["AsyncResetSynchronizer"]

class AsyncResetSynchronizer(Special):
    """AsyncResetSynchronizer
    Connects a synchronized reset signal to the provided ClockDomain. Synchronizing is done with two 
    D-Flip-Flops in the provided ClockDomain. The output of the second flip-flop is directly connected
    to the reset signal of the provided ClockDomain.
    
    Asynchronous rising edge of the async_reset signal propagates directly to the output. Clearing the
    async_reset signal is synchronized by the two flip-flops.
    
    Needs to be added to the specials list: self.specials += AsyncResetSynchronizer(cd, async_reset)
    
    cd : in
        ClockDomain the reset signal shall be connected to
    async_reset : in
        Reset signal (potentially) asynchronous to the ClockDomain provided in parameter "cd".
        Synchronized instance of the reset signal is connected to the ClockDomains "rst" signal.
        async_reset is high active.
    """
    def __init__(self, cd, async_reset):
        Special.__init__(self)
        self.cd = cd
        self.async_reset = wrap(async_reset)

    def iter_expressions(self):
        yield self.cd, "clk", SPECIAL_INPUT
        yield self.cd, "rst", SPECIAL_OUTPUT
        yield self, "async_reset", SPECIAL_INPUT

    @staticmethod
    def lower(dr):
        raise NotImplementedError("Attempted to use a reset synchronizer, but platform does not support them")
