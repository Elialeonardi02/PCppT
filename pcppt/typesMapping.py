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
    'float64': "double",
    'str' : "char"
}

pythonTypes_CppTypesArrays = {    #take from dace
    '[int]': "int",
    '[float]': "float",
    '[bool]': "bool",
    '[int8]': "char",
    '[int16]': "short",
    '[int32]': "int",
    '[int64]': "long long",
    '[uint8]': "unsigned char",
    '[uint16]': "unsigned short",
    '[uint32]': "unsigned int",
    '[uint64]': "unsigned long long",
    '[float16]': "half",
    '[float32]': "float",
    '[float64]': "double"
}


scope = {}  # variables scope{function{var:type}class:{function:{var:type},var:type}root:{var:type} use root for global scope

def get_type(ptype):
    if isinstance(ptype,dict):
        key_type = next(iter(ptype))
        value_type = ptype[key_type]
        return {key_type:value_type}

    else:
        if ptype in scope:  #is class
            return ptype
        if ptype in pythonTypes_CppTypes:
            return pythonTypes_CppTypes.get(ptype)
        if ptype in pythonTypes_CppTypesArrays:
            return pythonTypes_CppTypesArrays.get(ptype)
        raise ex.TypeNotExistError(ptype)

def get_var_type_scope(in_function, in_class, var=None):
    if in_function is not None and in_class is None and in_function in scope and var in scope[in_function]:        #var is in a function
        return  scope[in_function][var]
    if in_function is None and in_class is not None and in_class in scope and var in scope[in_class]:        #var is in a class, is an attribute
        return scope[in_class][var]
    if in_function is not None and in_class is not None and in_class in scope and in_function in scope[in_class] and var in scope[in_class][in_function]:    #var is in a method of a class
        return scope[in_class][in_function][var]
    if in_function is None and in_class is None and globalScope in scope and var in scope[globalScope]:            #var is in global scope
        return [globalScope][var]
    return None

def add_to_scope(in_function, in_class, var=None, type_var=None): #add variable(var) to scope
    if in_function is not None and in_class is None:        #var is in a function
        if in_function not in scope:
            scope[in_function]={}
        if var is not None:
            if var not in scope[in_function]:
                scope[in_function][var]=type_var
            else:
                raise ex.AlreadyDefinedError(var)
    if in_function is None and in_class is not None:        #var is in a class, is an attribute
        if in_class not in scope:
            scope[in_class]={}
        if var is not None:
            if var not in scope[in_class]:
                scope[in_class][var]=type_var
            else:
                raise ex.AlreadyDefinedError(var)
    if in_function is not None and in_class is not None:    #var is in a method of a class
        if in_class not in scope:
            scope[in_class] = {}
        if in_function not in scope[in_class]:
            scope[in_class][in_function] = {}
        if var is not None:
            if  var not in scope[in_class][in_function] :
                scope[in_class][in_function][var] = type_var
            else:
                raise ex.AlreadyDefinedError(var)
    if in_function is None and in_class is None:            #var is in global scope
        if globalScope not in scope:
            scope[globalScope]={}
        if var is not None:
            if var not in scope[globalScope]:
                scope[globalScope][var]=type_var
            else:
                raise ex.AlreadyDefinedError(var)



def check_scope(in_function, in_class, var):           #check if the variable is in the correct scope, if it is not, return the type of the value associated with the variable
    #FIXME now only check local scope
    return not(
            (in_function is not None and in_class is None and
             (scope.get(in_function) is None or var not in scope[in_function])) #var in function
            or
            (in_function is None and in_class is not None and
             (scope.get(in_class) is None or var not in scope[in_class]))   #var attribute of class
            or
            (in_function is not None and in_class is not None and
             (scope.get(in_class) is None or scope.get(in_class).get(in_function) is None or
              var not in scope[in_class][in_function]))
            or
            (in_function is None and in_class is None and
             (scope.get(globalScope) is None or var not in scope[globalScope]))
    )

def infer_type(val):
    if isinstance(val,ast.List):
        val=val.elts[0]
    if isinstance(val, ast.Constant):
        val=val.value
    python_type = str(type(val).__name__)
    if python_type in pythonTypes_CppTypes:
        return pythonTypes_CppTypes[python_type]
def corret_value(v):    #correct a rappresentation of a python value in cpp value
    if isinstance(v,float):
        return str(v)+'f'
    else:
        return str(v)

callableFunctions = {}  #{root:{fuctionName:[functionName,lambda]},nameclass:{MethodName:[MethodName,lambda]}} use root for global scope

def add_to_callableFunction(in_class, functionName, fname):
    scopeCall = globalScope if in_class is None else in_class
    if scopeCall not in callableFunctions:
        callableFunctions[scopeCall] = {}
    if functionName not in callableFunctions[scopeCall]:
        callableFunctions[scopeCall][functionName] = []
    callableFunctions[scopeCall][functionName].append(fname)


def check_callableFunction(in_class, functionName, fname):  #FIXME check if is a method or in in the correct scope
    scopeCall = globalScope if in_class is None else in_class
    return (scopeCall in callableFunctions and functionName in callableFunctions[scopeCall] and fname in callableFunctions[scopeCall][functionName]) or (fname in pythonFunction_toParse)



