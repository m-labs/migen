"""
Clock domain crossing module
"""
from math import gcd

from migen.fhdl.structure import *
from migen.fhdl.module import Module
from migen.fhdl.specials import Special, Memory
from migen.fhdl.bitcontainer import value_bits_sign
from migen.fhdl.decorators import ClockDomainsRenamer
from migen.genlib.misc import WaitTimer
from migen.genlib.resetsync import AsyncResetSynchronizer


class MultiRegImpl(Module):
    def __init__(self, i, o, odomain, n, reset=0):
        self.i = i
        self.o = o
        self.odomain = odomain

        w, signed = value_bits_sign(self.i)
        self.regs = [Signal((w, signed), reset=reset, reset_less=True)
                for i in range(n)]

        ###

        sd = getattr(self.sync, self.odomain)
        src = self.i
        for reg in self.regs:
            sd += reg.eq(src)
            src = reg
        self.comb += self.o.eq(src)
        for reg in self.regs:
            reg.attr.add("no_retiming")


class MultiReg(Special):
    def __init__(self, i, o, odomain="sys", n=2, reset=0):
        Special.__init__(self)
        self.i = wrap(i)
        self.o = wrap(o)
        self.odomain = odomain
        self.n = n
        self.reset = reset

    def iter_expressions(self):
        yield self, "i", SPECIAL_INPUT
        yield self, "o", SPECIAL_OUTPUT

    def rename_clock_domain(self, old, new):
        Special.rename_clock_domain(self, old, new)
        if self.odomain == old:
            self.odomain = new

    def list_clock_domains(self):
        r = Special.list_clock_domains(self)
        r.add(self.odomain)
        return r

    @staticmethod
    def lower(dr):
        return MultiRegImpl(dr.i, dr.o, dr.odomain, dr.n, dr.reset)


class PulseSynchronizer(Module):
    def __init__(self, idomain, odomain):
        self.i = Signal()
        self.o = Signal()

        ###

        toggle_i = Signal(reset_less=True)
        toggle_o = Signal()  # registered reset_less by MultiReg
        toggle_o_r = Signal(reset_less=True)

        sync_i = getattr(self.sync, idomain)
        sync_o = getattr(self.sync, odomain)

        sync_i += If(self.i, toggle_i.eq(~toggle_i))
        self.specials += MultiReg(toggle_i, toggle_o, odomain)
        sync_o += toggle_o_r.eq(toggle_o)
        self.comb += self.o.eq(toggle_o ^ toggle_o_r)


class BusSynchronizer(Module):
    """Clock domain transfer of several bits at once.

    Ensures that all the bits form a single word that was present
    synchronously in the input clock domain (unlike direct use of
    ``MultiReg``)."""
    def __init__(self, width, idomain, odomain, timeout=128):
        self.i = Signal(width)
        self.o = Signal(width, reset_less=True)

        if width == 1:
            self.specials += MultiReg(self.i, self.o, odomain)
        else:
            sync_i = getattr(self.sync, idomain)
            sync_o = getattr(self.sync, odomain)

            starter = Signal(reset=1)
            sync_i += starter.eq(0)
            self.submodules._ping = PulseSynchronizer(idomain, odomain)
            # Extra flop on i->o to avoid race between data and request
            # https://github.com/m-labs/nmigen/pull/40#issuecomment-484166790
            ping_o = Signal()
            sync_o += ping_o.eq(self._ping.o)
            self.submodules._pong = PulseSynchronizer(odomain, idomain)
            self.submodules._timeout = ClockDomainsRenamer(idomain)(
                WaitTimer(timeout))
            self.comb += [
                self._timeout.wait.eq(~self._ping.i),
                self._ping.i.eq(starter | self._pong.o | self._timeout.done),
                self._pong.i.eq(ping_o)
            ]

            ibuffer = Signal(width, reset_less=True)
            obuffer = Signal(width)  # registered reset_less by MultiReg
            sync_i += If(self._pong.o, ibuffer.eq(self.i))
            ibuffer.attr.add("no_retiming")
            self.specials += MultiReg(ibuffer, obuffer, odomain)
            sync_o += If(ping_o, self.o.eq(obuffer))


class BlindTransfer(Module):
    """
    PulseSynchronizer but with the input "blinded" until the pulse
    is received in the destination domain.

    This avoids situations where two pulses in the input domain
    at a short interval (shorter than the destination domain clock
    period) causes two toggles of the internal PulseSynchronizer
    signal and no output pulse being emitted.

    With this module, any activity in the input domain will generate
    at least one pulse at the output.

    An optional data word can be transferred with each registered pulse.
    """
    def __init__(self, idomain, odomain, data_width=0):
        self.i = Signal()
        self.o = Signal()
        if data_width:
            self.data_i = Signal(data_width)
            self.data_o = Signal(data_width, reset_less=True)

        # # #

        ps = PulseSynchronizer(idomain, odomain)
        ps_ack = PulseSynchronizer(odomain, idomain)
        self.submodules += ps, ps_ack
        blind = Signal()
        isync = getattr(self.sync, idomain)
        isync += [
            If(self.i, blind.eq(1)),
            If(ps_ack.o, blind.eq(0))
        ]
        self.comb += [
            ps.i.eq(self.i & ~blind),
            ps_ack.i.eq(ps.o),
            self.o.eq(ps.o)
        ]

        if data_width:
            bxfer_data = Signal(data_width, reset_less=True)
            isync += If(ps.i, bxfer_data.eq(self.data_i))
            bxfer_data.attr.add("no_retiming")
            self.specials += MultiReg(bxfer_data, self.data_o,
                                      odomain=odomain)


