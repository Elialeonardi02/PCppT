class UnsupportedCommandError(Exception):   #exception for unsupported command
    def __init__(self, command):
        super().__init__(f"Unsupported command: {command}")

class RecursiveFunctionError(Exception):    #exception for recursive functions
    def __init__(self, function_name):
        super().__init__(f"Recursive function not supported: {function_name}")

class AlreadyDefinedError(Exception):   #exception for class, function already defined
    def __init__(self, elem):
        super().__init__(f"{elem} is already defined")

class NotCallableError(Exception):   #exception for function uncullable
    def __init__(self, elem):
        super().__init__(f"{elem} is not callable")

class TypeNotExistError(Exception):   #exception for type doesn't exist
    def __init__(self, elem):
        super().__init__(f"{elem} not exist")