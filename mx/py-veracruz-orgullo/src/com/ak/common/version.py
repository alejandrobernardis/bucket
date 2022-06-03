#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Asumi Kamikaze Inc.
# Copyright (c) 2012 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Sep 3, 2012 2:36:58 AM

import os, subprocess
from datetime import datetime

#: -- helpers ------------------------------------------------------------------

__all__ = ['get_string_version', 'ALPHA', 'BETA', 'RELEASE', 'FINAL']

#: -- const --------------------------------------------------------------------

ALPHA   = 'alpha'
BETA    = 'beta'
RELEASE = 'rc'
FINAL   = 'final'

#: -- get_string_version -------------------------------------------------------

def get_string_version(version=None):
    assert version is not None
    assert len(version) == 5
    assert version[3] in (ALPHA, BETA, RELEASE, FINAL)
    
    parts = 2 if version[2] == 0 else 3
    main = '.'.join(str(a) for a in version[:parts])
    status = ''
    
    if version[3] == ALPHA and version[4] == 0:
        changeset = get_mercurial_changeset()
        if changeset:
            status = '.dev.' + changeset 
    
    elif version[3] != FINAL:
        status = '.%s.%s' % (version[3], version[4])
    
    return main + status

#: -- get_mercurial_changeset --------------------------------------------------

def get_mercurial_changeset():
    repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log = subprocess.Popen('hg log -r tip --template "{date}"', 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                           shell=True, cwd=repo_path, universal_newlines=True)
    timestamp = log.communicate()[0]
    try:
        timestamp = datetime.utcfromtimestamp(float(timestamp))
    except ValueError:
        return None    
    return timestamp.strftime('%Y%m%d%H%M%S')
