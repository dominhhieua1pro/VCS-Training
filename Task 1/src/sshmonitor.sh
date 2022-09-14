#!/bin/bash

touch OldList.txt NewList.txt Mail.txt

cat /var/log/auth.log | grep "(sshd:session): session opened" > NewList.txt

while read -r line;
do
    checkOldList=$(grep '$line' -m 1 OldList.txt)
    if [ ! $checkOldList ]; then
        echo -e "User" "$(echo $line | awk '{print $11}')" "dang nhap thanh cong vao thoi gian" "$(echo $line | awk '{print $3}') $(echo $line | awk '{print $1 $2}')" > Mail.txt
    fi
done < NewList.txt

cat NewList.txt > OldList.txt

cat Mail.txt | mail -s "SSH login log" root@localhost

