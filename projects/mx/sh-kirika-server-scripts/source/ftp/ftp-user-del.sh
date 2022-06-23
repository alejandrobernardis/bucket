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
	echo "";
    echo "Are you sure?";
    declare -a options;
    options[${#options[*]}]="No";
    options[${#options[*]}]="Yes";
    select opt in "${options[@]}"; do
        case ${opt} in
            ${options[0]})
				echo "";
				kc_func_log $L_WARN $KC_ACTION "Option (finished): Canceled";
				exit 2;
				;;
			${options[1]})
                userdel -f $CFG_USERNAME;
                break;
                ;;
            *)
				echo "";
				kc_func_log $L_WARN $KC_ACTION "Option (finished): Not found";
                exit 3;
                ;;
        esac;
    done
	echo "";
else
	kc_func_log $L_ERROR $KC_ACTION "Username (finished): Not exists";
    exit 4;
fi
#################################################################
# exit
#################################################################
kc_func_log $L_LOG $KC_ACTION "Finished: The user $CFG_USERNAME has been deleted.";
exit 0;