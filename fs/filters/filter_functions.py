#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
'''

'''
from fs.jogos import jogos_functions # get_line_patterns, get_column_patterns etc.
from fs import system_wide_lambdas as swlambda

def filter_sum_within(jogo, in_between):
  '''
  Metric 5: sum itself, sum compared to others, avg itself, avg compared to others
  Submetric: self sum in between a min-max range
  '''
  s = sum(jogo)
  if s < in_between[0] or s > in_between[1]:
    return False
  return True
  
def filter_within_n_impares(jogo, in_between):
  '''
  Metric 4: remainders (n_impares, remainder_n, column/line_pattern, column/line_drawing etc.)
  Submetric: n_impares (0 to N_DEZENAS_SORTEADAS) within a min-max range
  '''
  n_impares = jogos_functions.get_n_impares(jogo) 
  if n_impares < in_between[0] or n_impares > in_between[1]:
    return False
  return True

def filter_in_within_line_patterns(jogo, line_patterns):
  '''
  Metric 4: remainders (n_impares, remainder_n, column/line_pattern, column/line_drawing etc.)
  Submetric: line_pattern (eg. 012210 which means 1 dozen in line 2, 2 in line 3, 3 in line 4 and 1 in line 5)
             As a line_drawing, 012210 becomes 2211
  '''
  line_pattern = jogos_functions.get_line_pattern(jogo)
  if line_pattern in line_patterns:
    return True
  return False

def filter_in_within_line_drawings(jogo, line_drawings):
  '''
  Metric 4: remainders (n_impares, remainder_n, column/line_pattern, column/line_drawing etc.)
  Submetric: line_drawing (eg. 2211 which means 2 dozens in one indetermined line, 2 in another, 1 in another, and 1 in another
             As a line_pattern, 2211 might be various 0-stuffing patterns such as 012210 or 002121.
  '''
  line_drawing = jogos_functions.get_line_drawing(jogo)
  if line_drawing in line_drawings:
    return True
  return False

def filter_in_within_column_patterns(jogo, column_patterns):
  '''
  Metric 4: remainders (n_impares, remainder_n, column/line_pattern, column/line_drawing etc.)
  Submetric: column_pattern (see explanation above for line_pattern)
  '''
  column_pattern = jogos_functions.get_column_pattern(jogo)
  if column_pattern in column_patterns:
    return True
  return False

def filter_in_within_column_drawings(jogo, column_drawings):
  '''
  Metric 4: remainders (n_impares, remainder_n, column/line_pattern, column/line_drawing etc.)
  Submetric: column_drawing (see explanation above for line_drawing)
  '''
  column_drawing = jogos_functions.get_column_drawing(jogo)
  if column_drawing in column_drawings:
    return True
  return False

def filter_in_having_consecutive_patterns(jogo, consecutive_patterns):
  '''
  Metric 2: Consecutive

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

def filter_in_those_within_n_repeats_with_m_previous_games(jogo_as_dezenas, contrajogos, compare_repeat_list):
  '''
  Suppose the following "small" game history:
    ( 1, 2, 3, 4, 5, 6)
    ( 7, 8, 9,10,11,12)
    (13,14,15,16,17,18)
  Now we ask how many repeats there are for the game:
    ( 1, 7,13,19,25,26)
  One can see that 1, 7 and 13 happened in the "small" game history above, so there are 3 repeats
  
  Because these repeats are single, ie, they do not repeat more times in history, the repeat information comes in positional, ie,
  it's [3], 3 inside a list.
  
  The second element in such a list informs that its value should be applied for a double repeat.
    Example: [3, 1] means: allow up to 3 single repeats and 1 double repeat
             (a double repeat is a dozen that happens twice in the game history considered, ie, through contrajogos). 
  
  Double repeats are not contemplated here because the coincides_history filter above encompasses 
  
  '''
  repeats_array = jogos_functions.get_array_n_repeats_with_m_previous_games(jogo_as_dezenas, contrajogos)
  # repeats_array is not planned to return as None, but it can be returned empty
  if len(repeats_array) == 0:
    return False
  bool_array_result = map(swlambda.is_equal, repeats_array, compare_repeat_list)
  if False in bool_array_result:
    return False
  # This means: all elements in bool_array_result are True, jogo_as_dezenas passed the filter
  return True
  '''
  for i, max_repeat in enumerate(compare_repeat_list):
    n_repeats = i + 1
    tmp_lambda = lambda x : x >= n_repeats
    with_this_repeat = filter(tmp_lambda, actual_repeats)
    print 'with_this_repeat', with_this_repeat,  'max_repeat',  max_repeat 
    if len(with_this_repeat) > max_repeat:
      return False
  return True
  '''

def filter_in_and_out_tilpatterns(patterns_as_intlist, tilhistogram):
  '''
  tilhistogram is a "cut" filter, ie, if tilhistogram is [...]
  dezenas per tilslot: [7, 18, 20, 14, 1]
  '''
  filtered_in_patterns_as_intlist = []; filtered_out_patterns_as_intlist = []
  for pattern in patterns_as_intlist:
    if True in map(swlambda.greater_than, pattern, tilhistogram):
      filtered_in_patterns_as_intlist.append(pattern)
    else:
      filtered_out_patterns_as_intlist.append(pattern)
  return filtered_in_patterns_as_intlist, filtered_out_patterns_as_intlist 

def adhoc_test():
  '''
  repeat_list = [3, 1]
  print 'bool_result = filter_in_those_within_n_repeats_with_m_previous_games(jogo_as_dezenas, contrajogos, repeat_list)'
  print 'jogo_as_dezenas', jogo_as_dezenas
  print 'contrajogos', contrajogos
  print 'repeat_list', repeat_list
  bool_result = filter_in_those_within_n_repeats_with_m_previous_games(jogo_as_dezenas, contrajogos, repeat_list)
  print 'bool_result', bool_result
  '''
  contrajogos =[]
  contrajogo = ( 1, 2, 3, 4, 5, 6)
  contrajogos.append(contrajogo)
  contrajogo = ( 1, 7, 8, 9,11,12)
  contrajogos.append(contrajogo)
  contrajogo = (1, 13,14,15,17,18)
  contrajogos.append(contrajogo)
  jogo_as_dezenas = ( 1, 7,13,19,25,26)
  repeat_list = [3, 1, 1]
  print 'bool_result = filter_in_those_within_n_repeats_with_m_previous_games(jogo_as_dezenas, contrajogos, repeat_list)'
  print 'jogo_as_dezenas', jogo_as_dezenas
  print 'contrajogos', contrajogos
  print 'repeat_list', repeat_list
  bool_result = filter_in_those_within_n_repeats_with_m_previous_games(jogo_as_dezenas, contrajogos, repeat_list)
  print 'bool_result', bool_result
#  jogo = 1,10,12,21,31,60
#  print jogo, get_line_pattern(jogo)
#  print jogo, get_column_pattern(jogo)

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
