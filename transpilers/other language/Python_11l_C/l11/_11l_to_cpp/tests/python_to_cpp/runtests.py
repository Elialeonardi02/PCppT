import os, tempfile, sys, pqmarkup

test_id = 0
failed_tests = 0
kdiff_showed = False
def TEST(str1, str2, ohd = False, habr_html = False):
    global test_id, failed_tests, kdiff_showed
    test_id += 1
    print("Test " + str(test_id) + " ...", end = '')
    str1 = pqmarkup.to_html(str1, ohd = ohd, habr_html = habr_html)
    if str1 != str2:
        str1 = str(str1)
        str2 = str(str2)
        print("FAILED!")
        if not kdiff_showed:
            for envvar in ['ProgramFiles', 'ProgramFiles(x86)', 'ProgramW6432']:
                os.environ["PATH"] += os.pathsep + os.getenv(envvar, '') + r'\KDiff3'
            command = 'kdiff3'
            for file in [('wrong', str1), ('right', str2)]: # можно наоборот — [('right', str2), ('wrong', str1)], только цвет нужно оставить как при [('wrong', str1), ('right', str2)]
                full_fname = os.path.join(tempfile.gettempdir(), file[0])
                command += ' "' + full_fname + '"'
                open(full_fname, 'w', encoding = 'utf-8-sig', newline = "\n").write(file[1])
            os.system(command)
            kdiff_showed = True
        failed_tests += 1
    else:
        print("passed")

TEST("*‘bold’",          "<b>bold</b>")
TEST("_‘underlined’",    "<u>underlined</u>")
TEST("-‘strikethrough’", "<s>strikethrough</s>")
TEST("~‘italics’",       "<i>italics</i>")
TEST("H‘header’\n" +
     "H(1)‘header’",     "<h3>header</h3>\n"
                       + "<h2>header</h2>")
