#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys # numpy, os, pickle, 

import localpythonpath
localpythonpath.setlocalpythonpath()

# import local_settings as ls

from lib import jogos_functions
#from models.ReadConcursosHistory import find_last_nDoConc
from models.ReadConcursosHistory import ConcursosHistoryMetrics  # ConcursosHistoryPickledStorage
from models.ConcursoHTML         import ConcursoHTML


class Analyzer(object):
  
  def __init__(self, concurso):
    self.concurso = concurso
    self.nDoConc  = self.concurso.nDoConc
    self.jogo     = concurso.get_dezenas()
    self.jogo_in_orig_order = concurso.get_dezenas_in_orig_order()
    
  def run(self):

    print 'Running games_before_concurso' 
    games_before_concurso    = ConcursosHistoryMetrics(read_as_id=None, upper_nDoConc=self.nDoConc-1)

    print 'Running impares_histogram'     
    self.impares_histogram   = games_before_concurso.find_impares_histogram_for_games()

    print 'Running sum_histogram'         
    self.sum_histogram       = games_before_concurso.find_sum_histogram_for_games()

    print 'Running line_pattern_dict'     
    self.line_pattern_dict   = games_before_concurso.find_line_pattern_histogram_games()

    print 'Running column_pattern_dict'   
    self.column_pattern_dict = games_before_concurso.find_column_pattern_histogram_games()
    
  def report(self):

    print 'Reporting impares_histogram'     
    print self.impares_histogram
    print 'Concurso After', self.concurso.nDoConc, self.concurso.get_dezenas()
    n_impares = jogos_functions.get_n_impares(self.concurso.get_dezenas())
    print 'n_impares', n_impares

    print 'Reporting sum_histogram'         
    print self.sum_histogram         
    print 'Concurso After', self.concurso.nDoConc, self.concurso.get_dezenas()
    print 'Soma', sum(self.concurso.get_dezenas())
    
    print 'Reporting line_pattern_dict'     
    print self.line_pattern_dict     
    print 'Concurso After', self.concurso.nDoConc, self.concurso.get_dezenas()
    line_pattern = jogos_functions.get_line_pattern(self.concurso.get_dezenas())
    print 'line_pattern', line_pattern

    print 'column_pattern_dict'   
    print self.column_pattern_dict   
    print 'Concurso After', self.concurso.nDoConc, self.concurso.get_dezenas()
    column_pattern = jogos_functions.get_column_pattern(self.concurso.get_dezenas())
    print 'column_pattern', column_pattern

def adhoc_test():
  
  slider = ConcursoHTML()
  # last_nDoConc = find_last_nDoConc()
  # backtrack_amount = 400
  # down_to_nDoConc = last_nDoConc - backtrack_amount
  # for nDoConc in range(last_nDoConc, down_to_nDoConc - 1, -1):
  concurso = slider.get_last_concurso()
  analyzer = Analyzer(concurso)
  analyzer.run()
  analyzer.report()
  

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
