#!/bin/bash

# add userA to system if non-exist
if [[ -z `cat /etc/passwd | awk '{print $1}' | grep "userA"` ]]; then
    useradd userA -d /home/userA -m -s /bin/bash
fi

# set default password is "userA" to userA with SHA512 crypt-method
echo 'userA:userA' | chpasswd -c SHA512

# add userA to group sudo to run sudoer files
usermod -aG sudo userA
