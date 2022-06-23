#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Apr 1, 2012, 3:08:41 AM 

from django.utils.datastructures import MultiValueDict
from wtforms import Form, TextField, PasswordField, BooleanField, validators

#: -- helpers ------------------------------------------------------------------

__all__ = [
    "BaseForm",
    "LoginForm", 
    "ForgotPasswordForm", 
    "ChangePasswordForm",
]

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

_message_length_6_32 = u"Debe ser 6 carcateres como minímo."
_validators_required = validators.Required(message=u"El campo es requerido.")
_validators_length_6_to_32 = validators.Length(6, 128, _message_length_6_32)

class LoginForm(BaseForm):
    username = TextField("Nombre de Usuario", [
        _validators_required,
        _validators_length_6_to_32],
        default="")
    
    password = PasswordField(u"Contraseña", [
        _validators_required,
        _validators_length_6_to_32],
        default="")
    
    remember_me = BooleanField()

class ForgotPasswordForm(BaseForm):
    username_or_email = TextField("Usuario o Email", [
        _validators_required,
        _validators_length_6_to_32],
        default="")
    
class ChangePasswordForm(BaseForm):
    password_old = PasswordField()
    password_new = PasswordField()
    password_verify = PasswordField()
    
    