from enum import Enum
from pcppt import python_cpp_transpiling
class FOperatorKind(Enum):
    NONE = 1
    FILTER = 3 #OK
    MAP = 4 #OK
    FLAT_MAP = 5
uint32=int
float32=float

class tuple_t:
    key : uint32  # maybe `uint` is better, but it is less C++ like
    value : float32     # or simply `float`

    # if not defined, the C++ default constructor is used
    def __init__(self):
        self.key = 0
        self.value = 0.0

    def __init__(self, key : uint32, value : float32):
        self.key = key
        self.value = value

class result_t:
    sum : float32    # or simply `float`
    count : uint32     # maybe `unsigned int` is better, but it is less C++ like
    # if not defined, the C++ default constructor is used
    def __init__(self):
        self.sum = 0.0
        self.count = 0

    # `float32` can be deduced from the context?
    def mean(self, a:[int,10]):
        def a(self):
            a = 1
            bac=[1,2,3,4]
            return a
        self.result=self.sum+self.count
        return self.sum / self.count

# map
class map:
    def __call__(tuple: tuple_t, result: result_t):
        pass

print(python_cpp_transpiling(tuple_t))
print(python_cpp_transpiling(result_t))
print(python_cpp_transpiling(map,FOperatorKind.MAP ))
# struct map
# {
#     void operator()(const tuple_t & tuple, result_t & result)
#     {
#     }
# };

# filter
class filter:
    def __call__(tuple: tuple_t, result: result_t, keep: bool):
        pass

# struct filter
# {
#     void operator()(const tuple_t & tuple, result_t & result, bool & keep)
#     {
#     }
# };
print(python_cpp_transpiling(filter,FOperatorKind.FILTER ))

class shipper_t:
    def send(self,tuple):
        pass

    def send_eos(self):
        pass

# flatmap
class flatmap:
    def __call__(tuple: tuple_t, shipper: shipper_t):
        pass


# struct flatmap
# {
#     template <typename T>
#     void operator()(const tuple_t & tuple, shipper_t<T> & shipper)
#     {
#     }
# };
print(python_cpp_transpiling(shipper_t))
print(python_cpp_transpiling(flatmap,FOperatorKind.FLAT_MAP ))


def wireflow_const(param):
    def decorator(func):
        func._wireflow_param = param
        return func
    return decorator

def wireflow_ref(param):
    def decorator(func):
        func._wireflow_param = param
        return func
    return decorator



@wireflow_const(result_t)
@wireflow_ref(int)
def test(param1:result_t,param2:int):
    pass

def testa(param1:result_t,param2:int):
    pass
print(python_cpp_transpiling(test))

