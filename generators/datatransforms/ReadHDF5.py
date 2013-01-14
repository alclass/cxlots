#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys # , os, pickle, 
import numpy
import tables

import __init__
__init__.setlocalpythonpath()

import local_settings as ls

filename='Filtragem-TilR-excluding-97-patterns_2013-01-11.h5'
filepath = ls.GENERATED_DATA_DIR + filename
h5file = tables.openFile(filepath, mode='r')

#h5file.

def process():
  pass
  # read_textfile()

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
      process()

if __name__ == '__main__':
  look_up_cli_params_for_tests_or_processing()
