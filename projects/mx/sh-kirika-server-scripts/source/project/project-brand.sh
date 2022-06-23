#!/bin/bash
## TITLE ########################################################
## Project Creator v1.0 (2010-10-19).
## Author: Alejandro M. Bernardis (alejandro.bernardis@gmail.com)
#################################################################
# include
#################################################################
source /bin/prjclientadd;
#################################################################
# arguments
#################################################################
if [ "${#catch_cfg_brand}" -eq "0" ];then
    kc_func_log $L_ERROR $KC_ACTION "Brand (finished): Not found";
    exit 2;
fi
#################################################################
# set properties
#################################################################
## brand name
CFG_BRAND=$catch_cfg_brand;
kc_func_log $L_LOG $KC_ACTION "Brand: $CFG_CLIENT";
## direcotry
CFG_DIRECTORY=$CFG_BRAND;
CFG_PATH=$KC_DIR_CLIENTS/$CFG_CLIENT/$CFG_BRAND;
## log
if [ $KC_ACTION = "prjbrandadd" ]; then
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
	if [ $KC_ACTION = "prjbrandadd" ]; then
		kc_func_log $L_ERROR $KC_ACTION "Brand (finished): Already exists";
		exit 3;
	fi
    kc_func_log $L_WARN $KC_ACTION "Brand (direcotry): Already exists";
fi
##################################################################
# exit
##################################################################
if [ $KC_ACTION = "prjbrandadd" ]; then
	kc_func_log $L_LOG $KC_ACTION "Finished: The brand $CFG_BRAND has been created.";
    exit 0;
fi
