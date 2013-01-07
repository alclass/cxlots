#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy, sys # , os, pickle, 

import localpythonpath
localpythonpath.setlocalpythonpath()

# import local_settings as ls

from models.ConcursoExt import ConcursoExt
from generators.GeradorIter import Gerador
#from models.ReadConcursosHistory import get_contrajogos_as_dezenas_down_from
from lib import jogos_functions
from lib import filter_functions
#import lib.jogos_functions_dependent as jogos_fd
#from lib.filter_functions_dependent import filter_in_those_within_coincides_histogram_range

class AnalyzerOfCoincides(object):
  
  def __init__(self, aggregated_histogram):
    self.aggregated_histogram = aggregated_histogram
  
  def analyze(self):
    n_coincides_list = self.aggregated_histogram.keys()
    for self.n_of_coincides in n_coincides_list:
      self.analyze_coincidence()

  def analyze_coincidence(self):
    print 'n_of_coincides', self.n_of_coincides
    array_coincides_history = numpy.array( self.aggregated_histogram[self.n_of_coincides] )
    print array_coincides_history
    print 'min', array_coincides_history.min()
    print 'max', array_coincides_history.max()
    print 'avg', (1.0 + array_coincides_history.sum())/len(array_coincides_history)
    print 'std', array_coincides_history.std()
  

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
        # print n_passed, counter, 'Passed repeats_array', compare_repeat_list, str(jogo_as_dezenas) #, contrajogos, compare_repeat_list
        break
  print n_passed, counter, n_passed_for_each_compare_repeat_list 

leftFillToNSpaces  = lambda s, n : ' '*(n-len(s)) + s
rightFillToNSpaces = lambda s, n : s + ' '*(n-len(s))
def   analyze():
  START_AT_N_CONC = 5 
  slider = ConcursoExt()
  last_concurso = slider.get_last_concurso()
  repeats_dict = {}
  for nDoConc in range(START_AT_N_CONC, last_concurso.nDoConc+1):
    concurso = slider.get_concurso_by_nDoConc(nDoConc)
    contrajogos_as_dezenas_list = last_concurso.get_contrajogos_as_dezenas_list_down_to_depth(depth=4, inclusive=True)
    if contrajogos_as_dezenas_list == None:
      continue
    #print concurso.nDoConc, concurso.date, concurso.get_dezenas(), contrajogos_as_dezenas_list 
    repeats_array = jogos_functions.get_array_n_repeats_with_m_previous_games(concurso.get_dezenas(), contrajogos_as_dezenas_list)
    token = ''.join(map(str, repeats_array))
    if repeats_dict.has_key(token):
      repeats_dict[token]+=1
    else:
      repeats_dict[token]=1
  tokens_and_quants = repeats_dict.items()
  tokens_and_quants.sort(key = lambda x : x[1])
  tokens_and_quants.reverse()
  for token_and_quant in tokens_and_quants:
    token = token_and_quant[0]
    quant = token_and_quant[1]
    pattern = rightFillToNSpaces(token, 3)
    zquant  = leftFillToNSpaces(str(quant), 3)
    print pattern, ':', zquant 


def process():
  # analyze()
  generator_with_a_bet()

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
