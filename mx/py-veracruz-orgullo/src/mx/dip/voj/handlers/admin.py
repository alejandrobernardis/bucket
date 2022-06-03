#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.m.bernardis at gmail.com
# Created: Jan 4, 2013 1:09:35 PM

#: imports

import datetime, sys, os, shutil, re
from com.ak.common.security import token
from com.ak.common.utils import safe_str_cmp
from com.ak.common.wrappers import authenticated_plus
from com.ak.models.users import User
from dateutil.relativedelta import relativedelta
from mongoengine import Q
from mx.dip.voj.handlers.base import AuthBaseHandler, AuthLoginHandler
from mx.dip.voj.handlers.forms import RegisterUpdate, RegisterDelete, \
    EventDelete, EventAdd, EventUpdate, EventsDeploy
from mx.dip.voj.models.countries import Country
from mx.dip.voj.models.events import Event, Image, Track, Url
from PIL import Image as PImage
from settings import USER_DATA_IGNORE_EXTENDS, USER_ROLE_ID,\
    SITE_STATIC_DAT_EVENTS, SITE_STATIC_IMG_EVENTS, \
    SITE_IMAGE_IMG_EVENTS, SITE_IMAGE_PAT_EVENTS

ITEMS_PAGE = 25
E_0 = 'The process is finished correctly.'
E_1001 = 'Not Support.'

#: === === === === === === === === === === === === === === === === === === === ===

class HelperHandler(AuthBaseHandler):
    @authenticated_plus('admin')
    def get(self):
        return self.get_json_response_and_finish(1001, E_1001)

#: === === === === === === === === === === === === === === === === === === === ===
 
class MainHandler(AuthBaseHandler):
    @authenticated_plus('admin')
    def get(self):
        _Q = Q(enabled=True)&Q(available=True)
        registers = User.objects(_Q&Q(role_id=1)).count()
        events = Event.objects(_Q).count()
        self.render('admin/index.html', registers=registers, events=events)

#: === === === === === === === === === === === === === === === === === === === ===

class RegistersHandler(AuthBaseHandler):
    @authenticated_plus('admin')
    def get(self):
        try:
            _Q = Q(role_id=USER_ROLE_ID)&User.get_status_query()
            total_users = User.objects(_Q).count()
            if total_users < 1:
                raise
            page = int(self.get_argument('page', 1))
            pages = self.do_paginate(page, ITEMS_PAGE, total_users)
            users = User.do_paginate(_Q, page, pages.get('page_size'))
            users_list = dict()
            for a in users:
                users_list[str(a.id)] = a.to_object(USER_DATA_IGNORE_EXTENDS)
            users_list = self.get_json_dumps(obj=users_list)
            self.render('admin/registers.html', users=users, users_list=users_list,
                                                total_users=total_users, **pages)
        except:
            self.render('admin/not_found.html', message="Actually, we can't find registers into database.")

class RegisterHelperHandler(HelperHandler):
    def do_recalculate_pagination(self):
        _Q = Q(role_id=USER_ROLE_ID)&User.get_status_query()
        total_users = User.objects(_Q).count()
        if total_users < 1:
            return
        page = self.get_argument('page_number', 1)
        pagination = self.do_paginate(page, ITEMS_PAGE, total_users)
        page_total = pagination.get('page_total')
        if page > page_total:
            pagination['page_number'] = page_total
        return pagination

class RegisterUpdateHandler(RegisterHelperHandler):
    @authenticated_plus('admin')
    def post(self):
        try:
            response = self.do_update()
            return self.get_json_response_and_finish(obj=response)
        except Exception as E:
            return self.get_json_response_and_finish(1000, str(E))

    def do_update(self, form_data=None):
        if not form_data:
            form_data = RegisterUpdate(self)
        if not form_data.validate():
            return self.get_response_object(1, form_data.errors)
        try:
            user = User.get_by_uid(form_data.uid.data)
            if not user:
                return self.get_response_object(1, 'The user does not exist.')
            if user.token not in form_data.token.data:
                return self.get_response_object(1, "Object's keys does not match.")
            try:
                birthday = datetime.datetime.strptime(form_data.birthday.data, '%Y/%m/%d')
            except:
                return self.get_response_object(1, 'The date of birth is incorrect.')
            try:
                country = None
                if form_data.country.data > 0:
                    country = Country.get_by_id(form_data.country.data)
            except:
                return self.get_response_object(1, 'The country id is incorrect.')
            user.update(
                set__first_name = form_data.first_name.data,
                set__last_name = form_data.last_name.data,
                set__email = form_data.email.data,
                set__birthday = birthday,
                set__country = country,
                set__city = form_data.city.data,
                set__news = form_data.news.data,
                set__modified = datetime.datetime.now())
            user.reload()
            return self.get_response_object(0, E_0, user.to_object())
        except Exception as E:
            return self.get_response_object(1000, str(E))

