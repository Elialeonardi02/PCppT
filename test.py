int64=int
class person:
    age:int
    weight:float
    def __init__(self,a:int,w:float):
        self.age=a
        self.weight=w
    def get_age(self)->int:
        return self.age
    def set_age(self,a:int)->None:
        self.age=a

def create_person(a:int,w:int)->None:
    p:person=person(a,w)
    a1=2
    w1=4.6
    p1: person = person(a1, w1)
    p1.get_age()
    p1.set_age(10)