TEST("H(+1)‘header’",    "<h2>header</h2>")
TEST("H(-1)‘header’",    "<h4>header</h4>")
TEST("[http://address]", '<a href="http://address">http://address</a>')
TEST("link[http://address]", '<a href="http://address">link</a>')
TEST("link[https://address]", '<a href="https://address">link</a>')
TEST("‘multiword link’[http://address]", '<a href="http://address">multiword link</a>')
TEST("link[https://address ‘title &text[[[comment]]]’]", '<a href="https://address" title="title &amp;text">link</a>')
TEST("link[https://address title [.&.] text[[[comment]]]]", '<a href="https://address" title="title [.&amp;.] text">link</a>')
TEST('‘[[[Scoping rules/]]]Code blocks’[./code-blocks]', '<a href="./code-blocks" target="_self"><!--[[[Scoping rules/]]]-->Code blocks</a>')
TEST(R'‘Versioning with 100%/versions_threshold/\‘2’ overhead’[./versioning.pq]', '<a href="./versioning.pq" target="_self">Versioning with 100%/versions_threshold<sup>2</sup> overhead</a>')
TEST('‘compares files based on which ~‘lines’ have changed’[http://www.devuxer.com/2014/02/15/why-the-mercurial-zipdoc-extension-fails-for-excel-files/]', '<a href="http://www.devuxer.com/2014/02/15/why-the-mercurial-zipdoc-extension-fails-for-excel-files/">compares files based on which <i>lines</i> have changed</a>')
TEST("text[‘title text’]", '<abbr title="title text">text</abbr>')
TEST("[text][‘title text’]", '[text]<abbr title="title text"></abbr>') # чтобы получить '<abbr title="title text">[text]</abbr>' пишите так: ‘[text]’[‘title text’]
TEST('Примечание 1: только режимы ‘r’ и ‘w’ поддерживаются на данный момент [‘мои мысли на тему режимов открытия файлов’[./File]]', 'Примечание 1: только режимы ‘r’ и ‘w’ поддерживаются на данный момент [<a href="./File" target="_self">мои мысли на тему режимов открытия файлов</a>]')
TEST('Примечание 1: только режимы ‘r’ и ‘w’ поддерживаются на данный момент [[‘’]‘мои мысли на тему режимов открытия файлов’[./File]]', 'Примечание 1: только режимы ‘r’ и ‘w’ поддерживаются на данный момент [<abbr title=""></abbr><a href="./File" target="_self">мои мысли на тему режимов открытия файлов</a>]') # maybe this test is unnecessary
TEST('[[‘’][[[Справка/]]]Документация по методам доступна на данный момент только ‘на английском’[./../../built-in-types].]', '[<abbr title=""></abbr><!--[[[Справка/]]]-->Документация по методам доступна на данный момент только <a href="./../../built-in-types" target="_self">на английском</a>.]')
TEST('[‘мои мысли на тему режимов открытия файлов’[./File]]', '[<a href="./File" target="_self">мои мысли на тему режимов открытия файлов</a>]')
#TEST("‘`‘` и `’`’[‘`‘` и `’`’]", '<abbr title="`‘` и `’`"><code>‘</code> и <code>’</code></abbr>') # Почему оставил закомментированным: должна возникнуть необходимость использовать такое в реальном тексте прежде чем добавлять какой-либо функционал в код ‘на всякий случай’/‘на будущее’.
TEST("P‘http://image-url’", '<img src="http://image-url" />')
TEST("P‘http://image-url’[http://address]", '<a href="http://address"><img src="http://image-url" /></a>')
TEST("P‘http://image-url’[‘title text[[[comment]]]’]", '<img src="http://image-url" title="title text" />')
TEST("P‘http://image-url’[http://address ‘title text’]", '<a href="http://address" title="title text"><img src="http://image-url" /></a>')
TEST("P‘http://image-url’[http://address title text]", '<a href="http://address" title="title text"><img src="http://image-url" /></a>')
TEST("С(000)‘black text’", '<span style="color: #000000">black text</span>')
TEST("С(800)‘red text’", '<span style="color: #FF0000">red text</span>')
TEST("С(4)‘gray text’", '<span style="color: #808080">gray text</span>')
TEST("С(0000)‘transparent text’", '<span style="color: #00000000">transparent text</span>')
TEST('С(#фФ0000)‘red text’', '<span style="color: #fF0000">red text</span>')
TEST('C(#fF0000)‘red text’', '<span style="color: #fF0000">red text</span>')
TEST('C(-800)‘text on a red background’', '<span style="background-color: #FF0000">text on a red background</span>')
TEST('C(888-000)‘white text on black background’', '<span style="color: #FFFFFF; background-color: #000000">white text on black background</span>')
TEST("link[http://address][1] ‘the same link’[1]", '<a href="http://address">link</a>[1] ‘the same link’[1]')
TEST("link[http://address][-1] ‘the same link’[-1]", '<a href="http://address">link</a> <a href="http://address">the same link</a>')
TEST("[[[comment[[[[sensitive information]]]]]]]", "<!--[[[comment]]]-->")
TEST("[[[com]ment]]", "<!--[[[com]ment]]-->")
TEST("[[[[comment]]]]", "")
TEST("[[[[[com]m]e]n]t]", "")
TEST("\n A", "<br />\n&emsp;A")
TEST(" A", "&emsp;A")
TEST("---", "<hr />\n")
TEST("---\n", "<hr />\n")
TEST("a\n---\n", "a<br />\n<hr />\n")
TEST("a\n---\n\n", "a<br />\n<hr />\n<br />\n") # check for wrong code: `writepos = i = j + 1` (should be `i = j`)
TEST("a\n---=\n", "a<br />\n---=<br />\n")
TEST("a\n----\n", "a<br />\n<hr />\n")
TEST("a0‘*‘<non-bold>’’", "a*‘&lt;non-bold>’")
TEST("""a
‘b[[[comment]]]’{
c
‘d’{e}
}""", """a<br />
<spoiler title="b">
c<br />
<spoiler title="d">
e</spoiler>
</spoiler>
""", habr_html = True)
TEST("""‘title’{
te
}
xt""", """<span class="spoiler_title" onclick="return spoiler2(this, event)">title<br /></span><div class="spoiler_text" style="display: none">
te<br />
</div>
xt""", ohd = True) # пока что фиксирую такой некрасивый HTML-код, так как например этот HTML-код работает некорректно: '<span class="spoiler_title" onclick="return spoiler2(this, event)">title</span><div class="spoiler_text" style="display:none">te<br />\n</div><br />\nxt'
                   #                                                                                      и этот тоже: '<span class="spoiler_title" onclick="return spoiler2(this, event)">title</span><div class="spoiler_text" style="display:none">te</div><br />\nxt'
                   #                                                                                           и этот: '<span class="spoiler_title" onclick="return spoiler2(this, event)">title</span><div class="spoiler_text" style="display:none">te</div>xt'
