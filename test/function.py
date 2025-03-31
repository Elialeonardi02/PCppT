@transpile
def function(a:int)->int:
    b:int=10
    return a*b
def voidFunction(a:int):
    b:float=10.2
    c=a*b
@transpile
def returnTypeInferenceFunction(a:int):
    b:float=10.2
    return a*b
@transpile
def returnTypeInferenceFunction(a)->int:
    b:float=10.2

@transpile
def voidFunction(a:int):
    b:float=10.2
    c=a*b
