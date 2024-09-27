import math

#print([4] == [4])

#def testf():
k = 1000000
n = k * 17
primes = [True] * n
primes[0] = primes[1] = False

i = 2
ii = int(math.sqrt(n)) + 1
while i < ii:
    if not primes[i]:
        i += 1
        continue
    j = i * i
    while j < n:
        primes[j] = False
        j += i
    i += 1

i = 0
while i < n:
    if primes[i]:
        if k == 1:
            print(i)
            break
        k -= 1
    i += 1

#testf()