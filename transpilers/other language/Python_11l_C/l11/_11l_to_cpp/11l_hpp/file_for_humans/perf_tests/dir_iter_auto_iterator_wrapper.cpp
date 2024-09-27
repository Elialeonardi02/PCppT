#include <windows.h>
#include <iostream>
#include <optional>
#include <string>

class DirIter
{
    HANDLE search_handle;
    bool files_only;
    std::u16string cur_name;

    DirIter(const DirIter &) = delete;
    void operator=(const DirIter &) = delete;

    bool check_filedata(const WIN32_FIND_DATAW &file_data)
    {
        if (!(file_data.dwFileAttributes&FILE_ATTRIBUTE_DIRECTORY) || (wcscmp(file_data.cFileName, L".") != 0
                                                                    && wcscmp(file_data.cFileName, L"..") != 0))
            if (!files_only || !(file_data.dwFileAttributes&FILE_ATTRIBUTE_DIRECTORY)) {
                cur_name = (char16_t*)file_data.cFileName;
                return true;
            }
        return false;
    }

public:
    DirIter(const std::u16string &path, bool files_only, bool &empty) : files_only(files_only)
    {
        WIN32_FIND_DATAW file_data;
        if ((search_handle = FindFirstFileW((wchar_t*)(path + u"\\*.*").c_str(), &file_data)) != INVALID_HANDLE_VALUE)
            if (check_filedata(file_data))
                empty = false;
            else
                empty = !advance();
    }
    DirIter(DirIter &&d) :
        search_handle(d.search_handle),
        files_only(d.files_only),
        cur_name(std::move(d.cur_name))
    {
        d.search_handle = INVALID_HANDLE_VALUE;
    }
    ~DirIter()
    {
        if (search_handle != INVALID_HANDLE_VALUE)
            FindClose(search_handle);
    }

    const std::u16string &current()
    {
        return cur_name;
    }

    bool advance()
    {
        WIN32_FIND_DATAW file_data;
        while (FindNextFileW(search_handle, &file_data))
            if (check_filedata(file_data))
                return true;

        FindClose(search_handle);
        search_handle = INVALID_HANDLE_VALUE;
        return false;
    }
};

std::optional<DirIter> walk_dir(const std::u16string &path, bool files_only = true)
{
    bool empty = true;
    DirIter r(path, files_only, empty);
    if (empty)
        return std::nullopt;
    return r;
}

class Sentinel
{
};

template <class Iter> class Iterator
{
    std::optional<Iter> iter;
    bool has_next;

public:
    Iterator(std::optional<Iter> &&iter) : iter(std::move(iter)) {has_next = this->iter.has_value();}

    bool operator!=(Sentinel) const {return has_next;}

    auto &operator*() {return iter->current();}
    void operator++() {has_next = iter->advance();}
};

template <class Iter> auto begin(std::optional<Iter> &iter) // [на мысль заменить `&&` на `&` меня навела реализация `std::filesystem::begin(directory_iterator)` (хотя там `&` вообще отсутствует)]
{
    return Iterator(std::move(iter));
}
template <class Iter> auto end(std::optional<Iter> &iter)
{
    return Sentinel();
}

int main()
{

    for (auto &&fname : walk_dir(u"."))
        std::wcout << (std::wstring&)fname << L"\n";

}
