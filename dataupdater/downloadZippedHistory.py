#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

'''
import os
import sys
import urllib

import localpythonpath
localpythonpath.setlocalpythonpath()

import local_settings as ls

def downloadZippedHistory():
  url = ls.MS_RESULT_DRAWS_ZIPFILE_URL
  print 'Downloading zipped HTML Megasena Results History'
  print '  [url] ', url
  zipfile = os.path.join(ls.DATA_DIR, 'zippedhistory.zip')
  print '  [zipfile] ', zipfile
  # sys.exit(0)  
  filename, headers = urllib.urlretrieve(url, zipfile)
  print 'filename, headers', filename, headers
      
def adhoc_test():
  downloadZippedHistory()

def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
