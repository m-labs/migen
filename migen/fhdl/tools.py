from migen.fhdl.structure import *
from migen.fhdl.structure import _Slice, _Part, _Assign, _Fragment
from migen.fhdl.visit import NodeVisitor, NodeTransformer
from migen.fhdl.bitcontainer import value_bits_sign
from migen.util.misc import flat_iteration


class _SignalLister(NodeVisitor):
    def __init__(self):
        self.output_list = set()

    def visit_Signal(self, node):
        self.output_list.add(node)


class _TargetLister(NodeVisitor):
    def __init__(self):
        self.output_list = set()
        self.target_context = False

    def visit_Signal(self, node):
        if self.target_context:
            self.output_list.add(node)

    def visit_Assign(self, node):
        self.target_context = True
        self.visit(node.l)
        self.target_context = False

    def visit_ArrayProxy(self, node):
        for choice in node.choices:
            self.visit(choice)


class _InputLister(NodeVisitor):
    def __init__(self):
        self.output_list = set()

    def visit_Signal(self, node):
        self.output_list.add(node)

    def visit_Assign(self, node):
        self.visit(node.r)


def list_signals(node):
    lister = _SignalLister()
    lister.visit(node)
    return lister.output_list


def list_targets(node):
    lister = _TargetLister()
    lister.visit(node)
    return lister.output_list


def list_inputs(node):
    lister = _InputLister()
    lister.visit(node)
    return lister.output_list


def _resort_statements(ol):
    return [statement for i, statement in
            sorted(ol, key=lambda x: x[0])]


def group_by_targets(sl):
    groups = []
    seen = set()
    for order, stmt in enumerate(flat_iteration(sl)):
        targets = set(list_targets(stmt))
        group = [(order, stmt)]
        disjoint = targets.isdisjoint(seen)
        seen |= targets
        if not disjoint:
            groups, old_groups = [], groups
            for old_targets, old_group in old_groups:
                if targets.isdisjoint(old_targets):
                    groups.append((old_targets, old_group))
                else:
                    targets |= old_targets
                    group += old_group
        groups.append((targets, group))
    return [(targets, _resort_statements(stmts))
        for targets, stmts in groups]


def list_special_ios(f, ins, outs, inouts):
    r = set()
    for special in f.specials:
        r |= special.list_ios(ins, outs, inouts)
    return r


class _ClockDomainLister(NodeVisitor):
    def __init__(self):
        self.clock_domains = set()

    def visit_ClockSignal(self, node):
        self.clock_domains.add(node.cd)

    def visit_ResetSignal(self, node):
        self.clock_domains.add(node.cd)

    def visit_clock_domains(self, node):
        for clockname, statements in node.items():
            self.clock_domains.add(clockname)
            self.visit(statements)


def list_clock_domains_expr(f):
    cdl = _ClockDomainLister()
    cdl.visit(f)
    return cdl.clock_domains


def list_clock_domains(f):
    r = list_clock_domains_expr(f)
    for special in f.specials:
        r |= special.list_clock_domains()
    for cd in f.clock_domains:
        r.add(cd.name)
    return r


def is_variable(node):
    if isinstance(node, Signal):
        return node.variable
    elif isinstance(node, _Slice):
        return is_variable(node.value)
    elif isinstance(node, _Part):
        if is_variable(node.offset) != is_variable(node.value):
            raise TypeError
        return is_variable(node.value)
    elif isinstance(node, Cat):
        arevars = list(map(is_variable, node.l))
        r = arevars[0]
        for x in arevars:
            if x != r:
                raise TypeError
        return r
    else:
        raise TypeError


def generate_reset(rst, sl):
    targets = list_targets(sl)
    return [t.eq(t.reset) for t in sorted(targets, key=lambda x: x.duid)
            if not t.reset_less]


def insert_reset(rst, sl):
    return sl + [If(rst, *generate_reset(rst, sl))]


def insert_resets(f):
    newsync = dict()
    for k, v in f.sync.items():
        if f.clock_domains[k].rst is not None:
            newsync[k] = insert_reset(ResetSignal(k), v)
        else:
            newsync[k] = v
    f.sync = newsync


class _Lowerer(NodeTransformer):
    def __init__(self):
        self.target_context = False
        self.extra_stmts = []
        self.comb = []

    def visit_Assign(self, node):
        old_target_context, old_extra_stmts = self.target_context, self.extra_stmts
        self.extra_stmts = []

        self.target_context = True
        lhs = self.visit(node.l)
        self.target_context = False
        rhs = self.visit(node.r)
        r = _Assign(lhs, rhs)
        if self.extra_stmts:
            r = [r] + self.extra_stmts

        self.target_context, self.extra_stmts = old_target_context, old_extra_stmts
        return r


