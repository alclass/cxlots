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


import unittest
class MyTest(unittest.TestCase):

  def test_1(self):
    pass

def look_up_cli_params_for_tests_or_processing():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()
    elif arg.startswith('-u'):
      # unittest complains if argument is available, so remove it from sys.argv
      del sys.argv[1]
      unittest.main()
    elif arg.startswith('-p'):
      pass
      process()

if __name__ == '__main__':
  look_up_cli_params_for_tests_or_processing()
