#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Apr 28, 2012, 3:55:20 PM

import datetime, logging, csv, cStringIO, codecs

from mongoengine import Q
from mx.yr.xxx.luminous.landing.forms import UserActivateForm
from mx.yr.xxx.luminous.landing.models import *
from mx.yr.tornado.handlers import AuthBaseHandler
from mx.yr.tornado.models import User, LegalAudit, Location
from mx.yr.tornado.security import Role, roles
from mx.yr.tornado.utils import datetime_to_str
from tornado.web import authenticated

#: -- MainHandler --------------------------------------------------------------

class ObjectReport(object):
    def __init__(self, title, total):
        self.title = title
        self.total = total

class MainHandler(AuthBaseHandler):

    @authenticated
    @roles('admin')
    def get(self):
        _total = []
        #: ---------------------------------------------------------------------
        #_qDateTime = datetime.datetime(2012, 7, 20, 0, 0, 0)
        _qDateTime = datetime.datetime.today()
        _QDT = Q(modified__lt=_qDateTime)
        #: ---------------------------------------------------------------------
        t = User.objects(Q(enabled=True)&_QDT&\
                         Q(role=Role.get_role('user').permissions)).count() or 0
        _total.append(ObjectReport(title="Usuarios", total=t))
        t = User.objects(Q(enabled=False)&_QDT&\
                         Q(role=Role.get_role('user').permissions)).count() or 0
        _total.append(ObjectReport(title="Usuarios - Bloqueado", total=t))
        t = LegalAudit.objects(Q(enabled=True)&_QDT).count() or 0
        _total.append(ObjectReport(title="Auditorias", total=t))
        #: ---------------------------------------------------------------------
        t = ProductTicket.objects(Q(enabled=True)&_QDT).count() or 0
        _total.append(ObjectReport(title="Tickets", total=t))
        #: ---------------------------------------------------------------------
        t = Product.objects(Q(enabled=True)&_QDT).sum('quantity') or 0
        _total.append(ObjectReport(title="Productos", total=t))
        t = Product.objects(Q(enabled=True)&Q(category=2)&_QDT).sum('quantity') or 0
        _total.append(ObjectReport(title="Productos - Pasta", total=t))
        t = Product.objects(Q(enabled=True)&Q(category=1)&_QDT).sum('quantity') or 0
        _total.append(ObjectReport(title="Productos - Cepillo", total=t))
        t = Product.objects(Q(enabled=True)&Q(category=3)&_QDT).sum('quantity') or 0
        _total.append(ObjectReport(title="Productos - Enjuague", total=t))
        #: ---------------------------------------------------------------------
        t = Code.objects(Q(availabled=True)&_QDT).count() or 0
        _total.append(ObjectReport(title=u"Códigos", total=t))
        t = Code.objects(Q(enabled=True)&Q(availabled=True)&_QDT).count() or 0
        _total.append(ObjectReport(title=u"Códigos - Sin Redimir", total=t))
        t = Code.objects(Q(enabled=False)&_QDT).count() or 0
        _total.append(ObjectReport(title=u"Códigos - Redimidos", total=t))
        t = Code.objects(Q(enabled=False)&Q(category=2)&_QDT).count() or 0
        _total.append(ObjectReport(title=u"Códigos - Redimidos -  Flyers",
                                   total=t))
        t = Code.objects(Q(enabled=False)&Q(category=1)&_QDT).count() or 0
        _total.append(ObjectReport(title=u"Códigos - Redimidos - Accesorios",
                                   total=t))
        t = Code.objects(Q(enabled=False)&Q(category=3)&_QDT).count() or 0
        _total.append(ObjectReport(title=u"Códigos - Redimidos - Twitter",
                                   total=t))
        t = Code.objects(Q(enabled=False)&Q(category=4)&_QDT).count() or 0
        _total.append(ObjectReport(title=u"Códigos - Redimidos - Auditoria",
                                   total=t))
        #: ---------------------------------------------------------------------
        t = GamePoint.objects(Q(enabled=True)&_QDT).count() or 0
        _total.append(ObjectReport(title=u"Juego - Intentos", total=t))
        #: ---------------------------------------------------------------------
        top_10_users = Points.objects(Q(enabled=True)&_QDT)\
                             .skip(0)\
                             .limit(10)\
                             .order_by('-points') or []
        #: ---------------------------------------------------------------------
        top_10_audits = User.objects(Q(enabled=False)&_QDT&\
                                    Q(role=Role.get_role('user').permissions))\
                            .skip(0)\
                            .limit(50)\
                            .order_by('-modified') or []
        #: ---------------------------------------------------------------------
        self.render("admin/index.html",
                    totals=_total, top_10_users=top_10_users,
                    top_10_audits=top_10_audits)

