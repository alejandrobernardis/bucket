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
if [ "${#catch_cfg_username}" -eq "0" ];then
    kc_func_log $L_ERROR $KC_ACTION "Username (finished): Not found";
    exit 1;
elif [ "${#catch_cfg_password}" -eq "0" ];then
	kc_func_log $L_ERROR $KC_ACTION "Password (finished): Not found";
    exit 2;
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
## directory
if [ $catch_cfg_directory ];then 
	CFG_DIRECTORY=$catch_cfg_directory;
else 
	CFG_DIRECTORY=$CFG_USERNAME; 
fi
kc_func_log $L_LOG $KC_ACTION "Direcotry: $CFG_DIRECTORY";
## path
CFG_PATH=$KC_FTP_DIR/clarus/$CFG_DIRECTORY;
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
	## directories
    mkdir -m 0755 -p $CFG_PATH;
	mkdir -m 0755 -p $CFG_PATH/_clients;
	mkdir -m 0777 -p $CFG_PATH/_public;
	mkdir -m 0755 -p $CFG_PATH/_projects;
	mkdir -m 0775 -p $CFG_PATH/_share;
	kc_func_log $L_LOG $KC_ACTION "Directory: Created";
	## owner & permissions
	chown ftp:ftp $CFG_PATH/*;
	kc_func_log $L_LOG $KC_ACTION "Directory: Set owner and group";
	## mount
	kc_func_mount $KC_FTP_DIR/clarus/share $CFG_PATH/_share "Share folder";
	kc_func_mount $KC_FTP_DIR/clients $CFG_PATH/_clients "Clients folder";
	kc_func_mount $KC_FTP_DIR/projects $CFG_PATH/_projects "Projects folder";
	kc_func_mount $KC_FTP_DIR/public $CFG_PATH/_public "Public folder";
else
    kc_func_log $L_WARN $KC_ACTION "Directory: Already exists";
fi
#################################################################
# create user
#################################################################
CFG_USERNAME_TEST=`egrep -i "^${CFG_USERNAME}:" /etc/passwd`;
if [ "${#CFG_USERNAME_TEST}" -eq "0" ];then
	## create user
    useradd -g ftp -d $CFG_PATH -s /bin/ftp -c "Clarus FTP User" $CFG_USERNAME;
	## set password
	echo "$CFG_USERNAME:$CFG_PASSWORD" | chpasswd;
	## expire date
	if [[ $CFG_EXPIREDATE =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]];then
		usermod -e $CFG_EXPIREDATE $CFG_USERNAME;
	fi
	## owner & permissions
	chown $CFG_USERNAME:ftp $CFG_PATH;	
else
	kc_func_log $L_ERROR $KC_ACTION "Username (finished): Already exists";
    exit 3;
fi
#################################################################
# exit
#################################################################
kc_func_log $L_LOG $KC_ACTION "Finished: The user $CFG_USERNAME has been created.";
exit 0;