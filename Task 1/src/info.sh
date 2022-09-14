#!/bin/bash

echo "[Thong tin he thong]"

PCNAME=$(hostname)
echo "Ten may: $PCNAME"

RELEASE=$(lsb_release -d | cut -f2)
echo "Ten ban phan phoi: $RELEASE"

CPUNAME=$(lscpu | grep "Model name" | cut -c24-)
ARCHITECTURE=$(lscpu | grep "Architecture" | cut -c24-)
SPEED=$(lscpu | grep "CPU MHz" | cut -c24-)
echo -e "Thong tin CPU: \nTen CPU: $CPUNAME \nKien truc CPU: $ARCHITECTURE \nToc do CPU MHz: $SPEED\n"

DISKINFO=$(df -h | grep "dev/sda")
echo -e "Thong tin bo nho o dia: \n$DISKINFO\n"

IPLIST=$(ip addr show | grep "inet" | cut -ds -f1)
echo -e "Danh sach dia chi IP tren he thong: \n$IPLIST\n"

USERLIST=$(sudo awk -F: '{print $1}' /etc/passwd | sort)
echo -e "Danh sach user tren he thong: \n$USERLIST\n"

ROOTPROCESS=$(ps -U root -u root)
echo -e "Thong tin cac tien trinh dang chay voi quyen root: \n$ROOTPROCESS\n"

PORTOPEN=$(ss -lnptu | grep "LISTEN" | sort -r -k 6)
echo -e "Thong tin cac port dang mo: \n$PORTOPEN\n"

LIST10=$(find / -type d -perm /o=w)
echo -e "Danh sach cac thu muc tren he thong cho phep other co quyen ghi: \n$LIST10\n"

LIST11=$(dpkg-query -W)
echo -e "Danh sach cac goi phan mem duoc cai dat tren he thong: \n$LIST11\n"

