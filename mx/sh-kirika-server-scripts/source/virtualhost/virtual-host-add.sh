#!/bin/bash
## TITLE ########################################################
## Virtual Host Creator v1.0 (2010-10-21).
## Author: Alejandro M. Bernardis (alejandro.bernardis@gmail.com)
#################################################################
# include
#################################################################
#source /bin/kclib/vpcommon.sh;
source `pwd`/virtual-host-common.sh;
#################################################################
# arguments
#################################################################
if [ "${#catch_cfg_domain}" -eq "0" ];then
    kc_func_log $L_ERROR $KC_ACTION "Domain (finished): Not found";
    exit 1;
fi
#################################################################
# set properties
#################################################################
## domain name
CFG_DOMAIN=$catch_cfg_domain;
kc_func_log $L_LOG $KC_ACTION "Domain: $CFG_DOMAIN";
## path
declare -a CFG_PATH_TMP
CFG_PATH_TMP=(`echo $CFG_DOMAIN | tr '.' ' '`);
if [ ${#CFG_PATH_TMP[@]} -gt "2" ]; then
	CFG_PATH=${CFG_PATH_TMP[2]}/${CFG_PATH_TMP[1]}/${CFG_PATH_TMP[0]};
else
	CFG_PATH=${CFG_PATH_TMP[1]}/${CFG_PATH_TMP[0]};
fi
kc_func_log $L_LOG $KC_ACTION "Path: $CFG_PATH";
#################################################################
# validate
#################################################################
if [ ! -e $KC_DIR_SITES_AVAILABLE/$CFG_DOMAIN ]; then
	# path: live & staging
	mkdir -m 0775 -p $KC_DIR_HOME/$CFG_PATH/live/htdocs;
	mkdir -m 0775 -p $KC_DIR_HOME/$CFG_PATH/staging/htdocs;
	# file 	
	sed -e "s/@domain@/$CFG_DOMAIN/g" $KC_LIB/virtualhost.config > $KC_DIR_SITES_AVAILABLE/$CFG_DOMAIN.temp;
	sed -e "s/@path@/$CFG_PATH/g" $KC_DIR_SITES_AVAILABLE/$CFG_DOMAIN.temp > $KC_DIR_SITES_AVAILABLE/$CFG_DOMAIN;
else 
	kc_func_log $L_WARN $KC_ACTION "Domain: Already exists";
fi








