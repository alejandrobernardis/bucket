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
if [ "${#catch_cfg_clientname}" = "0" ];then
	kc_func_log $L_ERROR $KC_ACTION "Client (finished): Not found";
    exit 1;
elif [ "${#catch_cfg_brandname}" = "0" ];then
	kc_func_log $L_ERROR $KC_ACTION "Brand (finished): Not found";
    exit 2;
elif [ "${#catch_cfg_name}" = "0" ];then
	kc_func_log $L_ERROR $KC_ACTION "Project (finished): Not found";
    exit 3;
fi
#################################################################
# set properties
#################################################################
## client
CFG_CLIENTNAME=$catch_cfg_clientname;
kc_func_log $L_LOG $KC_ACTION "Client: $CFG_CLIENTNAME";
## brand
CFG_BRANDNAME=$catch_cfg_brandname;
kc_func_log $L_LOG $KC_ACTION "Brand: $CFG_BRANDNAME";
## project
CFG_PROJECTNAME=$catch_cfg_name;
kc_func_log $L_LOG $KC_ACTION "Brand: $CFG_PROJECTNAME";
## path
CFG_PATH="$KC_FTP_DIR/projects/$CFG_CLIENTNAME/$CFG_BRANDNAME/$CFG_PROJECTNAME";
kc_func_log $L_LOG $KC_ACTION "Path: $CFG_PATH";
#################################################################
# validates
#################################################################
if [ ! -d $CFG_PATH ];then
    mkdir -m 0775 -p $CFG_PATH;
	chown ftp:ftp $CFG_PATH;
	# log
	KC_FILE_PROJECT_PATH=$CFG_PATH/$KC_FILE_PROJECT;
	if [ ! -e $KC_FILE_PROJECT_PATH ]; then
		echo '<?xml version="1.0" encoding="UTF-8"?>' > $KC_FILE_PROJECT_PATH;
		echo "<kcproject>" >> $KC_FILE_PROJECT_PATH;
		echo "	<client>$CFG_CLIENTNAME</client>" >> $KC_FILE_PROJECT_PATH;
		echo "	<brand>$CFG_BRANDNAME</brand>" >> $KC_FILE_PROJECT_PATH;
		echo "	<project>$CFG_PROJECTNAME</project>" >> $KC_FILE_PROJECT_PATH;
		echo "	<date>$(date +%Y/%m/%d)</date>" >> $KC_FILE_PROJECT_PATH;
		echo "</kcproject>" >> $KC_FILE_PROJECT_PATH;
	fi
	kc_func_log $L_LOG $KC_ACTION "Directory: Created";
else
    kc_func_log $L_WARN $KC_ACTION "Directory (finished): Already exists";
	exit 4;
fi
#################################################################
# exit
#################################################################
kc_func_log $L_LOG $KC_ACTION "Finished: The user $CFG_USERNAME has been created.";
exit 0;
