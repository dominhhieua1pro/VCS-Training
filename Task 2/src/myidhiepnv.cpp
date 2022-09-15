#include <iostream>
#include <pwd.h>
#include <grp.h>
#include <string>
#include <unistd.h>
using namespace std;

int main() {
    string user;
    struct passwd *entry;
    cin >> user;
    entry = getpwnam(user.c_str());
    int ngroups = 0;
    if (!entry) {
        cout << "Not found user" << endl;
        return 0;    
    }
    cout << "username: " << entry->pw_name << endl;
    cout << "home directory: " << entry->pw_dir << endl;
    cout << "user id: " << entry->pw_uid << endl;
    group* gr = getgrgid(entry->pw_gid);
    getgrouplist(entry->pw_name, entry->pw_gid, NULL, &ngroups);
    __gid_t groups[ngroups];
    getgrouplist(entry->pw_name, entry->pw_gid, groups, &ngroups);
    cout << "groups: ";
    for (int i = 0; i < ngroups; i++) {
        struct group* gr = getgrgid(groups[i]);
        cout << gr->gr_name << " ";
    }
    cout << endl;
    return 0;
}
