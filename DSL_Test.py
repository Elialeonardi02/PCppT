
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

def window(**kwargs):
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
        
def CountTumbling(**kwargs):
    def decorator(cls):
        cls._window_params = kwargs  # Salviamo i parametri nella classe
        return cls
    return decorator

#Definizione di un decorator differente per ogni tipo di finestra
@CountTumbling(SIZE=1)
class WindowTest:
    def window(self):
        pass
'''
#-------------------------------------------------------------------------
#Operatori
