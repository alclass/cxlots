#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy, sys # , os, pickle, 

import __init__
__init__.setlocalpythonpath()

# import local_settings as ls

from models.Concursos.concurso_extended import ConcursoExt
from generators.GeradorIter import Gerador
import fs.jogosfs.jogos_functions_dependent as jogos_fd
from fs.gen.filters.filters import filter_in_those_within_coincides_histogram_range

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
  

def report():
  slider = ConcursoExt()
  concurso = slider.get_last_concurso()
  aggregated_histogram = {}
  N_SORTEADAS = len(concurso.get_dezenas())
  N_SORTEADAS_MAIS_NENHUMA_COINCIDENCIA = N_SORTEADAS + 1
  for i in range(N_SORTEADAS_MAIS_NENHUMA_COINCIDENCIA): 
    aggregated_histogram[i] = []
  for i in range(10):
    print i, concurso.n_conc, concurso.get_dezenas()
    coincides_histogram = jogos_fd.get_coincides_histogram_against_a_lookup_depth(concurso.get_dezenas(), up_to_nDoConc=concurso.n_conc - 1, LOOKUP_DEPTH=1000)
    if coincides_histogram == None:
      continue 
    print coincides_histogram
    the_n_coincides = coincides_histogram.values()
    print the_n_coincides, sum(the_n_coincides)
    for i, coincide_quantity in enumerate(the_n_coincides):
      aggregated_histogram[i].append(coincide_quantity)
    concurso = concurso.get_previous()
  analyzer = AnalyzerOfCoincides(aggregated_histogram)
  analyzer.analyze()


def process():
  '''
  '''
  pass

def adhoc_test():
  
  # slider = ConcursoHTML()
  # last_nDoConc = find_last_nDoConc()
  # backtrack_amount = 400
  # down_to_nDoConc = last_nDoConc - backtrack_amount
  # for nDoConc in range(last_nDoConc, down_to_nDoConc - 1, -1):
#  concurso = slider.get_last_concurso()
#  analyzer = Analyzer(concurso)
#  analyzer.run()
#  analyzer.report()
  # report()
  '''
  n_of_coincides 0
[507 510 535 533 530 538 518 512 506 485]
min 485
max 538
avg 517.5
std 15.8379291576
n_of_coincides 1
[376 375 356 364 373 368 382 385 376 395]
min 356
max 395
avg 375.1
std 10.4211323761
n_of_coincides 2
[112 107  99  96  92  87  94  95 104 108]
min 87
max 112
avg 99.5
std 7.6183987819
n_of_coincides 3
[ 4  8  8  7  5  6  6  7 14 12]
min 4
max 14
avg 7.8
std 2.93428015022
n_of_coincides 4
[1 0 2 0 0 1 0 1 0 0]
min 0
max 2

  '''

  coincides_ranges    = {}
  #coincides_ranges[0] = (485, 538)
  coincides_ranges[0] = (501, 518)
  # coincides_ranges[1] = (356, 395)
  coincides_ranges[1] = (366, 385)
  #coincides_ranges[2] = ( 87, 112)
  coincides_ranges[2] = ( 97, 102)
  #coincides_ranges[3] = (  4,  14)
  coincides_ranges[3] = (  5,  10)
  coincides_ranges[4] = (  0,   2)
  coincides_ranges[5] = (  0,   0)
  coincides_ranges[6] = (  0,   0)
  #slider = ConcursoExt()
  gerador = Gerador()
  # gerador = GeradorIterator()
  print len(gerador)
  for jogo_as_dezenas in gerador:
    i = gerador.iterator.at_index
    if i > 10:
      break
    print gerador.iterator.at_index, jogo_as_dezenas 
    bool_result = filter_in_those_within_coincides_histogram_range(jogo_as_dezenas, coincides_ranges, up_to_nDoConc=None, LOOKUP_DEPTH=1000)
    #if bool_result:
    print jogo_as_dezenas, bool_result


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
