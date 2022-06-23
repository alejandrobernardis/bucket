#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 22/Feb/2014 20:25

from com.feedback.security.auth import Role, Permission

# Roles

role_admin = Role('admin', True)
role_user = Role('user', True)
role_guest = Role('guest', True)
role_write = Role('write', True)
role_read = Role('read', True)
role_search = Role('search', True)
role_profile = Role('profile', True)

# Permissions

perms_admin = Permission(
    role_admin,
    role_profile,
    role_search
)

perms_user = Permission(
    role_user,
    role_profile,
    role_search
)

perms_guest = Permission(
    role_guest
)