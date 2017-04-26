from migen.fhdl.std import *
from migen.fhdl import verilog


class Example(Module):
    def __init__(self, width=8, n=6):
        # Declare signals
        mux_in = [Signal(width) for x in range(n)]
        mux_out = Signal(width)
        mux_sel = Signal(bits_for(n))

        # Add to set for easy io spec
        self.io = set(mux_in+[mux_out,mux_sel])

        # Build dictionary of mux inputs
        mux_dict = { 'default' : mux_out.eq(0) }
        for x in range(len(mux_in)):
            mux_dict[x] = mux_out.eq(mux_in[x])
        self.comb += Case(mux_sel, mux_dict)

e = Example()
print(verilog.convert(e, e.io))
