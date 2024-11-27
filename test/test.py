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

tuple_key_extractor = lambda t: t.key

class result_t:
    sum : float32    # or simply `float`
    count : uint32     # maybe `unsigned int` is better, but it is less C++ like
    # if not defined, the C++ default constructor is used
    def __init__(self):
        self.sum = 0.0
        self.count = 0

    # `float32` can be deduced from the context?
    @wireflow
    def mean(self):
        self.result=self.sum/self.count
        return self.sum / self.count

    # this is optional and it can be done after more important things are done

class window_functor:
    i1:int
    c1:float32
    def __call__(self, tuple : tuple_t, result : result_t):
        result.sum += tuple.value
        result.count = result.count + 1

def fun(a:int):
    b=0
    test=testl()
    return b

def testl()->int:
    return 1