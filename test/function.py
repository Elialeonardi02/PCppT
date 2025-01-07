@wireflow
def function(a:int)->int:
    b:int=10
    return a*b
def voidFunction(a:int):
    b:float=10.2
    c=a*b
@wireflow
def returnTypeInferenceFunction(a:int):
    b:float=10.2
    return a*b
@wireflow
def returnTypeInferenceFunction(a)->int:
    b:float=10.2

@wireflow
def voidFunction(a:int):
    b:float=10.2
    c=a*b
