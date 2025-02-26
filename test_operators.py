import inspect
from enum import Enum

import pcppt
import ast

from pcppt.main import get_ast_from_code


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
    def extra_method(self):
        pass

#print(pcppt.python_cpp_transpiling(tuple_t))
#print(pcppt.python_cpp_transpiling(result_t))

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
        cAst = ast.parse(inspect.getsource(self.func)).body[0]
        for eAst in cAst.body:
            if isinstance(eAst, ast.FunctionDef) and eAst.name=='__call__':
                cAst=cAst.body[0]
        if self.kind == FOperatorKind.FILTER:
            if len(cAst.args.args) != 4: #first is self
                raise Exception("operator filter needs 3 parameters: tuple, result, keep")
        elif self.kind == FOperatorKind.MAP:
            if len(cAst.args.args) != 3: #first is self
                raise Exception("operator map needs 2 parameters: tuple, result")
        elif self.kind == FOperatorKind.FLAT_MAP:
            if len(cAst.args.args) != 3:  # first is self
                raise Exception("operator map needs 2 parameters: tuple, result")
        return pcppt.python_cpp_transpiling(self.func, self.kind)

opMap = FOperator(FOperatorKind.MAP, map)
#print(opMap.transpile())
opFilter = FOperator(FOperatorKind.FILTER, filter)
#print(opFilter.transpile())
opFlatMap = FOperator(FOperatorKind.FLAT_MAP, flatmap)
#print(opFlatMap.transpile())



@pcppt.param_cref(result_t)
@pcppt.param_const(tuple_t)
def test(param1: result_t, param2: tuple_t):
    pass

def testAst():
    return 1

Lambda = lambda x: x + 1
astLambda=get_ast_from_code(Lambda)
testAst=get_ast_from_code(testAst)

print(pcppt.ast_cpp_transpiling(testAst))
print(pcppt.ast_cpp_transpiling(astLambda))
