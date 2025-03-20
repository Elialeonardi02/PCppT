from typing import Generic, TypeVar


import pcppt

#windows
#set of windows with correct parameters



class shipper_t:
    def send(self, tuple):
        pass

    def send_eos(self):
        pass

from DSL import operators, windows

uint32=int
float32=float

class tuple_t:
    key : uint32
    value : float32

    def __init__(self):
        self.key = 0
        self.value = 0.0

    def __init__(self, key : uint32, value : float32):
        self.key = key
        self.value = value

class result_t:
    sum : float32
    count : uint32
    def __init__(self):
        self.sum = 0.0
        self.count = 0

    def mean(self, a:[int,10]):
        pass


@operators.FOperator(gather_policy='LB')
class filterOperator:
    def __call__(self, inn:tuple_t, out:result_t,flag:bool):
        pass
    def __other_method(self):
        pass

pcppt.python_cpp_transpiling(tuple_t)
pcppt.python_cpp_transpiling(result_t)

#operators.operator_declaration(filterOperator)


@operators.FOperator()
class mapOperator:
    def __call__(self, input:tuple_t, output:result_t):
        pass
    def __other_method(self):
        pass

operators.operator_declaration(mapOperator)
R = TypeVar("R")
class Shipper(Generic[R]):
    def send(self, out):
        pass
pcppt.python_cpp_transpiling(Shipper)

@operators.FOperator(gather_policy='LB')
class flatmap:
    def __call__(self, inn:tuple_t, shipper:Shipper[tuple_t]):
        pass
    def __other_method(self):
        pass
operators.operator_declaration(flatmap)

@windows.FWindowTime(max_key=8, size=6, lateness=2)
class KeyedTimeWindowTest:
    def window(self):
        pass
windows.windows_declaration(KeyedTimeWindowTest)