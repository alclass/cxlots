#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy, sys

#import localpythonpath
#localpythonpath.setlocalpythonpath()

import __init__
__init__.setlocalpythonpath()

 
from maths.combinatorics.IndicesCombiner import IndicesCombiner
from maths.combinatorics.algorithmsForCombinatorics import combineNbyC 
from libfunctions.pattern_string_et_al.stringpatterns_functions import convert_intlist_to_spaced_zfillstr

addOneToEachElement = lambda x : x + 1
ONE_MILLION = 10**6

class GeradorIterator(object):

  def __init__(self, N_DEZENAS_NO_VOLANTE=60, N_DEZENAS_NO_SORTEIO=6):
    self.N_DEZENAS_NO_VOLANTE = N_DEZENAS_NO_VOLANTE
    self.N_DEZENAS_NO_SORTEIO = N_DEZENAS_NO_SORTEIO 
    self.lgiCombiner = IndicesCombiner(self.N_DEZENAS_NO_VOLANTE-1, self.N_DEZENAS_NO_SORTEIO, False)
    self.session_index = 0
    self.current_dezenas_list = self.lgiCombiner.current()

  def restart(self):
    self.lgiCombiner.parkBeforeFirst()
    indices = self.lgiCombiner.current()
    self.current_dezenas_list = map(addOneToEachElement, indices) 

  def move_to_element_by_its_indices(self, indices_position_to_move_at):
    self.lgiCombiner.move_to_position_by_iArray(indices_position_to_move_at)
    indices = self.lgiCombiner.current()
    self.current_dezenas_list = map(addOneToEachElement, indices) 
    # print 'current_dezenas_list', self.current_dezenas_list 

  def move_to_last(self):
    indices = self.lgiCombiner.moveToLastOne()
    self.current_dezenas_list = map(addOneToEachElement, indices) 

  def move_to_one_before_last(self):
    self.lgiCombiner.move_to_one_before_last()
    indices = self.lgiCombiner.current()
    self.current_dezenas_list = map(addOneToEachElement, indices) 

  def __iter__(self):
    return self.get_current()

  def next(self):
    self.produce_next()
    if self.current_dezenas_list != None:
        return copy.copy(self.current_dezenas_list) # self.current_dezenas_list[:]
    else:
      raise StopIteration, 'End of Iteration'
      # return None

  def get_index(self):
    # to implement using the lgi's technique
    pass
    
  def produce_next(self):
    indices = self.lgiCombiner.next()
    if indices != None: 
      self.session_index += 1
      self.current_dezenas_list = map(addOneToEachElement, indices)
    else:
      self.current_dezenas_list = None

  def get_current(self):
    if self.current_dezenas_list != None:
      return self.current_dezenas_list[:]
    return None

  def __str__(self):
    outlist = self.get_current()
    if outlist != None:
      return convert_intlist_to_spaced_zfillstr(outlist)
    return '<None>'

  # here ENDS GeradorIterator(object):
   
class Gerador(object):

  def __init__(self, N_DEZENAS_NO_VOLANTE=60, N_DEZENAS_NO_SORTEIO=6):
    self.iterator = GeradorIterator(N_DEZENAS_NO_VOLANTE, N_DEZENAS_NO_SORTEIO)
    self.N_DEZENAS_NO_VOLANTE = N_DEZENAS_NO_VOLANTE
    self.N_DEZENAS_NO_SORTEIO = N_DEZENAS_NO_SORTEIO 

  def __iter__(self):
    return self.iterator
  
  def __len__(self):
    return combineNbyC(self.N_DEZENAS_NO_VOLANTE, self.N_DEZENAS_NO_SORTEIO)
  
  # here ENDS class Gerador(object):

def testGerador():
  gerador = Gerador()
  # gerador = GeradorIterator()
  print len(gerador)
  #indices_position_to_move_at = [53,54,56,57,58,59]
  #indices_position_to_move_at = [54,55,56,57,58,59]
  #gerador.iterator.move_to_element_by_its_indices(indices_position_to_move_at)
  print 'gerador.iterator.move_to_one_before_last()'
  gerador.iterator.move_to_one_before_last()
  print '_one_before_last', gerador.iterator.get_current()
#  gerador.iterator.next()
#  print 'next/last', gerador.iterator.get_current()
  gerador.iterator.move_to_last()
  print 'move_to_last', gerador.iterator.get_current()
  #gerador.iterator.next() # exception will be raised
  # print 'next after last', gerador.iterator.get_current()

  gerador.iterator.restart()
  print 'restart', gerador.iterator.get_current()
  gerador.iterator.next()
  print 'next after restart', gerador.iterator.get_current()
  for jogo_as_dezenas in gerador:
    i = gerador.iterator.session_index
    if i > 10:
      break
    print i, convert_intlist_to_spaced_zfillstr(jogo_as_dezenas)
    # print gerador.iterator.index(100)
    

def adhoc_test():
  testGerador()


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
