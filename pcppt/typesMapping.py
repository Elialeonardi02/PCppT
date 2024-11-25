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
parsing_constant={
    True:'true',
    False:'false'
}
pythonTypes_CppTypesArrays = {    #TODO remov, use in get_type
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

pythonOperator_CppOperator= {
    #boolop
    "And": "&&",
    "Or": "||",

    #operator
    "Add": "+",
    "Sub": "-",
    "Mult": "*",
    #"MatMult"not implemented
    "Div": "/",
    "Mod": "%",
    "Pow": "**",
    "LShift":"<<",
    "Rshift":">>",
    "BitOr":"|",
    "BitXor":"^",
    "BidAnd":"&",
    "FloorDiv": "/",

    #UnaryOp
    "Invert":"~",
    "Not":"!",
    "UAdd":"+",
    "USub":"-",

    #cmpop
    "Eq": "==",
    "NotEq": "!=",
    "Lt": "<",
    "LtE": "<=",
    "Gt": ">",
    "GtE": ">=",
    #"Is" not implemented
    #"IsNot" not implemented
    #"In" not implemented
    #"NotIn" not implemented
    }

cppTypes_DefaultsValues = { #use for default constructor
    "void": "None",
    "int": "0",
    "float": "0.0",
    "bool": "False",
    "char": "0",
    "short": "0",
    "int16": "0",
    "int32": "0",
    "int64": "0",
    "unsigned char": "0",
    "unsigned short": "0",
    "unsigned int": "0",
    "unsigned long long": "0",
    "uint8": "0",
    "uint16": "0",
    "uint32": "0",
    "uint64": "0",
    "half": "0.0",
    "double": "0.0",
    "float16": "0.0",
    "float32": "0.0",
    "float64": "0.0",
    "char": '""'
}


def get_operator(nodeOperator): #provide aritmetic or boolean operator
    return pythonOperator_CppOperator[nodeOperator.__class__.__name__]

scope = {}  # variables scope{function{var:type}class:{function:{var:type},var:type}root:{var:type} use root for global scope

def get_type(ptype):    #provide type of a var in scope
    if isinstance(ptype,dict):  #use for array multitype #FIXME necessary?
        key_type = next(iter(ptype))
        value_type = ptype[key_type]
        return {key_type:value_type}
    else:
        if ptype in scope:  #is class
            return ptype
        if ptype in pythonTypes_CppTypes: #is type 
            return pythonTypes_CppTypes.get(ptype)
        if ptype in pythonTypes_CppTypesArrays: #is array of type
            return pythonTypes_CppTypesArrays.get(ptype)
        raise ex.TypeNotExistError(ptype)   

def get_var_type_scope(in_function, in_class, var=None):    #provide type of var in scope
    if in_function is not None and in_class is None and in_function in scope and var in scope[in_function]: #var is in a function
        return  scope[in_function][var]
    if in_function is None and in_class is not None and in_class in scope and var in scope[in_class]:   #var is in a class, is an attribute
        return scope[in_class][var]
    if in_function is not None and in_class is not None and in_class in scope and in_function in scope[in_class] and var in scope[in_class][in_function]:   #var is in a method of a class, is not an attribute
        return scope[in_class][in_function][var]
    if in_function is None and in_class is None and globalScope in scope and var in scope[globalScope]: #var is in global scope
        return [globalScope][var]
    return None #var is not delcare in this scope

def add_to_scope(in_function, in_class, var=None, type_var=None): #add variable(var) to scope
    if in_function is not None and in_class is None:    #var is in a function
        if in_function not in scope:    #add function to scope if not already in
            scope[in_function]={}
        if var is not None: 
            if var not in scope[in_function]:   #add var to function scope
                scope[in_function][var]=type_var
            else:   #var is already defined in this scope
                raise ex.AlreadyDefinedError(var)
    if in_function is None and in_class is not None:    #var is in a class, is an attribute
        if in_class not in scope:   #add class to scope if not already in
            scope[in_class]={}
        if var is not None: 
            if var not in scope[in_class]: #add var to class scope
                scope[in_class][var]=type_var
            else:   #var is already defined in this scope
                raise ex.AlreadyDefinedError(var)
    if in_function is not None and in_class is not None: #var is in a method of a class
        if in_class not in scope:   #add class to scope if not already in
            scope[in_class] = {}
        if in_function not in scope[in_class]:  #add method to scope of class if not already in
            scope[in_class][in_function] = {}
        if var is not None: 
            if  var not in scope[in_class][in_function]: #add var to scope of method if not already defined
                scope[in_class][in_function][var] = type_var
            else:   #var is already defined
                raise ex.AlreadyDefinedError(var)   
    if in_function is None and in_class is None:    #var is in global scope
        if globalScope not in scope:    #add global scope if not already in
            scope[globalScope]={}
        if var is not None: 
            if var not in scope[globalScope]: #add var to global scope if not already in
                scope[globalScope][var]=type_var
            else:   #var already declared in this scope
                raise ex.AlreadyDefinedError(var)   



def check_scope(in_function, in_class, var):    #check if the variable is in the correct scope
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
              var not in scope[in_class][in_function])) #var in a method of a class, not an attribute
            or
            (in_function is None and in_class is None and   
             (scope.get(globalScope) is None or var not in scope[globalScope])) #var il global scope
    )

def infer_type(val,value):  #infer type from val/value
    if isinstance(val,ast.List) :    #array type inference
        if all(isinstance(elem,ast.Constant) for elem in val.elts): #there is only constant (es:[1,2,3]) in the value node
            python_type=str(type(val.elts[0].value).__name__)   #take the type of the first element of the array
            for i in range(1, len(val.elts)):   #raise an exception for element of different type 
                if str(type(val.elts[i].value).__name__) != python_type:
                    raise ex.MultyTypesArrayNotAllowed(value)
            return pythonTypes_CppTypes[python_type]
    elif isinstance(val, ast.Constant): #type inference of constant
        return pythonTypes_CppTypes[str(type(val.value).__name__)]
    return f"auto"  #type inference of expression

def corret_value(v):    #correct a rappresentation of a python value in cpp value #FIXME necessary?
    if isinstance(v,float):
        return str(v)+'f'
    else:
        return str(v)

callableFunctions = {}  #{root:{fuctionName:[functionName,lambda]},nameclass:{MethodName:[MethodName,lambda]}} use root for global scope

def add_to_callableFunction(in_class, functionName, fname): #add function to callable function
    scopeCall = globalScope if in_class is None else in_class   #locate the scope of function, root or in a class
    if scopeCall not in callableFunctions:
        callableFunctions[scopeCall] = {}
    if functionName not in callableFunctions[scopeCall]:
        callableFunctions[scopeCall][functionName] = []
    callableFunctions[scopeCall][functionName].append(fname)


def check_callableFunction(in_class, functionName, fname):#false: can't call function, true: can call functions  #FIXME check if is a method or in in the correct scope
    scopeCall = globalScope if in_class is None else in_class
    return scopeCall in callableFunctions and functionName in callableFunctions[scopeCall] and fname in callableFunctions[scopeCall][functionName] or (fname in pythonFunction_toParse)



