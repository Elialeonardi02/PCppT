'''
Count
- CountTumbling(SIZE)
- KeyedCountTumbling(MAX_KEY, SIZE)
- CountSliding(SIZE, SLIDE)
- KeyedCountSliding(MAX_KEY, SIZE, SLIDE)

Time
- TimeTumbling(SIZE, LATENESS)
- KeyedTimeTumbling(MAX_KEY, SIZE, LATENESS)
- TimeSliding(SIZE, SLIDE, LATENESS)
- KeyedTimeSliding(MAX_KEY, SIZE, SLIDE, LATENESS)

'''
import ast

import pcppt
from DSL import exceptions as ex


def FWindowCount(size=None, max_key=None, slide=None ):
    def decorator(cls):
        cls._operator_params = {
            'size': size,
            'max_key': max_key,
            'slide': slide
        }
        return cls
    return decorator

def FWindowTime(size=None, max_key=None, slide=None, lateness=0):
    def decorator(cls):
        cls._operator_params = {
            'size': size,
            'max_key': max_key,
            'slide': slide,
            'lateness': lateness
        }
        return cls
    return decorator

def windows_declaration(window_code):
    astCode=pcppt.get_ast_from_code(window_code)
    windowCountparameters={}
    windowTimeParameters={}
    for parameters in astCode.body[0].decorator_list:
        if isinstance(parameters, ast.Call) and isinstance(parameters.func, ast.Attribute):
           for parameter in parameters.keywords:
               if parameters.func.attr=='FWindowCount':
                    windowCountparameters[parameter.arg.lower()]=parameter.value.value
               if parameters.func.attr=='FWindowTime':
                   windowTimeParameters[parameter.arg.lower()]=parameter.value.value
    astOperatorMethod = None
    for method in astCode.body[0].body: #method call AST
        if isinstance(method, ast.FunctionDef) and method.name == '__call__':
            if astOperatorMethod is None:
                astOperatorMethod = method
            else:
                raise ex.CallMethodException(astCode.body[0].name)  # Only one __call__ method allowed

    windowParameters={} #parameter:type
    for parameter in astOperatorMethod.args.args:
        if parameter.arg!='self':
            if isinstance(parameter.annotation,ast.Name):
                windowParameters[parameter.arg]=parameter.annotation.id
            elif isinstance(parameter.annotation, ast.Subscript):
                windowParameters[parameter.arg]=f"{parameter.annotation.value.id}[{parameter.annotation.slice.id}]"

    astOperatorMethod.name = 'operator'
    parameter= list(windowParameters.keys())
    if windowCountparameters!={}:#FWindowCount
        if (('size' in windowCountparameters and 'slide' in windowCountparameters) or #countSliding
                ('size' in windowCountparameters)):   #CountTumbling
            astOperatorMethod.decorator_list.append(ast.Call(
                func=ast.Name(id='param_cref', ctx=ast.Load()),
                args=[ast.Name(id=f"{parameter[0]}", ctx=ast.Load())],
                keywords=[]))
            astOperatorMethod.decorator_list.append(ast.Call(
                func=ast.Name(id='param_ref', ctx=ast.Load()),
                args=[ast.Name(id=f"{parameter[1]}", ctx=ast.Load())],
                keywords=[]))
        if (('max_key' in windowCountparameters and 'size' in windowCountparameters and 'slide' in windowCountparameters) or #keyCountSliding
                ('max_key' in windowCountparameters and 'size' in windowCountparameters)): #KeyedCountTumbling
            astOperatorMethod.decorator_list.append(ast.Call(
                func=ast.Name(id='param_ref', ctx=ast.Load()),
                args=[ast.Name(id=f"{parameter[2]}", ctx=ast.Load())],
                keywords=[]))
            astOperatorMethod.decorator_list.append(ast.Call(
                func=ast.Name(id='param_ref', ctx=ast.Load()),
                args=[ast.Name(id=f"{parameter[2]}", ctx=ast.Load())],
                keywords=[]))

    if windowTimeParameters!={}:#FWindowTime
        if (('size' in windowTimeParameters and 'lateness' in windowTimeParameters) or #TimeTumbling
                ('size' in windowTimeParameters and 'slide' in windowTimeParameters and 'lateness' in windowTimeParameters)): #TimeSliding
            astOperatorMethod.decorator_list.append(ast.Call(
                func=ast.Name(id='param_cref', ctx=ast.Load()),
                args=[ast.Name(id=f"{parameter[0]}", ctx=ast.Load())],
                keywords=[]))
            astOperatorMethod.decorator_list.append(ast.Call(
                func=ast.Name(id='param_ref', ctx=ast.Load()),
                args=[ast.Name(id=f"{parameter[1]}", ctx=ast.Load())],
                keywords=[]))
        if (('max_key' in windowTimeParameters and 'size' in windowTimeParameters and 'slide' in windowTimeParameters and 'latenesss' in windowTimeParameters) or #KeyedTimeSliding
                ('max_key' in windowTimeParameters and 'size' in windowTimeParameters and 'lateness' in windowTimeParameters)) :#keyTimeTumbling
            astOperatorMethod.decorator_list.append(ast.Call(
                func=ast.Name(id='param_ref', ctx=ast.Load()),
                args=[ast.Name(id=f"{parameter[2]}", ctx=ast.Load())],
                keywords=[]))
            astOperatorMethod.decorator_list.append(ast.Call(
                func=ast.Name(id='param_ref', ctx=ast.Load()),
                args=[ast.Name(id=f"{parameter[2]}", ctx=ast.Load())],
                keywords=[]))



    return pcppt.ast_cpp_transpiling(astCode)