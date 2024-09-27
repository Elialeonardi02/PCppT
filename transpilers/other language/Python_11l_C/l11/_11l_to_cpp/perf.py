import sys, time, os, tokenizer

s = open(r"C:\!!BITBUCKET\11l-lang\_11l_to_cpp\tests\python_to_cpp\python_to_11l\tokenizer.11l", encoding='utf8').read()

r = 1e10

for i in range(10):
    start = time.time()
    tokenizer.tokenize(s)
    r = min(r, time.time() - start)

print(r)