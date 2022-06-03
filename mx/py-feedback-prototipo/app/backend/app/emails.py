#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 28/Apr/2014 19:05

RECOVERY_PASSWORD_SUBJECT = u'[NO RESPONDER]: Feedback / Recuperación de Contraseña'
RECOVERY_PASSWORD = u'''
Hola %(username)s,

Su clave de verificación es: %(activation_key)s

Por favor, haga clic en la siguiente liga o copie la misma en su navegador de preferencia.

http://%(site_domain)s/auth/recovery/verify/%(activation_key)s

Recuerde: La clave es válida solo por un día.

Saludos,

Feedback.-
http://%(site_domain)s

'''

RECOVERY_PASSWORD_NEW_SUBJECT = u'[NO RESPONDER]: Feedback / Alta de Cuenta'
RECOVERY_PASSWORD_NEW = u'''
Hola %(first_name)s,


SUS DATOS DE ACCESO SON:

URL: http://%(site_domain)s
Email: %(email)s
Usuario: %(username)s
Contraseña: *** no definida ***


OBTENER CONTRASEÑA:

Por favor, haga clic en la siguiente liga o copie la misma en su navegador de preferencia.

http://%(site_domain)s/auth/recovery/verify/%(activation_key)s


Saludos,

Feedback.-
http://%(site_domain)s

'''


CONFIRMATION_SUBJECT = u'[NO RESPONDER]: Feedback / Verificación de datos'
CONFIRMATION = u'''
Hola %(username)s,

Para finalizar el proceso de pre-registro, necesitamos verificar la autenticidad de su cuenta de Email.

Por favor, haga clic en la siguiente liga o bien copie la misma en su navegador de preferencia.

http://%(site_domain)s/auth/request/verify/%(token)s/%(activation_key)s

Recuerde: Una vez verificada su cuenta, en un lapso de 48 horas recibirá otro correo para obtener los datos de acceso al sistema.

Saludos,

Feedback.-
http://%(site_domain)s

'''


ACCESS_SUBJECT = u'[NO RESPONDER]: Feedback / Datos de acceso'
ACCESS = u'''
Hola %(first_name)s,

BIEN!!

Hemos finalizado el proceso de verificación de datos, por este medio le hacemos llegar los datos de acceso al sistema.


SUS DATOS DE ACCESO SON:
URL: http://%(site_domain)s
Email: %(email)s
Usuario: %(username)s
Contraseña: %(password)s


Por favor, en caso de encontrarse con un problema, ponerse en contacto con el administrador de sistemas vía email sysadmin@feedback.com.mx

Saludos,

Feedback.-
http://%(site_domain)s

'''


ACTIVATION_SUBJECT = u'[NO RESPONDER]: Feedback / Verificación de usuario'
ACTIVATION = u'''
ACTIVACIÓN DE USUARIO:

--
Empresa: %(company)s
Nombre(s): %(first_name)s
Apellido(s): %(last_name)s
Email: %(email)s
Teléfono: %(phone_lada)s - %(phone_number)s
Creado: %(created)s


--
PERMITIR
http://%(site_domain)s/auth/request/allow/%(oid)s/%(token)s


--
DENEGAR
http://%(site_domain)s/auth/request/deny/%(oid)s/%(token)s


Saludos,

Feedback.-
http://%(site_domain)s

'''


NOTIFICATION_SUBJECT = u'[NO RESPONDER]: Feedback / Evaluación finalizada / %s'
NOTIFICATION = u'''
Hola,

%(client)s, ha realizado la siguiente evaluación:

--
Calificación:
%(rate)s

Comentarios:
%(comments)s


--
Link:
http://%(site_domain)s/a/evaluations?q=%(activation_key)s


Saludos,

Feedback.-
http://%(site_domain)s
'''

NOTIFICATION_ANSWER_SUBJECT = u'[NO RESPONDER]: Feedback / Respuesta'
NOTIFICATION_ANSWER = u'''
Hola %(first_name)s,

%(first_name_user)s, ha respondido a sus comentarios:

--
Calificación:
%(rate)s

Comentarios:
%(comments)s

Respuesta:
%(answer)s


--
Vias de contacto:
Teléfono: %(phone)s
Email: %(email)s


--
Link:
http://%(site_domain)s/evaluation/%(activation_key)s


Saludos,

Feedback.-
http://%(site_domain)s
'''

NOTIFICATION_EVALUATION_SUBJECT = u'[NO RESPONDER]: Feedback / Evaluación'
NOTIFICATION_EVALUATION = u'''
Hola %(first_name)s,

Por favor, haga clic en la siguiente liga o copie la misma en su navegador de preferencia.

http://%(site_domain)s/p/evaluation/verify/%(activation_key)s

Su clave de evaluación es:

%(activation_key)s

La evaluación expira en 7 días.


Saludos,

Feedback.-
http://%(site_domain)s
'''