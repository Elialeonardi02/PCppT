#include "C:\!!BITBUCKET\11l-lang\_11l_to_cpp\11l.hpp"

auto k = 1000000;
auto n = k * 17;
auto primes = create_array({true}) * n;

struct CodeBlock1
{
    CodeBlock1()
    {
        _set<0>(primes, _set<1>(primes, false));

        for (auto i : range_ee(2, to_int(sqrt(n)))) {
            if (!primes[i])
                continue;
            for (auto j : range_el(i * i, n).step(i))
                primes.set(j, false);
        }

        for (auto i : range_el(0, n))
            if (primes[i]) {
                if (k == 1) {
                    print(i);
                    break;
                }
                k--;
            }
    }
} code_block_1;

int main()
{
}
