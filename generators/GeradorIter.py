#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy, sys

import localpythonpath
localpythonpath.setlocalpythonpath()
 
from maths.combinatorics.IndicesCombiner import IndicesCombiner
from maths.combinatorics.algorithmsForCombinatorics import combineNbyC 
from lib.funcsForStringPatternsEtAl import convert_intlist_to_spaced_zfillstr

addOneToEachElement = lambda x : x + 1
ONE_MILLION = 10**6

class GeradorIterator(object):

  def __init__(self, N_DEZENAS_NO_VOLANTE=60, N_DEZENAS_NO_SORTEIO=6):
    self.N_DEZENAS_NO_VOLANTE = N_DEZENAS_NO_VOLANTE
    self.N_DEZENAS_NO_SORTEIO = N_DEZENAS_NO_SORTEIO 
    self.lgiCombiner = IndicesCombiner(self.N_DEZENAS_NO_VOLANTE-1, self.N_DEZENAS_NO_SORTEIO, False)
    self.session_index = 0
    self.set_first_element()

  def set_first_element(self):
    intlist = self.lgiCombiner.first()
    self.current_dezenas_list = map(addOneToEachElement, intlist)
    self.first_time = True

  def move_to_element_by_its_indices(self, indices_position_to_move_at):
    self.lgiCombiner.move_to_position_by_iArray(indices_position_to_move_at)
    intlist = self.lgiCombiner.current()
    print 'intlist', intlist 
    self.current_dezenas_list = map(addOneToEachElement, intlist)
    print 'current_dezenas_list', self.current_dezenas_list 

  def __iter__(self):
    return self.get_current()

  def next(self):
    if self.current_dezenas_list == None:
      raise StopIteration, 'End of Iteration'
      # return None
    if self.first_time:
      self.first_time = False
      if self.current_dezenas_list != None:
        return copy.copy(self.current_dezenas_list) # self.current_dezenas_list[:]
      else:
        raise StopIteration, 'End of Iteration'
        # return None
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
    intlist = self.lgiCombiner.next()
    if intlist != None: 
      self.session_index += 1
      self.current_dezenas_list = map(addOneToEachElement, intlist)
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
  indices_position_to_move_at = [53,54,55,56,57,58]
  gerador.iterator.move_to_element_by_its_indices(indices_position_to_move_at)
  for jogo_as_dezenas in gerador:
    i = gerador.iterator.session_index
#    if i < 50000000:
#      continue
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