class RegisterDeleteHandler(RegisterHelperHandler):
    @authenticated_plus('admin')
    def post(self):
        try:
            response = self.do_delete()
            return self.get_json_response_and_finish(obj=response)
        except Exception as E:
            return self.get_json_response_and_finish(1000, str(E))

    def do_delete(self, form_data=None):
        if not form_data:
            form_data = RegisterDelete(self)
        if not form_data.validate():
            return self.get_response_object(1, form_data.errors)
        try:
            user = User.get_by_uid(form_data.uid.data)
            if not user:
                return self.get_response_object(1, 'The user does not exist.')
            if user.token not in form_data.token.data:
                return self.get_response_object(1, "Object's keys does not match.")
            user.set_logic_low()
            pagination = self.do_recalculate_pagination()
            return self.get_response_object(0, E_0, pagination)
        except Exception as E:
            return self.get_response_object(1000, str(E))

#: === === === === === === === === === === === === === === === === === === === ===

class EventHandler(AuthBaseHandler):
    @authenticated_plus('admin')
    def get(self):
        try:
            _Q = Q(available=True)
            total_events = Event.objects(_Q).count()
            if total_events < 1:
                raise
            page = int(self.get_argument('page', 1))
            pages = self.do_paginate(page, ITEMS_PAGE, total_events)
            events = Event.do_paginate(_Q, page, pages.get('page_size'), order_by='-date')
            events_list = dict()
            for a in events:
                events_list[str(a.id)] = a.to_object()
            events_list = self.get_json_dumps(obj=events_list)
            self.render('admin/events.html', events=events, events_list=events_list,
                                             total_events=total_events, **pages)
        except:
            pages = self.do_paginate(1, ITEMS_PAGE, 25)
            self.render('admin/events.html', message="Actually, we can't find events into database.",
                        events=[], events_list=[], total_events=0, **pages)

