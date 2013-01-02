#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys # numpy, os, pickle, 

import localpythonpath
localpythonpath.setlocalpythonpath()

# import local_settings as ls

from lib.jogos_functions import get_coincides_histogram
from models.ConcursoHTML import ConcursoHTML
from models.ReadConcursosHistory import ConcursosHistoryPickledStorage

def report():
  slider = ConcursoHTML()
  concurso = slider.get_last_concurso()
  for i in range(400):
    print i, concurso.nDoConc, concurso.get_dezenas()
    pickled = ConcursosHistoryPickledStorage(upper_nDoConc=concurso.nDoConc-1) # read_as_id=None,
    previous_games_as_dezenas = pickled.read_or_create()
    coincides_histogram = get_coincides_histogram(concurso.get_dezenas(), previous_games_as_dezenas)
    print coincides_histogram.values(), sum(coincides_histogram.values())
    concurso = concurso.get_previous()
  

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
  report()

def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
