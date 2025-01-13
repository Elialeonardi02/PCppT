@wireflow
class personclass:
    age:int
    __height:float
    __weight:float=10
    def __init__(self, age:int, height:float):
        self.__height = height
        self.age = age


z=lambda x:x+1
class personstruct:
    age:int
    height:float

    @wireflow
    def __init__(self, age:int, height:float, person:personclass):
        self.age = age
        self.height = height
        self.person = person
        z(1)
    def reset(self,person:personclass):
        self.age = 0
        self.height = 0.0
        self.personC = person
@wireflow
class window_functor:
    def __call__(self,personS:personclass):
        personS.age+=1
@wireflow
def arrayParameter(b:int=1, c:float=2.23):
    pass




