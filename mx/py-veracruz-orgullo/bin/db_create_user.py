#!/usr/bin/env python
# -*- coding: utf-8 -*-
import db_cnx

# imports
try:
    import settings, datetime
    from com.ak.common.roles import Role
    from com.ak.common.security import token
    from com.ak.models.users import User
    from mx.dip.voj.models.countries import Country
    
except:
    exit(u'Ups!, no están todos los módulos.')
    
# helpers

for a in settings.USER_ROLES:
    Role(**settings.USER_ROLES[a])    

admin = Role.get_role('admin')
ruser = Role.get_role('user')

# admin user
user_list = [
    ('Sys', 'Admin', 'di Paola', admin.name, admin.permissions, 'sysadmin', '', '', 'fb__sysadmin'),
    ('Sys', 'Admin', 'Veracruz', admin.name, admin.permissions, 'admin', '', '', 'fb__admin'),
]

country = Country.get_by_id(10)

try:
    User.drop_collection()
    for _fn, _mn, _ln, _rn, _rid, _us, _ps, _em, _fb in user_list:
        user = User()
        user.token = token(32)
        user.facebook_uid = _fb
        user.email = _em
        user.username = _us
        user.password = _ps
        user.role_id = _rid
        user.role_name = _rn
        user.first_name = _fn
        user.last_name = _ln
        user.birthday = datetime.date(1980,1,1)
        user.country = country
        user.city = 'Mexico City'
        user.created = datetime.datetime.now()
        user.available = True
        user.enabled = True
        user.save()

except Exception as E:
    print E


#
#print 'USERS', User.objects.count()
#exit(0)
#
#for a in range(1,2):
#    a = str(a)
#    user = User()
#    user.token = token(32)
#    user.facebook_uid = 'fb__'+a
#    user.email = 'email'+a+'@gmail.com'
#    user.username = 'username'+a
#    user.password = 'username'+a
#    user.role_id = ruser.permissions
#    user.role_name = ruser.name
#    user.first_name = 'Ricardo '+a
#    user.last_name = 'Darin'
#    user.birthday = datetime.date(1983,9,2)
#    user.country = country
#    user.city = 'Buenos Aires'
#    user.available = True
#    user.enabled = True
#    user.save()
#
#print 'USERS', User.objects(role_id=1).count()