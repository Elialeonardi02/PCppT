from pickle import FALSE

import exceptions as ex

globalScope='root'

pythonFunction_toParse=['range']

pythonTypes_CppTypes = {    #take from dace
    'None': "void",
    'int': "int",
    'float': "float",
    'bool': "bool",
    'int8': "char",
    'int16': "short",
    'int32': "int",
    'int64': "long long",
    'uint8': "unsigned char",
    'uint16': "unsigned short",
    'uint32': "unsigned int",
    'uint64': "unsigned long long",
    'float16': "half",
    'float32': "float",
    'float64': "double"
}
scope = {}  # variables scope{function{var:type}class:{function:{var:type},var:type}} use root for global scope
def add_to_scope(in_function, in_class, var, type):
    if in_function is not None and in_class is None:
        if in_function not in scope:
            scope[in_function]={}
        if var not in scope[in_function]:
            scope[in_function][var]=type
        else:
            raise ex.AlreadyDefinedError(var)
    if in_function is None and in_class is not None:
        if in_class not in scope:
            scope[in_class]={}
        if var not in scope[in_class]:
            scope[in_class][var]=type
        else:
            raise ex.AlreadyDefinedError(var)
    if in_function is not None and in_class is not None:
        if in_class not in scope:
            scope[in_class] = {}
        if in_function not in scope[in_class]:
            scope[in_class][in_function] = {}
        if var not in scope[in_class][in_function]:
            scope[in_class][in_function][var] = type
        else:
            raise ex.AlreadyDefinedError(var)
    if in_function is None and in_class is None:
        if globalScope not in scope:
            scope[globalScope]={}
        if var not in scope[globalScope]:
            scope[globalScope][var]=type
        else:
            raise ex.AlreadyDefinedError(var)

def check_scope(in_function, in_class, var, val):
    ftype=False #false:not do type inferece, true:do type inference
    if ((in_function is not None and in_class is None and (in_function not in scope or var not in scope[in_function])) or
            (in_function is None and in_class is not None and(in_class not in scope or var not in scope[in_class]))or
            (in_function is not None and in_class is not None and(in_class not in scope or in_function not in scope[in_class] or var not in scope[in_class][in_function]))or
            (in_function is None and in_class is None and (globalScope not in scope or var not in scope[globalScope])) ):
        ftype=True
    if ftype:
        return infer_type(val)+" "
    else:
        return  ""


def infer_type(value):
    python_type = str(type(value).__name__)

    if python_type in pythonTypes_CppTypes:
        return pythonTypes_CppTypes[python_type]
    """
    if isinstance(value, int):
        if value >= 0:
            if value <= 255:
                return pythonTypes_CppTypes['uint8']
            elif value <= 65535:
                return pythonTypes_CppTypes['uint16']
            elif value <= 4294967295:
                return pythonTypes_CppTypes['uint32']
            else:
                return pythonTypes_CppTypes['uint64']
        else:
            if -128 <= value <= 127:
                return pythonTypes_CppTypes['int8']
            elif -32768 <= value <= 32767:
                return pythonTypes_CppTypes['int16']
            elif -2147483648 <= value <= 2147483647:
                return pythonTypes_CppTypes['int32']
            else:
                return pythonTypes_CppTypes['int64']
    elif isinstance(value, float):
        return pythonTypes_CppTypes['float64']
    """
