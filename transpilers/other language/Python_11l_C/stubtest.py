import l11.python_to_11l.tokenizer as tokenizer
source=open('test.py', encoding = 'utf-8-sig').read()
a=tokenizer.tokenize(source)
#a=tokenizer.parse.parse_and_to_str(, source, 'test.py')
print(a)
for i in range(len(a)):
   print(tokenizer.Token.value(a[i],source))
   if a[i].category==tokenizer.Token.Category.COMMENT:
      print(a[i].Category)