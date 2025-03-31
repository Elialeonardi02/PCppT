from DSL import exceptions as ex
import pcppt
import ast
from enum import Enum

# Dictionary to keep track of already processed operators
pipeOperators = {}

class FDispatchPolicy(Enum):
    NONE = 1
    RR = 2
    LB = 3
    KB = 4
    BR = 5
class FGatherPolicy(Enum):
    NONE = 1
    RR = 2
    LB = 3
    KB = 4

def FOperator(gather_policy=FGatherPolicy.LB, dispatch_policy=FDispatchPolicy.LB): #Decorator to assign gather and dispatch policies to an operator class.
    def decorator(cls):
        cls._operator_params = {}
        if gather_policy == FGatherPolicy.RR:
            cls._operator_params['gather_policy'] = gather_policy.name
        elif gather_policy == FGatherPolicy.KB:
            cls._operator_params['gather_policy'] = 'KB'
        else:
            cls._operator_params['gather_policy'] = 'LB'

        if dispatch_policy == FDispatchPolicy.RR:
            cls._operator_params['dispatch_policy'] = 'RR'
        elif dispatch_policy == FDispatchPolicy.KB:
            cls._operator_params['dispatch_policy'] = 'KB'
        elif dispatch_policy == FDispatchPolicy.BR:
            cls._operator_params['dispatch_policy'] = 'BR'
        else:
            cls._operator_params['dispatch_policy'] = 'LB'
        return cls
    return decorator


class FOperatorKind(Enum): #Types of operators.
    NONE = 1
    PARALLELFLATMAP = 2
    FILTER = 3
    MAP = 4
    FLATMAP = 5

def handlerParameters(parameter, operatorParameters):#Extracts the parameter type from the AST annotation and stores it in the dictionary.
    if isinstance(parameter.annotation, ast.Name):
        if parameter.annotation.id is not None:
            operatorParameters[parameter.arg] = parameter.annotation.id
    elif isinstance(parameter.annotation, ast.Subscript):
        if parameter.annotation.slice.id is not None:
            operatorParameters[parameter.arg] = f"{parameter.annotation.value.id}[{parameter.annotation.slice.id}]"

