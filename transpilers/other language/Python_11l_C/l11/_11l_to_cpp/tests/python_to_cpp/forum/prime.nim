from math import sqrt
 
var k = 1000000
var limit = 1000000 * 17

let sqrtLimit = int(sqrt(float64(limit)))
var composites = newSeq[bool](limit + 1)
for n in 2 .. sqrtLimit: # cull to square root of limit
  if not composites[n]: # if prime -> cull its composites
    for c in countup(n *% n, limit, n): # start at ``n`` squared
      composites[c] = true

for i in 2 .. limit: # separate iteration over results
  if not composites[i]:
    if k == 1:
       echo i
       break
    k -= 1
