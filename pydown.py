#!/bin/python3
import pycurl
import sys

"""
	Minimal pycurl downloader
"""

if len(sys.argv) == 3:
	URL = sys.argv[1]
	OFILE = sys.argv[2]
else:
	print("Usage: pydown.py url filename")
	sys.exit(1)

crl = pycurl.Curl()
crl.setopt(crl.URL, URL)

with open(OFILE, 'wb') as f:
    crl.setopt(crl.WRITEDATA, f)
    crl.perform()

crl.close()
