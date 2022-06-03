#!/bin/bash
## TITLE ########################################################
## Project Creator v1.0 (2010-10-09).
## Author: Alejandro M. Bernardis (alejandro.bernardis@gmail.com)
#################################################################
# Consts
#################################################################
KC_ACTION=$(basename $0);
KC_ACTION=${KC_ACTION%".sh"};
KC_ACTION=${KC_ACTION//"-"/""};
KC_LIB=/bin/kclib;
KC_LOG=1;
KC_LOG_DIR=/var/log/kclib;
KC_VERBOSE=0;
#################################################################
# Logging
#################################################################
## consts
L_LOG="LOG";
L_INFO="INFO";
L_WARN="WARN";
L_ERROR="ERROR";
## function
# $1: Nivel (LOG, INFO, WARN, ERROR).
# $2: Entorno.
# $3: Mensaje.
function kc_func_log {
    LOG_VALUE="$(date +%Y\/%m\/%d\ -\ %H:%M:%S) [$1] $2 :: $3";
    if [ $# == 3 -a $KC_LOG == 1 ]; then
        if [ ! -d $KC_LOG_DIR ]; then
            sudo mkdir -m 0777 -p $KC_LOG_DIR;
        fi
        echo $LOG_VALUE >> $KC_LOG_DIR/all.log;
        echo $LOG_VALUE >> $KC_LOG_DIR/$KC_ACTION.log;
    fi
    if [ $KC_VERBOSE = 1 ]; then
        echo $LOG_VALUE;
    fi
}
#################################################################
# Copyright
#################################################################
## function
function kc_func_copy {
    if [ $KC_VERBOSE = 1 ];then
        echo "#################################################################";
		echo "$KC_FULL_NAME - $KC_VERSION";
		echo "Author: $KC_AUTHOR ($KC_AUTHOR_EMAIL)";
        echo "#################################################################";
    fi
}
#################################################################
# Mount
#################################################################
## function
# $1: input.
# $2: output.
# $3: Mensaje.
function kc_func_mount {
	if [ -d $1 ];then
		mount --bind $1 $2;
		kc_func_log $L_LOG $KC_ACTION "Moutn: $3";
	fi
}