TEST("""#(JavaScript)‘
    { "keys": ["‘"], "command": "insert_pq" }, //also insert balancing ’
’""", """<source lang="JavaScript">
    { "keys": ["‘"], "command": "insert_pq" }, //also insert balancing ’
</source>""", habr_html = True)
TEST("""‘Code’{
#(Python)‘
import hashlib
’
}

Some text.""",
"""<spoiler title="Code">
<source lang="Python">
import hashlib
</source>
</spoiler>
<br />
Some text.""", habr_html = True)
TEST("[[[‘]]]test```’```test", "<!--[[[‘]]]-->test<code>’</code>test", habr_html = True)
TEST("[[[‘]]]`Don’t`", "<!--[[[‘]]]--><code>Don’t</code>", habr_html = True)
TEST("'‘<Don‘t! Don‘t! Don‘t!>’’’’''''", "<Don‘t! Don‘t! Don‘t!>")
TEST("`'‘<div>&lt;</div>’'`", "<code>'‘&lt;div>&amp;lt;&lt;/div>’'</code>", habr_html = True)
TEST("''‘‘’‘’’''", "’‘")
TEST("''''‘‘‘‘Don’t! Don’t! Don’t!’'", "Don’t! Don’t! Don’t!")
TEST('модуль #(11l)‘fs’', 'модуль <code>fs</code>', habr_html = True)
TEST('''\
Т‘
‘‘Python’ ‘#(Python)‘rn = {'I': 1, 'V': 5, 'X': 10, 'L': 50, ...}’’’
’''', '''<table>
<tr><td>Python</td><td><source lang="Python">rn = {'I': 1, 'V': 5, 'X': 10, 'L': 50, ...}</source></td></tr>
</table>
''', habr_html = True)
TEST('''\
Т‘
‘‘Python’ ‘#(Python)‘rn = {'I': 1, 'V': 5, 'X': 10, 'L': 50, ...}’ — ...’’
’''', '''<table>
<tr><td>Python</td><td><code>rn = {'I': 1, 'V': 5, 'X': 10, 'L': 50, ...}</code> — ...</td></tr>
</table>
''', habr_html = True)
#TEST(open("tests/test1.pq", encoding="utf-8").read(), open("tests/test1.pq.to_habr_html", encoding="utf-8").read(), habr_html = True) # для проверки безопасности рефакторинга нужен был какой-либо обширный тестовый текст на пк-разметке [-TODO подобрать такой текст, который не стыдно закоммитить :)(:-]
TEST("""<<‘выравнивание по левому краю’
>>‘выравнивание по правому краю’
><‘выравнивание по центру’
<>‘выравнивание по ширине’""", """\
<div align="left">выравнивание по левому краю</div>
<div align="right">выравнивание по правому краю</div>
<div align="center">выравнивание по центру</div>
<div align="justify">выравнивание по ширине</div>
""")
TEST("‘’<<", "‘’&lt;&lt;") # was [before this commit]: ‘’<div align="left"></div>&lt;&lt;
TEST(R"/\‘надстрочный\superscript’\/‘подстрочный\subscript’", R"<sup>надстрочный\superscript</sup><sub>подстрочный\subscript</sub>")
TEST("> Quote\n" +
     ">‘Quote2’\n", "<blockquote>Quote</blockquote>\n"
                  + "<blockquote>Quote2</blockquote>\n")
