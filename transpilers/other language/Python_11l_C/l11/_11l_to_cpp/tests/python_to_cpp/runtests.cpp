#define INCLUDE_FS
#include "C:\!!BITBUCKET\11l-lang\_11l_to_cpp\11l.hpp"

namespace pqmarkup {
#include "pqmarkup.hpp"
}

auto test_id = 0;
auto failed_tests = 0;
auto kdiff_showed = false;
template <typename T1, typename T2, typename T3 = decltype(false), typename T4 = decltype(false)> auto TEST(T1 str1, T2 str2, const T3 &ohd = false, const T4 &habr_html = false)
{
    ::test_id++;
    print(u"Test "_S & String(::test_id) & u" ..."_S, u""_S);
    str1 = pqmarkup::to_html(str1, nullptr, ohd, habr_html);
    if (str1 != str2) {
        str1 = String(str1);
        str2 = String(str2);
        print(u"FAILED!"_S);
        if (!::kdiff_showed) {
            for (auto &&envvar : create_array({u"ProgramFiles"_S, u"ProgramFiles(x86)"_S, u"ProgramW6432"_S}))
                os::environ[u"PATH"_S] &= os::env_path_sep & os::getenv(envvar, u""_S) & uR"(\KDiff3)"_S;
            auto command = u"kdiff3"_S;
            for (auto &&file : create_array({make_tuple(u"wrong"_S, str1), make_tuple(u"right"_S, str2)})) {
                auto full_fname = fs::path::join(fs::get_temp_dir(), _get<0>(file));
                command &= u" \""_S & full_fname & u"\""_S;
                FileWr(full_fname, u"utf-8-sig"_S).write(_get<1>(file));
            }
            os::_(command);
            ::kdiff_showed = true;
        }
        ::failed_tests++;
    }
    else
        print(u"passed"_S);
}

