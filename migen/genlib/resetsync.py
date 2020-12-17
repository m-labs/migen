from migen.fhdl.structure import *
from migen.fhdl.specials import Special


__all__ = ["AsyncResetSynchronizer"]

class AsyncResetSynchronizer(Special):
    """AsyncResetSynchronizer
    Add a reset signal to the provided ClockDomain synchronized into the desired ClockDomain.
    Synchronizing is done by adding two D-Flip-Flops in series with the ClockDomain clock.
    This way the "async_reset" input signal is brought through the two flip-flips into the provided ClockDomain.
    The output of the second flip-flop is directly connected to the reset signal of the provided ClockDomain.
    
    Needs to be added to the specials list: self.specials += AsyncResetSynchronizer()
    
    cd : in
        ClockDomain the reset signal shall be connected to
    async_reset : in
        Reset signal (potentially) asynchronous to the ClockDomain provided in parameter "cd".
        Synchronized instance of the reset signal is connected to ClockDomain "rst" signal.
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