def operator_declaration(class_code): #Parses the AST of the given class and generates the corresponding operator declaration.
    astCode = pcppt.get_ast_from_code(class_code)  # Generate AST from code
    operator_parameters = {}  # Stores operator-specific parameters
    print(ast.dump(astCode, indent=4))
    # Extracts parameters from class decorators
    for parameters in astCode.body[0].decorator_list:
        if isinstance(parameters, ast.Call) and isinstance(parameters.func, ast.Attribute) and parameters.func.attr == 'FOperator':
            for parameter in parameters.keywords:
                operator_parameters[parameter.arg.lower()] = parameter.value.attr

    operator_declaration = 'FOperator('
    # Operator name
    operator_declaration += f"'{astCode.body[0].name}',\n"

    # Identify the __call__ method in the class
    astOperatorMethod = None
    for method in astCode.body[0].body:  # Iterate over class methods
        if isinstance(method, ast.FunctionDef) and method.name == '__call__':
            if astOperatorMethod is None:
                astOperatorMethod = method
            else:
                raise ex.CallMethodException(astCode.body[0].name)  # Only one __call__ method allowed

    operatorParameters = {}  # Dictionary to store parameter names and their types
    prevOperator = {}  # Stores the last operator in the pipeline
    prevParameters = {}  # Stores parameters of the previous operator
    tempPipeOperator = []  # Temporary list to store parameter types for the current operator

    # Retrieve the last processed operator, if any
    if pipeOperators:
        prevOperator, prevParameters = next(reversed(pipeOperators.items()))

    # Process parameters in the __call__ method
    for i, parameter in enumerate(astOperatorMethod.args.args):
        i = i - 1  # The first argument is 'self' and should be ignored
        if parameter.arg != 'self':
            if isinstance(parameter.annotation, ast.Name) or isinstance(parameter.annotation, ast.Subscript):
                handlerParameters(parameter, operatorParameters)
            else:
                # If the parameter is missing a type, infer it from the previous operator's output
                if i == 0 and prevParameters[i + 1] is not None:
                    parameter.annotation = prevParameters[i + 1]
                    handlerParameters(parameter, operatorParameters)
            tempPipeOperator.append(parameter.annotation)

    # Store the current operator's parameters
    pipeOperators[astCode.body[0].name] = tempPipeOperator

    fOperatorKind = FOperatorKind.NONE  # Default kind

    # Determine the type of operator based on the number of parameters
    if len(operatorParameters) == 2:  # Map, ParallelFlatMap, or FlatMap
        for parameter in operatorParameters:
            if operatorParameters[parameter][:7] == 'Shipper':
                if fOperatorKind == FOperatorKind.NONE:
                    fOperatorKind = FOperatorKind.FLATMAP
                    operator_declaration += f"          FOperatorKind.FLATMAP,\n"
            if operatorParameters[parameter][:15] == 'ParallelShipper':
                if fOperatorKind == FOperatorKind.NONE:
                    fOperatorKind = FOperatorKind.PARALLELFLATMAP
                    operator_declaration += f"          FOperatorKind.PARALLELFLATMAP,\n"
        if fOperatorKind == FOperatorKind.NONE:
            fOperatorKind = FOperatorKind.MAP
            operator_declaration += f"          FOperatorKind.MAP,\n"

    if len(operatorParameters) == 3:  # Filter operator
        functionOperatorName = 'Filter'
        findBool = False
        for parameter in operatorParameters:
            if operatorParameters[parameter] == 'bool':
                if not findBool:
                    findBool = True
        if findBool:
            fOperatorKind = FOperatorKind.FILTER
        operator_declaration += f"          FOperatorKind.FILTER,\n"


    # Append gather and dispatch policies to the declaration
    if 'gather_policy' in operator_parameters:
        operator_declaration += f"          FGatherPolicy.{operator_parameters['gather_policy']},\n"
    else:
        operator_declaration += f"          FGatherPolicy.LB,\n"
    if 'dispatch_policy' in operator_parameters:
        operator_declaration += f"          FDispatchPolicy.{operator_parameters['dispatch_policy']},\n"
    else:
        operator_declaration += f"          FDispatchPolicy.LB,\n"

    operator_declaration += f"          functor={astCode.body[0].name})"

    # Rename __call__ method with operator
    parameter = list(operatorParameters.keys())
    astOperatorMethod.name = 'operator'


    # Add decorators for function parameters based on the operator type
    astOperatorMethod.decorator_list.append(ast.Call(
        func=ast.Name(id='param_cref', ctx=ast.Load()),
        args=[ast.Name(id=f"{parameter[0]}", ctx=ast.Load())],
        keywords=[]))
    astOperatorMethod.decorator_list.append(ast.Call(
        func=ast.Name(id='param_ref', ctx=ast.Load()),
        args=[ast.Name(id=f"{parameter[1]}", ctx=ast.Load())],
        keywords=[]))
    if fOperatorKind is FOperatorKind.FILTER:
        astOperatorMethod.decorator_list.append(ast.Call(
            func=ast.Name(id='param_ref', ctx=ast.Load()),
            args=[ast.Name(id=f"{parameter[2]}", ctx=ast.Load())],
            keywords=[]))
    # Append operator parameters to the pipeline
    for parameter in operatorParameters:
        tempPipeOperator.append(operatorParameters[parameter])
    pipeOperators[astCode.body[0].name] = tempPipeOperator

    # Return the final operator declaration and transpiled AST code
    return f"{operator_declaration}\n{pcppt.ast_cpp_transpiling(astCode,FOperatorKind)}"