struct CodeBlock1
{
    CodeBlock1()
    {
        TEST(u"*‘bold’"_S, u"<b>bold</b>"_S);
        TEST(u"_‘underlined’"_S, u"<u>underlined</u>"_S);
        TEST(u"-‘strikethrough’"_S, u"<s>strikethrough</s>"_S);
        TEST(u"~‘italics’"_S, u"<i>italics</i>"_S);
        TEST(u"H‘header’\n"_S & u"H(1)‘header’"_S, u"<h3>header</h3>\n"_S & u"<h2>header</h2>"_S);
        TEST(u"H(+1)‘header’"_S, u"<h2>header</h2>"_S);
        TEST(u"H(-1)‘header’"_S, u"<h4>header</h4>"_S);
        TEST(u"[http://address]"_S, u"<a href=\"http://address\">http://address</a>"_S);
        TEST(u"link[http://address]"_S, u"<a href=\"http://address\">link</a>"_S);
        TEST(u"link[https://address]"_S, u"<a href=\"https://address\">link</a>"_S);
        TEST(u"‘multiword link’[http://address]"_S, u"<a href=\"http://address\">multiword link</a>"_S);
        TEST(u"link[https://address ‘title &text[[[comment]]]’]"_S, u"<a href=\"https://address\" title=\"title &amp;text\">link</a>"_S);
        TEST(u"link[https://address title [.&.] text[[[comment]]]]"_S, u"<a href=\"https://address\" title=\"title [.&amp;.] text\">link</a>"_S);
        TEST(u"‘[[[Scoping rules/]]]Code blocks’[./code-blocks]"_S, u"<a href=\"./code-blocks\" target=\"_self\"><!--[[[Scoping rules/]]]-->Code blocks</a>"_S);
        TEST(uR"(‘Versioning with 100%/versions_threshold/\‘2’ overhead’[./versioning.pq])"_S, u"<a href=\"./versioning.pq\" target=\"_self\">Versioning with 100%/versions_threshold<sup>2</sup> overhead</a>"_S);
        TEST(u"‘compares files based on which ~‘lines’ have changed’[http://www.devuxer.com/2014/02/15/why-the-mercurial-zipdoc-extension-fails-for-excel-files/]"_S, u"<a href=\"http://www.devuxer.com/2014/02/15/why-the-mercurial-zipdoc-extension-fails-for-excel-files/\">compares files based on which <i>lines</i> have changed</a>"_S);
        TEST(u"text[‘title text’]"_S, u"<abbr title=\"title text\">text</abbr>"_S);
        TEST(u"[text][‘title text’]"_S, u"[text]<abbr title=\"title text\"></abbr>"_S);
        TEST(u"Примечание 1: только режимы ‘r’ и ‘w’ поддерживаются на данный момент [‘мои мысли на тему режимов открытия файлов’[./File]]"_S, u"Примечание 1: только режимы ‘r’ и ‘w’ поддерживаются на данный момент [<a href=\"./File\" target=\"_self\">мои мысли на тему режимов открытия файлов</a>]"_S);
        TEST(u"Примечание 1: только режимы ‘r’ и ‘w’ поддерживаются на данный момент [[‘’]‘мои мысли на тему режимов открытия файлов’[./File]]"_S, u"Примечание 1: только режимы ‘r’ и ‘w’ поддерживаются на данный момент [<abbr title=\"\"></abbr><a href=\"./File\" target=\"_self\">мои мысли на тему режимов открытия файлов</a>]"_S);
        TEST(u"[[‘’][[[Справка/]]]Документация по методам доступна на данный момент только ‘на английском’[./../../built-in-types].]"_S, u"[<abbr title=\"\"></abbr><!--[[[Справка/]]]-->Документация по методам доступна на данный момент только <a href=\"./../../built-in-types\" target=\"_self\">на английском</a>.]"_S);
        TEST(u"[‘мои мысли на тему режимов открытия файлов’[./File]]"_S, u"[<a href=\"./File\" target=\"_self\">мои мысли на тему режимов открытия файлов</a>]"_S);
        TEST(u"P‘http://image-url’"_S, u"<img src=\"http://image-url\" />"_S);
        TEST(u"P‘http://image-url’[http://address]"_S, u"<a href=\"http://address\"><img src=\"http://image-url\" /></a>"_S);
        TEST(u"P‘http://image-url’[‘title text[[[comment]]]’]"_S, u"<img src=\"http://image-url\" title=\"title text\" />"_S);
        TEST(u"P‘http://image-url’[http://address ‘title text’]"_S, u"<a href=\"http://address\" title=\"title text\"><img src=\"http://image-url\" /></a>"_S);
        TEST(u"P‘http://image-url’[http://address title text]"_S, u"<a href=\"http://address\" title=\"title text\"><img src=\"http://image-url\" /></a>"_S);
        TEST(u"С(000)‘black text’"_S, u"<span style=\"color: #000000\">black text</span>"_S);
        TEST(u"С(800)‘red text’"_S, u"<span style=\"color: #FF0000\">red text</span>"_S);
        TEST(u"С(4)‘gray text’"_S, u"<span style=\"color: #808080\">gray text</span>"_S);
        TEST(u"С(0000)‘transparent text’"_S, u"<span style=\"color: #00000000\">transparent text</span>"_S);
        TEST(u"С(#фФ0000)‘red text’"_S, u"<span style=\"color: #fF0000\">red text</span>"_S);
        TEST(u"C(#fF0000)‘red text’"_S, u"<span style=\"color: #fF0000\">red text</span>"_S);
        TEST(u"C(-800)‘text on a red background’"_S, u"<span style=\"background-color: #FF0000\">text on a red background</span>"_S);
        TEST(u"C(888-000)‘white text on black background’"_S, u"<span style=\"color: #FFFFFF; background-color: #000000\">white text on black background</span>"_S);
        TEST(u"link[http://address][1] ‘the same link’[1]"_S, u"<a href=\"http://address\">link</a>[1] ‘the same link’[1]"_S);
        TEST(u"link[http://address][-1] ‘the same link’[-1]"_S, u"<a href=\"http://address\">link</a> <a href=\"http://address\">the same link</a>"_S);
        TEST(u"[[[comment[[[[sensitive information]]]]]]]"_S, u"<!--[[[comment]]]-->"_S);
        TEST(u"[[[com]ment]]"_S, u"<!--[[[com]ment]]-->"_S);
        TEST(u"[[[[comment]]]]"_S, u""_S);
        TEST(u"[[[[[com]m]e]n]t]"_S, u""_S);
        TEST(u"\n A"_S, u"<br />\n&emsp;A"_S);
        TEST(u" A"_S, u"&emsp;A"_S);
        TEST(u"---"_S, u"<hr />\n"_S);
        TEST(u"---\n"_S, u"<hr />\n"_S);
        TEST(u"a\n---\n"_S, u"a<br />\n<hr />\n"_S);
        TEST(u"a\n---\n\n"_S, u"a<br />\n<hr />\n<br />\n"_S);
        TEST(u"a\n---=\n"_S, u"a<br />\n---=<br />\n"_S);
        TEST(u"a\n----\n"_S, u"a<br />\n<hr />\n"_S);
        TEST(u"a0‘*‘<non-bold>’’"_S, u"a*‘&lt;non-bold>’"_S);
        TEST(uR"(a
‘b[[[comment]]]’{
c
‘d’{e}
})"_S, uR"(a<br />
<spoiler title="b">
c<br />
<spoiler title="d">
e</spoiler>
</spoiler>
)"_S, false, true);
        TEST(uR"(‘title’{
te
}
xt)"_S, uR"'(<span class="spoiler_title" onclick="return spoiler2(this, event)">title<br /></span><div class="spoiler_text" style="display: none">
te<br />
</div>
xt)'"_S, true);
        TEST(uR"(#(JavaScript)‘
    { "keys": ["‘"], "command": "insert_pq" }, //also insert balancing ’
’)"_S, uR"(<source lang="JavaScript">
    { "keys": ["‘"], "command": "insert_pq" }, //also insert balancing ’
</source>)"_S, false, true);
        TEST(uR"(‘Code’{
#(Python)‘
import hashlib
’
}

