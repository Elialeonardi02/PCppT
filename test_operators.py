from enum import Enum
from pcppt import python_cpp_transpiling
class FOperatorKind(Enum):
    NONE = 1
    FILTER = 3 #OK
    MAP = 4 #OK
    FLAT_MAP = 5 # OK

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


def wireflow_const(*args, **kwargs):
    def decorator(func):
        func._wireflow_args = args
        func._wireflow_kwargs = kwargs
        return func
    return decorator


def wireflow_ref(*args, **kwargs):
    def decorator(func):
        func._wireflow_args = args
        func._wireflow_kwargs = kwargs
        return func
    return decorator




@wireflow_const(result_t)
@wireflow_ref(result_t, tuple_t)
def test(param1:result_t,param2:tuple_t):
    pass

print(python_cpp_transpiling(test))

