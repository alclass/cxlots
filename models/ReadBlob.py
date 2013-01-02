#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy, os, pickle, sys

import localpythonpath
localpythonpath.setlocalpythonpath()

import local_settings as ls

def process():  
  '''
  '''
  blob_name     = raw_input("Type blob's name ? ")
  blob_filename = blob_name + '.blob'
  blob_path     = ls.GENERATED_DATA_DIR + blob_filename
  unpickle_obj  = pickle.Unpickler(open(blob_path, 'rb'))
  eof_of_unpickle = False; counter = 0
  while not eof_of_unpickle:
    try:
      obj = unpickle_obj.load()
      counter += 1
      print counter, obj
    except EOFError:
      eof_of_unpickle = True    


def adhoc_test():
  pass

def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  # look_for_adhoctest_arg()
  process()