class EventHelperHandler(HelperHandler):
    def do_recalculate_pagination(self):
        _Q = Event.get_status_query()
        total_events = Event.objects(_Q).count()
        if total_events < 1:
            return
        page = self.get_argument('page_number', 1)
        pagination = self.do_paginate(page, ITEMS_PAGE, total_events)
        page_total = pagination.get('page_total')
        if page > page_total:
            pagination['page_number'] = page_total
        return pagination

    def do_get_date(self, form_data):
        try:
            date = datetime.datetime.strptime(form_data.date.data, '%Y/%m/%d')
            return date
        except:
            return None

    def do_validate_date(self, form_data):
        try:
            event_date = self.do_get_date(form_data)
            if not event_date:
                return False, self.get_response_object(1, u'La fecha del evento es incorrecta.')
            if event_date.year < datetime.datetime.now().year:
                return False, self.get_response_object(1, u'El año del evento en menor al año actual.')
            return True, event_date
        except:
            return False, None

    def do_resize_image(self, form_data):
        if form_data.image_src.data:
            image_name = form_data.image_src.data
            regex_str = r'^[a-z0-9]{16,64}\.[a-z]{3,4}'
            regex = re.compile(regex_str, re.IGNORECASE)
            if not regex.match(image_name):
                return False, self.get_response_object(1, u'La referencia de la imagen es incorrecta.')
            image_from = self.settings.get('temp_path') + '/' + image_name
            if not os.path.isfile(image_from):
                return False, self.get_response_object(1, u'La imagen subida no existe, por favor vuelva a subir una imagen nuevamente.')
            #image_to = self.settings.get('static_path') + '/img/events/' + image_name
            image_to = SITE_STATIC_IMG_EVENTS + '/' + image_name
            try:
                image_bin = PImage.open(image_from)
                image_real_w = image_bin.size[0]
                image_real_h = image_bin.size[1]
                image_final_w = 230
                if image_real_w < image_final_w:
                    return False, self.get_response_object(1, u'El ancho de la imagen debe ser mayor o igual a %spx.' % image_final_w)
                image_percentage_w = image_final_w / float(image_real_w)
                image_final_h = int(float(image_real_h) * float(image_percentage_w))
                image_output = image_bin.resize((image_final_w, image_final_h), PImage.ANTIALIAS)
                image_output.save(image_to)
            except:
                shutil.copyfile(image_from, image_to)
            try:
                if os.path.isfile(image_to):
                    os.remove(image_from)
            except:
                return False, self.get_response_object(1, u'La imagen subida no pudo ser cropiada.')
            return True, dict(image_name=image_name, image_from=image_from, image_to=image_to)
        return False, None

    def do_update_image(self, form_data):
        image = Image.get_by_uid(form_data.image_id.data)
        if not image:
            return self.do_save_image(form_data)
        if safe_str_cmp(image.src, form_data.image_src.data):
            try:
                image.update(
                    set__alt = form_data.image_alt.data or image.alt,
                    set__modified = datetime.datetime.now())
                image.reload()
            except Exception as E:
                return self.get_response_object(1, u'[IMG]::'+str(E))
        else:
            image_old = image.path
            image_status, image_data = self.do_resize_image(form_data)
            if not image_status:
                return image_data
            try:
                image.update(
                    set__src = SITE_IMAGE_PAT_EVENTS + '/' + image_data.get('image_name'),
                    set__alt = form_data.image_alt.data or image.alt,
                    set__path = image_data.get('image_to'),
                    set__modified = datetime.datetime.now())
                image.reload()
            except Exception as E:
                return self.get_response_object(1, u'[IMG]::'+str(E))
            try:
                if os.path.isfile(image_old):
                    os.remove(image_old)
            except:
                return self.get_response_object(1, u'La imagen antigua no puedo ser eliminada.')
        return image

    def do_save_image(self, form_data):
        image_status, image_data = self.do_resize_image(form_data)
        if not image_status:
            return image_data
        try:
            image = Image(enabled=True, available=True)
            image.token = token(32)
            image.src = SITE_IMAGE_PAT_EVENTS + '/' + image_data.get('image_name')
            image.alt = form_data.image_alt.data
            image.path = image_data.get('image_to')
            image.created = datetime.datetime.now()
            image.save()
            return image
        except Exception as E:
            return self.get_response_object(1, u'[IMG]::'+str(E))

    def do_validate_url(self, url):
        regex_str = r'^[a-z]+:(//)?([a-z]+\.)?([a-z0-9@]*)\.[a-z]{2,3}(\.[a-z]{2,3})?/?.*'
        regex = re.compile(regex_str, re.IGNORECASE)
        if not regex.match(url):
            return False, self.get_response_object(1, u'La liga del evento es incorrecta.')
        return True, None

    def do_save_url(self, form_data):
        if form_data.url_value.data:
            url_value, url_error = self.do_validate_url(form_data.url_value.data)
            if not url_value:
                return  url_error
            url = Url.get_by_value(form_data.url_value.data)
            if not url:
                track = Track()
                track.category = form_data.track_category.data or 'events'
                track.action = form_data.track_action.data or 'click'
                track.label = form_data.track_label.data or token(16)
                try:
                    url = Url(enabled=True, available=True)
                    url.token = token(32)
                    url.title = form_data.url_title.data or 'liga'
                    url.value = form_data.url_value.data
                    url.track = track
                    url.created = datetime.datetime.now()
                    url.save()
                except Exception as E:
                    return self.get_response_object(1, u'[URL]::'+str(E))
            return url
        return None

    def do_update_url(self, form_data):
        if form_data.url_value.data:
            url_value, url_error = self.do_validate_url(form_data.url_value.data)
            if not url_value:
                return  url_error
            url = Url.get_by_value(form_data.url_value.data)
            if not url:
                return self.do_save_url(form_data)
            try:
                url.update(
                    set__title = form_data.url_title.data or 'liga',
                    set__track__label = form_data.track_label.data or token(16),
                    set__modified = datetime.datetime.now())
                url.reload()
                return url
            except Exception as E:
                return self.get_response_object(1, u'[URL]::'+str(E))
        return None

    def do_validate_event(self, form_data):
        if form_data.uid.data:
            event = Event.get_by_uid_woc(form_data.uid.data)
            if not event:
                return False, self.get_response_object(1, 'The event does not exist.')
            if event.token not in form_data.token.data:
                return False, self.get_response_object(1, "Object's keys does not match.")
            return True, event
        return False, self.get_response_object(1, 'The event id is null.')

