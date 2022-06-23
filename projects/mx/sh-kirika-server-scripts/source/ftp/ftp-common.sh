#!/bin/bash
## TITLE ########################################################
## FTP Admin v1.0 (2010-10-09).
## Author: Alejandro M. Bernardis (alejandro.bernardis@gmail.com)
#################################################################
# copyright
#################################################################
KC_SHORT_NAME="KCFTPA";
KC_FULL_NAME="Kirika Code FTP Admin";
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
KC_LOG_DIR=/var/log/kcftp;
KC_FTP_DIR=/data/ftp
KC_FILE_PROJECT=".kcproject";
#################################################################
# function
#################################################################
## help function
function kc_func_help {
    echo "Help $KC_ACTION:";
        if [ $KC_ACTION = "ftpuseradd" ];then
			echo "- Usage: $KC_ACTION -u UserName -p UserPass [-d Directory] [-e Expire Date (YYYY-MM-DD)] [-v]";
			echo "- Usage: $KC_ACTION --username UserName --password UserPass [--direcotry Directory] [--expiredate Expire Date (YYYY-MM-DD)] [-verbose]";
		elif [ $KC_ACTION = "ftpclientadd" ];then
			echo "- Usage: $KC_ACTION -u UserName -p UserPass -c ClientName -b BrandName [-d Directory] [-e Expire Date (YYYY-MM-DD)] [-v]";
			echo "- Usage: $KC_ACTION --username UserName --password UserPass --client ClientName --brand BrandName [--direcotory Directory] [--expiredate Expire Date (YYYY-MM-DD)] [--verbose]";
		elif [ $KC_ACTION = "ftpuserdel" ] || [ $KC_ACTION = "ftpuserlock" ] || [ $KC_ACTION = "ftpuserunlock" ];then
			echo "- Usage: $KC_ACTION -u UserName [-v]";
			echo "- Usage: $KC_ACTION --username UserName [--verbose]";
		elif [ $KC_ACTION = "ftpuserpasswd" ];then
			echo "- Usage: $KC_ACTION -u UserName -p UserPass [-v]";
			echo "- Usage: $KC_ACTION --username UserName --password UserPass [--verbose]";
		elif [ $KC_ACTION = "ftpuserexpiredate" ];then
			echo "- Usage: $KC_ACTION -u UserName -e Expire Date (YYYY-MM-DD) [-v]";
			echo "- Usage: $KC_ACTION --username UserName --expiredate Expire Date (YYYY-MM-DD) [--verbose]";
		elif [ $KC_ACTION = "ftpdirdelete" ];then
			echo "- Usage: $KC_ACTION -d Directory [-v]";
			echo "- Usage: $KC_ACTION --directory Directory [--verbose]";
		elif [ $KC_ACTION = "ftpdirproject" ];then
			echo "- Usage: $KC_ACTION -c ClientName -b BrandName -n ProjectName [-v]";
			echo "- Usage: $KC_ACTION --client ClientName --brand BrandName --name ProjectName [--verbose]";
		fi
        echo "";
    exit 101;
}
## list function
function kc_func_list {
    echo "Parameters List $KC_ACTION:";
        echo "[-h] [--help] : Help";
        echo "[-l] [--list] : Parameters List";
		if [ $KC_ACTION = "ftpuseradd" ];then
			echo "[-u] [--username] : Username";
			echo "[-p] [--password] : Password";
			echo "[-d] [--directory] : Root Directory";
			echo "[-e] [--expiredate] : Expire Date";
		elif [ $KC_ACTION = "ftpclientadd" ];then
			echo "[-u] [--username] : Username";
			echo "[-p] [--password] : Password";
			echo "[-c] [--client] Client Name"; 
			echo "[-b] [--brand] : Brand Name";
			echo "[-d] [--directory] : Root Directory";
		elif [ $KC_ACTION = "ftpuserdel" ] || [ $KC_ACTION = "ftpuserlock" ] || [ $KC_ACTION = "ftpuserunlock" ];then
			echo "[-u] [--username] : Username";
		elif [ $KC_ACTION = "ftpuserpasswd" ];then
			echo "[-u] [--username] : Username";
			echo "[-p] [--password] : Password";
		elif [ $KC_ACTION = "ftpuserexpiredate" ];then
			echo "[-u] [--username] : Username";
			echo "[-e] [--expiredate] : Expire Date";
		elif [ $KC_ACTION = "ftpdirdelete" ];then
			echo "[-d] [--directory] : Root Directory";
		elif [ $KC_ACTION = "ftpdirproject" ];then
			echo "[-c] [--client] Client Name"; 
			echo "[-b] [--brand] : Brand Name";
			echo "[-n] [--name] : Project Name";
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

	        -u | --user-name)
	            shift
	                catch_cfg_username=$1;
	            shift
	            ;;

	        -p | --password)
	            shift
	                catch_cfg_password=$1;
	            shift
	            ;;

	        -c | --client)
	            shift
	                catch_cfg_clientname=$1;
	            shift
	            ;;
	
	        -b | --brand)
	            shift
	                catch_cfg_brandname=$1;
	            shift
	            ;;

	        -d | --directory)
	            shift
					catch_cfg_directory=$1;
	            shift
	            ;;
	
			-e | --expiredate)
	            shift
					catch_cfg_expiredate=$1;
	            shift
	            ;;

			-n | --name)
	            shift
					catch_cfg_name=$1;
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