Some text.)"_S, uR"(<spoiler title="Code">
<source lang="Python">
import hashlib
</source>
</spoiler>
<br />
Some text.)"_S, false, true);
        TEST(u"[[[‘]]]test```’```test"_S, u"<!--[[[‘]]]-->test<code>’</code>test"_S, false, true);
        TEST(u"[[[‘]]]`Don’t`"_S, u"<!--[[[‘]]]--><code>Don’t</code>"_S, false, true);
        TEST(u"'‘<Don‘t! Don‘t! Don‘t!>’’’’''''"_S, u"<Don‘t! Don‘t! Don‘t!>"_S);
        TEST(u"`'‘<div>&lt;</div>’'`"_S, u"<code>'‘&lt;div>&amp;lt;&lt;/div>’'</code>"_S, false, true);
        TEST(u"''‘‘’‘’’''"_S, u"’‘"_S);
        TEST(u"''''‘‘‘‘Don’t! Don’t! Don’t!’'"_S, u"Don’t! Don’t! Don’t!"_S);
        TEST(u"модуль #(11l)‘fs’"_S, u"модуль <code>fs</code>"_S, false, true);
        TEST(uR"(Т‘
‘‘Python’ ‘#(Python)‘rn = {'I': 1, 'V': 5, 'X': 10, 'L': 50, ...}’’’
’)"_S, uR"(<table>
<tr><td>Python</td><td><source lang="Python">rn = {'I': 1, 'V': 5, 'X': 10, 'L': 50, ...}</source></td></tr>
</table>
)"_S, false, true);
        TEST(uR"(Т‘
‘‘Python’ ‘#(Python)‘rn = {'I': 1, 'V': 5, 'X': 10, 'L': 50, ...}’ — ...’’
’)"_S, uR"(<table>
<tr><td>Python</td><td><code>rn = {'I': 1, 'V': 5, 'X': 10, 'L': 50, ...}</code> — ...</td></tr>
</table>
)"_S, false, true);
        TEST(uR"(<<‘выравнивание по левому краю’
>>‘выравнивание по правому краю’
><‘выравнивание по центру’
<>‘выравнивание по ширине’)"_S, uR"(<div align="left">выравнивание по левому краю</div>
<div align="right">выравнивание по правому краю</div>
<div align="center">выравнивание по центру</div>
<div align="justify">выравнивание по ширине</div>
)"_S);
        TEST(u"‘’<<"_S, u"‘’&lt;&lt;"_S);
        TEST(uR"(/\‘надстрочный\superscript’\/‘подстрочный\subscript’)"_S, uR"(<sup>надстрочный\superscript</sup><sub>подстрочный\subscript</sub>)"_S);
        TEST(u"> Quote\n"_S & u">‘Quote2’\n"_S, u"<blockquote>Quote</blockquote>\n"_S & u"<blockquote>Quote2</blockquote>\n"_S);
        TEST(u">[http://address]:‘Quoted text.’"_S, u"<blockquote><a href=\"http://address\"><i>http://address</i></a>:<br />\nQuoted text.</blockquote>"_S);
        TEST(u">[http://another-address][-1]:‘Quoted text.’\n"_S & u">[-1]:‘Another quoted text.’"_S, u"<blockquote><a href=\"http://another-address\">[1]<i>http://another-address</i></a>:<br />\nQuoted text.</blockquote>\n"_S & u"<blockquote><a href=\"http://another-address\">[1]<i>http://another-address</i></a>:<br />\nAnother quoted text.</blockquote>"_S);
        TEST(u">‘Author's name’[http://address]:‘Quoted text.’"_S, u"<blockquote><i><a href=\"http://address\">Author's name</a></i>:<br />\nQuoted text.</blockquote>"_S);
        TEST(u">‘Author's name’[http://address][-1]:‘Quoted text.’\n"_S & u">‘Author's name’[-1]:‘Another quoted text.’"_S, u"<blockquote><i><a href=\"http://address\">Author's name</a></i>:<br />\nQuoted text.</blockquote>\n"_S & u"<blockquote><i><a href=\"http://address\">Author's name</a></i>:<br />\nAnother quoted text.</blockquote>"_S);
        TEST(u">‘Author's name’:‘Quoted text.’"_S, u"<blockquote><i>Author's name</i>:<br />\nQuoted text.</blockquote>"_S);
        TEST(u"‘Quoted text.’:‘Author's name’<"_S, u"<blockquote>Quoted text.<br />\n<div align='right'><i>Author's name</i></div></blockquote>"_S);
        TEST(u">‘Как люди думают. Дмитрий Чернышев. 2015. 304с.’:‘[[[стр.89:]]]...’"_S, u"<blockquote><i>Как люди думают. Дмитрий Чернышев. 2015. 304с.</i>:<br />\n<!--[[[стр.89:]]]-->...</blockquote>"_S);
        TEST(u">‘>‘Автор против nullable-типов?’\nДа. Адрес, указывающий на незаконный участок памяти, сам незаконен.’"_S, u"<blockquote><blockquote>Автор против nullable-типов?</blockquote>\nДа. Адрес, указывающий на незаконный участок памяти, сам незаконен.</blockquote>"_S);
        TEST(u">‘> Автор против nullable-типов?\nДа. Адрес, указывающий на незаконный участок памяти, сам незаконен.’"_S, u"<blockquote><blockquote>Автор против nullable-типов?</blockquote>\nДа. Адрес, указывающий на незаконный участок памяти, сам незаконен.</blockquote>"_S);
        TEST(u">‘1. A\n’"_S, u"<blockquote><ol>\n<li>A</li>\n</ol>\n</blockquote>"_S);
        TEST(u"!‘1. A\n’"_S, u"<div class=\"note\"><ol>\n<li>A</li>\n</ol>\n</div>"_S);
        TEST(u">[http://ruscomp.24bb.ru/viewtopic.php?id=20]:‘> То есть обычные русские слова уже не являются для вас \"общепринятым\" языком?\nОбщепринятые – это те, которые я читаю в книгах, в том числе по программированию.’"_S, u"<blockquote><a href=\"http://ruscomp.24bb.ru/viewtopic.php?id=20\"><i>http://ruscomp.24bb.ru/viewtopic.php?id=20</i></a>:<br />\n<blockquote>То есть обычные русские слова уже не являются для вас \"общепринятым\" языком?</blockquote>\nОбщепринятые – это те, которые я читаю в книгах, в том числе по программированию.</blockquote>"_S);
        TEST(u"‘понимание [[[процесса]]] разбора [[[разметки]]] человеком’[‘говоря проще: приходится [[[гораздо]]] меньше думать о том, будет это работать или не будет, а просто пишешь в соответствии с чёткими/простыми/логичными правилами, и всё’]"_S, u"<abbr title=\"говоря проще: приходится  меньше думать о том, будет это работать или не будет, а просто пишешь в соответствии с чёткими/простыми/логичными правилами, и всё\">понимание  разбора  человеком</abbr>"_S);
        TEST(uR"(. unordered
. list)"_S, uR"(<ul>
<li>unordered</li>
<li>list</li>
</ul>
)"_S);
        TEST(uR"(1. ordered
2. list)"_S, uR"(<ol>
<li>ordered</li>
<li>list</li>
</ol>
)"_S);
        TEST(uR"(13. disordered
2. list)"_S, uR"(<ol start="13">
<li>disordered</li>
<li value="2">list</li>
</ol>
)"_S);
        TEST(uR"(1. interrupted
. ol
2. list)"_S, uR"(<ol>
<li>interrupted</li>
</ol>
<ul>
<li>ol</li>
</ul>
<ol start="2">
<li>list</li>
</ol>
)"_S);
        TEST(uR"(. interrupted
1. ul
. list)"_S, uR"(<ul>
<li>interrupted</li>
</ul>
<ol>
<li>ul</li>
</ol>
<ul>
<li>list</li>
</ul>
)"_S);
        TEST(uR"(1.‘multiline
list element’
2. second)"_S, uR"(<ol>
<li>multiline<br />
list element</li>
<li>second</li>
</ol>
)"_S);
        TEST(uR"(.‘multiline
list element’
. second)"_S, uR"(<ul>
<li>multiline<br />
list element</li>
<li>second</li>
</ul>
)"_S);
        TEST(uR"(4.‘А ещё мне коды[/годы] этих символов нравятся...’

Один существенный минус ...)"_S, uR"(<ol start="4">
<li>А ещё мне коды<span class="sq"><span class="sq_brackets">[</span>/годы<span class="sq_brackets">]</span></span> этих символов нравятся...</li>
</ol>
<br />
Один существенный минус ...)"_S, true);
        TEST(uR"(4. ‘А ещё мне коды[/годы] этих символов нравятся...’{...}

Один существенный минус ...)"_S, uR"'(<ol start="4">
<li><span class="spoiler_title" onclick="return spoiler2(this, event)">А ещё мне коды[/годы] этих символов нравятся...<br /></span><div class="spoiler_text" style="display: none">
...</div>
</li>
</ol>
<br />
Один существенный минус ...)'"_S, true);

        TEST(uR"(>‘. a
. b’
c
d)"_S, uR"(<blockquote><ul>
<li>a</li>
<li>b</li>
</ul>
</blockquote>
c<br />
d)"_S);

        TEST(uR"(>[https://habr.com/ru/articles/780372/comments/#comment_26271586]:‘
Джоэл Спольски в своё время подробно расписал, почему так получается:
> Чтобы создать хороший продукт, требуется 10 лет разработки, но когда он готов - он ~‘готов’. После этого уже никто не может придумать ни единой фичи, которая была бы реально нужна.’
Поддерживаю.)"_S, uR"(<blockquote><a href="https://habr.com/ru/articles/780372/comments/#comment_26271586"><i>https://habr.com/ru/articles/780372/comments/...</i></a>:<br />
<br />
Джоэл Спольски в своё время подробно расписал, почему так получается:<br />
<blockquote>Чтобы создать хороший продукт, требуется 10 лет разработки, но когда он готов - он <i>готов</i>. После этого уже никто не может придумать ни единой фичи, которая была бы реально нужна.</blockquote></blockquote>
Поддерживаю.)"_S);

        TEST(uR"(T‘
H‘‘1’ ‘2’’
 ‘‘3’ ‘4’[[[comment]]]’
[[[comment]]]’
5)"_S, uR"(<table>
<tr><th>1</th><th>2</th></tr>
<tr><td>3</td><td>4</td></tr>
</table>
5)"_S);
        TEST(uR"(T‘‘
‘ ’ ‘ ’ ‘1’ ’‘
‘ ’ ‘ ’  |  ’‘
‘2’  -   |  ’’)"_S, uR"(<table>
<tr><td> </td><td> </td><td rowspan="3">1</td></tr>
<tr><td> </td><td> </td></tr>
<tr><td colspan="2">2</td></tr>
</table>
)"_S);
        TEST(uR"(T‘‘
‘ ’ ‘ ’ ‘1’ ’‘
‘ ’ ‘ ’  |  ’‘
‘2’  -   -  ’’)"_S, uR"(<table>
<tr><td> </td><td> </td><td rowspan="2">1</td></tr>
<tr><td> </td><td> </td></tr>
<tr><td colspan="3">2</td></tr>
</table>
)"_S);
        TEST(uR"(T‘‘
‘1’  -   -  ‘2’ ’‘
 |   -   -  ‘3’ ’‘
 |   -   -  ‘4’ ’‘
‘5’ ‘6’ ‘7’     ’’)"_S, uR"(<table>
<tr><td colspan="3" rowspan="3">1</td><td>2</td></tr>
<tr><td>3</td></tr>
<tr><td>4</td></tr>
<tr><td>5</td><td>6</td><td>7</td></tr>
</table>
)"_S);
        TEST(uR"(T‘
/\>>‘‘top
right’ ‘top right’ \/‘bottom right’ ‘top right’’
‘‘default alignment’ ‘default
alignment’ ‘default alignment’ ‘default alignment’’
\/><‘‘bottom center’ ‘bottom
center’ >>‘bottom
right’ ‘bottom center’’
’)"_S, uR"(<table>
<tr><td style="text-align: right; vertical-align: top">top<br />
right</td><td style="text-align: right; vertical-align: top">top right</td><td style="text-align: right; vertical-align: bottom">bottom right</td><td style="text-align: right; vertical-align: top">top right</td></tr>
<tr><td>default alignment</td><td>default<br />
alignment</td><td>default alignment</td><td>default alignment</td></tr>
<tr><td style="text-align: center; vertical-align: bottom">bottom center</td><td style="text-align: center; vertical-align: bottom">bottom<br />
center</td><td style="text-align: right; vertical-align: bottom">bottom<br />
right</td><td style="text-align: center; vertical-align: bottom">bottom center</td></tr>
</table>
)"_S);
        TEST(u"[[[[https://fuse.wikichip.org/news/2823/samsung-5-nm-and-4-nm-update/ <- https://en.wikipedia.org/wiki/Extreme_ultraviolet_lithography]]]]\
T‘\n\
C(-#c4f5d1)><‘‘5LPE’ - -’\n\
C(-#c4f5d1)><‘‘’ ‘7.5T (HD)’ ‘6T (UHD)’’\n\
><‘C(-#c4f5d1)‘FP’ ‘27 nm’ -’\n\
><‘C(-#c4f5d1)‘CPP’ ‘60 nm’ ‘54 nm’’\n\
’"_S, uR"(<table>
<tr style="background-color: #c4f5d1"><td style="text-align: center" colspan="3">5LPE</td></tr>
<tr style="background-color: #c4f5d1"><td style="text-align: center"></td><td style="text-align: center">7.5T (HD)</td><td style="text-align: center">6T (UHD)</td></tr>
<tr><td style="text-align: center; background-color: #c4f5d1">FP</td><td style="text-align: center" colspan="2">27 nm</td></tr>
<tr><td style="text-align: center; background-color: #c4f5d1">CPP</td><td style="text-align: center">60 nm</td><td style="text-align: center">54 nm</td></tr>
</table>
)"_S);
        TEST(uR"(A
```
let s2 = str
        .lowercaseString
        .replace("hello", withString: "goodbye")
```
B
C)"_S, uR"(A<br />
<pre>
let s2 = str
        .lowercaseString
        .replace("hello", withString: "goodbye")
</pre>
B<br />
C)"_S);
        TEST(uR"(#(11l)‘(‘\‘’’')
('‘‘Don’t!’)
('''‘‘‘‘Don’t! Don’t! Don’t!’)
(‘Don‘t! Don‘t! Don‘t!’’’’''')
('‘‘’‘’’')’)"_S, uR"(<style>
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
(<span class="string-literal"><span style="opacity: 0.25">'‘</span>‘’‘’<span style="opacity: 0.25">’'</span></span>)</pre>)"_S, true);
        TEST(uR"(#‘
...
’[[[comment]]]
---
)"_S, uR"(<pre class="code_block">
...
</pre><!--[[[comment]]]-->
<hr />
)"_S);
        TEST(uR"(#‘
BOOOsssSSSdddDDD
│└┬┘└┬┘└┬┘└┬┘└┬┘
│ │  │  │  │  └─ 0-2 биты: регистр-приёмник
│ │  │  │  └──── 3-5 биты: режим адресации регистра-приёмника
│ │  │  └─────── 6-8 биты: регистр-источник
│ │  └───────── 9-11 биты: режим адресации регистра-источника
│ └─────────── 12-14 биты: код операции
└───────────────── 15 бит: признак byte-инструкций[[[ (если 0, то инструкция выполняется над словом, а если 1 — над байтом)]]|]
’)"_S, uR"(<pre class="code_block">
BOOOsssSSSdddDDD
│└┬┘└┬┘└┬┘└┬┘└┬┘
│ │  │  │  │  └─ 0-2 биты: регистр-приёмник
│ │  │  │  └──── 3-5 биты: режим адресации регистра-приёмника
│ │  │  └─────── 6-8 биты: регистр-источник
│ │  └───────── 9-11 биты: режим адресации регистра-источника
│ └─────────── 12-14 биты: код операции
└───────────────── 15 бит: признак byte-инструкций
</pre>)"_S);
        TEST(uR"(#(Python)‘
array3d = [[[1, 2, 3], [4, 5, 6]]] # this should not be treated as a comment!
’)"_S, uR"(<pre class="code_block">
array3d = [[[1, 2, 3], [4, 5, 6]]] # this should not be treated as a comment!
</pre>)"_S);
        TEST(uR"(#(Python)‘
array3d = [[[1, 2, 3],[[[ hidden comment]]|]
            [4, 5, 6]]]
’)"_S, uR"(<pre class="code_block">
array3d = [[[1, 2, 3],
            [4, 5, 6]]]
</pre>)"_S);

        test_id++;
    }
} code_block_1;

