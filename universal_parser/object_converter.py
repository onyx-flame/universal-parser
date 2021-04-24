import dis
import inspect
import opcode
import weakref
import types
import copy
import importlib


def is_class_instance2(o):
    return bool(type(o).__flags__ & (1 << 9))


def walk_global_ops(code):
    for instr in dis.get_instructions(code):
        op = instr.opcode
        if op in (opcode.opmap['STORE_GLOBAL'], opcode.opmap['DELETE_GLOBAL'], opcode.opmap['LOAD_GLOBAL']):
            yield op, instr.arg


def extract_code_globals(co):
    out_names = weakref.WeakKeyDictionary().get(co)
    if out_names is None:
        names = co.co_names
        out_names = {names[oparg] for _, oparg in walk_global_ops(co)}
        if co.co_consts:
            for const in co.co_consts:
                if isinstance(const, types.CodeType):
                    out_names |= extract_code_globals(const)

        weakref.WeakKeyDictionary()[co] = out_names
    return out_names


def refactor_dict(new_obj):
    for i in new_obj:
        if type(new_obj[i]) in (int, float, bool, str, type(None)):
            continue
        elif type(new_obj[i]) is list:
            new_obj[i] = refactor_list(new_obj[i])
        elif type(new_obj[i]) is tuple:
            new_obj[i] = refactor_list(list(new_obj[i]))
        elif isinstance(new_obj[i], types.FunctionType):
            new_obj[i] = function_to_dict(new_obj[i])
        elif type(new_obj[i]) is dict:
            new_obj[i] = refactor_dict(new_obj[i])
        elif is_class_instance2(new_obj[i]):
            new_obj[i] = class_instance_to_dict(new_obj[i])
    return new_obj


def refactor_list(new_obj):
    for i in range(len(new_obj)):
        if type(new_obj[i]) in (int, float, bool, str, type(None)):
            continue
        elif type(new_obj[i]) is list:
            new_obj[i] = refactor_list(new_obj[i])
        elif type(new_obj[i]) is tuple:
            new_obj[i] = refactor_list(list(new_obj[i]))
        elif isinstance(new_obj[i], types.FunctionType):
            new_obj[i] = function_to_dict(new_obj[i])
        elif type(new_obj[i]) is dict:
            new_obj[i] = refactor_dict(new_obj[i])
        elif is_class_instance2(new_obj[i]):
            new_obj[i] = class_instance_to_dict(new_obj[i])
        else:
            raise ValueError
    return new_obj


def refactor_object(obj):
    new_obj = copy.copy(obj)
    if type(new_obj) in (int, float, bool, str, type(None)):
        return new_obj
    elif type(new_obj) is list:
        return refactor_list(new_obj)
    elif type(new_obj) is tuple:
        return refactor_list(list(new_obj))
    elif isinstance(new_obj, types.FunctionType):
        return function_to_dict(new_obj)
    elif type(new_obj) is dict:
        return refactor_dict(new_obj)
    elif is_class_instance2(new_obj):
        return class_instance_to_dict(new_obj)
    else:
        raise ValueError(f"{type(new_obj)} isn't supported")


def restore_object(obj):
    new_obj = copy.copy(obj)
    if type(new_obj) is list:
        for i in range(len(new_obj)):
            if type(new_obj[i]) is dict:
                if new_obj[i].get('type') == 'function':
                    new_obj[i] = dict_to_function(new_obj[i])
    elif type(new_obj) is dict:
        if new_obj.get('type') == 'function':
            new_obj = dict_to_function(obj)
        else:
            for i in new_obj:
                if type(new_obj[i]) is dict:
                    if new_obj[i].get('type') == 'function':
                        new_obj[i] = dict_to_function(new_obj[i])
    return new_obj


def dict_to_function(obj):
    source = obj['source']
    function_globals = obj['globals']
    for key in function_globals:
        if function_globals[key] == 'module':
            if globals().get(key) is not None:
                function_globals[key] = globals()[key]
            else:
                function_globals[key] = importlib.import_module(key)
    function_code = types.CodeType(source[0], source[1], source[2], source[3], source[4],
                                   source[5], bytes.fromhex(source[6]), tuple(source[7]),
                                   tuple(source[8]), tuple(source[9]), source[10],
                                   source[11], source[12], bytes.fromhex(source[13]))
    return types.FunctionType(function_code, function_globals)


def function_to_dict(obj):
    used_globals_names = [item for item in extract_code_globals(obj.__code__)]
    globs_dct = {}
    for x in used_globals_names:
        if obj.__globals__.get(x) is not None:
            if inspect.ismodule(obj.__globals__.get(x)):
                globs_dct[x] = "module"
            else:
                globs_dct[x] = obj.__globals__[x]
    globs_dct['__builtins__'] = 'module'
    source = get_function_code_attributes(obj)
    return {'type': 'function', 'source': source, "globals": globs_dct}


def class_instance_to_dict(obj):
    variables = vars(obj)
    return refactor_dict(variables)


def get_function_code_attributes(obj):
    source = [
        obj.__code__.co_argcount,
        obj.__code__.co_posonlyargcount,
        obj.__code__.co_kwonlyargcount,
        obj.__code__.co_nlocals,
        obj.__code__.co_stacksize,
        obj.__code__.co_flags,
        obj.__code__.co_code.hex(),
        list(obj.__code__.co_consts),
        list(obj.__code__.co_names),
        list(obj.__code__.co_varnames),
        obj.__code__.co_filename,
        obj.__code__.co_name,
        obj.__code__.co_firstlineno,
        obj.__code__.co_lnotab.hex()
    ]
    return source
