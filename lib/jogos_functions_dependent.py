#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
'''
jogos_functions_dependent.py contains some function that were
  separated from jogos_function due either to dependency on local system modules
  or cross-dependency issues
'''

from models.ReadConcursosHistory import ConcursosHistoryPickledStorage
from models.ConcursoHTML import ConcursoHTML
from lib import jogos_functions
def get_coincides_histogram_against_a_lookup_depth(jogo, up_to_nDoConc=None, LOOKUP_DEPTH=1000):
  slider = ConcursoHTML()
  concurso     = slider.get_last_concurso()
  last_nDoConc = concurso.nDoConc
  if up_to_nDoConc == None:
    # Default
    up_to_nDoConc = last_nDoConc
  elif up_to_nDoConc < 0 or up_to_nDoConc <= last_nDoConc:
    # Default
    up_to_nDoConc = last_nDoConc
  # slider.get_concurso_by_nDoConc(up_to_nDoConc)
  pickled = ConcursosHistoryPickledStorage(upper_nDoConc=up_to_nDoConc) # read_as_id=None,
  previous_games_as_dezenas = pickled.read_or_create()
  if len(previous_games_as_dezenas) < LOOKUP_DEPTH:
    return None
  previous_games_as_dezenas = previous_games_as_dezenas[:LOOKUP_DEPTH]
  coincides_histogram = jogos_functions.get_coincides_histogram(jogo, previous_games_as_dezenas)
  return coincides_histogram

def filter_in_with_in_tilr_list(jogo, tilr_list, n_slots=5, up_to_concurso=None):
  TilR = None # will be dynamically replaced by the module TilR; otherwise cross-dependency will arise as an operation sqlalchemy runtime exception
  exec('from maths.tils import TilR')
  tilrwpattern = TilR.get_tilrwpattern_of_game(jogo, n_slots, up_to_concurso)
  if tilrwpattern in tilr_list:
    return True
  return False



def adhoc_test():
  pass

def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
