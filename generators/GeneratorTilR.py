#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
GeneratorTilR.py
'''
import sys

import localpythonpath
localpythonpath.setlocalpythonpath()

#from models.Concurso import ConcursoBase
#from maths.tils.TilPatternsProducerByNumberBase import TilProducerByNumberBase
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
        sc.addSetWithQuantities(workSet)
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
        sc.addSetWithQuantities(workSet)
      allCombinations = sc.getAllCombinations()
      for self.combined in allCombinations:
        gencounter+=1
        self.save(self.combined)
        #print gencounter, combined
    print 'gencounter', gencounter, 'expected', expected 

      
      
def adhoc_test2():
  sc = SetsCombiner()
  sc.addSetWithQuantities(([1,2,3],2))
  sc.addSetWithQuantities(([4,5,6],2))
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

def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()