class AdminReportHandler(AuthBaseHandler):

    @authenticated
    @roles('admin')
    def get(self):
        user = self.get_argument("u", None)
        if not user:
            return self.render_error(message=u"The username is undefined,",
                                     next="/_/admin")
        user = User.get_user_by_uid(user)
        if not user:
            return self.render_error(message=u"The username is not found.",
                                     next="/_/admin")
        report_points = Points.get_points_by_user(user)
        report_game = GamePoint.get_by_user(user, True)
        report_codes = Code.get_codes_by_user(user)
        report_audit = LegalAudit.objects(Q(enabled=True)&Q(user_id=user))\
                                 .order_by('-created')\
                                 .all() or []
        report_tickets = ProductTicket.get_by_user(user, True)
        report_tickets_list = [0,0,0,0]
        report_tickets_points_list = [0,0,0,0]
        for a in report_tickets:
            items_list = Product.get_all(a, only_enabled=True)
            for b in items_list:
                report_tickets_list[b.category] += b.quantity
                report_tickets_list[0] += b.quantity
                report_tickets_points_list[b.category] += b.points
                report_tickets_points_list[0] += b.points
        self.render("admin/report.html",
                    report_points=report_points,
                    report_audit=report_audit,
                    report_game=report_game,
                    report_codes=report_codes,
                    report_tickets=report_tickets,
                    report_tickets_list=report_tickets_list,
                    report_tickets_points_list=report_tickets_points_list,
                    user=user)

class AdminMicroReportHandler(AuthBaseHandler):

    @authenticated
    @roles('admin')
    def get(self):
        u = self.get_argument("u", None)
        if not u:
            return self.render_error(message=u"The username is undefined,",
                                     next="/_/admin")
        user = User.get_user_complex(u)
        if not user:
            return self.render_error(message=u"The username is not found.",
                                     next="/_/admin")
        report_tickets = ProductTicket.get_by_user(user, True)
        _result = []
        self.write('<pre><br>')
        self.write('<strong>%s, %s (%s)</strong><br>' % (user.last_name, user.first_name, user.username))
        self.write('================================================================================<br>')
        self.write(' * Email: %s<br>' % user.email)
        self.write(' * Creado: %s<br>' % datetime_to_str(user.created))
        self.write(u' * Último Acceso: %s<br>' % datetime_to_str(user.last_login))
        self.write('<br><br><strong>REPORTE:</strong><br>================================================================================<br>')
        for a in report_tickets:
            self.write('<strong>[%s]:</strong><br>' % datetime_to_str(a.created))
            self.write(' - rfc: %s<br>' % a.rfc)
            self.write(' - date: %s<br>' % datetime_to_str(a.date_and_time))
            items_list = Product.get_all(a, only_enabled=True)
            self.write(' + <u>Productos:</u><br>')
            for b in items_list:
                self.write('   - %s: %s (%s)<br>' % (b.get_category(),
                                                     b.quantity, b.points))
            self.write("<span style=\"color: #ddd;\">--------------------------------------------------------------------------------</span><br>")
        self.write('</pre>')

