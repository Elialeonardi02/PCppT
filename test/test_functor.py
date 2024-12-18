class tuple_t:
    key : unsigned int  # maybe `uint` is better, but it is less C++ like
    value : float32     # or simply `float`

    # if not defined, the C++ default constructor is used
    def __init__(self):
        self.key = 0
        self.value = 0.0

    def __init__(self, key : unsigned int, value : float32):
        self.key = key
        self.value = value

    # this is optional and it can be done after more important things are done
    def __str__(self):
        return f"(key: {self.key}, value: {self.value})"


tuple_key_extractor = lambda t: t.key


class result_t:
    sum : float32    # or simply `float`
    count : uint     # maybe `unsigned int` is better, but it is less C++ like

    # if not defined, the C++ default constructor is used
    def __init__(self):
        self.sum = 0.0
        self.count = 0

    # `float32` can be deduced from the context?
    def mean(self) -> float32:
        return self.sum / self.count

    # this is optional and it can be done after more important things are done
    def __str__(self):
        return f"(sum: {self.sum}, count: {self.count})"


class window_functor:
    def __call__(self, tuple : tuple_t, result : result_t):
        result.sum += tuple.value
        result.count = result.count + 1
