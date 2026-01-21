from migen.fhdl.structure import *
from migen.fhdl.module import Module

(SP_WITHDRAW, SP_CE, SP_TIMESLICE) = range(3)

class RoundRobin(Module):
    def __init__(self, n, switch_policy=SP_WITHDRAW, max_cycles=64):
        self.request = Signal(n)
        self.grant = Signal(max=max(2, n))
        self.switch_policy = switch_policy

        if self.switch_policy == SP_CE:
            self.ce = Signal()

        if self.switch_policy == SP_TIMESLICE:
            self.transok = Signal(n)
            self.max_cycles = max_cycles
            self.counter = Signal(max=max_cycles + 1)

        ###

        if n > 1:
            cases = {}
            for i in range(n):
                switch = []
                for j in reversed(range(i+1, i+n)):
                    t = j % n
                    switch = [
                        If(self.request[t],
                           self.grant.eq(t)
                        ).Else(
                            *switch
                        )
                    ]

                if self.switch_policy == SP_WITHDRAW:
                    case = [If(~self.request[i], *switch)]

                elif self.switch_policy == SP_TIMESLICE:
                    case = [
                        If((~self.request[i]) | ((self.counter >= self.max_cycles) & self.transok[i]),
                           self.counter.eq(0),  # reset counter when switching
                           *switch
                        ).Else(
                           self.counter.eq(self.counter + 1)
                        )
                    ]

                else:
                    case = switch  # SP_CE

                cases[i] = case

            statement = Case(self.grant, cases)

            if self.switch_policy == SP_CE:
                statement = If(self.ce, statement)

            self.sync += statement

        else:
            self.comb += self.grant.eq(0)

