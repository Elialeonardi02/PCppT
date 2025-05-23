@transpile
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

tuple_key_extractor = lambda t: t+1

@transpile
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

    # this is optional and it can be done after more important things are done
@transpile
class window_functor:
    i1:int
    c1:float32
    def __call__(self, tuple : tuple_t, result : result_t):
        result.sum += tuple.value
        result.count = result.count + 1
    def test(self,tuple:tuple_t):
        return tuple
@wireflow
def testl()->int:
    def a():
        a=1
        return a
    z=lambda x:x+1
    a=1
    t=tuple_key_extractor(1)
    return 1
@wireflow
def fun(a:int):
    b=0
    test=testl()
    return b
