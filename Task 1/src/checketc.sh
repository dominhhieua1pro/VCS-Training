#!/bin/bash

TIME=$(date +%T)
DATE=$(date +%d'/'%m'/'%Y)

echo -e "\n\n\n[Log checketc - $TIME $DATE]" >> /var/log/checketc.log

function createFile() {
    if [ ! -e $1 ]; then
        touch $1
    fi
}


function checkTextFile() {
    check=$(file -i $1| grep -w "text/plain")
    if [[ $check ]]; then
        echo $line >> /var/log/checketc.log 
        head -n 10 "$1" >> /var/log/checketc.log
    else 
        echo $1 >> /var/log/checketc.log
    fi 
}


function checkNewFile() {
    old=$1
    current=$2
    while read -r line; do
        check=$(grep -w $line -m 1 $old)
        if [ ! $check ]; then 
            checkTextFile $line >> /var/log/checketc.log
            echo -e "\n" >> /var/log/checketc.log
        fi
    done < $current
}


function checkDeleteFile() { 
    old=$1
    current=$2
    while read -r line; do
        check=$(grep -w $line -m 1 $current)
        if [ ! $check ]; then
            echo $line >> /var/log/checketc.log
        fi
    done < $old
}


listOldFiles='/home/mha3t/Desktop/Task1/checketcfile/listoldfiles.txt'
listCurrentFiles='/home/mha3t/Desktop/Task1/checketcfile/listcurrentfiles.txt'
listCheckFiles='/home/mha3t/Desktop/Task1/checketcfile/listcheckfiles.txt'


#create files check
createFile $listCheckFiles
createFile $listCurrentFiles
createFile $listOldFiles


#write list files
sudo find /etc -type f > $listCurrentFiles
sudo find /etc -type f -cmin -30 > $listCheckFiles


#list new files
echo -e "\n=== Danh sach file tao moi ===\n" >> /var/log/checketc.log
checkNewFile $listOldFiles $listCheckFiles


#list file modified
echo -e "\n\n=== Danh sach file sua doi ===\n" >> /var/log/checketc.log
filesModified=$(sudo find /etc -mmin -30)
echo $filesModified | sed 's/ /\n/g' >> /var/log/checketc.log


#list file deleted
echo -e "\n\n=== Danh sach file bi xoa ===\n" >> /var/log/checketc.log
checkDeleteFile $listOldFiles $listCurrentFiles
cat $listCurrentFiles > $listOldFiles


#send mail to root@localhost
mail -s "Log checketc" root@localhost < /var/log/checketc.log