class EventAddHandler(EventHelperHandler):
    @authenticated_plus('admin')
    def post(self):
        try:
            response = self.do_add()
            return self.get_json_response_and_finish(obj=response)
        except Exception as E:
            return self.get_json_response_and_finish(1000, str(E))

    def do_add(self, form_data=None):
        if not form_data:
            form_data = EventAdd(self)
        if not form_data.validate():
            return self.get_response_object(1, form_data.errors)
        try:
            event_date_error, event_date = self.do_validate_date(form_data)
            if not event_date_error:
                return event_date
            image = self.do_save_image(form_data)
            if image and not isinstance(image, Image):
                return image
            url = self.do_save_url(form_data)
            if url and not isinstance(url, Url):
                if image:
                    image.delete()
                return url
            try:
                event = Event(available=True)
                event.token = token(32)
                event.title = form_data.title.data
                event.date = event_date
                event.place = form_data.place.data
                event.phone = form_data.phone.data
                event.url = url
                event.image = image
                event.enabled = form_data.enabled.data
                event.created = datetime.datetime.now()
                event.save()
            except Exception as E:
                if image:
                    image.delete()
                if url:
                    url.delete()
                return self.get_response_object(1, u'[EVENT]::'+str(E))
            return self.get_response_object(0, E_0)
        except Exception as E:
            return self.get_response_object(1000, str(E))

class EventUpdateHandler(EventHelperHandler):
    @authenticated_plus('admin')
    def post(self):
        try:
            response = self.do_update()
            return self.get_json_response_and_finish(obj=response)
        except Exception as E:
            return self.get_json_response_and_finish(1000, str(E))

    def do_update(self, form_data=None):
        if not form_data:
            form_data = EventUpdate(self)
        if not form_data.validate():
            return self.get_response_object(1, form_data.errors)
        try:
            event_status, event = self.do_validate_event(form_data)
            if not event_status:
                return event
            event_date_error, event_date = self.do_validate_date(form_data)
            if not event_date_error:
                return event_date
            image = self.do_update_image(form_data)
            url = self.do_update_url(form_data)
            try:
                event.update(
                    set__title = form_data.title.data,
                    set__date = event_date,
                    set__place = form_data.place.data,
                    set__phone = form_data.phone.data,
                    set__url = url,
                    set__image = image,
                    set__enabled = form_data.enabled.data,
                    set__modified = datetime.datetime.now())
                event.reload()
            except Exception as E:
                return self.get_response_object(1, u'[EVENT]::'+str(E))
            return self.get_response_object(0, E_0)
        except Exception as E:
            return self.get_response_object(1000, str(E))

class EventDeleteHandler(EventHelperHandler):
    @authenticated_plus('admin')
    def post(self):
        try:
            response = self.do_delete()
            return self.get_json_response_and_finish(obj=response)
        except Exception as E:
            return self.get_json_response_and_finish(1000, str(E))

    def do_delete(self, form_data=None):
        if not form_data:
            form_data = EventDelete(self)
        if not form_data.validate():
            return self.get_response_object(1, form_data.errors)
        try:
            event_status, event = self.do_validate_event(form_data)
            if not event_status:
                return event
            event.set_logic_low()
            pagination = self.do_recalculate_pagination()
            return self.get_response_object(0, E_0, pagination)
        except Exception as E:
            return self.get_response_object(1000, str(E))

