import pcppt
import ast
from enum import Enum
def FOperator(gather_policy='LB', dispatch_policy='LB'):
    def decorator(cls):
        cls._operator_params = {
            'gather_policy': gather_policy,
            'dispatch_policy': dispatch_policy,
        }
        return cls
    return decorator

class FOperatorKind(Enum):
    NONE = 1
    PARALLELFLATMAP=2
    FILTER = 3
    MAP = 4
    FLAT_MAP = 5

def operator_declaration(class_code):
    astCode=pcppt.get_ast_from_code(class_code)
    print(ast.dump(astCode, indent=4))
    operator_parametes={}
    for parameters in astCode.body[0].decorator_list:
        if isinstance(parameters, ast.Call) and isinstance(parameters.func, ast.Name) and parameters.func.id=='FOperator':
            for parameter in parameters.keywords:
                operator_parametes[parameter.arg.lower()]=parameter.value.value
    operator_declaration='FOperator('
    #name operator
    operator_declaration+=f"'{astCode.body[0].name}',\n"
    #kind of operator
    for method in astCode.body[0].body: #method call AST
        if isinstance(method, ast.FunctionDef) and method.name=='__call__':
            astOperatorMethod=method
    operatorParameters={} #parameter:type
    for parameter in astOperatorMethod.args.args:
        if parameter.arg!='self':
            operatorParameters[parameter.arg]=parameter.annotation.id
    fOperatorKind=FOperatorKind.NONE
    if (len(operatorParameters)==2):#map or Parallel FlatMap or FlatMap
        for parameter in operatorParameters:
            if operatorParameters[parameter][:7] == 'Shipper':
                if fOperatorKind==FOperatorKind.NONE:
                    fOperatorKind=FOperatorKind.FLAT_MAP
                    functionOperatorName='FlatMap'
                else:
                    pass #uncorret signature
            if operatorParameters[parameter][:15] == 'ParallelShipper':
                if fOperatorKind==FOperatorKind.NONE:
                    fOperatorKind=FOperatorKind.PARALLELFLATMAP
                    functionOperatorName='ParallelFlatMap'
                else:
                    pass #uncorret signature
        if fOperatorKind==FOperatorKind.NONE:
            fOperatorKind=FOperatorKind.MAP
            functionOperatorName='Map'

    if (len(operatorParameters)==3):#filter
        functionOperatorName='Filter'
        findBool=False
        for parameter in operatorParameters:
            if operatorParameters[parameter]=='bool':
                if findBool==False:
                    findBool=True
                else:   #signature not valid, exception
                    pass
        if findBool:
            fOperatorKind=FOperatorKind.FILTER
        operator_declaration+=f"          FOperatorKind.FILTER,\n"
    if 'gather_policy' in operator_parametes:
        operator_declaration+=f"          FGatherPolicy.{operator_parametes['gather_policy']},\n"
    else:
        operator_declaration+=f"          FGatherPolicy.LB,\n"
    if 'dispatch_policy' in operator_parametes:
        operator_declaration+=f"          FDispatchPolicy.{operator_parametes['dispatch_policy']},\n"
    else:
        operator_declaration+=f"          FDispatchPolicy.LB,\n"
    operator_declaration+=f"          compute_function={functionOperatorName})"

    parameter= list(operatorParameters.keys())
    astOperatorMethod.name=f"{functionOperatorName}()"
    if fOperatorKind is FOperatorKind.FILTER:
        astOperatorMethod.decorator_list.append(ast.Call(
            func=ast.Name(id='param_cref', ctx=ast.Load()),
            args=[ast.Name(id=f"{parameter[0]}", ctx=ast.Load())],
            keywords=[]))
        astOperatorMethod.decorator_list.append(ast.Call(
            func=ast.Name(id='param_ref', ctx=ast.Load()),
            args=[ast.Name(id=f"{parameter[1]}", ctx=ast.Load())],
            keywords=[]))
        astOperatorMethod.decorator_list.append(ast.Call(
            func=ast.Name(id='param_ref', ctx=ast.Load()),
            args=[ast.Name(id=f"{parameter[2]}", ctx=ast.Load())],
            keywords=[]))
    if fOperatorKind is FOperatorKind.MAP:
        astOperatorMethod.decorator_list.append(ast.Call(
            func=ast.Name(id='param_cref', ctx=ast.Load()),
            args=[ast.Name(id=f"{parameter[0]}", ctx=ast.Load())],
            keywords=[]))
        astOperatorMethod.decorator_list.append(ast.Call(
            func=ast.Name(id='param_ref', ctx=ast.Load()),
            args=[ast.Name(id=f"{parameter[1]}", ctx=ast.Load())],
            keywords=[]))

    print(pcppt.ast_cpp_transpiling(astCode))

    print(operator_declaration)

