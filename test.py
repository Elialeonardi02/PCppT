class persona:
    age:int
    weight:float
    def __init__(self,a:int,w:float):
        self.age=a
        self.weight=w
    def get_age(self)->int:
        return self.age
    def set_age(self,a:int)->None:
        self.age=a
def fun()->None:
    p:persona=persona(1,1.1)
    c:int=1
    c=2
    a=3
