#include "C:\!!BITBUCKET\11l-lang\_11l_to_cpp\11l.hpp"

auto k = 1000000;
auto n = k * 17;
auto primes = create_array({true}) * n;

struct CodeBlock1
{
    CodeBlock1()
    {
        _set<0>(primes, _set<1>(primes, false));
    }
} code_block_1;

auto i = 2;
auto ii = to_int(sqrt(n)) + 1;

struct CodeBlock2
{
    CodeBlock2()
    {
        while (i < ii) {
            if (!primes[i]) {
                i++;
                continue;
            }
            auto j = i * i;
            while (j < n) {
                primes.set(j, false);
                j += i;
            }
            i++;
        }

        i = 0;
        while (i < n) {
            if (primes[i]) {
                if (k == 1) {
                    print(i);
                    break;
                }
                k--;
            }
            i++;
        }
    }
} code_block_2;

int main()
{
}
