class code():
    def __init__(self):
        self.globalCode=''  #code in the global scope
        self.classes={}     #{name class:{protected:{'attributes':[],'methods':{}}.private: {'attributes':[],'methods':{}},public: {'attributes':[],'methods':{}}}
        self.functions={}   #functions {signature: body

cppCodeObject=code()
cppCodeObject.globalCode+="#include <ostream>\n" #use to generate method for user debugging #FIXME use ore remove?

def param_const(*args, **kwargs):
    def decorator(func):
        func._wireflow_args = args
        func._wireflow_kwargs = kwargs
        return func
    return decorator


def param_ref(*args, **kwargs):
    def decorator(func):
        func._wireflow_args = args
        func._wireflow_kwargs = kwargs
        return func
    return decorator

def param_cref(*args, **kwargs):
    def decorator(func):
        func._wireflow_args = args
        func._wireflow_kwargs = kwargs
        return func
    return decorator