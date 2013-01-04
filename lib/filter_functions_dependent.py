#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
'''

'''
from lib import jogos_functions_dependent as jogos_fd # get_line_patterns, get_column_patterns etc.
def filter_in_those_within_coincides_histogram_range(jogo, coincides_ranges, up_to_nDoConc=None, LOOKUP_DEPTH=1000):
  coincides_histogram = jogos_fd.get_coincides_histogram_against_a_lookup_depth(jogo, up_to_nDoConc, LOOKUP_DEPTH)
  each_coincide_list = coincides_histogram.keys()
  for n_coincide in each_coincide_list:
    min_concursos_against_depth_with_n_coincides = coincides_ranges[n_coincide][0]
    max_concursos_against_depth_with_n_coincides = coincides_ranges[n_coincide][1]
    if coincides_histogram[n_coincide] < min_concursos_against_depth_with_n_coincides or coincides_histogram[n_coincide] > max_concursos_against_depth_with_n_coincides:
      return False
    return True

def adhoc_test():
  '''
  '''
  pass

def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
