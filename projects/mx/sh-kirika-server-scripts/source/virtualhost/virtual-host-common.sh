#!/bin/bash
## TITLE ########################################################
## Project Creator v1.0 (2010-10-19).
## Author: Alejandro M. Bernardis (alejandro.bernardis@gmail.com)
#################################################################
# copyright
#################################################################
KC_SHORT_NAME="KCPRJC";
KC_FULL_NAME="Kirika Code Project Creator";
KC_VERSION="v1.0";
KC_COPYRIGHT="(c)2010 Kirika Code - Alejandro M. Bernardis";
KC_AUTHOR="Alejandro M. Bernardis";
KC_AUTHOR_EMAIL="alejandrob@kirikacode.com";
#################################################################
# include
#################################################################
source /bin/kclib/common.sh;
#################################################################
# consts
#################################################################
KC_LOG_DIR=/var/log/kcvh;
KC_DIR_HOME=/data/www/production;
KC_DIR_LIVE=/data/www/production/live;
KC_DIR_STAGING=/data/www/production/staging;
KC_DIR_SITES_AVAILABLE=/etc/apache2/sites-available;
KC_DIR_SITES_ENABLED=/etc/apache2/sites-enabled;
#################################################################
# function
#################################################################
## help function
function kc_func_help {
    echo "Help $KC_ACTION:";
        if [ $KC_ACTION = "vhadd" ] || [ $KC_ACTION = "vhdel" ] || [ $KC_ACTION = "vhlock" ] || [ $KC_ACTION = "vhunlock" ];then
        	echo "- Usage: $KC_ACTION -d DomainName [-v]";
        	echo "- Usage: $KC_ACTION --domain DomainName [--verbose]";
		fi
        echo "";
    exit 101;
}
## list function
function kc_func_list {
    echo "Parameters List $KC_ACTION:";
        echo "[-h] [--help] : Help";
        echo "[-l] [--list] : Parameters List";
        echo "[-d] [--domain] Domain Name";
        echo "[-v] [--verbose  ] : Verbose";
        echo "";
    exit 102;
}
#################################################################
# catch parameters
#################################################################
if [ "$#" -eq 0 ]; then
	kc_func_help;
else
	while [ "$#" -gt 0 ]; do
	    case $1 in
		
	        -h | --help)
	                kc_func_help;
	            shift
	            ;;

	        -l | --list)
	                kc_func_list;
	            shift
	            ;;

	        -d | --domain)
	            shift
					catch_cfg_domain=$1;
	            shift
	            ;;

	        -v | --verbose)
	            shift
	                KC_VERBOSE=1;
	            shift
	            ;;

	        *)
	            exit 100;
	            shift
	            ;;

	    esac
	done
fi
#################################################################
# initialize...
#################################################################
kc_func_copy;
kc_func_log $L_LOG $KC_ACTION "### Initialize ###";