TEST(">[http://address]:‘Quoted text.’",                '<blockquote><a href="http://address"><i>http://address</i></a>:<br />\nQuoted text.</blockquote>')
TEST(">[http://another-address][-1]:‘Quoted text.’\n" +
     ">[-1]:‘Another quoted text.’",                    '<blockquote><a href="http://another-address">[1]<i>http://another-address</i></a>:<br />\nQuoted text.</blockquote>\n'
                                                      + '<blockquote><a href="http://another-address">[1]<i>http://another-address</i></a>:<br />\nAnother quoted text.</blockquote>')
TEST(">‘Author's name’[http://address]:‘Quoted text.’", '<blockquote><i><a href="http://address">Author\'s name</a></i>:<br />\nQuoted text.</blockquote>')
TEST(">‘Author's name’[http://address][-1]:‘Quoted text.’\n" +
     ">‘Author's name’[-1]:‘Another quoted text.’",     '<blockquote><i><a href="http://address">Author\'s name</a></i>:<br />\nQuoted text.</blockquote>\n'
                                                      + '<blockquote><i><a href="http://address">Author\'s name</a></i>:<br />\nAnother quoted text.</blockquote>')
TEST(">‘Author's name’:‘Quoted text.’",                 '<blockquote><i>Author\'s name</i>:<br />\nQuoted text.</blockquote>')
TEST("‘Quoted text.’:‘Author's name’<",                 "<blockquote>Quoted text.<br />\n<div align='right'><i>Author's name</i></div></blockquote>")
TEST('>‘Как люди думают. Дмитрий Чернышев. 2015. 304с.’:‘[[[стр.89:]]]...’', "<blockquote><i>Как люди думают. Дмитрий Чернышев. 2015. 304с.</i>:<br />\n<!--[[[стр.89:]]]-->...</blockquote>")
TEST(">‘>‘Автор против nullable-типов?’\nДа. Адрес, указывающий на незаконный участок памяти, сам незаконен.’", '<blockquote><blockquote>Автор против nullable-типов?</blockquote>\nДа. Адрес, указывающий на незаконный участок памяти, сам незаконен.</blockquote>')
TEST(">‘> Автор против nullable-типов?\nДа. Адрес, указывающий на незаконный участок памяти, сам незаконен.’", '<blockquote><blockquote>Автор против nullable-типов?</blockquote>\nДа. Адрес, указывающий на незаконный участок памяти, сам незаконен.</blockquote>')
TEST(">‘1. A\n’", "<blockquote><ol>\n<li>A</li>\n</ol>\n</blockquote>")
TEST("!‘1. A\n’", "<div class=\"note\"><ol>\n<li>A</li>\n</ol>\n</div>")
TEST('>[http://ruscomp.24bb.ru/viewtopic.php?id=20]:‘> То есть обычные русские слова уже не являются для вас "общепринятым" языком?\nОбщепринятые – это те, которые я читаю в книгах, в том числе по программированию.’', '<blockquote><a href="http://ruscomp.24bb.ru/viewtopic.php?id=20"><i>http://ruscomp.24bb.ru/viewtopic.php?id=20</i></a>:<br />\n<blockquote>То есть обычные русские слова уже не являются для вас "общепринятым" языком?</blockquote>\nОбщепринятые – это те, которые я читаю в книгах, в том числе по программированию.</blockquote>')
TEST("‘понимание [[[процесса]]] разбора [[[разметки]]] человеком’[‘говоря проще: приходится [[[гораздо]]] меньше думать о том, будет это работать или не будет, а просто пишешь в соответствии с чёткими/простыми/логичными правилами, и всё’]", '<abbr title="говоря проще: приходится  меньше думать о том, будет это работать или не будет, а просто пишешь в соответствии с чёткими/простыми/логичными правилами, и всё">понимание  разбора  человеком</abbr>')
TEST(
""". unordered
. list""",
"""<ul>
<li>unordered</li>
<li>list</li>
</ul>
""")
TEST(
"""1. ordered
2. list""",
"""<ol>
<li>ordered</li>
<li>list</li>
</ol>
""")
TEST(
"""13. disordered
2. list""",
"""<ol start="13">
<li>disordered</li>
<li value="2">list</li>
</ol>
""")
TEST(
"""1. interrupted
. ol
2. list""",
"""<ol>
<li>interrupted</li>
</ol>
<ul>
<li>ol</li>
</ul>
<ol start="2">
<li>list</li>
</ol>
""")
TEST(
""". interrupted
1. ul
. list""",
"""<ul>
<li>interrupted</li>
</ul>
<ol>
<li>ul</li>
</ol>
<ul>
<li>list</li>
</ul>
""")
TEST(
"""1.‘multiline
list element’
2. second""",
"""<ol>
<li>multiline<br />
list element</li>
<li>second</li>
</ol>
""")
TEST(
""".‘multiline
list element’
. second""",
"""<ul>
<li>multiline<br />
list element</li>
<li>second</li>
</ul>
""")
TEST(
"""4.‘А ещё мне коды[/годы] этих символов нравятся...’

Один существенный минус ...""",
"""<ol start="4">
<li>А ещё мне коды<span class="sq"><span class="sq_brackets">[</span>/годы<span class="sq_brackets">]</span></span> этих символов нравятся...</li>
</ol>
<br />
Один существенный минус ...""", ohd = True)
TEST(
"""4. ‘А ещё мне коды[/годы] этих символов нравятся...’{...}

Один существенный минус ...""",
"""<ol start="4">
<li><span class="spoiler_title" onclick="return spoiler2(this, event)">А ещё мне коды[/годы] этих символов нравятся...<br /></span><div class="spoiler_text" style="display: none">
...</div>
</li>
</ol>
<br />
Один существенный минус ...""", ohd = True)

