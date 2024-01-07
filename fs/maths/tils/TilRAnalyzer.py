#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
TilRAnalyzer.py
'''
# import numpy, time, sys
import sys

import localpythonpath
localpythonpath.setlocalpythonpath()

from models.Concurso import ConcursoBase
# import maths2.frequencies.HistoryFrequency as hf
from TilR import TilR, Dict2
from TilPattern import TilDefiner
from TilPatternsProducerByNumberBase import TilProducerByNumberBase 

class TilRAnalyzer(object):
  
  def __init__(self):
    self.wpattern_histogram = Dict2()
    self.concurso = ConcursoBase()
    self.n_slots = 5
    tildefiner = TilDefiner(self.n_slots, self.concurso.N_DE_DEZENAS)
    self.tilprodbyNBase = TilProducerByNumberBase(tildefiner)
    self.run_history()
    self.summarize()
  
  def run_history(self):
    for nDoConc in xrange(1301, self.concurso.get_total_concursos()+1):
      concurso = self.concurso.get_concurso_by_nDoConc(nDoConc)
      tilrobj = TilR(self.n_slots, concurso)
      wpatt = tilrobj.get_wpattern()
      wpatt_index = self.tilprodbyNBase.index(wpatt)
      print concurso, wpatt
      self.wpattern_histogram.add1_or_set1_to_key((wpatt_index, wpatt))

  def summarize(self):
    to_unpack = self.wpattern_histogram.items()
    index_and_pattern_tuple_list, n_occurrences = zip(*to_unpack )
    index_list, pattern_list = zip(*index_and_pattern_tuple_list)
    triple_list = zip(index_list, pattern_list, n_occurrences)  
    triple_list.sort( key = lambda x : x[2])
    triple_list.reverse()
    n_last_index = self.tilprodbyNBase.get_total() - 1
    for triple in triple_list:
      wpattern = triple[1]
      self.tilprodbyNBase.move_to_wpattern(wpattern)
      n_combinations = self.tilprodbyNBase.get_n_combinations(self.concurso) 
      print triple, n_combinations 
    print len(self.wpattern_histogram)
    print 'not happened'; c=0
    for index in xrange(n_last_index + 1):
      if index not in index_list:
        c+=1
        print '>>>%d' %c, index, self.tilprodbyNBase.at(index), '::',

    # list out those wpatterns that have not occurred
    
def adhoc_test():
  TilRAnalyzer()

def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
