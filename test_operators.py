import inspect
import sys
from enum import Enum
from pcppt import python_cpp_transpiling
from pcppt import codeCppClass as param
import ast

class FOperatorKind(Enum):
    NONE = 1
    FILTER = 3
    MAP = 4
    FLAT_MAP = 5

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

class map:
    def __call__(self, tuple: tuple_t,  result: result_t):
        pass

print(python_cpp_transpiling(tuple_t))
print(python_cpp_transpiling(result_t))

class filter:
    def __call__(self, p1: tuple_t, p2: result_t, keep: bool):
        pass

class shipper_t:
    def send(self, tuple):
        pass

    def send_eos(self):
        pass

class flatmap:
    def __call__(self, tuple: tuple_t, shipper: shipper_t):
        pass

class FOperator:
    def __init__(self, kind: FOperatorKind, func):
        self.kind = kind
        self.func = func

    def transpile(self):
        cAst = ast.parse(inspect.getsource(self.func)).body[0].body[0]
        if self.kind == FOperatorKind.FILTER:
            if len(cAst.args.args) != 4: #first is self
                raise Exception("operator filter needs 3 parameters: tuple, result, keep")
        elif self.kind == FOperatorKind.MAP:
            if len(cAst.args.args) != 3: #first is self
                raise Exception("operator map needs 2 parameters: tuple, result")
        elif self.kind == FOperatorKind.FLAT_MAP:
            if len(cAst.args.args) != 3:  # first is self
                raise Exception("operator map needs 2 parameters: tuple, result")
        return python_cpp_transpiling(self.func, self.kind)

opMap = FOperator(FOperatorKind.MAP, map)
print(opMap.transpile())
opFilter = FOperator(FOperatorKind.FILTER, filter)
print(opFilter.transpile())
opFlatMap = FOperator(FOperatorKind.FLAT_MAP, flatmap)
print(opFlatMap.transpile())

@param.param_cref(result_t)
@param.param_const(tuple_t)
def test(param1: result_t, param2: tuple_t):
    pass

print(python_cpp_transpiling(test))
