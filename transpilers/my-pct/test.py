#counts even numbers between two integers
def fun(a:int, b:int)->int:
    c:int=0
    #pragma HLS PIPELINE II=1
    for i in range(a,b):
        if i%2==0:
            c+=1
    return c
