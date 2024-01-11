#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys # , os, pickle, numpy 

import __init__
__init__.setlocalpythonpath()

from models.Files.ReadConcursosHistory import ConcursosHistoryPickledStorage
import models.Files.ReadConcursosHistory as RCH
from fs.util.pyobjects_ext import Dict2
from maths.tils import TilR
from maths.metrics.PatternDistanceAnalyzer import PatternDistanceAnalyzer

start_nDoConc = 101
def report():
  wpatterndict = Dict2(); desc_stair_dict = Dict2()
  reader = ConcursosHistoryPickledStorage(read_as_id=RCH.READ_CONCHIST_AS_TIMEONWARDS_ORDERED_INTS)
  jogos_as_dezenas = reader.get_games_up_to()
  start_index = start_nDoConc - 1
  patternDistance = PatternDistanceAnalyzer()
  for i, jogo_as_dezenas in enumerate(jogos_as_dezenas[start_index:]):
    passing_nDoConc = start_nDoConc + i
    the_one_just_before = passing_nDoConc - 1
    tilr     = TilR.get_tilr_from_pool(n_slots=5, history_nDoConc_range = (1, the_one_just_before)) 
    wpattern = tilr.get_game_tilrpattern_as_str(jogo_as_dezenas)
    #print wpattern, 'concurso', passing_nDoConc, jogo_as_dezenas
    desc_stair_str = tilr.get_game_tilrpattern_as_desc_stair(jogo_as_dezenas) 
    print str(passing_nDoConc).zfill(4), wpattern, desc_stair_str
    wpatterndict.add1_or_set1_to_key(wpattern)
    patternDistance.add_pattern(wpattern)
    desc_stair_dict.add1_or_set1_to_key(desc_stair_str)
  for wpattern in wpatterndict.keys():
    print wpattern, ':', wpatterndict[wpattern]
  for wpattern in desc_stair_dict.keys():
    print wpattern, ':', desc_stair_dict[wpattern]
  patternDistance.mount_distances_histogram()
  patternDistance.summarize()
     
def process():
  '''
  '''
  report()
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