class GrayCounter(Module):
    def __init__(self, width):
        self.ce = Signal()
        self.q = Signal(width)
        self.q_next = Signal(width)
        self.q_binary = Signal(width)
        self.q_next_binary = Signal(width)

        ###

        self.comb += [
            If(self.ce,
                self.q_next_binary.eq(self.q_binary + 1)
            ).Else(
                self.q_next_binary.eq(self.q_binary)
            ),
            self.q_next.eq(self.q_next_binary ^ self.q_next_binary[1:])
        ]
        self.sync += [
            self.q_binary.eq(self.q_next_binary),
            self.q.eq(self.q_next)
        ]


class GrayDecoder(Module):
    def __init__(self, width):
        self.i = Signal(width)
        self.o = Signal(width, reset_less=True)

        # # #

        o_comb = Signal(width)
        self.comb += o_comb[-1].eq(self.i[-1])
        for i in reversed(range(width-1)):
            self.comb += o_comb[i].eq(o_comb[i+1] ^ self.i[i])
        self.sync += self.o.eq(o_comb)


class ElasticBuffer(Module):
    def __init__(self, width, depth, idomain, odomain):
        self.din = Signal(width)
        self.dout = Signal(width)

        # # #

        reset = Signal()
        cd_write = ClockDomain()
        cd_read = ClockDomain()
        self.comb += [
            cd_write.clk.eq(ClockSignal(idomain)),
            cd_read.clk.eq(ClockSignal(odomain)),
            reset.eq(ResetSignal(idomain) | ResetSignal(odomain))
        ]
        self.specials += [
            AsyncResetSynchronizer(cd_write, reset),
            AsyncResetSynchronizer(cd_read, reset)
        ]
        self.clock_domains += cd_write, cd_read

        wrpointer = Signal(max=depth, reset=depth//2)
        rdpointer = Signal(max=depth)

        storage = Memory(width, depth)
        self.specials += storage

        wrport = storage.get_port(write_capable=True, clock_domain="write")
        rdport = storage.get_port(clock_domain="read")
        self.specials += wrport, rdport

        self.sync.write += wrpointer.eq(wrpointer + 1)
        self.sync.read += rdpointer.eq(rdpointer + 1)

        self.comb += [
            wrport.we.eq(1),
            wrport.adr.eq(wrpointer),
            wrport.dat_w.eq(self.din),

            rdport.adr.eq(rdpointer),
            self.dout.eq(rdport.dat_r)
        ]


def lcm(a, b):
    """Compute the lowest common multiple of a and b"""
    return (a*b)//gcd(a, b)


class Gearbox(Module):
    def __init__(self, iwidth, idomain, owidth, odomain):
        self.i = Signal(iwidth)
        self.o = Signal(owidth, reset_less=True)

        # # #

        rst = Signal()
        cd_write = ClockDomain()
        cd_read = ClockDomain()
        self.comb += [
            rst.eq(ResetSignal(idomain) | ResetSignal(odomain)),
            cd_write.clk.eq(ClockSignal(idomain)),
            cd_read.clk.eq(ClockSignal(odomain)),
            cd_write.rst.eq(rst),
            cd_read.rst.eq(rst)
        ]
        self.clock_domains += cd_write, cd_read

        storage = Signal(2*lcm(iwidth, owidth), reset_less=True)
        wrchunks = len(storage)//iwidth
        rdchunks = len(storage)//owidth
        wrpointer = Signal(max=wrchunks, reset=0 if iwidth > owidth else wrchunks//2)
        rdpointer = Signal(max=rdchunks, reset=rdchunks//2 if iwidth > owidth else 0)

        self.sync.write += \
            If(wrpointer == wrchunks-1,
                wrpointer.eq(0)
            ).Else(
                wrpointer.eq(wrpointer + 1)
            )
        cases = {}
        for i in range(wrchunks):
            cases[i] = [storage[iwidth*i:iwidth*(i+1)].eq(self.i)]
        self.sync.write += Case(wrpointer, cases)


        self.sync.read += \
            If(rdpointer == rdchunks-1,
                rdpointer.eq(0)
            ).Else(
                rdpointer.eq(rdpointer + 1)
            )
        cases = {}
        for i in range(rdchunks):
            cases[i] = [self.o.eq(storage[owidth*i:owidth*(i+1)])]
        self.sync.read += Case(rdpointer, cases)
