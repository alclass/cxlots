#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy, sys # , os, pickle, 

import __init__
__init__.setlocalpythonpath()

# import local_settings as ls

from models.Concursos.concurso_extended import ConcursoExt
from generators.GeradorIter import Gerador
#from models.ReadConcursosHistory import get_contrajogos_as_dezenas_down_from
from fs.jogosfs import jogos_functions
from fs.gen.filters.filters import filter_functions
from maths.metrics.PatternDistanceAnalyzer import PatternDistanceAnalyzer
from fs.util.pyobjects_ext import Dict2

class AnalyzerOfRepeats(object):
  
  def __init__(self, aggregated_histogram):
    self.aggregated_histogram = aggregated_histogram
  
  def analyze(self):
    n_repeats_array = self.aggregated_histogram.keys()
    for self.n_repeats in n_repeats_array:
      self.analyze_coincidence()

  def analyze_repeats(self):
    print 'n_repeats_', self.n_repeats
    array_repeats_history = numpy.array( self.aggregated_histogram[self.n_of_coincides] )
    print array_repeats_history
    print 'min', array_repeats_history.min()
    print 'max', array_repeats_history.max()
    print 'avg', (1.0 + array_repeats_history.sum())/len(array_repeats_history)
    print 'std', array_repeats_history.std()
  

def generator_with_a_bet():
  '''

  The 4 most occurring repeats_array (processed on 2013-01-06)
  
  repeats_array : occurrence (from nDoConc=5 to 1556) 
            2   : 363
            1   : 300
            3   : 218
            21  : 132
  '''
  compare_repeat_lists = [[4], [3,1]]
  gerador = Gerador()
  slider = ConcursoExt() 
  last_concurso = slider.get_last_concurso()
  contrajogos = last_concurso.get_contrajogos_as_dezenas_list_down_to_depth(depth=4, inclusive=True)
  n_passed = 0; counter = 0; n_passed_for_each_compare_repeat_list = {0:0, 1:0} 
  for jogo_as_dezenas in gerador:
    counter += 1
#    if counter > 100:
#      break
    for compare_repeat_list in compare_repeat_lists:
      passed = filter_functions.filter_in_those_within_n_repeats_with_m_previous_games(jogo_as_dezenas, contrajogos, compare_repeat_list)
      if passed:
        n_passed += 1 
        n_passed_for_each_compare_repeat_list[compare_repeat_lists.index(compare_repeat_list)]+=1
        print n_passed, counter, 'Passed repeats_array', compare_repeat_list, str(jogo_as_dezenas) #, contrajogos, compare_repeat_list
        break
  print n_passed, counter, n_passed_for_each_compare_repeat_list 

leftFillToNSpaces  = lambda s, n : ' '*(n-len(s)) + s
rightFillToNSpaces = lambda s, n : s + ' '*(n-len(s))
def   analyze():
  patternDistance = PatternDistanceAnalyzer()
  START_AT_N_CONC = 5 
  slider = ConcursoExt()
  last_concurso = slider.get_last_concurso()
  repeats_dict = Dict2()
  for nDoConc in range(START_AT_N_CONC, last_concurso.n_conc + 1):
    concurso = slider.get_concurso_by_nDoConc(nDoConc)
    contrajogos_as_dezenas_list = last_concurso.get_contrajogos_as_dezenas_list_down_to_depth(depth=4, inclusive=True)
    if contrajogos_as_dezenas_list == None:
      continue
    #print concurso.nDoConc, concurso.date, concurso.get_dezenas(), contrajogos_as_dezenas_list 
    repeats_array = jogos_functions.get_array_n_repeats_with_m_previous_games(concurso.get_dezenas(), contrajogos_as_dezenas_list)
    token = ''.join(map(str, repeats_array))
    patternDistance.add_pattern(token)
    repeats_dict.add1_or_set1_to_key(token)
  tokens_and_quants = repeats_dict.items()
  tokens_and_quants.sort(key = lambda x : x[1])
  tokens_and_quants.reverse()
  for token_and_quant in tokens_and_quants:
    token = token_and_quant[0]
    quant = token_and_quant[1]
    pattern = rightFillToNSpaces(token, 3)
    zquant  = leftFillToNSpaces(str(quant), 3)
    print pattern, ':', zquant 
  patternDistance.mount_distances_histogram()
  patternDistance.summarize()
  analyze()

def process():
  pass
  #analyze()
  # generator_with_a_bet()

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
