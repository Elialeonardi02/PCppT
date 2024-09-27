#include "C:\!!BITBUCKET\11l-lang\_11l_to_cpp\11l.hpp"

class SierpinskiCurve
{
public:
    double x;
    template <typename T1> auto line(const T1 &out)
    {
        out.write(u" L#."_S.format(gconvfmt(x)));
    }
};

int main()
{
}
