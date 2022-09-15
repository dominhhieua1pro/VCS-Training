       #include <pwd.h>
       #include <stdint.h>
       #include <stdio.h>
       #include <stdlib.h>
       #include <unistd.h>
       #include <errno.h>

       int main()
       {
           char user[100];
           printf("Enter user: ");
           scanf("%s", user);
           struct passwd *userinfo;;
           userinfo = getpwnam(user);
           if(!userinfo) {
               printf("User not found!");
           } 

//           printf("Name: %s; UID: %jd\n", pwd.pw_gecos, (intmax_t) pwd.pw_uid);
           exit(EXIT_SUCCESS);
       }
