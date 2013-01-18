#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy, pickle, sys # , os, pickle, 

import __init__
__init__.setlocalpythonpath()

import local_settings as ls

from generators.GeradorIter import Gerador
from libfunctions.filters.filter_functions_dependent import  filter_in_those_within_coincides_histogram_range

n_pass=0
def get_coincides_range_dict():
  global n_pass
  coincides_ranges    = {}
  if n_pass % 2 == 0:
    coincides_ranges[0] = (501, 518)
    coincides_ranges[1] = (366, 385)
    coincides_ranges[2] = ( 97, 102)
    coincides_ranges[3] = (  5,  10)
    coincides_ranges[4] = (  0,   2)
    coincides_ranges[5] = (  0,   0)
    coincides_ranges[6] = (  0,   0)
  else:
    coincides_ranges[0] = (485, 538)
    coincides_ranges[1] = (356, 395)
    coincides_ranges[2] = ( 87, 112)
    coincides_ranges[3] = (  4,  14)
    coincides_ranges[4] = (  0,   2)
    coincides_ranges[5] = (  0,   0)
    coincides_ranges[6] = (  0,   0)
  n_pass+=1
  return coincides_ranges

def process():
  
  gerador = Gerador()
  print 'Going to process', len(gerador), 'games'
  filename = ls.GENERATED_DATA_DIR + 'coincides_hist_range-%d.blob' %(n_pass)
  fileobj = open(filename, 'wb')
  pickler = pickle.Pickler(fileobj, pickle.HIGHEST_PROTOCOL)
  coincides_ranges = get_coincides_range_dict()
  print 'coincides_ranges', coincides_ranges 
  for jogo_as_dezenas in gerador:
#    i = gerador.iterator.at_index
#    if i > 10:
#      break
    jogo_passed_filter = filter_in_those_within_coincides_histogram_range(jogo_as_dezenas, coincides_ranges, up_to_nDoConc=None, LOOKUP_DEPTH=1000)
    if jogo_passed_filter:
      pickler.dump(numpy.array(jogo_as_dezenas))
    print gerador.iterator.at_index, jogo_as_dezenas, jogo_passed_filter

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
