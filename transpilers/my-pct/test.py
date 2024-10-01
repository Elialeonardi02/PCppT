#counts even numbers between two integers
def fun(a:int, b:int)->int:
    c:int=0
    #pragma HLS LATENCY min=1 max=2
    for i in range(a,b):
        if i%2==0:
            c+=1
    return c
