#!/bin/bash
## TITLE ########################################################
## Project Creator v1.0 (2010-10-09).
## Author: Alejandro M. Bernardis (alejandro.bernardis@gmail.com)
#################################################################

## function
function kc_func_uninstall {
	if [ -f $1 ];then
		rm -f $1;
		if  [ -f $2 ];then
			rm -f $2;
		fi
		echo $3;
	fi
}

## uninstall
## install
kc_func_uninstall /data/scripts/deploy/prjcommon.sh /bin/kclib/prjcommon.sh "Project Common uninstalled.";
kc_func_uninstall /data/scripts/deploy/prjadd /bin/prjadd "Project Add uninstalled.";
kc_func_uninstall /data/scripts/deploy/prjbrandadd /bin/prjbrandadd "Project Brand uninstalled.";
kc_func_uninstall /data/scripts/deploy/prjclientadd /bin/prjclientadd "Project Client uninstalled.";
kc_func_uninstall /data/scripts/deploy/prjdel /bin/prjdel "Project Del uninstalled.";
kc_func_uninstall /data/scripts/deploy/prjlock /bin/prjlock "Project Lock uninstalled.";
kc_func_uninstall /data/scripts/deploy/prjunlock /bin/prjunlock "Project Unlock uninstalled.";


# eixt
echo "Project Helper has been uninstalled.";
exit 0;