TEST('''>‘. a
. b’
c
d''', '''<blockquote><ul>
<li>a</li>
<li>b</li>
</ul>
</blockquote>
c<br />
d''')

TEST('''>[https://habr.com/ru/articles/780372/comments/#comment_26271586]:‘
Джоэл Спольски в своё время подробно расписал, почему так получается:
> Чтобы создать хороший продукт, требуется 10 лет разработки, но когда он готов - он ~‘готов’. После этого уже никто не может придумать ни единой фичи, которая была бы реально нужна.’
Поддерживаю.''', '''<blockquote><a href="https://habr.com/ru/articles/780372/comments/#comment_26271586"><i>https://habr.com/ru/articles/780372/comments/...</i></a>:<br />
<br />
Джоэл Спольски в своё время подробно расписал, почему так получается:<br />
<blockquote>Чтобы создать хороший продукт, требуется 10 лет разработки, но когда он готов - он <i>готов</i>. После этого уже никто не может придумать ни единой фичи, которая была бы реально нужна.</blockquote></blockquote>
Поддерживаю.''')

TEST(
"""T‘
H‘‘1’ ‘2’’
 ‘‘3’ ‘4’[[[comment]]]’
[[[comment]]]’
5""",
"""<table>
<tr><th>1</th><th>2</th></tr>
<tr><td>3</td><td>4</td></tr>
</table>
5""")
TEST(
"""T‘‘
‘ ’ ‘ ’ ‘1’ ’‘
‘ ’ ‘ ’  |  ’‘
‘2’  -   |  ’’""",
"""<table>
<tr><td> </td><td> </td><td rowspan="3">1</td></tr>
<tr><td> </td><td> </td></tr>
<tr><td colspan="2">2</td></tr>
</table>
""")
TEST(
"""T‘‘
‘ ’ ‘ ’ ‘1’ ’‘
‘ ’ ‘ ’  |  ’‘
‘2’  -   -  ’’""",
"""<table>
<tr><td> </td><td> </td><td rowspan="2">1</td></tr>
<tr><td> </td><td> </td></tr>
<tr><td colspan="3">2</td></tr>
</table>
""")
TEST(
"""T‘‘
‘1’  -   -  ‘2’ ’‘
 |   -   -  ‘3’ ’‘
 |   -   -  ‘4’ ’‘
‘5’ ‘6’ ‘7’     ’’""",
"""<table>
<tr><td colspan="3" rowspan="3">1</td><td>2</td></tr>
<tr><td>3</td></tr>
<tr><td>4</td></tr>
<tr><td>5</td><td>6</td><td>7</td></tr>
</table>
""")
TEST(
R"""T‘
/\>>‘‘top
right’ ‘top right’ \/‘bottom right’ ‘top right’’
‘‘default alignment’ ‘default
alignment’ ‘default alignment’ ‘default alignment’’
\/><‘‘bottom center’ ‘bottom
center’ >>‘bottom
right’ ‘bottom center’’
’""",
"""<table>
<tr><td style="text-align: right; vertical-align: top">top<br />
right</td><td style="text-align: right; vertical-align: top">top right</td><td style="text-align: right; vertical-align: bottom">bottom right</td><td style="text-align: right; vertical-align: top">top right</td></tr>
<tr><td>default alignment</td><td>default<br />
alignment</td><td>default alignment</td><td>default alignment</td></tr>
<tr><td style="text-align: center; vertical-align: bottom">bottom center</td><td style="text-align: center; vertical-align: bottom">bottom<br />
center</td><td style="text-align: right; vertical-align: bottom">bottom<br />
right</td><td style="text-align: center; vertical-align: bottom">bottom center</td></tr>
</table>
""")
TEST('''[[[[https://fuse.wikichip.org/news/2823/samsung-5-nm-and-4-nm-update/ <- https://en.wikipedia.org/wiki/Extreme_ultraviolet_lithography]]]]\
T‘
C(-#c4f5d1)><‘‘5LPE’ - -’
C(-#c4f5d1)><‘‘’ ‘7.5T (HD)’ ‘6T (UHD)’’
><‘C(-#c4f5d1)‘FP’ ‘27 nm’ -’
><‘C(-#c4f5d1)‘CPP’ ‘60 nm’ ‘54 nm’’
’''', '''\
<table>
<tr style="background-color: #c4f5d1"><td style="text-align: center" colspan="3">5LPE</td></tr>
<tr style="background-color: #c4f5d1"><td style="text-align: center"></td><td style="text-align: center">7.5T (HD)</td><td style="text-align: center">6T (UHD)</td></tr>
<tr><td style="text-align: center; background-color: #c4f5d1">FP</td><td style="text-align: center" colspan="2">27 nm</td></tr>
<tr><td style="text-align: center; background-color: #c4f5d1">CPP</td><td style="text-align: center">60 nm</td><td style="text-align: center">54 nm</td></tr>
</table>
''')
TEST("""A
```
let s2 = str
        .lowercaseString
        .replace("hello", withString: "goodbye")
```
B
C""",
"""A<br />
<pre>
let s2 = str
        .lowercaseString
        .replace("hello", withString: "goodbye")
</pre>
B<br />
C""") # с тегом <code> пробелы ‘корректно не отображаются’/коллапсируются
TEST(R"""#(11l)‘(‘\‘’’')
('‘‘Don’t!’)
('''‘‘‘‘Don’t! Don’t! Don’t!’)
(‘Don‘t! Don‘t! Don‘t!’’’’''')
('‘‘’‘’’')’""", R"""<style>
span.keyword {color: #0000FF; font-weight: bold;}
span.identifier {color: #00009F;}
span.string-literal {color: #800000;}
span.numeric-literal {color: #008000;}
span.constant {color: #008000;}
span.comment {color: #808080;}
</style><pre style="display: inline">(<span class="string-literal">‘\‘’<span style="opacity: 0.25">’'</span></span>)
(<span class="string-literal"><span style="opacity: 0.25">'‘</span>‘Don’t!’</span>)
(<span class="string-literal"><span style="opacity: 0.25">'''‘‘‘</span>‘Don’t! Don’t! Don’t!’</span>)
(<span class="string-literal">‘Don‘t! Don‘t! Don‘t!’<span style="opacity: 0.25">’’’'''</span></span>)
(<span class="string-literal"><span style="opacity: 0.25">'‘</span>‘’‘’<span style="opacity: 0.25">’'</span></span>)</pre>""", ohd = True)
TEST('''#‘
...
’[[[comment]]]
---
''', '''<pre class="code_block">
...
</pre><!--[[[comment]]]-->
<hr />
''')
TEST('''#‘
BOOOsssSSSdddDDD
│└┬┘└┬┘└┬┘└┬┘└┬┘
│ │  │  │  │  └─ 0-2 биты: регистр-приёмник
│ │  │  │  └──── 3-5 биты: режим адресации регистра-приёмника
│ │  │  └─────── 6-8 биты: регистр-источник
│ │  └───────── 9-11 биты: режим адресации регистра-источника
│ └─────────── 12-14 биты: код операции
└───────────────── 15 бит: признак byte-инструкций[[[ (если 0, то инструкция выполняется над словом, а если 1 — над байтом)]]|]
’''', '''<pre class="code_block">
BOOOsssSSSdddDDD
│└┬┘└┬┘└┬┘└┬┘└┬┘
│ │  │  │  │  └─ 0-2 биты: регистр-приёмник
│ │  │  │  └──── 3-5 биты: режим адресации регистра-приёмника
│ │  │  └─────── 6-8 биты: регистр-источник
│ │  └───────── 9-11 биты: режим адресации регистра-источника
│ └─────────── 12-14 биты: код операции
└───────────────── 15 бит: признак byte-инструкций
</pre>''')
TEST('''#(Python)‘
array3d = [[[1, 2, 3], [4, 5, 6]]] # this should not be treated as a comment!
’''', '''<pre class="code_block">
array3d = [[[1, 2, 3], [4, 5, 6]]] # this should not be treated as a comment!
</pre>''')
TEST('''#(Python)‘
array3d = [[[1, 2, 3],[[[ hidden comment]]|]
            [4, 5, 6]]]
’''', '''<pre class="code_block">
array3d = [[[1, 2, 3],
            [4, 5, 6]]]
</pre>''')