class AdminLegalReportHandler(AuthBaseHandler):

    @authenticated
    @roles('admin')
    def get(self):
        audit = LegalAudit.objects
        self.write('<pre>')
        for a in audit:
            try:
                if not isinstance(a.user_id, User):
                    raise
                self.write("<strong>[%s]:</strong><br>" % datetime_to_str(a.created))
                self.write(" - %s<br>" % a.menssage)
                self.write(" - %s, %s<br>" % (
                    a.user_id.last_name.encode('utf-8').upper(),
                    a.user_id.first_name.encode('utf-8').upper()))
                self.write(" - %s<br>" % a.user_id.email)
                self.write(" - (%s) %s<br>" % (str(a.user_id.phone_lada),
                                               str(a.user_id.phone_number)))
                self.write("---- ---- ---- ---- ---- ---- ---- ---- ----<br>")
            except:
                pass
        self.write('</pre>')
        self.finish('')

class AdminUserEnabledHandler(AuthBaseHandler):
    __template = "admin/user.html"

    @authenticated
    @roles('admin')
    def get(self):
        self.render(self.__template, form=UserActivateForm(),
                    report_audit=None, errors={})

    @authenticated
    @roles('admin')
    def post(self):
        form_data = UserActivateForm(self)
        if not form_data.validate():
            errors = self.get_json_dumps(1, form_data.errors)
            return self.render(self.__template, form=form_data,
                               report_audit=None, errors=errors)
        try:
            user = User.get_user_complex(form_data.username.data)
            if not user:
                message = u"El nombre de usuario es incorrecto."
                errors = self.get_json_dumps(2, message)
                return self.render(self.__template, report_audit=None,
                                   form=form_data, next="/_/admin/user",
                                   errors=errors)
            else:
                _Q = Q(enabled=True)&Q(user_id=user)
                report_audit = LegalAudit.objects(_Q)\
                                         .order_by('-created').all() or None
                if not report_audit:
                    message = u"El nombre de usuario no posee auditorias."
                    errors = self.get_json_dumps(3, message)
                else: errors = {}
                self.render(self.__template, form=UserActivateForm(),
                            report_audit=report_audit, user=user, errors=errors)
        except Exception as E:
            return self.render_error(message=str(E), next="/_/admin/user")


class AdminUserActivateHandler(AuthBaseHandler):

    @authenticated
    @roles('admin')
    def get(self):
        next_url = "/_/admin/user"
        k = self.get_argument('k', None)
        if not k:
            message = u"El ID del usuario no esta definido."
            return self.render_error(message=message, next=next_url)
        try:
            user = User.get_user_by_uid(k)
            if not user:
                message = u"El usuario no existe."
                return self.render_error(message=message, next=next_url)
            _Q = Q(enabled=True)&Q(user_id=user)
            _report = LegalAudit.objects(_Q).order_by('-created').all() or None
            if not _report:
                message = u"El usuario no posee auditorias."
                return self.render_error(message=message, next=next_url)
            _report.update(set__enabled=False,
                           set__modified=datetime.datetime.now())
            user.update(set__enabled=True,
                        set__modified=datetime.datetime.now())
            message = u"El proceso finalizo correctamente."
            return self.render_success(message=message, next="/_/admin")
        except Exception as E:
            return self.render_error(message=str(E), next=next_url)


#: -----------------------------------------------------------------------------

class AdminTicketRemoveHandler(AuthBaseHandler):

    @authenticated
    @roles('admin')
    def get(self):
        next_url = "/_/admin"
        k = self.get_argument('k', None)
        if not k:
            message=u"El ticket no esta definido."
            return self.render_error(message=message, next=next_url)
        try:
            ticket = ProductTicket.get_by_token(k, True)
            if not ticket:
                message=u"El ticket no existe."
                return self.render_error(message=message, next=next_url)
            ticket = ticket[0]
            products = Product.get_all(ticket, only_enabled=True)
            if not products:
                message=u"El ticket no posee productos."
                return self.render_error(message=message, next=next_url)
            points_dec = 0
            for a in products:
                points_dec += a.points
            points = Points.objects(user_id=ticket.user_id).first()
            if not points or points < 1:
                message=u"El usuario no posee puntos."
                return self.render_error(message=message, next=next_url)
            old_points = points.points
            points.update(dec__points=points_dec,
                          set__modified=datetime.datetime.now())
            points.reload()
            logging.info("Points (t=%s): %s [-%s], %s" %
                         (k, old_points, points_dec, points.points))
            ticket.update(set__enabled=False,
                          set__modified=datetime.datetime.now())
            products.update(set__enabled=False,
                            set__modified=datetime.datetime.now())
            message = u"El ticket '%s' fue removido." % k
            logging.info(message)
            next_url = "/_/admin/report?u=%s" % ticket.user_id.id
            return self.render_success(message=message, next=next_url)
        except Exception as E:
            return self.render_error(message=str(E), next="/_/admin/user")

