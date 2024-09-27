#include "C:\!!BITBUCKET\11l-lang\_11l_to_cpp\11l.hpp"

struct CodeBlock1
{
    CodeBlock1()
    {
        for (auto __unused : range_ee(1, to_int(input()))) {
            auto s = input();
            auto m = to_int(input());
            auto b = input().split(u" "_S).map([](const auto &x){return to_int(x);});
            auto array = sorted(create_array(create_set(create_array(s))));
            auto answer = create_array({u'\0'_C}) * m;
            while (sum(b) != -m) {
                Set<int> индексы;
                for (auto i : range_el(0, m))
                    if (b[i] == 0) {
                        индексы.add(i);
                        b.set(i, -1);
                    }
                while (true) {
                    auto q = array.pop();
                    if (индексы.len() <= s.count(q)) {
                        for (auto &&i : индексы)
                            answer.set(i, q);
                        break;
                    }
                }
                for (auto &&i : индексы)
                    for (auto j : range_el(0, m))
                        if (b[j] != -1)
                            b[j] -= abs(i - j);
            }
            print(answer.join(u""_S));
        }
    }
} code_block_1;

int main()
{
}
