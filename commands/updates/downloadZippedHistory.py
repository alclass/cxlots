#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

'''
import os
import sys
# import urllib
import requests
import local_settings as ls


def download_zipped_history():
  url = ls.MS_RESULT_DRAWS_ZIPFILE_URL
  print('Downloading zipped HTML Megasena Results History')
  print('  [url] ', url)
  zipfile = os.path.join(ls.DATA_DIR, 'zippedhistory.zip')
  print('  [zipfile] ', zipfile)
  # sys.exit(0)  
  filename, headers = urllib.urlretrieve(url, zipfile)
  print('filename, headers', filename, headers)


def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()


def process():
  look_for_adhoctest_arg()
  download_zipped_history()


def adhoc_test():
  pass


if __name__ == '__main__':
  """
  """
  process()
