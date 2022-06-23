#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Apr 9, 2012, 10:16:04 AM 

import re

from mx.yr.tornado.forms import BaseForm
from wtforms import TextField, PasswordField, IntegerField, BooleanField, \
                    DateField, validators

#: -- helpers ------------------------------------------------------------------

__all__ = []

#: -----------------------------------------------------------------------------

r_email = (r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
           r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'
           r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$')

_message_between = u"Es necesario tener de %(min)s a %(max)s caracteres."
_message_length_6_32 = u"De 6 a 32 carcateres como máximo."

_validators_required = validators.Required(message=u"El campo es requerido.")
_validators_optional = validators.Optional()
_validators_length_6_to_32 = validators.Length(6, 32, _message_length_6_32)

#: -----------------------------------------------------------------------------

class RegisterForm(BaseForm):
    first_name = TextField("Nombre/s", [
        _validators_required], 
        default="")
    
    last_name = TextField("Apellido/s", [
        _validators_required],
        default="")
    
    email = TextField("Email", [
        _validators_required,
        validators.Regexp(r_email, re.IGNORECASE, message=u"El email es incorrecto.")],
        default="")
    
    email_verify = TextField("Validar Email", [
        _validators_required,
        validators.EqualTo("email", u"El email no es válido.")],
        default="")
    
    gender = IntegerField("Sexo",[
        _validators_required,
        validators.NumberRange(1, 2, _message_between)],
        default=1)
    
    birthday = DateField("", [
        _validators_optional],
        default="Fecha de Nacimiento")
    
    birthday_day = IntegerField(u"Fecha de Nacimiento, Día", [
        _validators_required,
        validators.NumberRange(1, 31, _message_between)],
        default=0)
    
    birthday_month = IntegerField(u"Fecha de Nacimiento, Mes", [
        _validators_required,
        validators.NumberRange(1, 12, _message_between)],
        default=0)
    
    birthday_year = IntegerField(u"Fecha de Nacimiento, Año", [
        _validators_required,
        validators.NumberRange(1900, 2012, _message_between)],
        default=0)
    
    phone_lada = TextField(u"Teléfono, Lada", [
        _validators_optional,
        validators.Regexp(r"^[0-9]{2,5}$", message=u"El lada debe contener de 2 a 5 dígitos.")],
        default="")
    
    phone_number = TextField(u"Teléfono, Número", [
        _validators_optional,
        validators.Regexp(r"^[0-9]{10}$", message=u"El número de teléfono debe contener 10 dígitos.")],
        default="")
    
    address_state = IntegerField("Estado", [
        _validators_required,
        validators.NumberRange(1, 32, _message_between)],
        default=0)
    
    username = TextField("Nombre de Usuario", [
        _validators_required,
        _validators_length_6_to_32,
        validators.Regexp(r"^([a-zA-Z0-9_\-\.]+)$", message=u"Para el nombre de usuario solo se aceptan letras minúsculas, letras mayúsculas, números, guiones medios, guiones bajos y puntos.")],
        default="")
    
    password = PasswordField(u"Contraseña", [
        _validators_required,
        _validators_length_6_to_32,
        validators.Regexp(r"^[A-Za-z0-9+_\-!\$\.#@%]+$", message=u"Para la contraseña solo se aceptan letras minúsculas, letras mayúsculas, números y los siguiente símbolos: + _ - ! $ # @ %.")],
        default="")
    
    password_verify = PasswordField(u"Validar Contraseña", [
        _validators_required,
        validators.EqualTo("password", u"La contraseña no concuerda.")],
        default="")
    
    terms =  BooleanField(u"Términos y Condiciones", [
        _validators_required],
        default=False)
    
    policy =  BooleanField(u"Políticas de Privacidad", [
        _validators_required],
        default=False)
    
    news =  BooleanField()
    
#: -----------------------------------------------------------------------------
    
class RedeemAccessoriesForm(BaseForm):
    accessory_code = TextField(u"Código", [                  
        _validators_required,
        validators.Length(8, message=u"El código debe contener 8 dígitos."),
        validators.Regexp(r"^[a-z0-9]{8}$", re.IGNORECASE, message=u"El código es in correcto, inténtalo de nuevo.")],
        default="")
    
    accessory_type = IntegerField("Tipo",[
        _validators_optional,
        validators.NumberRange(1, 2, _message_between)],
        default="")

#: -----------------------------------------------------------------------------
    
class RedeemTicketsForm(BaseForm):
    
    ticket_date = TextField("Fecha y Hora", [
        _validators_optional],
        default="")
    
    # $:1,2:3,20
    products_list = TextField("Productos", [                  
        _validators_optional,
        validators.Regexp(r"^(\$:)([0-9]{1,2}:[0-9]{1,2},?)+")],
        default="")
    
    ticket_rfc = TextField("RFC", [
        _validators_required],
        default="")
    
    product_pasta = IntegerField("Pasta Dental",[
        _validators_optional,
        validators.NumberRange(0, 25, _message_between)],
        default=0)
    
    product_cepillo = IntegerField("Cepillo de Dientes",[
        _validators_optional,
        validators.NumberRange(0, 25, _message_between)],
        default=0)
    
    product_enjuague = IntegerField("Enjuague Bucal",[
        _validators_optional,
        validators.NumberRange(0, 25, _message_between)],
        default=0)
    
    ticket_hour = IntegerField("Horas",[
        validators.NumberRange(0, 23, _message_between)],
        default=-1)
    
    ticket_minutes = IntegerField("Minutos",[
        validators.NumberRange(0, 59, _message_between)],
        default=-1)
    
    ticket_day = IntegerField(u"Día",[
        validators.NumberRange(1, 31, _message_between)],
        default=0)
    
    ticket_month = IntegerField("Mes",[
        validators.NumberRange(1, 12, _message_between)],
        default=0)
    
    ticket_year = IntegerField(u"Año",[
        _validators_required],
        default=0)

#: -----------------------------------------------------------------------------
    
class RedeemGameForm(BaseForm):
    points = IntegerField("Puntos", [
        validators.NumberRange(0)],
        default=0)

#: -----------------------------------------------------------------------------
    
class UserActivateForm(BaseForm):
    username = TextField("Nombre de Usuario", [
        _validators_required,
        _validators_length_6_to_32],
        default="")

#: -----------------------------------------------------------------------------

class UserDataForm(BaseForm):
    user = TextField("", [])
    
    