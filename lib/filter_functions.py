#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
'''

'''
from lib import jogos_functions # get_line_patterns, get_column_patterns etc.

def filter_sum_within(jogo, in_between):
  s = sum(jogo)
  if s < in_between[0] or s > in_between[1]:
    return False
  return True
  
def filter_within_n_impares(jogo, in_between):
  n_impares = jogos_functions.get_n_impares(jogo) 
  if n_impares < in_between[0] or n_impares > in_between[1]:
    return False
  return True

def filter_in_within_line_patterns(jogo, line_patterns):
  line_pattern = jogos_functions.get_line_pattern(jogo)
  if line_pattern in line_patterns:
    return True
  return False

def filter_in_within_line_drawings(jogo, line_drawings):
  line_drawing = jogos_functions.get_line_drawing(jogo)
  if line_drawing in line_drawings:
    return True
  return False

def filter_in_within_column_patterns(jogo, column_patterns):
  column_pattern = jogos_functions.get_column_pattern(jogo)
  if column_pattern in column_patterns:
    return True
  return False

def filter_in_within_column_drawings(jogo, column_drawings):
  column_drawing = jogos_functions.get_column_drawing(jogo)
  if column_drawing in column_drawings:
    return True
  return False

def filter_in_having_consecutive_patterns(jogo, consecutive_patterns):
  '''
  Possible consecutive_patterns by examples:
  1 (2 3 4 5 6) ==>> 51 meaning 5 consecutive dozens in one group
  1 (2 3 4 5) 7 ==>> 41 means 4 consecutive dozens in one group 
  (...)
  1 (2 3) 5 (6) 8 ==>> 32 means 3 consecutive dozens in two (2) groups 
  (...)
  1(2) 4(5) 7(8) ==>> 33 means 3 consecutive dozens in three (3) groups
   
  '''
  consecutive_pattern = jogos_functions.get_consecutive_pattern(jogo)
  if consecutive_pattern in consecutive_patterns:
    return True
  return False


def adhoc_test():
  '''
  '''
  pass
#  jogo = 1,10,12,21,31,60
#  print jogo, get_line_pattern(jogo)
#  print jogo, get_column_pattern(jogo)

def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
