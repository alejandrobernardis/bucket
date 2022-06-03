#!/bin/bash
## TITLE ########################################################
## Project Creator v1.0 (2010-10-21).
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

## kclib install.
if [ -e /bin/kclib/common.sh ]; then
	echo "KC Lib Common already exists.";
else 
	kc_func_install /data/scripts/source/kclib/common.sh /data/scripts/deploy/common.sh /bin/kclib/common.sh "KC Lib Common installed.";
fi 

## install
kc_func_install /data/scripts/source/project/project-common.sh /data/scripts/deploy/prjcommon.sh /bin/kclib/prjcommon.sh "Project Common installed.";
kc_func_install /data/scripts/source/project/project-add.sh /data/scripts/deploy/prjadd /bin/prjadd "Project Add installed.";
kc_func_install /data/scripts/source/project/project-brand.sh /data/scripts/deploy/prjbrandadd /bin/prjbrandadd "Project Brand installed.";
kc_func_install /data/scripts/source/project/project-client.sh /data/scripts/deploy/prjclientadd /bin/prjclientadd "Project Client installed.";
kc_func_install /data/scripts/source/project/project-del.sh /data/scripts/deploy/prjdel /bin/prjdel "Project Del installed.";
kc_func_install /data/scripts/source/project/project-lock.sh /data/scripts/deploy/prjlock /bin/prjlock "Project Lock installed.";
kc_func_install /data/scripts/source/project/project-unlock.sh /data/scripts/deploy/prjunlock /bin/prjunlock "Project Unlock installed.";

# exit
echo "Project Helper has been installed.";
exit 0;