#!/bin/bash
## TITLE ########################################################
## FTP Admin v1.0 (2010-10-11).
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
elif [ "${#catch_cfg_expiredate}" -eq "0" ];then
	kc_func_log $L_ERROR $KC_ACTION "Expire Date (finished): Not found";
    exit 2;
fi
#################################################################
# set properties
#################################################################
## username
CFG_USERNAME=$catch_cfg_username;
kc_func_log $L_LOG $KC_ACTION "Username: $CFG_USERNAME";
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
CFG_USERNAME_TEST=`egrep -i "^${CFG_USERNAME}:" /etc/passwd`;
if [ "${#CFG_USERNAME_TEST}" -gt "0" ];then
	## expire date
	if [[ $CFG_EXPIREDATE =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]];then
		usermod -e $CFG_EXPIREDATE $CFG_USERNAME;
	else
		kc_func_log $L_ERROR $KC_ACTION "Expire Date (finished): Not found";
    	exit 3;
	fi
else
	kc_func_log $L_ERROR $KC_ACTION "Username (finished): Not exists";
    exit 4;
fi
#################################################################
# exit
#################################################################
kc_func_log $L_LOG $KC_ACTION "Finished: The user $CFG_USERNAME has been changed.";
exit 0;