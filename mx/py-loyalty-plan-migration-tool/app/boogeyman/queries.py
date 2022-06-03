#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Asumi Kamikaze Inc.
# Copyright (c) 2014 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 29/Jan/2014 18:16

USER_TRUNCATE = \
    "truncate user;"

RECEIPT_TRUNCATE = \
    "truncate receipt;"

TRANSACTION_TRUNCATE = \
    "truncate transaction;"

USER_SELECT = \
    "select * from usuarios where id_perfil=2 and nombre_usuario IS NOT NULL order by id_usuario asc;"

USER_INSERT = \
    "insert into " \
    "user (" \
        "id, username, email, email_alternative, password, firstname, " \
        "last_name, mothers_maiden_name, telephone, mobile, gender, " \
        "birthdate, street, exterior, interior, newsletter, email_balance, " \
        "terms_conditions, privacy_policy, recovery, enabled, available, " \
        "created, modified, user_role_id, neighborhood_id, reference_id" \
    ") values (" \
        "%(id)s, %(username)s, %(email)s, %(email_alternative)s, " \
        "%(password)s, %(firstname)s, %(last_name)s, " \
        "%(mothers_maiden_name)s, %(telephone)s, %(mobile)s, %(gender)s, " \
        "%(birthdate)s, %(street)s, %(exterior)s, %(interior)s, " \
        "%(newsletter)s, %(email_balance)s, %(terms_conditions)s, " \
        "%(privacy_policy)s, %(recovery)s, %(enabled)s, " \
        "%(available)s, %(created)s, %(modified)s, %(user_role_id)s, " \
        "%(neighborhood_id)s, %(reference_id)s);"
    


USER_POINTS = \
    "select distinct (" \
    "select sum(puntos_obtenidos) from tickets " \
    "where id_cliente=%(id)s and fecha>'2013-11-30' and aprobado=1 and cancelado=0)-(" \
    "select IFNULL(sum(puntos), 0) from articulos_recibidos " \
    "where id_cliente=%(id)s and fecha_registro>'2013-11-30') as points;"
    
    
"""
    select distinct points.user_id as user_id, points.total-redeem.total as total
    from (
        select tickets.id_cliente as user_id, sum(tickets.puntos_obtenidos) as total
        from tickets where aprobado=1 and  cancelado=0 group by tickets.id_cliente
    ) points
    left join (
        select articulos_recibidos.id_cliente as user_id, sum(articulos_recibidos.puntos) as total
        from articulos_recibidos group by articulos_recibidos.id_cliente
    ) redeem on redeem.user_id=points.user_id
    order by user_id asc;    
"""    

USER_CARD_CLEAN = \
    "update card " \
    "set available=1, " \
        "status_id=2, " \
        "user_id=0, " \
        "number=replace(trim(number), '\t', '')" \
    "where 1=1;"

USER_CARD = \
    "select id, number from card " \
    "where available=1 and status_id=2 and type_id=%s and user_id=0 " \
    "order by id asc limit 1;"

# USER_CARD_ASSIGNED = \
#     "update card set user_id=%(id)s, status_id=1, modified=%(date)s " \
#     "where id=%(card)s"

USER_CARD_ASSIGNED = \
    "insert into " \
    "card (" \
        "available, modified, created, enabled, number, type_id, status_id, user_id" \
    ") values (" \
        "1, NOW(), NOW(), 1, %(real_username)s, 4, 1, %(id)s);"



USER_BONUS = \
    "insert into " \
    "receipt (" \
        "available, modified, created, enabled, number, amount, date, " \
        "store_id, encrypted" \
    ") values (" \
        "1, '2014-01-01 00:00:00','2014-01-01 00:00:00', 1, %(bonus)s, " \
        "%(amout)s, %(date)s, 0, %(encrypted)s);"

USER_TRANSACTION = \
    "insert into " \
    "transaction(" \
        "available, modified, created, enabled, point, redeemed, " \
        "transaction_type_id, transaction_status_id, receipt_id, " \
        "user_id, card_id, expired, total" \
    ") values (" \
        "1, '2014-01-01 00:00:00','2014-01-01 00:00:00', 1, %(points)s, 0, 3, 1, " \
        "%(receipt)s, %(id)s, %(card)s, 0, %(points)s);"
