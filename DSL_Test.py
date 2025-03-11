from twisted.logger import FilteringLogObserver

import pcppt
import ast

#windows
#set of windows with correct parameters
window_type = {
    #count
    "counttumbling": {"size"},
    "keyedcounttumbling": {"max_key", "size"},
    "countsliding": {"size", "slide"},
    "keyedcountsliding": {"max_key", "size", "slide"},
    #time

    "timetumbling": {"size", "lateness"},
    "keyedtimetumbling": {"max_key", "size", "lateness"},
    "timesliding": {"size", "slide", "lateness"},
    "keyedtimesliding": {"max_key", "size", "slide", "lateness"}
}
def CountTumbling(size):
    def decorator(cls):
        cls._window_params = {'size': size}
        return cls
    return decorator

@CountTumbling(size=1)
class WindowTest:
    def window(self):
        pass


def KeyedCountTumbling(max_key, size):
    def decorator(cls):
        cls._window_params = {'max_key': max_key, 'size': size}
        return cls
    return decorator

@KeyedCountTumbling(max_key=10, size=2)
class KeyedWindowTest:
    def window(self):
        pass


def CountSliding(size, slide):
    def decorator(cls):
        cls._window_params = {'size': size, 'slide': slide}
        return cls
    return decorator

@CountSliding(size=3, slide=1)
class SlidingWindowTest:
    def window(self):
        pass


def KeyedCountSliding(max_key, size, slide):
    def decorator(cls):
        cls._window_params = {'max_key': max_key, 'size': size, 'slide': slide}
        return cls
    return decorator

@KeyedCountSliding(max_key=5, size=4, slide=2)
class KeyedSlidingWindowTest:
    def window(self):
        pass


def TimeTumbling(size, lateness):
    def decorator(cls):
        cls._window_params = {'size': size, 'lateness': lateness}
        return cls
    return decorator

@TimeTumbling(size=5, lateness=1)
class TimeWindowTest:
    def window(self):
        pass


def KeyedTimeTumbling(max_key, size, lateness):
    def decorator(cls):
        cls._window_params = {'max_key': max_key, 'size': size, 'lateness': lateness}
        return cls
    return decorator

@KeyedTimeTumbling(max_key=8, size=6, lateness=2)
class KeyedTimeWindowTest:
    def window(self):
        pass


def TimeSliding(size, slide, lateness):
    def decorator(cls):
        cls._window_params = {'size': size, 'slide': slide, 'lateness': lateness}
        return cls
    return decorator

@TimeSliding(size=7, slide=3, lateness=2)
class TimeSlidingWindowTest:
    def window(self):
        pass


def KeyedTimeSliding(max_key, size, slide, lateness):
    def decorator(cls):
        cls._window_params = {'max_key': max_key, 'size': size, 'slide': slide, 'lateness': lateness}
        return cls
    return decorator

@KeyedTimeSliding(max_key=12, size=8, slide=4, lateness=3)
class KeyedTimeSlidingWindowTest:
    def window(self):
        pass



"""def window(**kwargs):
    def decorator(cls):
        cls._window_params = kwargs
        return cls
    return decorator


#deduco il tipo di finestra dal nome di un dei metodi della classe e controllo la correttezza.

@window(MAX_KEY=1,SIZE=1)
class window_test:
    def keyedcounttumbling(self):
        pass
    def plus_function(self):
        pass

astWindow=pcppt.get_ast_from_code(window_test)
print(ast.dump(astWindow, indent=4))

params_window_check={} #correct parameter of the windows in the class
for window_type_name in astWindow.body[0].body: #explore name of methods in the class
    if window_type_name.name in window_type:    #the method name is the same name of a window
        if params_window_check !={}:    #if already find another window method, stop
            raise Exception("Duplicate window code")
        params_window_check=window_type[window_type_name.name]  #copy set of corret parameters
params_window={}    #contais the parameter of windows with is value
for decorator in astWindow.body[0].decorator_list: #explore decorator_list
    if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name) and decorator.func.id=='window': #analyze only the decorator "window"
        for param_window in decorator.keywords: #access arg and value of the parameters in the decorator
            param=param_window.arg.lower()
            if param not in params_window_check or param in params_window: #the parameter is not corret or is already declared
                raise Exception(f"Incorrect parameter: {param}")
            params_window[param]=param_window.value.value
            params_window_check.remove(param)



#Deduco il tipo di finestra dai parametri contenuti nel decorator window, all'interno della classe almeno una funzione "window" che contiene il codice di una finestra
'''
@window(SIZE=1)
class window_test:
    def window(self):
        pass
"""
#-------------------------------------------------------------------------
#Operatori


class shipper_t:
    def send(self, tuple):
        pass

    def send_eos(self):
        pass

from DSL import operators

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


@operators.FOperator()
class filterOperator:
    def __call__(self, inn:tuple_t, out:result_t,flag:bool):
        pass
    def __other_method(self):
        pass

pcppt.python_cpp_transpiling(tuple_t)
pcppt.python_cpp_transpiling(result_t)

operators.operator_declaration(filterOperator)


@operators.FOperator()
class mapOperator:
    def __call__(self, inn:tuple_t, out:result_t):
        pass
    def __other_method(self):
        pass

operators.operator_declaration(mapOperator)
'''
@operators.FOperator(name='filter', kind='FILTER', gather_policy='LB', dispatch_policy='LB', compute_function='filter_fun')
class FilterOperator:
    def __call__(self, p1: tuple_t, p2: result_t, keep: bool):
        pass

@operators.FOperator(name='flatmap', kind='FLATMAP', gather_policy='LB', dispatch_policy='LB', compute_function='flatmap_fun')
class FlatMapOperator:
    def __call__(self, tuple: tuple_t, shipper: shipper_t):
        pass

'''
