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
    self.at_index = 0
    self.set_first_element()
    self.first_time = True

  def set_first_element(self):
    intlist = self.lgiCombiner.first()
    self.current_dezenas_list = map(addOneToEachElement, intlist)

  def __iter__(self):
    return self.get_current()

  def next(self):
    if self.current_dezenas_list == None:
      raise StopIteration, 'End of Iteration'
    if self.first_time:
      self.first_time = False
      if self.current_dezenas_list != None:
        return copy.copy(self.current_dezenas_list) # self.current_dezenas_list[:]
      else:
        return None
    self.produce_next()
    if self.current_dezenas_list != None:
        return copy.copy(self.current_dezenas_list) # self.current_dezenas_list[:]
    else:
      return None

  def produce_next(self):
    intlist = self.lgiCombiner.next()
    if intlist != None: 
      self.at_index += 1
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
  for jogo_as_dezenas in gerador:
    i = gerador.iterator.at_index
    if i > 10:
      break
    print gerador.iterator.at_index, convert_intlist_to_spaced_zfillstr(jogo_as_dezenas)
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
