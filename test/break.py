@transpile
def breakCycle():
    limit = 50
    total = 0
    sum=0
    for i in range(1, limit):
        sum +=i
        if sum > 100:
            break
        total += i * 2





