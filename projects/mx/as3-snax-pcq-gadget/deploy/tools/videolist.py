#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Young and Rubicam Digital Mexico.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: Feb 17, 2012 11:16:18 AM
#

import gdata.youtube.service
import os
import re
import shutil

from datetime import datetime

#: --
ytsrv = gdata.youtube.service.YouTubeService()
ytsrv.ssl = True
ytsrv.source = "Danone, Danette, Landning AGO_SEP_2011"
ytsrv.client_id = "Danone, Danette, Landning AGO_SEP_2011"
ytsrv.developer_key = "AI39si5m-XtUfOaWuP1BhhMB4pysCugPYr8TMIkQU4sS4gHIKYzv3rCXahDKiwguMD5NxTsBD1446dvL0WqcjQ6ZLfA5BJ0kTQ"

#: --
def PrintVideoList(vlist=None, vcount=0, vtotal=8, vi=0, user_name=None, file_name="db/database.csv"):
	if not user_name:
		raise TypeError('PrintVideoList() required the user_name define.')
		
	if vlist:
		with open(file_name, "a") as f:
			for entry in vlist.entry:
				vi += 1
				vid = re.sub(r"http:\/\/gdata.youtube.com\/feeds\/api\/videos\/", "", entry.id.text)
				vna = entry.media.title.text
				vpf = re.sub(r"_[A-Z](.+)\.mp4$", "", vna)
				vpx = vpf.split("_")
				line = "%s,%s,%s,%s\n" % (vi, vid, vna, ",".join(a for a in vpx))
				f.write(line)
				print "Video N:", vi, "ID:", vid
			f.close()
		
	else:
		if os.path.exists(file_name):
			shutil.move(file_name, 
						"db/backup_%s.csv" % datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f'))
		
	if vcount < (vtotal+1):
		i = (1 if vcount == 0 else (vcount*25)+1)
		uri = "http://gdata.youtube.com/feeds/api/users/%s/uploads?start-index=%s&amp;max-results=25" % (user_name, i)
		vcount += 1
		PrintVideoList(ytsrv.GetYouTubeVideoFeed(uri=uri), vcount, vtotal, vi, user_name, file_name)
		
	else:
		print
		print 'PrintVideoList (%s): %s videos' % (user_name, vi)
	
if __name__ == '__main__':
	PrintVideoList(user_name="snaxmx")