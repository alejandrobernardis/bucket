#!/bin/bash
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 07/10/2013

CFG_PATH=`pwd`/application_config

################################################################################

function copy_file(){
    if [ -e $2 ]; then cp -f $2 $2".$(date +%Y%m%d%H%M%S).bak"; fi
    cp -f $1 $2
    return 0
}

function profile_config(){
    rm -fR /data
    mkdir -p ~/{backups,downloads} /data/{db,src,sys}
    copy_file ${CFG_PATH}/root/dot_bashrc ~/.bashrc
    copy_file ${CFG_PATH}/root/dot_bash_profile ~/.bash_profile
    . ~/.bash_profile
    localedef -i en_US -c -f UTF-8 en_US.UTF-8
}

function memcached_install() {
    yum -y install memcached
    chkconfig memcached on
    cd ~/downloads
    wget https://launchpad.net/libmemcached/1.0/1.0.18/+download/libmemcached-1.0.18.tar.gz
    tar xfvz libmemcached-1.0.18.tar.gz
    cd libmemcached-1.0.18
    ./configure
    make
    make install
    copy_file ${CFG_PATH}/etc/sysconfig/memcached /etc/sysconfig/memcached
    echo "/usr/local/lib/" > /etc/ld.so.conf.d/local-x86_64.conf
    ldconfig
}

function python_install() {
    cd ~/downloads
    curl -O http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz
    tar xfvz Python-2.7.6.tgz
    cd Python-2.7.6
    ./configure
    make
    make install
    cd ~/downloads
    curl -O https://pypi.python.org/packages/source/s/setuptools/setuptools-2.2.tar.gz
    tar xfvz setuptools-2.2.tar.gz
    cd setuptools-2.2
    python setup.py build
    python setup.py install
    cd ~/downloads
    curl -O https://pypi.python.org/packages/source/p/pip/pip-1.5.2.tar.gz
    tar xfvz pip-1.5.2.tar.gz
    cd pip-1.5.2
    python setup.py build
    python setup.py install
    cd ~/downloads
    curl -O https://pypi.python.org/packages/source/s/supervisor/supervisor-3.0.tar.gz
    tar xfvz supervisor-3.0.tar.gz
    cd supervisor-3.0
    python setup.py build
    python setup.py install
    groupadd -r supervisord
    useradd -M -r -g supervisord -d /var/lib/supervisord -s /bin/false -c supervisord supervisord > /dev/null 2>&1
    mkdir -p /etc/supervisord /var/log/supervisord /var/run/supervisord
    copy_file ${CFG_PATH}/etc/supervisord.conf /etc/supervisord.conf
    copy_file ${CFG_PATH}/etc/supervisord/mx_com_addicted_verify.supervisor /etc/supervisord/mx_com_addicted_verify.supervisor
    copy_file ${CFG_PATH}/etc/rc.d/init.d/supervisord /etc/rc.d/init.d/supervisord
    chmod a+x /etc/rc.d/init.d/supervisord
    chown -R supervisord:supervisord /etc/supervisord /var/log/supervisord /var/run/supervisord
    chkconfig --add supervisord
    chkconfig supervisord on
}

function python_dependencies_install() {
    pip install -r ${CFG_PATH}/tmp/python-requirements.txt
}

function mongodb_install() {
    RS="mx_com_addicted_verify"
    ROOT_PATH=/data/db
    REPLICASET_PATH=${ROOT_PATH}/${RS}
    rm -fR ${REPLICASET_PATH}
    mkdir -p ${REPLICASET_PATH}
    mkdir -p ${ROOT_PATH}/pid
    mkdir -p ${ROOT_PATH}/log
    copy_file ${CFG_PATH}/etc/yum.repos.d/10gen.repo /etc/yum.repos.d/10gen.repo
    yum -y update
    yum -y install mongo-10gen mongo-10gen-server
    copy_file ${CFG_PATH}/etc/mongod.conf /etc/mongod.conf
    copy_file ${CFG_PATH}/etc/rc.d/init.d/mongod /etc/rc.d/init.d/mongod
    chown -R mongod:mongod ${ROOT_PATH} ${ROOT_PATH}/pid ${ROOT_PATH}/log ${REPLICASET_PATH} 
    chmod a+x /etc/mongod/replicaset /etc/rc.d/init.d/mongod
}

function application_install(){
    echo ""
    echo "Install Application:"
    username=figment_alejandro
    password=\!sY54dm1N
    echo "* Get Repository... "
    mkdir -p /data/{src,sys}
    git clone https://${username}:${password}@bitbucket.org/kinetiq_mexico/kinetiq-mx-com-addicted-verify-system.git /data/src/kinetiq-mx-com-addicted-verify-system
    cd /data/sys
    ln -s ../src/kinetiq-mx-com-addicted-verify-system/app/verify/
    ln -s ../src/kinetiq-mx-com-addicted-verify-system/app/public/
    echo "Finish."
}

################################################################################

if [ $(id -u) -ne 0 ]; then
    echo "You don't have permissions for install"
    exit 1
elif [ ! -d ${CFG_PATH} ]; then
    echo "Application configuration path, not found: ${CFG_PATH}"
    exit 2
else
    echo ""
    echo "Install..."
    profile_config;
    memcached_install;
    python_install;
    python_dependencies_install;
    mongodb_install;
    application_install;
    echo ""
    echo "Checking:"
    echo -n '* Memcached... '
    [ ! -e /usr/bin/memcached        ] && echo 'error' || echo 'ok'
    echo -n '* MongoDB..... '
    [ ! -e /usr/bin/mongod           ] && echo 'error' || echo 'ok'
    echo -n '* Python...... '
    [ ! -e /usr/local/bin/python2.7  ] && echo 'error' || echo 'ok'
    echo ""
    echo "Merci et au revoir!"
    rm -fR ~/downloads/*
fi

################################################################################
