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
#################################################################
# validates
#################################################################
CFG_USERNAME_TEST=`egrep -i "^${CFG_USERNAME}:" /etc/passwd`;
if [ "${#CFG_USERNAME_TEST}" -gt "0" ];then
    echo "$CFG_PASSWORD:$CFG_USERNAME" | chpasswd;
else
	kc_func_log $L_ERROR $KC_ACTION "Username (finished): Not exists";
    exit 3;
fi
#################################################################
# exit
#################################################################
kc_func_log $L_LOG $KC_ACTION "Finished: The user $CFG_USERNAME has been deleted.";
exit 0;