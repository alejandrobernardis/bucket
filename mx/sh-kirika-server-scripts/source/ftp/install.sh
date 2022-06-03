#!/bin/bash
## TITLE ########################################################
## FTP Admin v1.0 (2010-10-09).
## Author: Alejandro M. Bernardis (alejandro.bernardis@gmail.com)
#################################################################

## KC Lib Direcotry.
mkdir -m 0770 -p /bin/kclib;

## Ftp Directory.
rm -fR /var/data;
mkdir -m 0755 -p /data/ftp/clarus;
mkdir -m 0775 -p /data/ftp/clarus/share;
mkdir -m 0755 -p /data/ftp/clients;
mkdir -m 0755 -p /data/ftp/projects;
mkdir -m 0777 -p /data/ftp/public;
chown -R ftp:ftp /data/ftp/*;

# deploy
mkdir -m 0755 -p /data/scripts/deploy;

# links
mkdir -m 0755 -p /data/www/ftp;
ln -s /data/ftp/clients /data/www/ftp/clients;
ln -s /data/ftp/clarus /data/www/ftp/clarus;
ln -s /data/ftp/public /data/www/ftp/public;
ln -s /data/ftp/projects /data/www/projects;

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

## kclib install.
if [ -e /bin/kclib/common.sh ]; then
	echo "KC Lib Common already exists.";
else 
	kc_func_install /data/scripts/source/kclib/common.sh /data/scripts/deploy/common.sh /bin/kclib/common.sh "KC Lib Common installed.";
fi 

## FTP install.
kc_func_install /data/scripts/source/ftp/ftp-common.sh /data/scripts/deploy/ftpcommon.sh /bin/kclib/ftpcommon.sh "FTP Common installed.";
kc_func_install /data/scripts/source/ftp/ftp-client-add.sh /data/scripts/deploy/ftpclientadd /bin/ftpclientadd "FTP Client Add installed.";
kc_func_install /data/scripts/source/ftp/ftp-dir-delete.sh /data/scripts/deploy/ftpdirdelete /bin/ftpdirdelete "FTP Dir Delete installed.";
kc_func_install /data/scripts/source/ftp/ftp-dir-project.sh /data/scripts/deploy/ftpdirproject /bin/ftpdirproject "FTP Dir Project installed.";
kc_func_install /data/scripts/source/ftp/ftp-user-add.sh /data/scripts/deploy/ftpuseradd /bin/ftpuseradd "FTP User Add installed.";
kc_func_install /data/scripts/source/ftp/ftp-user-del.sh /data/scripts/deploy/ftpuserdel /bin/ftpuserdel "FTP User Delete installed.";
kc_func_install /data/scripts/source/ftp/ftp-user-lock.sh /data/scripts/deploy/ftpuserlock /bin/ftpuserlock "FTP User Lock installed.";
kc_func_install /data/scripts/source/ftp/ftp-user-unlock.sh /data/scripts/deploy/ftpuserunlock /bin/ftpuserunlock "FTP User Unlock installed.";
kc_func_install /data/scripts/source/ftp/ftp-user-passwd.sh /data/scripts/deploy/ftpuserpasswd /bin/ftpuserpasswd "FTP User Password installed.";
kc_func_install /data/scripts/source/ftp/ftp-user-expire-date.sh /data/scripts/deploy/ftpuserexpiredate /bin/ftpuserexpiredate "FTP User Expire Date installed.";

# .htpasswd
htpasswd -cb /data/htpasswd/.ftpclarus clarusftp ftpCDx09-ext07;
htpasswd -cb /data/htpasswd/.ftpclients clientftp ftpCLx08-ext09;
htpasswd -cb /data/htpasswd/.projects viewprojects prjCDx07-ext02;

# apache default config 
/etc/init.d/apache2 stop;
cp -f /etc/apache2/sites-available/default "/etc/apache2/sites-available/default.$(date +%Y%m%d).old";
cp -f /data/scripts/soruce/ftp/default.conf /etc/apache2/sites-available/default;
chmod 644 /etc/apache2/sites-available/default;
chown root:root /etc/apache2/sites-available/default;
/etc/init.d/apache2 start;

# exit
echo "FTP Helper has been installed.";
exit 0;