#!/bin/bash
## TITLE ########################################################
## FTP Admin v1.0 (2010-10-21).
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
kc_func_uninstall /bin/kclib/ftpcommon.sh /data/scripts/deploy/ftpcommon.sh "FTP Common uninstalled.";
kc_func_uninstall /bin/ftpclientadd /data/scripts/deploy/ftpclientadd "FTP Client Add uninstalled.";
kc_func_uninstall /bin/ftpdirdelete /data/scripts/deploy/ftpdirdelete "FTP Dir Delete uninstalled.";
kc_func_uninstall /bin/ftpdirproject /data/scripts/deploy/ftpdirproject "FTP Dir Project uninstalled.";
kc_func_uninstall /bin/ftpuseradd /data/scripts/deploy/ftpuseradd "FTP User Add uninstalled.";
kc_func_uninstall /bin/ftpuserdel /data/scripts/deploy/ftpuserdel "FTP User Delete uninstalled.";
kc_func_uninstall /bin/ftpuserlock /data/scripts/deploy/ftpuserlock "FTP User Lock uninstalled.";
kc_func_uninstall /bin/ftpuserunlock /data/scripts/deploy/ftpuserunlock "FTP User Unlock uninstalled.";
kc_func_uninstall /bin/ftpuserpasswd /data/scripts/deploy/ftpuserpasswd "FTP User Password uninstalled.";
kc_func_uninstall /bin/ftpuserexpiredate /data/scripts/deploy/ftpuserexpiredate "FTP User Expire Date uninstalled.";

# eixt
echo "Project Helper has been uninstalled.";
exit 0;