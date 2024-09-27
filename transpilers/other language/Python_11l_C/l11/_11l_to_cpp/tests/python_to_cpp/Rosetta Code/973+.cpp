#include <math.h>
#include <iostream>
#include <vector>

int main()
{
    int k=1000000;
    //std::cin >> k;
    int n = k * 17;
    std::vector<char> primes(n, true);
    primes[0] = primes[1] = false;

    for (int i = 2, ii = sqrt(n); i <= ii; i++) {
        if (!primes[i])
            continue;

        for (int j = i * i; j < n; j += i)
            primes[j] = false;
    }

    for (int i = 0; ; i++)
        if (primes[i]) {
            if (k == 1) {
                std::cout << i << "\n";
                break;
            }
            k--;
        }
}
