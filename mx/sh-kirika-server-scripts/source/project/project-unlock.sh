#!/bin/bash
## TITLE ########################################################
## Project Creator v1.0 (2010-10-21).
## Author: Alejandro M. Bernardis (alejandro.bernardis@gmail.com)
#################################################################
# include
#################################################################
source /bin/prjbrandadd;
#################################################################
# arguments
#################################################################
if [ "${#catch_cfg_project}" -eq "0" ];then
    kc_func_log $L_ERROR $KC_ACTION "Project (finished): Not found";
    exit 3;
fi
#################################################################
# set properties
#################################################################
## project name
CFG_PROJECT=$catch_cfg_project;
kc_func_log $L_LOG $KC_ACTION "Project: $CFG_PROJECT";
## type
CFG_TYPE=$catch_cfg_type;
kc_func_log $L_LOG $KC_ACTION "Type: $CFG_TYPE";
## direcotry
CFG_DIRECTORY=$CFG_PROJECT;
kc_func_log $L_LOG $KC_ACTION "Direcotry: $CFG_DIRECTORY";
## path
CFG_PATH=$KC_DIR_CLIENTS/$CFG_CLIENT/$CFG_BRAND/$CFG_PROJECT;
kc_func_log $L_LOG $KC_ACTION "Path: $CFG_PATH";
#################################################################
# delete
#################################################################
if [ -d $CFG_PATH ]; then
	chmod 755 $CFG_PATH;
else
	kc_func_log $L_ERROR $KC_ACTION "Project (finished): Not exists";
	exit 4;
fi
#################################################################
# exit
#################################################################
kc_func_log $L_LOG $KC_ACTION "Finished: The project $CFG_PROJECT has been unlocked.";
exit 0;