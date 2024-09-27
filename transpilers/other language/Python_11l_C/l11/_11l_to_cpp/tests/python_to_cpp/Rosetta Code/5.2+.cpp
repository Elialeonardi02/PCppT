#include "C:\!!BITBUCKET\11l-lang\_11l_to_cpp\11l.hpp"

auto l = create_array(range_ee(u'A'_C, u'Z'_C)) + create_array(range_ee(u'0'_C, u'9'_C));

template <typename T1, typename T2> auto pop_fast(T1 &li, const T2 &i)
{
    auto r = li[i];
    li.set(i, li.last());
    li.pop();
    return r;
}

struct CodeBlock1
{
    CodeBlock1()
    {
        for (int Lindex = 0; Lindex < 6; Lindex++) {
            for (int Lindex = 0; Lindex < 6; Lindex++) {
                auto rnd = randomns::_(l.len());
                print(pop_fast(l, rnd), u" "_S);
            }
            print();
        }
    }
} code_block_1;

int main()
{
}
