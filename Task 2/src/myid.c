#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main ()
{
    char username[100];
    printf("Nhap username: ");
    scanf("%s", username);
    char command[5][256];
//    printf("Thong tin user ");
    snprintf(command[0], sizeof(command[0]), "sudo cat /etc/passwd | grep -w %s | cut -d: -f1", username);
//    strcpy(listUser,username);
//    strcpy(command, "sudo cat /etc/passwd | grep -w %s | cut -d':' -f1", username );
//    system("username="listUser);
//    system(command[0]);
//    printf("\n%d\n",checkUser);
//    system() returns 0 if successful
    char checkUser = system(command[0]);
    fprintf (stdout, "system ret: [%d] \n", checkUser >> 8); 
//    printf("%s",checkUser);
    if (system(NULL)) {
//        printf("Thong tin user %s \n", username);
        printf("\nuid: ");
        snprintf(command[1], sizeof(command[1]), "sudo cat /etc/passwd | grep -w %s | cut -d: -f3", username);
        system(command[1]);
        printf("\nusername: ");
        snprintf(command[2], sizeof(command[2]), "sudo cat /etc/passwd | grep -w %s | cut -d: -f1", username);
        system(command[2]);
        printf("\nhome directory: ");
        snprintf(command[3], sizeof(command[2]), "sudo cat /etc/passwd | grep -w %s | cut -d: -f6", username);
        system(command[3]);
        printf("\ngroups: ");
        strcpy(command[4], "groups");
        system(command[4]);
    } else {
        printf("Khong tim thay user %s", username);
    }
    return(0);
} 
