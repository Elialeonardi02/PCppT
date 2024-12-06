import pcppt
class testclass:
    p1:int
    p2:float
    def fun1(self):
        return p1+p2
def fun(a:int):
    a=a+1
print(pcppt.python_cpp_transpiling(testclass))
print(pcppt.python_cpp_transpiling(testclass))
print(pcppt.python_cpp_transpiling(fun))