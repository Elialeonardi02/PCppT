@transpile
class testC:
    c:int
    def rint(self):
        return 1
    def __init__(self):
        self.c=0
        self.a=self.c
        c=self.rint()
@transpile
def testa():
    return 1

@transpile
def testF(t:testC):
    a=t
    t.c=1
    z=t.rint()
    t.rint()
    testa()







