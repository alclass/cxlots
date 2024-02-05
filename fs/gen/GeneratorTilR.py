#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
GeneratorTilR.py
'''
import sys

import localpythonpath
localpythonpath.setlocalpythonpath()

#from models.Concurso import ConcursoBase
#from maths2.tils.TilPatternsProducerByNumberBase import TilProducerByNumberBase
from maths.tils.TilPatternsProducerByNumberBase import TilDefiner
from maths.tils.TilR import TilR
from maths.combinatorics.SetsCombiner import SetsCombiner, SetsCombinerMemoryIntensive

def get_tildefiner_by_wpattern(wpattern):
  array = [int(c) for c in wpattern]
  soma = sum(array)
  n_slots = len(array)
  tildefiner = TilDefiner(n_slots, soma)
  return tildefiner
  
class GeneratorTilR(object):
  
  def __init__(self, wpattern_list, tilr, filename=None):
    self.wpattern_list = wpattern_list
    self.tilr = tilr
    #tildefiner = get_tildefiner_by_wpattern(self.wpattern_list[0])
    #self.tilproducernb = TilProducerByNumberBase(tildefiner)
    # tablename = ''
    
  def generate(self):
    gencounter = 0; expected = 1634688
    for wpattern in self.wpattern_list:
      array = [int(c) for c in wpattern]
      workSetList = zip(self.tilr.tilrsets, array)
      # print 'workSetList', workSetList 
      sc = SetsCombiner()
      for workSet in workSetList:
        n_elems_in_the_slots = workSet[1]
        if n_elems_in_the_slots == 0:
          continue
        sc.add_set_with_quantities(workSet)
      for self.combined in sc.next_combination():
        gencounter+=1
        self.save(self.combined)
        # print gencounter, self.combined
    print 'gencounter', gencounter, 'expected', expected 
      #self.tilproducernb.move_to_wpattern(wpattern)

  def save(self):
    pass


  def generateMemoryHungry(self):
    gencounter = 0; expected = 1634688
    for wpattern in self.wpattern_list:
      array = [int(c) for c in wpattern]
      workSetList = zip(self.tilr.tilrsets, array)
      #print 'workSetList', workSetList 
      sc = SetsCombinerMemoryIntensive()
      for workSet in workSetList:
        n_elems_in_the_slots = workSet[1]
        if n_elems_in_the_slots == 0:
          continue
        sc.add_set_with_quantities(workSet)
      allCombinations = sc.get_all_combinations()
      for self.combined in allCombinations:
        gencounter+=1
        self.save(self.combined)
        #print gencounter, combined
    print 'gencounter', gencounter, 'expected', expected 

      
    
def adhoc_test2():
  sc = SetsCombiner()
  sc.add_set_with_quantities(([1, 2, 3], 2))
  sc.add_set_with_quantities(([4, 5, 6], 2))
  sc.combineSets()
  print sc.getAllCombinationsAfterCombine()
                          
def write_genmass_file():
  wpattern_list = ['02211', '01221', '13110'] 
  tilr = TilR(n_slots=5, concurso = None, inclusive=True)
  gtr = GeneratorTilR(wpattern_list, tilr)
  gtr.generate()
  # gtr.generateMemoryHungry()
  
def adhoc_test():
  write_genmass_file()


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
