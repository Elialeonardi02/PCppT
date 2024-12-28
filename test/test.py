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
def testa():
    return 1

@wireflow
def testF(t:testC):
    a=t
    t.c=1
    z=t.rint()+0.0000000001
    t.rint()
    testa()



