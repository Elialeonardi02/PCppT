import math

#print([4] == [4])

#def testf():
k = 1000000
n = k * 17
primes = [True] * n
primes[0] = primes[1] = False

for i in range(2, int(math.sqrt(n)) + 1):
    if not primes[i]:
        continue
    for j in range(i * i, n, i):
        primes[j] = False

for i in range(n):
    if primes[i]:
        if k == 1:
            print(i)
            break
        k -= 1

#testf()