from collections import OrderedDict

from migen.fhdl.structure import *
from migen.fhdl.structure import _Statement, _Slice, _Part, _ArrayProxy
from migen.fhdl.module import Module, FinalizeError
from migen.fhdl.visit import NodeTransformer
from migen.fhdl.bitcontainer import value_bits_sign


__all__ = ["AnonymousState", "NextState", "NextValue", "FSM"]


class AnonymousState:
    pass


# do not use namedtuple here as it inherits tuple
# and the latter is used elsewhere in FHDL
class NextState(_Statement):
    def __init__(self, state):
        self.state = state


class NextValue(_Statement):
    def __init__(self, target, value):
        self.target = target
        self.value = value


def _target_eq(a, b):
    if type(a) != type(b):
        return False
    ty = type(a)
    if ty == Constant:
        return a.value == b.value
    elif ty == Signal:
        return a is b
    elif ty == Cat:
        return all(_target_eq(x, y) for x, y in zip(a.l, b.l))
    elif ty == _Slice:
        return (_target_eq(a.value, b.value)
                    and a.start == b.start
                    and a.stop == b.stop)
    elif ty == _Part:
        return (_target_eq(a.value, b.value)
                    and _target_eq(a.offset == b.offset)
                    and a.width == b.width)
    elif ty == _ArrayProxy:
        return (all(_target_eq(x, y) for x, y in zip(a.choices, b.choices))
                    and _target_eq(a.key, b.key))
    else:
        raise ValueError("NextValue cannot be used with target type '{}'"
                         .format(ty))


class _LowerNext(NodeTransformer):
    def __init__(self, next_state_signal, encoding, aliases):
        self.next_state_signal = next_state_signal
        self.encoding = encoding
        self.aliases = aliases
        # (target, next_value_ce, next_value)
        self.registers = []

    def _get_register_control(self, target):
        for x in self.registers:
            if _target_eq(target, x[0]):
                return x[1], x[2]
        raise KeyError

    def visit_unknown(self, node):
        if isinstance(node, NextState):
            try:
                actual_state = self.aliases[node.state]
            except KeyError:
                actual_state = node.state
            return self.next_state_signal.eq(self.encoding[actual_state])
        elif isinstance(node, NextValue):
            try:
                next_value_ce, next_value = self._get_register_control(node.target)
            except KeyError:
                related = node.target if isinstance(node.target, Signal) else None
                next_value = Signal(bits_sign=value_bits_sign(node.target), related=related)
                next_value_ce = Signal(related=related)
                self.registers.append((node.target, next_value_ce, next_value))
            return next_value.eq(node.value), next_value_ce.eq(1)
        else:
            return node


class FSM(Module):
    """
    Finite state machine

    Any Python objects can be used as states, e.g. strings.

    Parameters
    ----------
    reset_state
        Reset state. Defaults to the first added state.

    Examples
    --------

    >>> self.active = Signal()
    >>> self.bitno = Signal(3)
    >>>
    >>> fsm = FSM(reset_state="START")
    >>> self.submodules += fsm
    >>>
    >>> fsm.act("START",
    ...     self.active.eq(1),
    ...     If(strobe,
    ...         NextState("DATA")
    ...     )
    ... )
    >>> fsm.act("DATA",
    ...     self.active.eq(1),
    ...     If(strobe,
    ...         NextValue(self.bitno, self.bitno + 1),
    ...         If(self.bitno == 7,
    ...             NextState("END")
    ...         )
    ...     )
    ... )
    >>> fsm.act("END",
    ...     self.active.eq(0),
    ...     NextState("STOP")
    ... )

    """
    def __init__(self, reset_state=None):
        self.actions = OrderedDict()
        self.state_aliases = dict()
        self.reset_state = reset_state

        self.before_entering_signals = OrderedDict()
        self.before_leaving_signals = OrderedDict()
        self.after_entering_signals = OrderedDict()
        self.after_leaving_signals = OrderedDict()

    def act(self, state, *statements):
        """
        Schedules `statements` to be executed in `state`. Statements may include:

            * combinatorial statements of form `a.eq(b)`, equivalent to
              `self.comb += a.eq(b)` when the FSM is in the given `state`;
            * synchronous statements of form `NextValue(a, b)`, equivalent to
              `self.sync += a.eq(b)` when the FSM is in the given `state`;
            * a statement of form `NextState(new_state)`, selecting the next state;
            * `If`, `Case`, etc.
        """
        if self.finalized:
            raise FinalizeError
        if self.reset_state is None:
            self.reset_state = state
        if state not in self.actions:
            self.actions[state] = []
        self.actions[state] += statements

    def delayed_enter(self, name, target, delay):
        if self.finalized:
            raise FinalizeError
        if delay > 0:
            state = name
            for i in range(delay):
                if i == delay - 1:
                    next_state = target
                else:
                    next_state = AnonymousState()
                self.act(state, NextState(next_state))
                state = next_state
        else:
            self.state_aliases[name] = target

    def ongoing(self, state):
        """
        Returns a signal that has the value 1 when the FSM is in the given `state`,
        and 0 otherwise.
        """
        is_ongoing = Signal()
        self.act(state, is_ongoing.eq(1))
        return is_ongoing

    def _get_signal(self, d, state):
        if state not in self.actions:
            self.actions[state] = []
        try:
            return d[state]
        except KeyError:
            is_el = Signal()
            d[state] = is_el
            return is_el

    def before_entering(self, state):
        return self._get_signal(self.before_entering_signals, state)

    def before_leaving(self, state):
        return self._get_signal(self.before_leaving_signals, state)

    def after_entering(self, state):
        signal = self._get_signal(self.after_entering_signals, state)
        self.sync += signal.eq(self.before_entering(state))
        return signal

    def after_leaving(self, state):
        signal = self._get_signal(self.after_leaving_signals, state)
        self.sync += signal.eq(self.before_leaving(state))
        return signal

    def do_finalize(self):
        nstates = len(self.actions)
        self.encoding = dict((s, n) for n, s in enumerate(self.actions.keys()))
        self.decoding = {n: s for s, n in self.encoding.items()}

        self.state = Signal(max=nstates, reset=self.encoding[self.reset_state])
        self.state._enumeration = self.decoding
        self.next_state = Signal(max=nstates)
        self.next_state._enumeration = {n: "{}:{}".format(n, s) for n, s in self.decoding.items()}

        # drive entering/leaving signals
        for state, signal in self.before_leaving_signals.items():
            encoded = self.encoding[state]
            self.comb += signal.eq((self.state == encoded) & ~(self.next_state == encoded))
        if self.reset_state in self.after_entering_signals:
            self.after_entering_signals[self.reset_state].reset = 1
        for state, signal in self.before_entering_signals.items():
            encoded = self.encoding[state]
            self.comb += signal.eq(~(self.state == encoded) & (self.next_state == encoded))

        # Allow overriding and extending control functionality (Next*) in subclasses.
        self._finalize_sync(self._lower_controls())

    def _lower_controls(self):
        return _LowerNext(self.next_state, self.encoding, self.state_aliases)

    def _finalize_sync(self, ls):
        cases = dict((self.encoding[k], ls.visit(v)) for k, v in self.actions.items() if v)
        self.comb += [
            self.next_state.eq(self.state),
            Case(self.state, cases).makedefault(self.encoding[self.reset_state])
        ]
        self.sync += self.state.eq(self.next_state)
        for register, next_value_ce, next_value in ls.registers:
            self.sync += If(next_value_ce, register.eq(next_value))
