#!/usr/bin/env python3
import sys
"""
jogos_functions_dependent.py contains some function that were
  separated from jogos_function due either to dependency on local system modules
  or cross-dependency issues
"""
import jogos_functions
from models.Concursos.ConcursoHTML import ConcursoHTML
from models.Files.ReadConcursosHistory import ConcursosHistoryPickledStorage


def get_coincides_histogram_against_a_lookup_depth(jogo, up_to_n_do_conc=None, lookup_depth=1000):
  slider = ConcursoHTML()
  concurso = slider.get_last_concurso()
  last_n_do_conc = concurso.n_conc
  if up_to_n_do_conc is None:
    # Default
    up_to_n_do_conc = last_n_do_conc
  elif up_to_n_do_conc < 0 or up_to_n_do_conc <= last_n_do_conc:
    # Default
    up_to_n_do_conc = last_n_do_conc
  # slider.get_concurso_by_nDoConc(up_to_nDoConc)
  pickled = ConcursosHistoryPickledStorage(upper_nDoConc=up_to_n_do_conc) # read_as_id=None,
  previous_games_as_dezenas = pickled.read_or_create()
  if len(previous_games_as_dezenas) < lookup_depth:
    return None
  previous_games_as_dezenas = previous_games_as_dezenas[:lookup_depth]
  coincides_histogram = jogos_functions.get_coincides_histogram(jogo, previous_games_as_dezenas)
  return coincides_histogram


def filter_in_with_in_tilr_list(jogo, tilr_list, n_slots=5, up_to_concurso=None):
  # will be dynamically replaced by the module til_r; otherwise cross-dependency will arise
  # as an operation sqlalchemy runtime exception
  til_r = None
  exec('from maths2.tils import til_r')
  tilrwpattern = til_r.get_tilrwpattern_of_game(jogo, n_slots, up_to_concurso)
  if tilrwpattern in tilr_list:
    return True
  return False


def adhoc_test():
  pass


if __name__ == '__main__':
  look_for_adhoctest_arg()
