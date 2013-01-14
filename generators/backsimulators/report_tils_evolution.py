#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy, sys # , os, pickle, 

import __init__
__init__.setlocalpythonpath()

# import local_settings as ls

from models.Concursos.ConcursoExt import ConcursoExt
# from generators.GeradorIter import Gerador
from models.Files.ReadConcursosHistory import ConcursosHistoryPickledStorage
import models.Files.ReadConcursosHistory as RCH
import libfunctions.jogos.jogos_functions_dependent as jogos_fd
# from libfunctions.filters.filter_functions_dependent import filter_in_those_within_coincides_histogram_range

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
  n_last_concurso = slider.get_n_last_concurso()
  for nDoConc in range(1001, n_last_concurso+1):
    reader = ConcursosHistoryPickledStorage(read_as_id=RCH.READ_CONCHIST_AS_TIMEONWARDS_ORDERED_INTS)
    reader.set_upper_nDoConc(upper_nDoConc=nDoConc)
    jogos_as_dezenas = reader.get_concursos_up_to_upper_nDoConc()
    
     
  slider = ConcursoExt()
  concurso = slider.get_last_concurso()
  aggregated_histogram = {}
  N_SORTEADAS = len(concurso.get_dezenas())
  N_SORTEADAS_MAIS_NENHUMA_COINCIDENCIA = N_SORTEADAS + 1
  for i in range(N_SORTEADAS_MAIS_NENHUMA_COINCIDENCIA): 
    aggregated_histogram[i] = []
  for i in range(10):
    print i, concurso.nDoConc, concurso.get_dezenas()
    coincides_histogram = jogos_fd.get_coincides_histogram_against_a_lookup_depth(concurso.get_dezenas(), up_to_nDoConc=concurso.nDoConc-1, LOOKUP_DEPTH=1000) 
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