# Basics are FHDL structure elements that back-ends are not required to support
# but can be expressed in terms of other elements (lowered) before conversion.
class _BasicLowerer(_Lowerer):
    def __init__(self, clock_domains):
        self.clock_domains = clock_domains
        _Lowerer.__init__(self)

    def visit_ArrayProxy(self, node):
        # TODO: rewrite without variables
        array_muxed = Signal(value_bits_sign(node), variable=True)
        if self.target_context:
            k = self.visit(node.key)
            cases = {}
            for n, choice in enumerate(node.choices):
                cases[n] = [self.visit_Assign(_Assign(choice, array_muxed))]
            self.extra_stmts.append(Case(k, cases).makedefault())
        else:
            cases = dict((n, _Assign(array_muxed, self.visit(choice)))
                for n, choice in enumerate(node.choices))
            self.comb.append(Case(self.visit(node.key), cases).makedefault())
        return array_muxed

    def visit_ClockSignal(self, node):
        return self.clock_domains[node.cd].clk

    def visit_ResetSignal(self, node):
        rst = self.clock_domains[node.cd].rst
        if rst is None:
            if node.allow_reset_less:
                return 0
            else:
                raise ValueError("Attempted to get reset signal of resetless"
                                 " domain '{}'".format(node.cd))
        else:
            return rst


class _ComplexSliceLowerer(_Lowerer):
    def visit_Slice(self, node):
        if not isinstance(node.value, Signal):
            slice_proxy = Signal(value_bits_sign(node.value))
            if self.target_context:
                a = _Assign(node.value, slice_proxy)
            else:
                a = _Assign(slice_proxy, node.value)
            self.comb.append(self.visit_Assign(a))
            node = _Slice(slice_proxy, node.start, node.stop)
        return NodeTransformer.visit_Slice(self, node)

class _ComplexPartLowerer(_Lowerer):
    def visit_Part(self, node):
        value_proxy = node.value
        offset_proxy = node.offset
        if not isinstance(node.value, Signal):
            value_proxy = Signal(value_bits_sign(node.value))
            if self.target_context:
                a = _Assign(node.value, value_proxy)
            else:
                a = _Assign(value_proxy, node.value)
            self.comb.append(self.visit_Assign(a))
        if not isinstance(node.offset, Signal):
            offset_proxy = Signal(value_bits_sign(node.offset))
            if self.target_context:
                a = _Assign(node.offset, offset_proxy)
            else:
                a = _Assign(offset_proxy, node.offset)
            self.comb.append(self.visit_Assign(a))
        node = _Part(value_proxy, offset_proxy, node.width)
        return NodeTransformer.visit_Part(self, node)

def _apply_lowerer(l, f):
    f = l.visit(f)
    f.comb += l.comb

    for special in sorted(f.specials, key=lambda s: s.duid):
        for obj, attr, direction in special.iter_expressions():
            if direction != SPECIAL_INOUT:
                # inouts are only supported by Migen when connected directly to top-level
                # in this case, they are Signal and never need lowering
                l.comb = []
                l.target_context = direction != SPECIAL_INPUT
                l.extra_stmts = []
                expr = getattr(obj, attr)
                expr = l.visit(expr)
                setattr(obj, attr, expr)
                f.comb += l.comb + l.extra_stmts

    return f


def lower_basics(f):
    return _apply_lowerer(_BasicLowerer(f.clock_domains), f)


def lower_complex_slices(f):
    return _apply_lowerer(_ComplexSliceLowerer(), f)

def lower_complex_parts(f):
    return _apply_lowerer(_ComplexPartLowerer(), f)

class _ClockDomainRenamer(NodeVisitor):
    def __init__(self, old, new):
        self.old = old
        self.new = new

    def visit_ClockSignal(self, node):
        if node.cd == self.old:
            node.cd = self.new

    def visit_ResetSignal(self, node):
        if node.cd == self.old:
            node.cd = self.new


def rename_clock_domain_expr(f, old, new):
    cdr = _ClockDomainRenamer(old, new)
    cdr.visit(f)


def rename_clock_domain(f, old, new):
    rename_clock_domain_expr(f, old, new)
    if new != old:
        if old in f.sync:
            if new in f.sync:
                f.sync[new].extend(f.sync[old])
            else:
                f.sync[new] = f.sync[old]
            del f.sync[old]
    for special in f.specials:
        special.rename_clock_domain(old, new)
    try:
        cd = f.clock_domains[old]
    except KeyError:
        pass
    else:
        cd.rename(new)


def call_special_classmethod(overrides, obj, method, *args, **kwargs):
    cl = obj.__class__
    if cl in overrides:
        cl = overrides[cl]
    if hasattr(cl, method):
        return getattr(cl, method)(obj, *args, **kwargs)
    else:
        return None


def _lower_specials_step(overrides, specials):
    f = _Fragment()
    lowered_specials = set()
    for special in sorted(specials, key=lambda x: x.duid):
        impl = call_special_classmethod(overrides, special, "lower")
        if impl is not None:
            f += impl.get_fragment()
            lowered_specials.add(special)
    return f, lowered_specials


def _can_lower(overrides, specials):
    for special in specials:
        cl = special.__class__
        if cl in overrides:
            cl = overrides[cl]
        if hasattr(cl, "lower"):
            return True
    return False


def lower_specials(overrides, specials):
    f, lowered_specials = _lower_specials_step(overrides, specials)
    while _can_lower(overrides, f.specials):
        f2, lowered_specials2 = _lower_specials_step(overrides, f.specials)
        f += f2
        lowered_specials |= lowered_specials2
        f.specials -= lowered_specials2
    return f, lowered_specials
