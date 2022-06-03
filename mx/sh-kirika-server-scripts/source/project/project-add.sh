#!/bin/bash
## TITLE ########################################################
## Project Creator v1.0 (2010-10-19).
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
if [ "${#catch_cfg_type}" -eq "0" ];then
	CFG_TYPE="full";
else
	CFG_TYPE=$catch_cfg_type;    
fi
kc_func_log $L_LOG $KC_ACTION "Type: $CFG_TYPE";
## direcotry
CFG_DIRECTORY=$CFG_PROJECT;
kc_func_log $L_LOG $KC_ACTION "Direcotry: $CFG_DIRECTORY";
# path
CFG_PATH=$KC_DIR_CLIENTS/$CFG_CLIENT/$CFG_BRAND/$CFG_PROJECT;
kc_func_log $L_LOG $KC_ACTION "Path: $CFG_PATH";
#################################################################
# create
#################################################################
if [ -d $CFG_PATH ]; then
	kc_func_log $L_ERROR $KC_ACTION "Project (finished): Already exists";
	exit 4;
fi
if [ "$CFG_TYPE" = "empty" ]; then
	mkdir -m 0777 -p $CFG_PATH;
else
	# basedir
	mkdir -m 0755 -p $CFG_PATH;
	mkdir -m 0755 -p $CFG_PATH/01_Documentation;
	mkdir -m 0755 -p $CFG_PATH/02_Production;
	mkdir -m 0755 -p $CFG_PATH/03_Deploy;
	# documentation
	mkdir -m 0777 -p $CFG_PATH/01_Documentation/01_Reference;
	mkdir -m 0777 -p $CFG_PATH/01_Documentation/02_Research+Planning;
	mkdir -m 0777 -p $CFG_PATH/01_Documentation/03_MediaPlanning;
	mkdir -m 0777 -p $CFG_PATH/01_Documentation/04_CreativeBrief;
	mkdir -m 0777 -p $CFG_PATH/01_Documentation/05_ProductionBrief;
	# creativity
	mkdir -m 0755 -p $CFG_PATH/02_Production/01_Creativity;	
	mkdir -m 0777 -p $CFG_PATH/02_Production/01_Creativity/ai;
	mkdir -m 0777 -p $CFG_PATH/02_Production/01_Creativity/flash;
	mkdir -m 0777 -p $CFG_PATH/02_Production/01_Creativity/fonts;
	mkdir -m 0777 -p $CFG_PATH/02_Production/01_Creativity/images;
	mkdir -m 0777 -p $CFG_PATH/02_Production/01_Creativity/psd;
	mkdir -m 0777 -p $CFG_PATH/02_Production/01_Creativity/sound;
	mkdir -m 0777 -p $CFG_PATH/02_Production/01_Creativity/video;
	# development
	mkdir -m 0755 -p $CFG_PATH/02_Production/02_Development;
	mkdir -m 0755 -p $CFG_PATH/02_Production/02_Development/01_ClientSide;
	mkdir -m 0777 -p $CFG_PATH/02_Production/02_Development/01_ClientSide/assets;
	mkdir -m 0777 -p $CFG_PATH/02_Production/02_Development/01_ClientSide/lib;
	mkdir -m 0777 -p $CFG_PATH/02_Production/02_Development/01_ClientSide/src;
	mkdir -m 0755 -p $CFG_PATH/02_Production/02_Development/02_ServerSide;
	mkdir -m 0777 -p $CFG_PATH/02_Production/02_Development/02_ServerSide/application;
	mkdir -m 0777 -p $CFG_PATH/02_Production/02_Development/02_ServerSide/library;
	mkdir -m 0777 -p $CFG_PATH/02_Production/02_Development/02_ServerSide/public;
	# deploy
	mkdir -m 0777 -p $CFG_PATH/03_Deploy/backup;
	mkdir -m 0777 -p $CFG_PATH/03_Deploy/last;
	## Public
	if [ ! -d $KC_DIR_PUBLIC ]; then
		mkdir -m 0755 -p $KC_DIR_PUBLIC;
	fi
	ln -s "$CFG_PATH/03_Deploy/last" "$KC_DIR_PUBLIC/$CFG_CLIENT-$CFG_BRAND-$CFG_PROJECT";
	## Projects
	if [ ! -d $KC_DIR_PROJECTS ]; then
		mkdir -m 0755 -p $KC_DIR_PROJECTS;
	fi	
	ln -s $CFG_PATH "$KC_DIR_PROJECTS/$CFG_CLIENT-$CFG_BRAND-$CFG_PROJECT";
fi
#################################################################
# log
#################################################################
CFG_KC_FILE_PROJECT=$CFG_PATH/$KC_FILE_PROJECT;
if [ ! -f $CFG_KC_FILE_PROJECT ]; then
	echo '<?xml version="1.0" encoding="UTF-8"?>' > $CFG_KC_FILE_PROJECT;
	echo "<kcproject>" >> $CFG_KC_FILE_PROJECT;
	echo "	<client>$CFG_CLIENT</client>" >> $CFG_KC_FILE_PROJECT;
	echo "	<brand>$CFG_BRAND</brand>" >> $CFG_KC_FILE_PROJECT;
	echo "	<project>$CFG_PROJECT</project>" >> $CFG_KC_FILE_PROJECT;
	echo "	<date>$(date +%Y/%m/%d)</date>" >> $CFG_KC_FILE_PROJECT;
	echo "</kcproject>" >> $CFG_KC_FILE_PROJECT;
fi
##################################################################
# exit
##################################################################
kc_func_log $L_LOG $KC_ACTION "Finished: The project $CFG_PROJECT has been created.";
exit 0;




