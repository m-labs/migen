import inspect
import sys
from sys import version_info
from opcode import opname
from collections import defaultdict


def get_var_name(frame):
    code = frame.f_code
    call_index = frame.f_lasti
    while call_index > 0 and opname[code.co_code[call_index]] == "CACHE":
        call_index -= 2
    while True:
        call_opc = opname[code.co_code[call_index]]
        if call_opc in ("EXTENDED_ARG",):
            call_index += 2
        else:
            break
    if call_opc not in ("CALL_FUNCTION", "CALL_FUNCTION_KW", "CALL_FUNCTION_EX",
                        "CALL_METHOD", "CALL", "CALL_KW"):
        return None

    index = call_index + 2
    imm = 0
    while True:
        opc = opname[code.co_code[index]]
        if opc == 'EXTENDED_ARG':
            imm |= int(code.co_code[index + 1])
            imm <<= 8
            index += 2
        elif opc in ("STORE_NAME", "STORE_ATTR"):
            imm |= int(code.co_code[index + 1])
            return code.co_names[imm]
        elif opc == "STORE_FAST":
            imm |= int(code.co_code[index + 1])
            if sys.version_info >= (3, 11):
                return code._varname_from_oparg(imm)
            else:
                return code.co_varnames[imm]
        elif opc == "STORE_DEREF":
            imm |= int(code.co_code[index + 1])
            if sys.version_info >= (3, 11):
                return code._varname_from_oparg(imm)
            else:
                if imm < len(code.co_cellvars):
                    return code.co_cellvars[imm]
                else:
                    return code.co_freevars[imm - len(code.co_cellvars)]
        elif opc in ("LOAD_GLOBAL", "LOAD_NAME", "LOAD_ATTR", "LOAD_FAST", "LOAD_DEREF",
                     "DUP_TOP", "BUILD_LIST", "CACHE", "COPY"):
            imm = 0
            index += 2
        else:
            return None


def remove_underscore(s):
    if len(s) > 2 and s[0] == "_" and s[1] != "_":
        s = s[1:]
    return s


def get_obj_var_name(override=None, default=None):
    if override:
        return override

    frame = inspect.currentframe().f_back
    # We can be called via derived classes. Go back the stack frames
    # until we reach the first class that does not inherit from us.
    ourclass = frame.f_locals["self"].__class__
    while "self" in frame.f_locals and isinstance(frame.f_locals["self"], ourclass):
        frame = frame.f_back

    vn = get_var_name(frame)
    if vn is None:
        vn = default
    else:
        vn = remove_underscore(vn)
    return vn

name_to_idx = defaultdict(int)
classname_to_objs = dict()


def index_id(l, obj):
    for n, e in enumerate(l):
        if id(e) == id(obj):
            return n
    raise ValueError


def trace_back(varname=None):
    l = []
    frame = inspect.currentframe().f_back.f_back
    while frame is not None:
        if varname is None:
            varname = get_var_name(frame)
        if varname is not None:
            varname = remove_underscore(varname)
            l.insert(0, (varname, name_to_idx[varname]))
            name_to_idx[varname] += 1

        try:
            obj = frame.f_locals["self"]
        except KeyError:
            obj = None
        if hasattr(obj, "__del__"):
            obj = None

        if obj is None:
            if varname is not None:
                coname = frame.f_code.co_name
                if coname == "<module>":
                    modules = frame.f_globals["__name__"]
                    modules = modules.split(".")
                    coname = modules[len(modules)-1]
                coname = remove_underscore(coname)
                l.insert(0, (coname, name_to_idx[coname]))
                name_to_idx[coname] += 1
        else:
            classname = obj.__class__.__name__.lower()
            try:
                objs = classname_to_objs[classname]
            except KeyError:
                classname_to_objs[classname] = [obj]
                idx = 0
            else:
                try:
                    idx = index_id(objs, obj)
                except ValueError:
                    idx = len(objs)
                    objs.append(obj)
            classname = remove_underscore(classname)
            l.insert(0, (classname, idx))

        varname = None
        frame = frame.f_back
    return l
