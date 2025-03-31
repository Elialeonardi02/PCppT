@transpile
class personclass:
    age:int
    __height:float
    __weight:float=10
    def __init__(self, age:int, height:float):
        self.__height = height
        self.age = age



class personstruct:
    age:int
    height:float

    @transpile
    def __init__(self, age:int, height:float, person:personclass):
        self.age = age
        self.height = height
        self.person = person
    def reset(self,person:personclass):
        self.age = 0
        self.height = 0.0
        self.personC = person
@transpile
class window_functor:
    def __call__(self,personS:personclass):
        personS.age+=1