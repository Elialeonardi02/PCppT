//#include <sys/syscall.h>
//#include <linux/stat.h>

#include "IFile.hpp"
#include "OFile.hpp"
#include <time.h>
#include <iostream>
#include <sys/syscall.h>
#include <linux/stat.h>

int main()
{
    IFile f;
    f = IFile("test.dat", strlen("test.dat"));

    OFile of;of = OFile("test2.dat");
/*
    //std::cout << f.read_line(true);

//  f.peek_byte();

    //for (int i = 0; i < 1024;i++)
    //f.seek(f.get_file_size());

    for (;;) {
        auto a = f.read_bytes_at_most(rand()%4096);
        if (a.empty())
            break;
        of.write(a);
    }
*/
   detail::FileHandle<false>("/home/tav/1").set_last_write_time(IFile("utf.hpp").get_last_write_time());
//    try {
    // utf::as_str8(std::u16string_view(u"abc"));
    // IFile f("копия.tgitconfig");
    // while (!f.at_eof())
    //     puts(f.read_line(true).c_str());
    //IFile fh("utf.hpp");
    detail::FileHandle<true> fh("/home/tav/1");
    //fh.fd = STDIN_FILENO;
    printf("%i\n", (int)fh.get_file_size());
    // fh.
    char buff[20];
    struct tm * timeinfo;
    time_t mtime = fh.get_creation_time().to_time_t();
    timeinfo = localtime(&mtime);
    strftime(buff, sizeof(buff), "%Y-%m-%d %H:%M:%S", timeinfo);
    puts(buff);
  /*  }
    catch(...)
    {
       //printf(__cxxabiv1::__cxa_current_exception_type()->name().c_str());
    }*/
}
