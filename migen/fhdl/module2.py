import inspect
import sys
import ast
import textwrap
from collections import OrderedDict

from migen.fhdl.structure import *
from migen.fhdl.structure import _Assign, _Operator, _Fragment


__all__ = ["Module2", "ports", "comb", "sync"]


class PortManager:
    def __init__(self):
        object.__setattr__(self, "_migen_port_order", [])

    def __setattr__(self, k, v):
        object.__setattr__(self, k, v)
        self._migen_port_order.append(k)


class PortManagerFactory:
    def __setattr__(self, k, v):
        pm = PortManager()
        setattr(pm, k, v)
        ns = inspect.currentframe().f_back.f_locals
        ns["ports"] = pm


ports = PortManagerFactory()


def find_node_by_lineno(node, lineno):
    if getattr(node, "lineno", None) == lineno:
        return node
    for child in ast.iter_child_nodes(node):
        r = find_node_by_lineno(child, lineno)
        if r is not None:
            return r
    return None


def get_ast_node_at(lines, lineno):
    lines = textwrap.dedent("".join(lines))
    top_node = ast.parse(lines)
    return find_node_by_lineno(top_node, lineno)


def eval_ast(node, globs, locs):
    if not isinstance(node, ast.Expression):
        node = ast.Expression(node, ctx=ast.Load())
    co = compile(node, "<string>", "eval")
    return eval(co, globs, locs)


boolop_to_fhdl = {
    ast.And: "&", 
    ast.Or: "|"
}

unop_to_fhdl = {
    ast.Invert: "~",
    ast.Not: "-"
}

binop_to_fhdl = {
    ast.Add: "+",
    ast.Sub: "-",
    ast.Mult: "*",
    ast.LShift: "<<<",
    ast.RShift: ">>>",
    ast.BitOr: "|",
    ast.BitXor: "^",
    ast.BitAnd: "&"
}

def ast_expr_to_fhdl(node, globs, locs):
    if isinstance(node, ast.BoolOp):
        op = boolop_to_fhdl[type(node.op)]
        r = _Operator(op, 
                      [ast_expr_to_fhdl(node.values[0], globs, locs),
                       ast_expr_to_fhdl(node.values[1], globs, locs)])
        for v in node.values[2:]:
            r = _Operator(op, [r, ast_expr_to_fhdl(v, globs, locs)])
        return r
    elif isinstance(node, ast.UnaryOp):
        return _Operator(unop_to_fhdl[type(node.op)],
                         [ast_expr_to_fhdl(node.operand, globs, locs)])
    elif isinstance(node, ast.BinOp):
        return _Operator(binop_to_fhdl[type(node.op)],
                         [ast_expr_to_fhdl(node.left, globs, locs),
                          ast_expr_to_fhdl(node.right, globs, locs)])
    else:
        return eval_ast(node, globs, locs)


def ast_stmt_to_fhdl(node, globs, locs):
    if isinstance(node, list):
        return [ast_stmt_to_fhdl(x, globs, locs)
                for x in node]
    if isinstance(node, ast.Assign):
        value = ast_expr_to_fhdl(node.value, globs, locs)
        r = []
        for t in node.targets:
            assert isinstance(t, ast.Attribute)
            assert t.attr == "next"
            r.append(_Assign(eval_ast(t.value, globs, locs), value))
        return r
    elif isinstance(node, ast.If):
        return If(ast_expr_to_fhdl(node.test, globs, locs),
                  *ast_stmt_to_fhdl(node.body, globs, locs)).Else(
                  *ast_stmt_to_fhdl(node.orelse, globs, locs))
    elif isinstance(node, ast.Expr):
        return eval_ast(node.value, globs, locs)
    else:
        raise NotImplementedError
        

class ContextHackException(Exception):
    pass


def trace_raise_che(frame, event, arg):
    raise ContextHackException


class TranslateContextManager:
    def __init__(self, clock_domain):
        self.clock_domain = clock_domain

    def __enter__(self):
        frame = inspect.currentframe().f_back
        lines, lnum = inspect.getsourcelines(frame)

        with_stmt = get_ast_node_at(lines, frame.f_lineno-lnum+1)
        stmts = ast_stmt_to_fhdl(with_stmt.body, frame.f_globals, frame.f_locals)

        module = frame.f_locals["self"]
        module._add_logic(self.clock_domain, stmts)

        if sys.gettrace() is None:
            sys.settrace(lambda *args, **keys: None)
        frame.f_trace = trace_raise_che

    def __exit__(self, type, value, traceback):
        return type is ContextHackException


class SyncContextManager(TranslateContextManager):
    def __init__(self):
        TranslateContextManager.__init__(self, "sys")

    def __call__(self, clock_domain):
        return TranslateContextManager(clock_domain)


comb = TranslateContextManager(None)
sync = SyncContextManager()


class Module2:
    def __init__(self, *args, **kwargs):
        if not hasattr(self.__class__, "ports"):
            self.__class__.ports = PortManager()
        ports = self.__class__.ports

        leftovers = OrderedDict((k, getattr(ports, k))
                                for k in ports._migen_port_order)
        for name, value in zip(ports._migen_port_order, args):
            setattr(self, name, value)
            del leftovers[name]
        for name, value in kwargs.items():
            setattr(self, name, value)
            del leftovers[name]
        for name, desc in leftovers.items():
            if callable(desc):
                value = desc()
            else:
                value = Signal(desc, name=name)
            setattr(self, name, value)

        self.__fragment = _Fragment()

    def _add_logic(self, clock_domain, stmts):
        if clock_domain is None:
            self.__fragment.comb += stmts
        else:
            if clock_domain not in self.__fragment.sync:
                self.__fragment.sync[clock_domain] = []
            self.__fragment.sync[clock_domain] += stmts

    def get_ports(self):
        for name in self.ports._migen_port_order:
            yield getattr(self, name)

    def build(self):
        pass

    def finalize(self):
        pass

    def get_fragment(self):
        return self.__fragment
