#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 20/Feb/2014 13:42

from com.feedback.core.regex import regex_username, regex_password, \
    regex_activation_key, regex_phone_lada, regex_phone_number
from com.feedback.forms.base import ListField
from wtforms.fields import TextField, PasswordField, BooleanField, RadioField
from wtforms.validators import InputRequired, Length, Email, Regexp, EqualTo
from wtforms_tornado import Form


class SignInForm(Form):
    username = TextField('Usuario / Email', [
        InputRequired(u'El nombre de usuario o email es requerido.'),
        Length(min=8, message=u'El mínimo requerido es de 8 caracteres '
                              u'para el usuario o email.'),
        Regexp(regex_username, message=u'Para el nombre de usuario solo se '
                                       u'permiten los siguientes caracteres: '
                                       u'a-z, 0-9, @, ., -, _')
    ], default='')
    password = PasswordField(u'Contraseña', [
        InputRequired(u'La contraseña es requerido.'),
        Length(8, 32, u'El mínimo requerido es de 8 caracteres y el '
                      u'máximo de 32 para la contraseña.'),
        Regexp(regex_password, message=u'Para la contraseñas solo se '
                                       u'permiten los siguientes caracteres: '
                                       u'A-Z, a-z, 0-9, !, @, #, $, =, +, ., '
                                       u'-, _')
    ], default='')


class RecoveryForm(Form):
    email = TextField('Email', [
        InputRequired(u'El email es requerido.'),
        Length(min=6, message=u'El mínimo requerido es de 6 caracteres '
                              u'para el email.'),
        Email(u'El email no es válido.')
    ], default='')


class RecoveryVerifyForm(Form):
    activation_key = TextField('Clave', [
        InputRequired(u'La clave de verificaicón es requerida.'),
        Regexp(regex_activation_key, message=u'El formato de la clave de '
                                             u'verificación es incorrecto.')
    ], default='')


class RecoveryPasswordForm(Form):
    password = PasswordField(u'Contraseña', [
        InputRequired(u'La contraseña es requerida.'),
        Length(8, 32, u'El mínimo requerido es de 8 caracteres y el '
                      u'máximo de 32 para la contraseña.'),
        Regexp(regex_password, message=u'Para la contraseñas solo se '
                                       u'permiten los siguientes caracteres: '
                                       u'A-Z, a-z, 0-9, !, @, #, $, =, +, ., '
                                       u'-, _'),
        EqualTo('password_verify', u'Las contraseñas no concuerdan.')
    ], default='')

    password_verify = PasswordField(u'Confirmar Contraseña', [
        InputRequired(u'La contraseña es requerida.')
    ], default='')


class ChangePasswordForm(Form):
    password = PasswordField(u'Contraseña', [
        InputRequired(u'La contraseña es requerida.'),
        Length(8, 32, u'El mínimo requerido es de 8 caracteres y el '
                      u'máximo de 32 para la contraseña.'),
        Regexp(regex_password, message=u'Para la contraseñas solo se '
                                       u'permiten los siguientes caracteres: '
                                       u'A-Z, a-z, 0-9, !, @, #, $, =, +, ., '
                                       u'-, _')

    ], default='')

    password_new = PasswordField(u'Contraseña', [
        InputRequired(u'La contraseña es requerida.'),
        Length(8, 32, u'El mínimo requerido es de 8 caracteres y el '
                      u'máximo de 32 para la contraseña.'),
        Regexp(regex_password, message=u'Para la contraseñas solo se '
                                       u'permiten los siguientes caracteres: '
                                       u'A-Z, a-z, 0-9, !, @, #, $, =, +, ., '
                                       u'-, _'),
        EqualTo('password_verify', u'Las contraseñas no concuerdan.')
    ], default='')

    password_verify = PasswordField(u'Confirmar Contraseña', [
        InputRequired(u'La confirmación de la contraseña es requerida.')
    ], default='')


class ProfileBaseForm(Form):
    company = TextField('Empresa', [
        InputRequired(u'El nombre de la tienda o empresa es requerido.')
    ], default='')
    position = TextField('Cargo', [
        InputRequired(u'El nombre de la posición que ocupa.')
    ], default='')
    first_name = TextField('Nombre(s)', [
        InputRequired(u'El nombre(s) es requerido.')
    ], default='')
    last_name = TextField('', [
        InputRequired(u'El apellido(s) es requerido.')
    ], default='')
    phone_lada = TextField('Lada', [
        InputRequired(u'El número de lada es requerido.'),
        Regexp(regex_phone_lada, message=u'El formato del lada no es correcto.')
    ], default='')
    phone_number = TextField(u'Número', [
        InputRequired(u'El número de teléfono es requerido.'),
        Regexp(regex_phone_number, message=u'El formato del número de '
                                           u'teléfono no es correcto.')
    ], default='')


class ProfileForm(ProfileBaseForm):
    dispatch = RadioField(u'Recibir la evaluación', [
        InputRequired(u'Por favor, seleccione con que periodicidad desea '
                      u'recibir las evaluaciones.')
    ], choices=[
        ('1', 'w1'),
        ('2', 'w2'),
        ('4', 'w4'),
    ], default='4')


class RequestForm(ProfileBaseForm):
    email = TextField('Email', [
        InputRequired(u'El email es requerido.'),
        Length(min=6, message=u'El mínimo requerido es de 6 caracteres '
                              u'para el email.'),
        Email(u'El email no es válido.')
    ], default='')
    provider = RadioField(u'Es cliente de', [
        InputRequired(u'Por favor, selecciene la empresa a la que es cliente.')
    ], choices=[
        ('1', 'provider_all'),
        ('2', 'provider_figment'),
        ('3', 'provider_kinetiq'),
    ], default='1')
    policy = BooleanField(u'Políticas de Privacidad', [
        InputRequired(u'Las Politícas de Privacidad son requeridas.')
    ], default=False)


class NewUserForm(RequestForm):
    executives = ListField('Involucrados')
    permissions = RadioField(u'Es cliente de', [
        InputRequired(u'Por favor, debe asignarle un nivel de usuario.')
    ], choices=[
        ('user', ''),
        ('admin', ''),
    ], default='user')
    policy = BooleanField(u'Políticas de Privacidad', [
        InputRequired(u'Las Politícas de Privacidad son requeridas.')
    ], default=True)


class EvaluationForm(Form):
    rate = RadioField(u'Evaluación', [
        InputRequired(u'Por favor, seleccione una de las 5 calificaciones.')
    ], choices=[
        ('1', 'rate_1'),
        ('2', 'rate_2'),
        ('3', 'rate_3'),
        ('4', 'rate_4'),
        ('5', 'rate_5'),
    ])
    comments = TextField('Comentarios', [
        # InputRequired(u'Por favor, describa brevemente el motivo de su '
        #               u'calificación.'),
        Length(0, 500, message=u'Los comentarios deben tener un mínimo de 10 '
                                u'carcateres o un máximo de 500.')
    ], default='')
    policy = BooleanField(u'Políticas de Privacidad', [
        InputRequired(u'Las Politícas de Privacidad son requeridas.')
    ], default=True)