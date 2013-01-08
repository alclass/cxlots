#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
'''
  This module should not, by design, depend on local system modules
    "import sys" above is fine!
  
  For the functions that do depend on local system modules, they were organized in 
    another module called jogos_function_dependent
    
  This was to help see and control any dynamic "import" (with exec()) that was found necessary
    due to cross-dependency issues (example: x imports y that imports back x)
    
  One way we solve this is to import x, in y, dynamically. But, because this may generate confusion,
    functions that had this issue of cross-dependency were moved to "smaller" modules where it's
    easier to "keep track" of them 
'''

def get_n_acertos(jogo, contrajogo):
  n_acertos = 0
  for dezena in jogo:
    if dezena in contrajogo:
      n_acertos += 1
  return n_acertos

def get_coincides_histogram(jogo_dezenas, previous_games_as_dozens, N_SORTEADAS=6):
  coincides_histogram = {}
  # How many coincides dict-keys are there?  There should be N_SORTEADAS_MAIS_NENHUMA_COINCIDENCIA 
  N_SORTEADAS_MAIS_NENHUMA_COINCIDENCIA = N_SORTEADAS + 1
  for n_coincides in range(N_SORTEADAS_MAIS_NENHUMA_COINCIDENCIA):
    coincides_histogram[n_coincides]=0
  for previous_game in previous_games_as_dozens:
    n_acertos = get_n_acertos(jogo_dezenas, previous_game)
    coincides_histogram[n_acertos]+=1
  return coincides_histogram 

def has_game_equal_or_more_than_n_acertos(compare_dezenas, all_jogos_as_dezenas, cant_have_n_acertos = 3):
  '''
  This function is a filter-like operator that runs compare_dezenas (a list of ints) against a history of games
    (each game is a compare_dezenas compatible)
  If, as all games loop up to be compared, more than upToAcertos dozens coincide, False is returned
    right away (no need to expend any extra time!)
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


def get_array_n_repeats_with_m_previous_games(jogo_as_dezenas, contrajogos):
  '''
  Suppose the following "small" game history:
    ( 1, 2, 3, 4, 5, 6)
    ( 1, 7, 8, 9,10,11)
    ( 1,12,13,14,15,16)
  Now we ask how many repeats there are for the game:
    ( 1, 7,13,19,25,26)
  The repeats are 1, 7 and 13. 1 repeats 3 times, 7 once, 13 once.
  So, the result should be:
    output_array_as_in_documentation = [3,1,1]
  Why?
  Because 3 dozens (1, 7 & 13) repeat at least once.  
  The 1 in the second array position is because 1 repeats at least twice.
  The 1 in the last array position is because 1 repeats 3 times.
  Because there's no dozen repeating a 4th time, the array ends with its 3rd element.
  '''
  if jogo_as_dezenas == None or contrajogos == None:
    return []
  each_dozen_repeat_dict = {}
  for dezena in jogo_as_dezenas:
    each_dozen_repeat_dict[dezena]=0
  for contrajogo_as_dezenas in contrajogos:
    for dezena in contrajogo_as_dezenas:
      if dezena in jogo_as_dezenas:
        each_dozen_repeat_dict[dezena]+=1
  # print 'each_dozen_repeat_dict', each_dozen_repeat_dict        
  actual_repeats = each_dozen_repeat_dict.values()
  tmp_lambda = lambda x : x > 0
  actual_repeats = filter(tmp_lambda, actual_repeats) # ie, filter out zeros
  if len(actual_repeats) == 0:
    return []
  max_repeating = max(actual_repeats)
  output_array_as_in_documentation = []
  for n_repeats in range(1, max_repeating + 1):
    tmp_lambda = lambda x : x >= n_repeats
    with_this_repeat = filter(tmp_lambda, actual_repeats)
    total_with_this_repeat = len(with_this_repeat)
    output_array_as_in_documentation.append(total_with_this_repeat)
    # print 'with_this_repeat', with_this_repeat,  'max_repeat',  max_repeat 
  return output_array_as_in_documentation

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
  
  
import unittest
class MyTest(unittest.TestCase):

  def test_1(self):
    pass
 
    contrajogos =[]
    contrajogo = ( 1, 2, 3, 4, 5, 6)
    contrajogos.append(contrajogo)
    contrajogo = ( 1, 7, 8, 9,11,12)
    contrajogos.append(contrajogo)
    contrajogo = (1, 13,14,15,17,18)
    contrajogos.append(contrajogo)
    jogo_as_dezenas = ( 1, 7,13,19,25,26)
    repeats_array = get_array_n_repeats_with_m_previous_games(jogo_as_dezenas, contrajogos)
    expected_result = [3,1,1] # ie, 3 dozens repeating once (d=1,7 & 13), 1 dozen repeats (at least) twice (d=1), 1 dozen repeats 3 times (d=1)
    # print 'repeats_array', repeats_array
    self.assertEqual(repeats_array, expected_result, 'expected_result must equal repeats_array from get_array_n_repeats_with_m_previous_games(jogo_as_dezenas, contrajogos)')
  
    contrajogos =[]
    contrajogo = ( 1, 2, 3, 4, 5, 6)
    contrajogos.append(contrajogo)
    contrajogo = ( 1, 7, 8, 9,11,12)
    contrajogos.append(contrajogo)
    contrajogo = (1, 13,14,15,17,18)
    contrajogos.append(contrajogo)
    contrajogo = ( 1, 2, 3, 4, 5, 6)
    contrajogos.append(contrajogo)
    jogo_as_dezenas = ( 1, 6,7,13,19,25)
    repeats_array = get_array_n_repeats_with_m_previous_games(jogo_as_dezenas, contrajogos)
    expected_result = [4, 2, 1, 1] # ie, 4 dozens repeating once (d=1,6,7 & 13), 2 dozen repeats twice (d=1&6), 1 dozen repeats 3 times (d=1), , 1 dozen repeats 3 times (d=1),
    #print 'repeats_array', repeats_array
    self.assertEqual(repeats_array, expected_result, 'expected_result must equal repeats_array from get_array_n_repeats_with_m_previous_games(jogo_as_dezenas, contrajogos)')


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


