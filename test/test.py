@wireflow
class testC:
    c:int
    def rint(self):
        return 1
    def __init__(self):
        self.c=0
        self.a=self.c
        c=self.rint()
@wireflow
class testB:
    def __init__(self, a:testC):
        self.b=a

@wireflow
def testa():
    return 1






