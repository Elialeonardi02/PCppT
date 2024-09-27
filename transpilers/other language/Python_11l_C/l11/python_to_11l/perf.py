import sys, time, os, tokenizer, parse

s = open(r"C:\!!BITBUCKET\11l-lang\_11l_to_cpp\tests\python_to_cpp\_11l_to_cpp\tokenizer.py", encoding='utf-8-sig').read()
tokens = tokenizer.tokenize(s)

r = 1e10

for i in range(10):
    start = time.time()
    parse.parse_and_to_str(tokens, s, 'ff')
    r = min(r, time.time() - start)

print(r)