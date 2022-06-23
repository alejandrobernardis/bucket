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
KC_LOG_DIR=/var/log/kcprj;
KC_DIR_HOME=/home/projects;
KC_DIR_CLIENTS=$KC_DIR_HOME/clients;
KC_DIR_PUBLIC=$KC_DIR_HOME/public;
KC_DIR_PROJECTS=$KC_DIR_HOME/projects;
KC_SYS_USER="nobody";
KC_SYS_GROUP="nogroup";
KC_FILE_PROJECT=".kcproject";
#################################################################
# function
#################################################################
## help function
function kc_func_help {
    echo "Help $KC_ACTION:";
    	## prjclientadd, prjbrandadd, prjadd, prjdel, prjlock, prjunlock
        if [ $KC_ACTION = "prjclientadd" ];then
        	echo "- Usage: $KC_ACTION -c ClientName [-v]";
        	echo "- Usage: $KC_ACTION --client ClientName [--verbose]";
        elif [ $KC_ACTION = "prjbrandadd" ];then
        	echo "- Usage: $KC_ACTION -c ClientName -b BrandName [-v]";
        	echo "- Usage: $KC_ACTION --client ClientName --brand BrandName [--verbose]";
        elif [ $KC_ACTION = "prjadd" ];then
        	echo "- Usage: $KC_ACTION -c ClientName -b BrandName -p ProjectName [-t TypeValue (empty)] [-v]";
        	echo "- Usage: $KC_ACTION --client ClientName --brand BrandName --project ProjectName [--type TypeValue (empty)] [--verbose]";
        elif [ $KC_ACTION = "prjdel" ] || [ $KC_ACTION = "prjlock" ] || [ $KC_ACTION = "prjunlock" ];then
        	echo "- Usage: $KC_ACTION -c ClientName -b BrandName -p ProjectName [-v]";
        	echo "- Usage: $KC_ACTION --client ClientName --brand BrandName --project ProjectName [--verbose]";
		fi
        echo "";
    exit 101;
}
## list function
function kc_func_list {
    echo "Parameters List $KC_ACTION:";
        echo "[-h] [--help] : Help";
        echo "[-l] [--list] : Parameters List";
        echo "[-c] [--client] Client Name";
        if [ $KC_ACTION != "prjclientadd" ]; then 
			echo "[-b] [--brand] : Brand Name";
        fi
        if [ $KC_ACTION != "prjclientadd" ] && [ $KC_ACTION != "prjbrandadd" ]; then
			echo "[-p] [--project] : Project Name";
			if [ $KC_ACTION = "prjadd" ];then
				echo "[-t] [--type] : Type Value";
			fi
        fi
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

			-c | --client)
	            shift
	                catch_cfg_client=$1;
	            shift
	            ;;
	
	        -b | --brand)
	            shift
	                catch_cfg_brand=$1;
	            shift
	            ;;
	            
	        -p | --project)
	            shift
	                catch_cfg_project=$1;
	            shift
	            ;;

	        -t | --type)
	            shift
					catch_cfg_type=$1;
	            shift
	            ;;

	        -d | --directory)
	            shift
					catch_cfg_directory=$1;
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