#!/bin/bash
## TITLE ########################################################
## FTP Admin v1.0 (2010-10-09).
## Author: Alejandro M. Bernardis (alejandro.bernardis@gmail.com)
#################################################################

## Function Install.
# $1: Input.
# $2: Output.
# $3: Link.
# $4: Mensaje.
function kc_func_install {
	## deploy
	rm -f $2;
	cp -f $1 $2;
	chmod +x $2;
	## install
	rm -f $3;
	ln -s $2 $3;
	echo $4;
}

## FTP install.
kc_func_install /data/scripts/source/ftp/ftp-common.sh /data/scripts/deploy/ftpcommon.sh /bin/kclib/ftpcommon.sh "FTP Common pdated.";
kc_func_install /data/scripts/source/ftp/ftp-client-add.sh /data/scripts/deploy/ftpclientadd /bin/ftpclientadd "FTP Client Add pdated.";
kc_func_install /data/scripts/source/ftp/ftp-dir-delete.sh /data/scripts/deploy/ftpdirdelete /bin/ftpdirdelete "FTP Dir Delete pdated.";
kc_func_install /data/scripts/source/ftp/ftp-dir-project.sh /data/scripts/deploy/ftpdirproject /bin/ftpdirproject "FTP Dir Project pdated.";
kc_func_install /data/scripts/source/ftp/ftp-user-add.sh /data/scripts/deploy/ftpuseradd /bin/ftpuseradd "FTP User Add pdated.";
kc_func_install /data/scripts/source/ftp/ftp-user-del.sh /data/scripts/deploy/ftpuserdel /bin/ftpuserdel "FTP User Delete pdated.";
kc_func_install /data/scripts/source/ftp/ftp-user-lock.sh /data/scripts/deploy/ftpuserlock /bin/ftpuserlock "FTP User Lock pdated.";
kc_func_install /data/scripts/source/ftp/ftp-user-unlock.sh /data/scripts/deploy/ftpuserunlock /bin/ftpuserunlock "FTP User Unlock pdated.";
kc_func_install /data/scripts/source/ftp/ftp-user-passwd.sh /data/scripts/deploy/ftpuserpasswd /bin/ftpuserpasswd "FTP User Password pdated.";
kc_func_install /data/scripts/source/ftp/ftp-user-expire-date.sh /data/scripts/deploy/ftpuserexpiredate /bin/ftpuserexpiredate "FTP User Expire Date pdated.";

# exit
echo "FTP Helper has been updated.";
exit 0;