class EventUploadHandler(EventHelperHandler):
    @authenticated_plus('admin')
    def post(self):
        try:
            response = self.do_upload()
            return self.get_json_response_and_finish(obj=response)
        except Exception as E:
            return self.get_json_response_and_finish(1000, str(E))

    def do_upload(self):
        files = self.request.files
        if not len(files):
            return self.get_response_object(1, 'File not found.')
        result = dict()
        for f in files:
            f = files[f][0]
            if not self.is_image(f.content_type):
                return self.get_response_object(1, 'File not found.')
            if not self.get_size_image(f.body):
                return self.get_response_object(1, 'Default image upload size is 300KB.')
            file_extension =  str(os.path.splitext(f.filename)[1]).lower()
            file_name_new = '%s%s' % (token(32), file_extension)
            file_path_new = '%s/%s' % (self.settings.get('temp_path'), file_name_new)
            if self.write_image(file_path_new, f.body):
                result['src'] = file_name_new
                break
            else:
                return self.get_response_object(1, "Can't write file.")
        return self.get_response_object(0, E_0, result)

    def is_image(self, content_type):
        return content_type in ["image","image/png","image/jpeg","image/pjpeg","image/jpg","image/gif"]

    def get_size_image(self, body):
        size = sys.getsizeof(body)
        return (size / 1024) <= 300

    def write_image(self, file_name, file_body):
        try:
            f = open(file_name, 'w+')
            f.write(file_body)
        except:
            return False
        finally:
            return True

class EventDeployHandler(EventHelperHandler):
    @authenticated_plus('admin')
    def post(self):
        try:
            response = self.do_create()
            return self.get_json_response_and_finish(obj=response)
        except Exception as E:
            return self.get_json_response_and_finish(1000, str(E))

    def do_create(self, form_data=None):
        if not form_data:
            form_data = EventsDeploy(self)
        if not form_data.validate():
            return self.get_response_object(1, form_data.errors)
        try:
            _dt = datetime.datetime.now()
            year = int(form_data.year.data)
            if 0 < year < _dt.year:
                return self.get_response_object(1, u'El año del evento en menor al año actual.')
            if year < 1:
                year = _dt.year
            months = int(form_data.month.data)
            months = range(1,13) if months < 1 else range(months, months+1)
            month_name = ['','enero','febrero','marzo','abril','mayo','junio',
                          'julio','agosto','septiembre','octubre','noviembre','diciembre']
            status = Event.get_status_query()
            ignore = ['id','available','enabled','created','modified','token','path']
            for month in months:
                month_min = datetime.datetime(year,month,1)
                month_max = month_min + relativedelta(months=1)
                _Q = Q(date__gte=month_min)&Q(date__lt=month_max)&status
                events = Event.objects(_Q).order_by('+date').skip(0).limit(100)
                events_month = []
                for event in events:
                    ref = event.to_object(ignore)
                    events_month.append(ref)
                result = dict(
                    type='events',
                    year=year,
                    month=month,
                    image=SITE_IMAGE_IMG_EVENTS,
                    list=events_month)
                file_name = '%s.json' % month_name[month]
                file_path = '%s/%s' % (SITE_STATIC_DAT_EVENTS, year)
                file_output = '%s/%s' % (file_path, file_name)
                if not os.path.isdir(file_path):
                    os.mkdir(file_path)
                if os.path.isfile(file_output):
                    os.remove(file_output)
                with open(file_output, 'wb+') as f:
                    f.write(self.get_json_dumps(0,E_0,result))
            return self.get_response_object(0, E_0)
        except Exception as E:
            return self.get_response_object(1000, str(E))

#: === === === === === === === === === === === === === === === === === === === ===

class AuthLogoutHandler(AuthBaseHandler):
    def get(self):
        self.render('auth/logout.html')
        
    def post(self):
        self.do_logout('/a')

#: === === === === === === === === === === === === === === === === === === === ===

handlers_list = [
    (r'/a', MainHandler),
    (r'/a/registers', RegistersHandler),
    (r'/a/register/update', RegisterUpdateHandler),
    (r'/a/register/delete', RegisterDeleteHandler),
    (r'/a/events', EventHandler),
    (r'/a/events/deploy', EventDeployHandler),
    (r'/a/event/add', EventAddHandler),
    (r'/a/event/update', EventUpdateHandler),
    (r'/a/event/delete', EventDeleteHandler),
    (r'/a/event/upload', EventUploadHandler),
    #(r'/a/event/new', EventHandler),
    (r'/auth/login', AuthLoginHandler),
    (r'/auth/logout', AuthLogoutHandler),
]

