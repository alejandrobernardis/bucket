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
if [ "${#catch_cfg_directory}" -eq "0" ];then
    kc_func_log $L_ERROR $KC_ACTION "Directory (finished): Not found";
    exit 1;
fi
#################################################################
# set properties
#################################################################
## directory
CFG_DIRECTORY=$catch_cfg_directory;
kc_func_log $L_LOG $KC_ACTION "Direcotry: $CFG_DIRECTORY";
#################################################################
# validates
#################################################################
if [ -d $CFG_DIRECTORY ]; then
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
                umount $CFG_DIRECTORY/_clients;
				umount $CFG_DIRECTORY/_projects;
				umount $CFG_DIRECTORY/_public;
				umount $CFG_DIRECTORY/_share;
				rm -fR $CFG_DIRECTORY;
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
	kc_func_log $L_ERROR $KC_ACTION "Direcotry (finished): Not exists";
    exit 2;
fi
#################################################################
# exit
#################################################################
kc_func_log $L_LOG $KC_ACTION "Finished: The direcotry $CFG_DIRECTORY has been deleted.";
exit 0;