class ParameterType(Exception):
    def __init__(self, parameter):
        super().__init__(f"Parameter '{parameter}' must have a specified type.")

class SignatureCallNotValid(Exception):
    def __init__(self, className):
        super().__init__(f"Invalid __call__ signature in class '{className}'.")

class CallMethodException(Exception):
    def __init__(self, className):
        super().__init__(f"There can be only one __call__ method in class '{className}'.")

