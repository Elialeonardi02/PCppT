


x = lambda t: t+1

@transpile
def test():
    #Assegnazione variabile con type hits
    a1: int
    b1: float64 = 0.0

    #Assegnazione Array con type hits
    #a:[int] #istruzione errata
    b:[float]=[1,2,3,4]
     #a[1]=10

    #Assegnazione Array con type hits e dimensione
    c:[int,2]=[1,2]
    d:[int,10]=[9,8]
    d[4]=5
    #e:[int,3]=[1,2,3,4] #istruzione errata
    f:[int,4]
    f[1]=4

    #assegnazioni, accesso, assegnazioni combinate
    g=1
    h=0.2
    i=g+h
    l=[1,g+2+h,h]
    l[1]+=1
    i+=0.2

    #lambda function
    x1 = lambda t: t + 1

    #destrutturazione
    c1,c2,c3,c4=lambda t: t + 1
    d1,d2,d3=[1,2,0.4+1]


