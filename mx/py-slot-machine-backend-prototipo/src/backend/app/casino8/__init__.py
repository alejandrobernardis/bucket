#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 21/06/2013 09:01

from __future__ import unicode_literals
import os
import subprocess
from datetime import datetime

# Ref: Django Version

__all__ = ['get_string_version', 'VERSION', 'ALPHA', 'BETA', 'RELEASE', 'FINAL']


ALPHA = 'alpha'
BETA = 'beta'
RELEASE = 'rc'
FINAL = 'final'


def get_string_version(version=None):
    assert version
    assert len(version) == 5
    assert version[3] in (ALPHA, BETA, RELEASE, FINAL)
    parts = 2 if version[2] == 0 else 3
    main = '.'.join(str(a) for a in version[:parts])
    status = ''
    if version[3] == ALPHA and version[4] == 0:
        changeset = get_git_changeset()
        if changeset:
            status = '.dev.' + changeset
    elif version[3] != FINAL:
        status = '.%s.%s' % (version[3], version[4])
    return main + status


def get_git_changeset():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    git_log = subprocess.Popen('git log --pretty=format:%ct --quiet -1 HEAD',
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               shell=True, cwd=repo_dir,
                               universal_newlines=True)
    timestamp = git_log.communicate()[0]
    try:
        timestamp = datetime.datetime.utcfromtimestamp(int(timestamp))
    except ValueError:
        return None
    return timestamp.strftime('%Y%m%d%H%M%S')


VERSION = (1, 0, 0, ALPHA, 0)