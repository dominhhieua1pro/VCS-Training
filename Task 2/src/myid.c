#include <stdio.h>
#include <stdlib.h>

#include <pwd.h>
/*
struct passwd {
    char *pw_name;
    char *pw_passwd;
    uid_t pw_uid;
    gid_t pw_gid;
    time_t pw_change;
    char *pw_class;
    char *pw_gecos;
    char *pw_dir;
    char *pw_shell;
    time_t pw_expire;
}; 
*/

#include <grp.h>
/*
struct group {
    char *gr_name;
    char *gr_passwd;
    gid_t gr_gid;
    char **gr_mem;
};
*/

int main()
{
    int i;
    char user[100];
    printf("Enter user: ");
    scanf("%s", user);
    struct passwd *userinfo;
    struct group *gr;

    userinfo = getpwnam(user);

    if(!userinfo) {
        printf("User %s not found!\n", user);
        exit(EXIT_SUCCESS);
    }

    printf("User ID: %d", userinfo->pw_uid);
    printf("\nUsername: %s", userinfo->pw_name);
    printf("\nHome Directory: %s", userinfo->pw_dir);

    int ngroups = 0; // number of groups
    getgrouplist(userinfo->pw_name, userinfo->pw_gid, NULL, &ngroups); // return -1 due to the user is a member of more than *ngroups groups (current ngroups = 0)
/*
    getgrouplist() stores an array of GroupID to 'groups' and number of these groups to ngroups if the number of groups of which user is a member <= *ngroups passed
    then, the value returned in *ngroups can be used to resize the buffer passed to a further call getgrouplist().
*/
    gid_t groups[ngroups]; // declare an array of GroupID
    getgrouplist(userinfo->pw_name, userinfo->pw_gid, groups, &ngroups);
    
    printf("\nGroups: ");
    for (i = 0; i < ngroups; i++) {
        gr = getgrgid(groups[i]); // returns pointer to group struct (get the group ID's info struct)
        if (gr != NULL)
            printf("%s ", gr->gr_name);
    }
    printf("\n");
        
    exit(EXIT_SUCCESS);
}
