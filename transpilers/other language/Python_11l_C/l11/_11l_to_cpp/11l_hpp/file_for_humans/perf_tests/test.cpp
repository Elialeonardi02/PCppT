#include "../IFile.hpp"

void f(IFile &&f)
{
    while (!f.at_eof())
        puts(f.read_line(true).c_str());
}

int main()
{
    f(IFile("../копия.tgitconfig"));
}

