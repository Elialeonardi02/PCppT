#include "C:\!!BITBUCKET\11l-lang\_11l_to_cpp\11l.hpp"

struct CodeBlock1
{
    CodeBlock1()
    {
        print(Fraction(3));
        print(Fraction(2, 4));
        uR"(
def generating_function(n):
    return sum((-n)**i for i in range(DEGREE + 1))

def optimum_polynomial(k, n):
    # Lagrange interpolation
    sum = fractions.Fraction(0)
    for i in range(k + 1):
        product = fractions.Fraction(generating_function(i))
        for j in range(1, k + 1):
            if j != i:
                product *= fractions.Fraction(n - j, i - j)
        sum += product
    return sum


DEGREE = 10
ans = fractions.Fraction(0)
for k in range(1, DEGREE + 1):
    for n in itertools.count(k + 1):
        if n == DEGREE + 2:
            raise AssertionError()
        reference = fractions.Fraction(generating_function(n))
        term = optimum_polynomial(k, n)
        if term != reference:
            ans += term
            break
print(ans)
)"_S;
    }
} code_block_1;

int main()
{
}
