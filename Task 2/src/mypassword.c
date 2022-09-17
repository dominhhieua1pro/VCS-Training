#include <unistd.h>
#include <pwd.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <shadow.h>
/*
struct spwd {
    char          	*sp_namp;     // user login name
    char          	*sp_pwdp;     // encrypted password
    long int      	sp_lstchg;    // last password change 
    long int      	sp_min;       // days until change allowed
    long int      	sp_max;       // days before change required 
    long int      	sp_warn;      // days warning for expiration 
    long int      	sp_inact;     // days before account inactive 
    long int      	sp_expire;    // date when account expires 
    unsigned long int  sp_flag;      // reserved for future use 
}
*/

char* generate_salt(char salt[]) {
    const char *const seedchars = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
    int i, seedchars_length = strlen(seedchars);
    srand(time(NULL));
    for (i = 0; i < 16; i++) {
        unsigned int seed_rand = rand() % seedchars_length;
        salt[3+i] = seedchars[seed_rand];
    }
    return salt;
}

void remove_user(char user[]) {
    FILE *fptrr, *fptrw;
    fptrr = fopen("/etc/shadow", "r");
    if(fptrr == NULL) {
      printf("Error opening file /etc/shadow\n");   
      exit(1);             
    }
    fptrw = fopen("/tmp/shadow", "w");
    if(fptrw == NULL) {
      printf("Error writing file /tmp/shadow\n");   
      exit(1);             
    }
    char arr[256];
    char *p, *tmp;
    while (fgets(arr, 256, fptrr) != NULL) {
        strcpy(tmp, arr);
        p = strtok(arr, ":");
        if (strcmp(user, p) != 0) {
             fprintf(fptrw, "%s", tmp);
        }
    }
    fclose(fptrr);
    fclose(fptrw);
    remove("/etc/shadow");
    rename("/tmp/shadow", "/etc/shadow");
}

int check_password(char password[], char user[]) {
    struct spwd* shadow = getspnam(user);
    if (shadow != NULL) {
        return strcmp(shadow->sp_pwdp, crypt(password, shadow->sp_pwdp));
    }        
}

int main() {
    char old_password[128], new_password[128], user[] = "userA";
    char salt[20] = "$6$";
    struct spwd *shadow_entry;
    printf("Input old password: ");
    scanf("%s", old_password);
    char shadow_entry_name[128];
    if (!check_password(old_password, user)) {
        while ((shadow_entry = getspent()) != NULL) {
            strcpy(shadow_entry_name, shadow_entry->sp_namp);
            if(!strcmp(shadow_entry_name, user)) {
                break;
            }
        };       
        printf("Enter a new password: ");
        scanf("%s", new_password);
        strcpy(salt, generate_salt(salt));
        char* hash_char = crypt(new_password, salt);
        remove_user(user);
        shadow_entry->sp_pwdp = hash_char;       
        FILE* shadow_file = fopen("/etc/shadow", "a");
        if (!shadow_file) {
            printf("Failed to open file /etc/shadow! Permission denied\n");
            remove("/tmp/shadow");
            return 0;
        }
        if (putspent(shadow_entry, shadow_file) == -1) {
            printf("An error occurred\n");
            return 0;
        }      
        printf("Password updated successfully!!!\n");
        return 1;
    }   
    printf("Password authentication failure\n");
    return 1;
    
//  The getspent() function returns a pointer to the next entry in the shadow password database.
//  The putspent() function writes the contents of the supplied struct spwd *p as a text line in the shadow password file format to stream.
}
