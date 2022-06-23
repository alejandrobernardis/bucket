import datetime, os, sys
#: -----------------------------------------------------------------------------
def print_data(value, encode="utf-8"):
	print 'Content-type: text/plain; charset=%s;' % encode
	print
	print value
#: -----------------------------------------------------------------------------
print_data(os.environ)
#: -----------------------------------------------------------------------------
