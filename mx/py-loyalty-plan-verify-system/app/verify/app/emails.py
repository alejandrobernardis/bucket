#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 26/Feb/2014 18:45


RECOVERY_PASSWORD = u'''
Hola %(username)s,

Su clave de verificación es: %(activation_key)s

Por favor, haga clic en la siguiente liga o copie la misma en su navegador de preferencia.

http://%(site_domain)s/auth/recovery/verify/%(activation_key)s

Recuerde: La clave es válida solo por un día.

Saludos,

Addicted.-
http://www.addicted.com.mx

'''


CONFIRMATION = u'''
Hola %(username)s,

Para finalizar el proceso de pre-registro, necesitamos verificar la autenticidad de su cuenta de Email.

Por favor, haga clic en la siguiente liga o bien copie la misma en su navegador de preferencia.

http://%(site_domain)s/auth/request/verify/%(token)s/%(activation_key)s

Recuerde: Una vez verificada su cuenta, en un lapso de 48 horas recibirá otro correo para obtener los datos de acceso al sistema.

Saludos,

Addicted.-
http://www.addicted.com.mx

'''


ACCESS = u'''
Hola %(first_name)s,

BIEN!!

Hemos finalizado el proceso de verificación de datos, por este medio le hacemos llegar los datos de acceso al sistema.


SUS DATOS DE ACCESO SON:
URL: http://%(site_domain)s
Email: %(email)s
Usuario: %(username)s
Contraseña: %(password)s


Por favor, en caso de encontrarse con un problema, ponerse en contacto con el administrador de sistemas vía email sysadmin@addicted.com.mx

Saludos,

Addicted.-
http://www.addicted.com.mx

'''


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

Addicted.-
http://www.addicted.com.mx

'''
