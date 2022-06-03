EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mx.yr.mail@gmail.com'
EMAIL_HOST_PASSWORD = 'yrNSx09-mx3011'
EMAIL_USE_TLS = True

import os
op = os.path

PICKLE_LOCATION = op.join(op.dirname(__file__), 'pickled_messages')
if not op.isdir(PICKLE_LOCATION):
    os.mkdir(PICKLE_LOCATION)