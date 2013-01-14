#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
TilR.py
'''
# import numpy, time, sys
import sys

import __init__
__init__.setlocalpythonpath()

from libfunctions.utils.pyobjects_ext import Dict2
from TilProducer import TilProducer

  
class TilStats(TilProducer):
  
  def __init__(self, n_slots=None, soma=None):
    super(TilStats, self).__init__(n_slots, soma)
    self.wpatterndict = Dict2()
    self.wpatterns = []
 
  def add_pattern_as_str(self, pattern_str):
    self.wpatterndict.add1_or_set1_to_key(pattern_str)
    self.wpatterns = self.wpatterndict.keys()

  def add_pattern_as_list(self, pattern_list):
    pattern_str = ''.join(map(str, pattern_list))
    self.add_pattern_as_str(pattern_str)

  def get_wpatterns(self):
    return self.wpatterns # to gain performance instead of issuing dict.keys() (below)
    # return self.wpatterndict.keys()
  
  def print_difference(self):
    self.alltilwpatterns
    added_wpatterns = self.wpatterndict.keys() 
    for wpattern in self.alltilwpatterns:
      if wpattern not in added_wpatterns:
        print 'Not occurred', wpattern   

  def print_summary(self):
    wpatterns_and_quants = self.wpatterndict.items()
    wpatterns_and_quants.sort(key = lambda x : x[1])
    for wpattern_and_quant in wpatterns_and_quants:
      wpattern = wpattern_and_quant[0]
      quant    = wpattern_and_quant[1]
      print wpattern, ':', quant, 'times'
    print 'pattern total', len(wpatterns_and_quants)
    self.print_difference()
    self.print_python_list_for_all_patterns_with_less_than_n_occurrences(4)

  def print_python_list_for_all_patterns_with_less_than_n_occurrences(self, n_occurrences):
    outlist = []
    print 'self.alltilwpatterns', self.alltilwpatterns
    for wpattern in self.alltilwpatterns:
      if self.wpatterndict.has_key(wpattern):
        quant = self.wpatterndict[wpattern]
        if quant >= n_occurrences:
          continue
    # ie, either not wpattern is not in self.wpatterndict or its quant < n_occurrences
      outlist.append(wpattern)
    # now write a Python list source code
    print 'outlist', outlist
    outstr = "tilrwpatterns_to_filter_out = ["
    for wpattern in outlist:
      sourcecode ="'%s'," %wpattern 
      outstr += sourcecode
    outstr += "] # len/size = %d" %(len(outlist))
    # return outstr
    print outstr
    
  # (inherited) get_n_all_tilrpatterns(self) or __len__(self):
  # (inherited) def get_alltilpatterns_as_intlists(self):
    
      
def adhoc_test():
  '''
  
  '''
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
      # process()

if __name__ == '__main__':
  look_up_cli_params_for_tests_or_processing()