#: -----------------------------------------------------------------------------

class AdminUsersDownloadHandler(AuthBaseHandler):

    #@authenticated
    #@roles('admin')
    def get(self):
        _Q = Q(role=1)
        _total = User.objects(_Q).count()

        if _total < 1:
            return self.render_error(message="No hay usuarios disponibles",
                                     next="/")

        else:
            _skip = 0
            _limit = 100
            _range = int(_total/_limit)+1

            _file_dir = self.settings.get("download_path")
            _file_name = "users_dump_%s.csv" % \
                         datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f")

            _file_path = "%s/%s" % (_file_dir, _file_name)
            _file_header = ["id", "fuid", "created", "modified", "first_name",
                            "middle_name", "last_name", "gender", "birthday",
                            "username", "email", "phone_lada", "phone_number",
                            "location", "remote_ip", "news", "terms", "policy"]

            def csv_write_row(row, _queue, _writer, _stream, _encoder, _encoding="utf-8"):

                """try:
                    for s in row:
                        s.encode(_encoding)
                except Exception as E:
                    print E, s

                return"""

                _writer.writerow([s.encode(_encoding) for s in row])
                data = _queue.getvalue()
                data = data.decode(_encoding)
                data = _encoder.encode(data)
                _stream.write(data)
                _queue.truncate(0)

            with open(_file_path, "wb") as f:
                _encoding = "utf-8" or "iso-8859-1"
                _queue = cStringIO.StringIO()
                _writer = csv.writer(_queue, dialect=csv.excel, delimiter=',',
                                     quotechar="'")
                _stream = f
                _encoder = codecs.getincrementalencoder(_encoding)()
                csv_write_row(_file_header, _queue, _writer, _stream, _encoder)

                for _ in range(_range):
                    _recordset = User.objects(_Q)\
                                     .skip(_skip*_limit)\
                                     .limit(_limit)

                    for row in _recordset:
                        _location = Location.get_location(row.address_state)
                        if type(_location) is not Location:
                            _location = ""
                        else:
                            _location = _location.name

                        _data = [
                            str(row.id),
                            row.facebook_uid or "",
                            datetime_to_str(row.created) or "",
                            datetime_to_str(row.modified) or "",
                            row.first_name or "",
                            row.middle_name or "",
                            row.last_name or "",
                            row.get_gender() or "",
                            datetime_to_str(row.birthday) or "",
                            row.username or "",
                            row.email or "",
                            str(row.phone_lada) or "-",
                            str(row.phone_number) or "-",
                            _location,
                            row.remote_ip or "0.0.0.0",
                            "yes" if row.news else "no",
                            "yes" if row.terms else "no",
                            "yes" if row.policy else "no"
                        ]

                        csv_write_row(_data, _queue, _writer, _stream, _encoder, _encoding)
                    _skip += 1

                recordset = dict(total=_total, file=_file_name)
                f.close()



#: -- handlers_list ------------------------------------------------------------

handlers_list = [
    (r"/_/admin", MainHandler),
    (r"/_/admin/report", AdminReportHandler),
    (r"/_/admin/microreport", AdminMicroReportHandler),
    (r"/_/admin/audits", AdminLegalReportHandler),
    (r"/_/admin/user", AdminUserEnabledHandler),
    (r"/_/admin/user/activate", AdminUserActivateHandler),
    (r"/_/admin/users/download", AdminUsersDownloadHandler),
    (r"/_/admin/ticket/remove", AdminTicketRemoveHandler),
]

#: -- ui_modules_list ----------------------------------------------------------

ui_modules_list = {}
