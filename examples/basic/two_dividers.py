# -*- coding: utf-8 -*-
# vim:noexpandtab:ts=8:sw=8:si:smarttab:tw=80
from migen.fhdl import convert
from migen.corelogic import divider

d1 = divider.Divider(16)
d2 = divider.Divider(16)
frag = d1.get_fragment() + d2.get_fragment()
convert(frag, {
	d1.ready_o, d1.quotient_o, d1.remainder_o, d1.start_i, d1.dividend_i, d1.divisor_i,
	d2.ready_o, d2.quotient_o, d2.remainder_o, d2.start_i, d2.dividend_i, d2.divisor_i})
