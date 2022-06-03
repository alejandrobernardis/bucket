#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Jan 7, 2013 8:44:47 AM

import re 
from com.ak.common.utils import regex_username_str, regex_password_str, \
    regex_email_str
from django.utils.datastructures import MultiValueDict
from wtforms import Form, TextField, PasswordField, BooleanField, validators

#: -- helpers ------------------------------------------------------------------

__all__ = [
    "BaseForm",
    "LoginForm", 
    "ForgotPasswordForm", 
    "ChangePasswordForm",
    "RegisterBaseForm",
]

#: -----------------------------------------------------------------------------

_validator_required = validators.Required()
_validator_length_8_to_32 = validators.Length(8, 32)
_validator_length_8_to_96 = validators.Length(8, 96)
_validator_regex_username = validators.Regexp(regex_username_str, re.IGNORECASE)
_validator_regex_password = validators.Regexp(regex_password_str, re.IGNORECASE)
_validator_regex_email = validators.Regexp(regex_email_str, re.IGNORECASE)

#: -- BaseForm -----------------------------------------------------------------

class BaseForm(Form):
    def __init__(self, handler=None, 
                 obj=None, prefix="", formdata=None, **kwargs):
        
        if handler:
            formdata = MultiValueDict()
            for name in handler.request.arguments.keys():
                formdata.setlist(name, handler.get_arguments(name))
        
        Form.__init__(self, formdata=formdata, obj=obj, prefix=prefix, 
                      **kwargs)
        
#: -- AuthForm's ---------------------------------------------------------------

class LoginForm(BaseForm):
    username = TextField(
        "Username or Email", 
        [
         _validator_required, 
         _validator_length_8_to_96, 
        ],
        default="")
    
    password = PasswordField(
        "Password", 
        [
         _validator_required, 
         _validator_length_8_to_32,
         _validator_regex_password
        ],
        default="")
    
    remember_me = BooleanField()
    
#: -----------------------------------------------------------------------------
    
class ForgotPasswordForm(BaseForm):
    username_or_email = TextField(
        "Username or Email", 
        [
         _validator_required, 
         _validator_length_8_to_96,
        ],
        default="")
    
#: -----------------------------------------------------------------------------
    
class ChangePasswordForm(BaseForm):
    password_old = PasswordField(
        "Old Password", 
        [
         _validator_required, 
         _validator_length_8_to_32,
         _validator_regex_password
        ], 
        default="")
    
    password_new = PasswordField(
        "New Password", 
        [
         _validator_required, 
         _validator_length_8_to_32,
         _validator_regex_password
        ], 
        default="")
    
    password_verify = PasswordField(
        "Verify Password", 
        [
         validators.EqualTo("password_new")
        ], 
        default="")

#: -- RegisterBaseForm ---------------------------------------------------------

class RegisterBaseForm(BaseForm):
    username = TextField(
        "Username", 
        [
         _validator_required, 
         _validator_length_8_to_32, 
         _validator_regex_username
        ],
        default="")
    
    password = PasswordField(
        "Password", 
        [
         _validator_required, 
         _validator_length_8_to_32,
         _validator_regex_password
        ],
        default="")
    
    password_verify = PasswordField(
        "Verify Password", 
        [
         validators.EqualTo("password")
        ], 
        default="")
    
    email = TextField(
        "Email", 
        [
         _validator_required, 
         _validator_length_8_to_96,
         _validator_regex_email
        ],
        default="")
    
    email_verify = TextField(
        "Verify Email", 
        [
         validators.EqualTo("email")
        ], 
        default="")
    
