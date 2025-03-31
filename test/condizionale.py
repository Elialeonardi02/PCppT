@transpile
def ifelse():
    x = 12
    y = 20
    if x + y > 30:
        x= (x * y)
    else:
        x = (x * y)+30
@transpile
def ifelseifelse():
    x = 45
    if x*3 > 70:
        x = x * 2
    elif 40 <= x <= 70:
        x = x*3
    else:
        x = x*4
@transpile
def ifelseshort():
    x, y = 1
    x = (x *2 + y * 3) if x > y else (y * 2 + x * 3) * 2