# Check for error handling
test_id += 1
was_error = False
print("Test " + str(test_id) + " (error handling) ...", end = '')
try:
    pqmarkup.to_html("\nT‘‘‘`’’’")
except pqmarkup.Exception as e:
    was_error = True
    if e.line == 2 and e.column == 5 and e.pos == 5:
        print("passed")
    else:
        print("FAILED!")
        failed_tests += 1
assert(was_error)

# Check for presence of TAB and CR characters in source files and forbid them
test_id += 1
print("Test " + str(test_id) + ". Checking source files for unallowed characters...")
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d[0] != '.'] # exclude hidden folders (e.g. `.hg`)
    for name in files:
        if name.endswith(('.py', '.txt')):
            file_bytes = open(os.path.join(root, name), 'rb').read()
            if b"\r" in file_bytes or b"\t" in file_bytes:
                print(R"Unallowed character (\r or \t) found in file '" + os.path.join(root, name)[2:] + "'")
                failed_tests += 1

# Unfortunately addition of this line:
# precommit.check_docs.en = python pqmarkup.py docs/en/syntax.pq.txt > nul
# to [hooks] section in hgrc is not working, so perform this check here.
# Почему unfortunately: потому, что было бы лучше, если бы возник прецедент необходимости в этом исключении во внешнем коде,
# так как тогда бы я передавал в этом исключении информацию, необходимую для этого [внешнего] кода, а так получается, что я
# уже не смогу узнать, какая информация необходима внешнему коду, так как при наличии данного/этого исключения внешний код
# будет просто подстраиваться под ту информацию, что я уже передаю в исключении. В данном случае, возможно это и не играет
# большой роли, но сам принцип должен быть такой: выдавать следует информацию тогда, когда появляется реальная/насущная
# необходимость в ней, так как именно в этот момент возможно наиболее точно установить требования к тому, в какой форме, в
# каком формате необходимо передавать информацию. Заранее сделать это ‘на будущее’/‘на всякий случай’ получится всегда хуже
# [кроме того случая, когда человек, которому поручили это, уже имеет соответствующий опыт].
def check_file(fname):
    try:
        pqmarkup.to_html(open(fname, encoding='utf-8').read(), ohd = True)
    except pqmarkup.Exception as e:
        print(e.message + " at file '" + fname + "', line " + str(e.line) + ", column " + str(e.column))
        sys.exit(1)
check_file("docs/en/syntax.pq.txt")
check_file("docs/ru/syntax.pq.txt")

if failed_tests == 0:
    print("OK (all " + str(test_id) + " tests passed)")
    sys.exit(0)
else:
    print(str(test_id-failed_tests) + " tests passed and " + str(failed_tests) + " failed.")
    sys.exit(1)
