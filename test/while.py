@transpile
def nWhile():
    limit = 15
    total = 0
    i = 1
    while i <= limit:
        total += i * 3
        i += 2
@transpile
def doWhile():
    product = 1
    i = 1
    limit = 10
    while True:
        product *= i
        i += 2
        if i > limit:
            break




