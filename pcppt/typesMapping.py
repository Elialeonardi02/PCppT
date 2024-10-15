from reportlab.lib.validators import isInstanceOf

import exceptions as ex
import  ast
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
scope = {}  # variables scope{function{var:type}class:{function:{var:type},var:type}root:{var:type} use root for global scope

def get_type(ptype):
    if ptype in scope:
        return ptype
    else:
        return pythonTypes_CppTypes.get(ptype)


def add_to_scope(in_function, in_class, var, type): #add variable(var) to scope
    if in_function is not None and in_class is None:        #var is in a function
        if in_function not in scope:
            scope[in_function]={}
        if var not in scope[in_function]:
            scope[in_function][var]=type
        else:
            raise ex.AlreadyDefinedError(var)
    if in_function is None and in_class is not None:        #var is in a class, is an attribute
        if in_class not in scope:
            scope[in_class]={}
        if var not in scope[in_class]:
            scope[in_class][var]=type
        else:
            raise ex.AlreadyDefinedError(var)
    if in_function is not None and in_class is not None:    #var is in a method of a class
        if in_class not in scope:
            scope[in_class] = {}
        if in_function not in scope[in_class]:
            scope[in_class][in_function] = {}
        if var not in scope[in_class][in_function]:
            scope[in_class][in_function][var] = type
        else:
            raise ex.AlreadyDefinedError(var)
    if in_function is None and in_class is None:            #var is in global scope
        if globalScope not in scope:
            scope[globalScope]={}
        if var not in scope[globalScope]:
            scope[globalScope][var]=type
        else:
            raise ex.AlreadyDefinedError(var)



def check_scope(in_function, in_class, var, val):           #check if the variable is in the correct scope, if it is not, return the type of the value associated with the variable
    #FIXME now only check local scope
    ftype=False #false:not do type inferece, true:do type inference
    if (isinstance(val, ast.Constant)and
            (in_function is not None and in_class is None and (in_function not in scope or var not in scope[in_function] or var not in scope[globalScope])) or
            (in_function is None and in_class is not None and(in_class not in scope or var not in scope[in_class]))or
            (in_function is not None and in_class is not None and(in_class not in scope or in_function not in scope[in_class] or var not in scope[in_class][in_function]))or
            (in_function is None and in_class is None and (globalScope not in scope or var not in scope[globalScope])) ):
        ftype=True
    elif isinstance(val, ast.Call):
        f = val.func.id
        if f in scope:
            return f
        else:
            raise ex.TypeNotExistError(f)
    if ftype:   #type inference
        return infer_type(val)+" "
    else:       #no type inference
        return  ""


def infer_type(val):
    if isinstance(val, ast.Constant):
        python_type = str(type(val.value).__name__)
        if python_type in pythonTypes_CppTypes:
            return pythonTypes_CppTypes[python_type]


callableFunctions = {}  #{root:[fuctionName],nameclass:[function_name]} use root for global scope

def add_to_callableFunction(in_class, fname): #add variable(var) to scope
    if in_class is None:
        if globalScope not in callableFunctions:
            callableFunctions[globalScope]=[]
        callableFunctions[globalScope].append(fname)
    else:
        if in_class not in callableFunctions:
            callableFunctions[in_class]=[]
        callableFunctions[in_class].append(fname)

def check_callableFunction(fname):  #FIXME check if is a method or in in the correct scope
    for fs in callableFunctions:
        for f in callableFunctions[fs]:
            if f==fname: return
    if fname in pythonFunction_toParse:
        return
    raise ex.NotCallableError(fname)

