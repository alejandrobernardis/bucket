#!/bin/bash
## TITLE ########################################################
## FTP Admin v1.0 (2010-10-09).
## Author: Alejandro M. Bernardis (alejandro.bernardis@gmail.com)
#################################################################
# include
#################################################################
source /bin/kclib/ftpcommon.sh;
#################################################################
# arguments
#################################################################
if [ "${#catch_cfg_username}" = "0" ];then
    kc_func_log $L_ERROR $KC_ACTION "Username (finished): Not found";
    exit 1;
elif [ "${#catch_cfg_password}" = "0" ];then
	kc_func_log $L_ERROR $KC_ACTION "Password (finished): Not found";
    exit 2;
elif [ "${#catch_cfg_clientname}" = "0" ];then
	kc_func_log $L_ERROR $KC_ACTION "Client (finished): Not found";
    exit 3;
elif [ "${#catch_cfg_brandname}" = "0" ];then
	kc_func_log $L_ERROR $KC_ACTION "Brand (finished): Not found";
    exit 4;
fi
#################################################################
# set properties
#################################################################
## username
CFG_USERNAME=$catch_cfg_username;
kc_func_log $L_LOG $KC_ACTION "Username: $CFG_USERNAME";
## password
CFG_PASSWORD=$catch_cfg_password;
kc_func_log $L_LOG $KC_ACTION "Password: xxxxxx";
## client
CFG_CLIENTNAME=$catch_cfg_clientname;
kc_func_log $L_LOG $KC_ACTION "Client: $CFG_CLIENTNAME";
## brand
CFG_BRANDNAME=$catch_cfg_brandname;
kc_func_log $L_LOG $KC_ACTION "Brand: $CFG_BRANDNAME";
## directory
if [ $catch_cfg_directory ];then 
	CFG_DIRECTORY=$catch_cfg_directory;
else 
	CFG_DIRECTORY=""; 
fi
kc_func_log $L_LOG $KC_ACTION "Direcotry: $CFG_DIRECTORY";
## path
CFG_PATH=$KC_FTP_DIR/clients/$CFG_CLIENTNAME/$CFG_BRANDNAME;
kc_func_log $L_LOG $KC_ACTION "Path: $CFG_PATH";
## expire date
if [ $catch_cfg_expiredate ];then 
	CFG_EXPIREDATE=$catch_cfg_expiredate;
else 
	CFG_EXPIREDATE=""; 
fi
kc_func_log $L_LOG $KC_ACTION "Expire date: $CFG_EXPIREDATE";
#################################################################
# validates
#################################################################
if [ ! -d $CFG_PATH ];then
    mkdir -m 0755 -p $CFG_PATH;
	kc_func_log $L_LOG $KC_ACTION "Directory: Created";
else
    kc_func_log $L_WARN $KC_ACTION "Directory: Already exists";
fi
#
CFG_DIRECTORY=$CFG_PATH/$CFG_DIRECTORY;
if [ ! -d $CFG_DIRECTORY ];then
	mkdir -m 0775 -p $CFG_DIRECTORY;
	kc_func_log $L_LOG $KC_ACTION "Directory (optional): Created";
else
    kc_func_log $L_WARN $KC_ACTION "Directory (optional): Already exists";
fi
#################################################################
# create user
#################################################################
CFG_USERNAME_TEST=`egrep -i "^${CFG_USERNAME}:" /etc/passwd`;
if [ "${#CFG_USERNAME_TEST}" -eq "0" ];then
	## create user
    useradd -g ftpclients -d $CFG_PATH -s /bin/ftp -c "Client FTP User" $CFG_USERNAME;
	## set password
	echo "$CFG_USERNAME:$CFG_PASSWORD" | chpasswd;
	## expire date
	if [[ $CFG_EXPIREDATE =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]];then
		usermod -e $CFG_EXPIREDATE $CFG_USERNAME;
	fi
	## owner & permissions
	chown -R $CFG_USERNAME:ftpclients $CFG_PATH;
else
	kc_func_log $L_ERROR $KC_ACTION "Username (finished): Already exists";
    exit 5;
fi
#################################################################
# exit
#################################################################
kc_func_log $L_LOG $KC_ACTION "Finished: The user $CFG_USERNAME has been created.";
exit 0;