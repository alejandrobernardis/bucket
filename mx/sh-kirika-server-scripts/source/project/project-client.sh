#!/bin/bash
## TITLE ########################################################
## Project Creator v1.0 (2010-10-19).
## Author: Alejandro M. Bernardis (alejandro.bernardis@gmail.com)
#################################################################
# include
#################################################################
source /bin/kclib/prjcommon.sh;
#################################################################
# arguments
#################################################################
if [ "${#catch_cfg_client}" -eq "0" ];then
    kc_func_log $L_ERROR $KC_ACTION "Client (finished): Not found";
    exit 1;
fi
#################################################################
# set properties
#################################################################
## client name
CFG_CLIENT=$catch_cfg_client;
kc_func_log $L_LOG $KC_ACTION "Client: $CFG_CLIENT";
## direcotry
CFG_DIRECTORY=$CFG_CLIENT;
CFG_PATH=$KC_DIR_CLIENTS/$CFG_CLIENT;
## log
if [ $KC_ACTION = "prjclientadd" ]; then
	kc_func_log $L_LOG $KC_ACTION "Direcotry: $CFG_DIRECTORY";
	kc_func_log $L_LOG $KC_ACTION "Path: $CFG_PATH";
fi
##################################################################
# create
##################################################################
if [ ! -d $CFG_PATH ]; then
    mkdir -m 0755 -p $CFG_PATH;
    chown $KC_SYS_USER:$KC_SYS_GROUP $CFG_PATH;
else
	if [ $KC_ACTION = "prjclientadd" ]; then
		kc_func_log $L_ERROR $KC_ACTION "Client (finished): Already exists";
		exit 2;
	fi
    kc_func_log $L_WARN $KC_ACTION "Client (direcotry): Already exists";
fi
##################################################################
# exit
##################################################################
if [ $KC_ACTION = "prjclientadd" ]; then
	kc_func_log $L_LOG $KC_ACTION "Finished: The client $CFG_CLIENT has been created.";
    exit 0;
fi
