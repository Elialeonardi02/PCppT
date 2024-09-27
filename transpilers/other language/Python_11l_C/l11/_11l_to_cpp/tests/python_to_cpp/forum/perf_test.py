import time, os, hashlib, sys

python_time = 0

# for tool, tool_name in (('python pqmarkup_result_list.py', 'CPython [list]'),
#                         ('python pqmarkup_result_str.py',  'CPython [str]'),
#                         ('pqmarkup_result_list.exe',       'exe [list]'),
#                         ('pqmarkup_result_str.exe',        'exe [str]')):
for tool, tool_name in (('python 1.exs2sfz.py',       'CPython'),
                        ('1.exs2sfz.exe',             'exe'),
                        #(R'C:\Users\DNS\Downloads\pypy3.7-v7.3.2-win32\pypy3.exe 1.exs2sfz.py', 'PyPy'),
                        ('python cython.py',          'Cython')
                        ):

    for i in range(10):
        if os.path.isfile('output' + str(i)):
            os.remove('output' + str(i))

    ss = float('inf')
    for i in range(10):
        s = time.perf_counter()
        os.system(tool + ' NaturalKit.exs output' + str(i))
        #os.system(tool + ' BLUTHNER.exs output' + str(i))
        ss = min(ss, time.perf_counter() - s)

    if python_time == 0:
        python_time = ss

    print(tool_name + ': ' + str(ss) + ' (' + str(round(python_time/ss, 1)) + 'x)')
