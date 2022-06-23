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
fi
#################################################################
# set properties
#################################################################
## username
CFG_USERNAME=$catch_cfg_username;
kc_func_log $L_LOG $KC_ACTION "Username: $CFG_USERNAME";
#################################################################
# validates
#################################################################
CFG_USERNAME_TEST=`egrep -i "^${CFG_USERNAME}:" /etc/passwd`;
if [ "${#CFG_USERNAME_TEST}" -gt "0" ];then
    usermod -L $CFG_USERNAME;
else
	kc_func_log $L_ERROR $KC_ACTION "Username (finished): Not exists";
    exit 2;
fi
#################################################################
# exit
#################################################################
kc_func_log $L_LOG $KC_ACTION "Finished: The user $CFG_USERNAME has been locked.";
exit 0;