auto was_error = false;

struct CodeBlock2
{
    CodeBlock2()
    {
        print(u"Test "_S & String(test_id) & u" (error handling) ..."_S, u""_S);
        try
        {
            pqmarkup::to_html(u"\nT‘‘‘`’’’"_S);
        }
        catch (const pqmarkup::Exception& e)
        {
            was_error = true;
            if (e.line == 2 && e.column == 5 && e.pos == 5)
                print(u"passed"_S);
            else {
                print(u"FAILED!"_S);
                failed_tests++;
            }
        }
        assert(was_error);

        test_id++;
        print(u"Test "_S & String(test_id) & u". Checking source files for unallowed characters..."_S);
        for (auto &&_fname : fs::walk_dir(u"."_S, [](const auto &d){return _get<0>(d) != u'.';}, false)) {
            auto root = fs::path::dir_name(_fname);
            Array<String> dirs, files;
            if (fs::is_dir(_fname))
                dirs.append(fs::path::base_name(_fname));
            else
                files.append(fs::path::base_name(_fname));
            for (auto &&name : files)
                if (name.ends_with(make_tuple(u".py"_S, u".txt"_S))) {
                    auto file_bytes = File(fs::path::join(root, name)).read_bytes();
                    if (in(u'\r'_C.code, file_bytes) || in(u'\t'_C.code, file_bytes)) {
                        print(uR"(Unallowed character (\r or \t) found in file ')"_S & fs::path::join(root, name)[range_ei(2)] & u"'"_S);
                        failed_tests++;
                    }
                }
        }
    }
} code_block_2;

template <typename T1> auto check_file(const T1 &fname)
{
    try
    {
        pqmarkup::to_html(File(fname, u"utf-8"_S).read(), nullptr, true);
    }
    catch (const pqmarkup::Exception& e)
    {
        print(e.message & u" at file '"_S & fname & u"', line "_S & String(e.line) & u", column "_S & String(e.column));
        exit(1);
    }
}

struct CodeBlock3
{
    CodeBlock3()
    {
        check_file(u"docs/en/syntax.pq.txt"_S);
        check_file(u"docs/ru/syntax.pq.txt"_S);

        if (failed_tests == 0) {
            print(u"OK (all "_S & String(test_id) & u" tests passed)"_S);
            exit(0);
        }
        else {
            print(String(test_id - failed_tests) & u" tests passed and "_S & String(failed_tests) & u" failed."_S);
            exit(1);
        }
    }
} code_block_3;

int main()
{
}
