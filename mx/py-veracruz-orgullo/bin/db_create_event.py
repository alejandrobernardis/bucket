#!/usr/bin/env python
# -*- coding: utf-8 -*-
import db_cnx

# imports
try:
    import settings, datetime
    from com.ak.common.security import token
    from dateutil.relativedelta import relativedelta
    from mx.dip.voj.models.events import Event, Track, Url, Image

except:
    exit(u'Ups!, no están todos los módulos.')

Url.drop_collection()
Image.drop_collection()
Event.drop_collection()

exit(0)

date_cero = datetime.date(2013,1,1)

for a in range(100):
    event = Event(enabled=True, available=True)
    event.token = token(32)
    event.title = u'Evento especial en las oficinas de México'
    event.date = date_cero + relativedelta(days=a*5)
    event.place = u'Paseo de la Reforma n.º 115, Piso 22, Col. Lomas de Chapultepec, México D.F. 11000, México'
    event.phone = u'+52 55-5342-8400'
    event.url = None
    event.image = None
    event.save()

exit(0)

image = Image(enabled=True, available=True)
image.token = token(32)
image.src = '/static/img/events/demo.jpg'
image.alt = u'datos de la imagen'
image.path = '/vol/static/img/events/demo.jpg'
image.save()

track = Track()
track.category = 'external'
track.action = 'click'
track.label = 'google-com'

url = Url(enabled=True, available=True)
url.token = token(32)
url.title = 'google'
url.value = 'http://google.com'
url.track = track
url.save()

event = Event(enabled=True, available=True)
event.token = token(32)
event.title = u'Evento especial en las oficinas de México'
event.date = datetime.datetime(2013,10,10)
event.place = u'Paseo de la Reforma n.º 115, Piso 22, Col. Lomas de Chapultepec, México D.F. 11000, México'
event.phone = u'+52 55-5342-8400'
event.url = url
event.image = image
event.save()

ignore = ['id','available','enabled','created','modified','token','path']

#
print Event.objects.count()
print event.to_object(ignore)
exit(0)

#
print url.to_object(ignore)
url.update(set__track__category='new-category')
url.reload()
print url.to_object(ignore)

#
print image.to_object(ignore)
image.update(set__alt=u'nueva descripción')
image.reload()
print image.to_object(ignore)
print event.to_object(ignore)