#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
'''

'''

def has_game_equal_or_more_than_n_acertos(compare_dezenas, all_jogos_as_dezenas, cant_have_n_acertos = 3):
  '''
  This function is a filter-like operator that runs compare_dezenas (a list of ints) against a history of games
    (each game is a compare_dezenas compatible)
  If, as all games loop up to be compare, more than upToAcertos coincide, False is returned rightaway
  After all games have looped up -- ie, a False not happening before -- True will be returned at the end
  '''
  for jogo in all_jogos_as_dezenas:
    n_acertos = 0
    equals = []
    for compare_dezena in compare_dezenas:
      if compare_dezena in jogo:
        n_acertos += 1
        equals.append(compare_dezena)
      if n_acertos >= cant_have_n_acertos:
        # print 'n_acertos=%d >= cant_have_n_acertos=%d %s %s %s' %(n_acertos, cant_have_n_acertos, str(compare_dezenas), str(jogo), str(equals))
        return True
  return False

lambda_par_impar = lambda x : x % 2  # when even, 0 (which is also False) returns; when odd, 1 (which is True) returns :: they are used in a filter()
def get_n_impares(jogo):
  return len(filter(lambda_par_impar, jogo))

def get_line_pattern_and_drawing(jogo):
  tens_digit_dict = {}
  for line in range(6): tens_digit_dict[line] = 0 
  for dezena in jogo:
    tens_digit = (dezena - 1) / 10  # integer division!
    tens_digit_dict[tens_digit] += 1
  return tens_digit_dict

def get_line_pattern(jogo):
  line_pattern = ''
  tens_digit_dict = get_line_pattern_and_drawing(jogo)
  for line in range(6):
    line_pattern += str(tens_digit_dict[line])
  return line_pattern

f_not_zero = lambda x : x != 0
def get_line_drawing(jogo):
  tens_digit_dict = get_line_pattern_and_drawing(jogo)
  quantities = tens_digit_dict.values()
  quantities = filter(f_not_zero, quantities)
  quantities.sort()
  quantities.reverse()
  quantities = map(str, quantities)
  drawing = ''.join(quantities)
  return drawing

def get_column_pattern_and_drawing(jogo):
  unit_minus_one_digit_dict = {}
  for column in range(10): unit_minus_one_digit_dict[column] = 0 
  for dezena in jogo:
    remainder = (dezena - 1) % 10
    unit_minus_one_digit_dict[remainder] += 1
  return unit_minus_one_digit_dict

def get_column_pattern(jogo):
  unit_minus_one_digit_dict = get_column_pattern_and_drawing(jogo)
  column_pattern = ''
  for column in range(10):
    column_pattern += str(unit_minus_one_digit_dict[column])
  return column_pattern

def get_column_drawing(jogo):
  unit_minus_one_digit_dict = get_column_pattern_and_drawing(jogo)
  quantities = unit_minus_one_digit_dict.values()
  quantities = filter(f_not_zero, quantities)
  quantities.sort()
  quantities.reverse()
  quantities = map(str, quantities)
  drawing = ''.join(quantities)
  return drawing

def get_consecutive_pattern(jogo, to_sort = False):
  if to_sort:
    jogo.sort()
  n_consecutives = 0; n_groups = 1
  for i, dezena in enumerate(jogo):
    if i==0:
      continue
    if dezena - 1 == jogo[i-1]:
      n_consecutives += 1
      if n_consecutives > 1:
        if dezena - 2 != jogo[i-2]:
          n_groups += 1
  consecutive_pattern = '%d%d' %(n_consecutives, n_groups)
  return consecutive_pattern 

def get_n_repeats_against_contrajogo(jogo, contrajogo):
  n_repeats = 0
  for dezena in jogo:
    if dezena in contrajogo:
      n_repeats += 1
  return n_repeats 



def test_jogo_metrics(jogo):
  print jogo, get_line_pattern(jogo)
  print jogo, get_line_drawing(jogo)
  print jogo, get_column_pattern(jogo)
  print jogo, get_column_drawing(jogo)
  print jogo, get_consecutive_pattern(jogo)

def adhoc_test():
  '''
  1 (2 3 4 5 6) ==>> 51 meaning 5 consecutive dozens in one group
  1 (2 3 4 5) 7 ==>> 41 means 4 consecutive dozens in one group 
  (...)
  1 (2 3) 5 (6) 8 ==>> 32 means 3 consecutive dozens in two (2) groups 
  (...)
  1(2) 4(5) 7(8) ==>> 33 means 3 consecutive dozens in three (3) groups  
  
  '''
  pass
  jogo = 1,11,12,21,22,60; test_jogo_metrics(jogo)
  jogo = 1,2,11,12,21,22,60; test_jogo_metrics(jogo)
  jogo = 1,2,3,4,5,6; test_jogo_metrics(jogo)
  jogo = 1,2,3,4,5,7; test_jogo_metrics(jogo)
  jogo = 1,2,3,5,6,8; test_jogo_metrics(jogo)
  jogo = 1,2,4,5,7,8; test_jogo_metrics(jogo)
  

def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
