#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
sys.path.insert(0, '/var/www/vhosts/orgullojarocho.mx/backoffice/apps/administrator')

#: === === === === === === === === === === === === === === === === === === === =

try:
  import datetime, time
  from dateutil.relativedelta import relativedelta
  from optparse import OptionParser
  
except:
  print u'Not found modules'
  exit(0) 

#: === === === === === === === === === === === === === === === === === === === =

parser = OptionParser()
parser.add_option('-i', '--ignore', action='store_true', dest='ignore', default=False)
opts, args = parser.parse_args()

if not opts.ignore:
  message = u'\n - Are you sure to proceed? [y/n] --> '
  action = raw_input(message.encode('utf-8'))
  
  if action not in ['y','Y']:
    print u'Operation Canceled.'
    exit(0)
    
#: === === === === === === === === === === === === === === === === === === === =

base_path = '/var/www/vhosts/orgullojarocho.mx/backoffice/apps/administrator/mx/dip/voj/tmp'

if not os.path.isdir(base_path):
  print u'The directory does not exixts.'
  exit(0)
  
date_max = datetime.datetime.now() - relativedelta(days=7)
date_max_unix = time.mktime(date_max.timetuple())

print '\nProcess:'
print 'Unix Time:', date_max_unix
print 'ISO Time:', date_max
print 'Path:', base_path

cfind = 0
cremove = 0
print '\nFiles:'

for root, dirs, files in os.walk(base_path):
  if not len(files):
    exit(u'The directory is empty.')
  
  for name in files:
    cfind += 1
    file_tmp = base_path + '/' + name
    file_info = os.stat(file_tmp)
    file_time = file_info.st_atime
    print '\nFind:', file_tmp
    
    if file_time < date_max_unix:
      try:
        cremove += 1
        os.remove(file_tmp)
        print '\t[result]: remove =>', file_time, date_max_unix
      except:
        print '\t[result]: error (can\'t remove)'
    else:
      print '\t[result]: not remove'
      
#: === === === === === === === === === === === === === === === === === === === =

print '\nRemove:', cremove, 'of', cfind, '\n\n'

    