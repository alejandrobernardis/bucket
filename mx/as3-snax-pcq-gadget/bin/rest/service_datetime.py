#!/usr/bin/python
# -*- coding: utf-8 -*-
#: -----------------------------------------------------------------------------
import datetime, os, sys
#: -----------------------------------------------------------------------------
def print_data(value, encode="utf-8"):
	print 'Content-type: text/plain; charset=%s;' % encode
	print
	print value
#: -----------------------------------------------------------------------------
error = -1
try:
	_port = os.environ["SERVER_PORT"]
	if int(_port) != 443:
		raise
	_method = os.environ["REQUEST_METHOD"]
	if _method.lower() in ["post"]:
		week_one = dict(
			d15="I058028030075092070049091087092133001028024019079080031033077082018064084109002018005092068",
			d18="I051063044042019083065031011122112126081004001001127025068007",
			d19="I039053004028065030106089073030005107104097010093078",
			d20="I038012052089012083106014127113103001109010086018",
			d21="I096090028017029088005054126106005075007126015084126096114017113",
			d25="I036060070001081083057075028094029099027091014069106020070001065013",
			d26="I058028030075092070049091087092133001028024019079080031033077082018064084109002018005092068",
			d27="I032064088024054044086096039001032024005002079116123017112124086126085",
			d28="I007016053077095029078100002065018006066093102010003"
		)
		try:
			_date = datetime.datetime.now()
			word = week_one["d%s" % _date.day]
		except:
			raise
		print_data(word)
	else:
		raise
except:
	print_data(error)
#: -----------------------------------------------------------------------------
