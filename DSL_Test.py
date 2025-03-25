from typing import Generic, TypeVar


import pcppt

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

pcppt.python_cpp_transpiling(tuple_t)
pcppt.python_cpp_transpiling(result_t)
R = TypeVar("R")
class Shipper(Generic[R]):
    def send(self, out):
        pass
pcppt.python_cpp_transpiling(Shipper)
'''
@operators.FOperator(gather_policy='LB')
class filterOperator:
    def __call__(self, inn:tuple_t, out:result_t,flag:bool):
        pass
    def __other_method(self):
        pass



#operators.operator_declaration(filterOperator)
'''

@operators.FOperator()
class mapOperator:
    a:int
    def __call__(self, input:tuple_t, output:result_t):
        self.a =1
    def __other_method(self):
        pass

print(operators.operator_declaration(mapOperator))

@operators.FOperator(gather_policy=operators.FGatherPolicy.RR)
class flatmap:
    def __call__(self, inn, shipper:Shipper[tuple_t]):
        pass
    def __other_method(self):
        pass
print(operators.operator_declaration(flatmap))


@operators.FOperator()
class flatmapp:
    def __call__(self, inn, shipper:Shipper[tuple_t]):
        pass
    def __other_method(self):
        pass
print(operators.operator_declaration(flatmapp))

#Finestre
class stream_in_t:
    def __init__(self):
        # Inizializzazione degli attributi o altro codice necessario
        pass

class stream_out_t:
    def __init__(self):
        # Inizializzazione degli attributi o altro codice necessario
        pass

class key_extractor_t:
    def __init__(self):
        # Inizializzazione degli attributi o altro codice necessario
        pass
pcppt.python_cpp_transpiling(stream_in_t)
pcppt.python_cpp_transpiling(stream_out_t)
pcppt.python_cpp_transpiling(key_extractor_t)
'''
@windows.FWindowCount(size=6)
class CountTumbling:
    def window(self, inn: stream_in_t, out: result_t):
        pass

print(windows.windows_declaration(CountTumbling))

@windows.FWindowCount(max_key=8, size=6)
class KeyedCountTumbling:
    def window(self, inn: stream_in_t, out: result_t, key: key_extractor_t):
        pass

print(windows.windows_declaration(KeyedCountTumbling))

@windows.FWindowCount(size=6, slide=2)
class CountSliding:
    def window(self, inn: stream_in_t, out: result_t):
        pass

print(windows.windows_declaration(CountSliding))

@windows.FWindowCount(max_key=8, size=6, slide=2)
class KeyedCountSliding:
    def window(self, inn: stream_in_t, out: result_t, key: key_extractor_t):
        pass

print(windows.windows_declaration(KeyedCountSliding))

@windows.FWindowTime(size=6, lateness=3)
class TimeTumbling:
    def window(self, inn: stream_in_t, out: result_t):
        pass

print(windows.windows_declaration(TimeTumbling))

@windows.FWindowTime(max_key=8, size=6, lateness=3)
class KeyedTimeTumbling:
    def window(self, inn: stream_in_t, out: result_t, key: key_extractor_t):
        pass

print(windows.windows_declaration(KeyedTimeTumbling))

@windows.FWindowTime(size=6, slide=2, lateness=3)
class TimeSliding:
    def window(self, inn: stream_in_t, out: result_t):
        pass

print(windows.windows_declaration(TimeSliding))
'''
@windows.FWindowTime(max_key=8, size=6, slide=2, lateness=3)
class KeyedTimeSliding:
    def window(self, inn: stream_in_t, out: result_t, key: key_extractor_t):
        pass

print(windows.windows_declaration(KeyedTimeSliding))
