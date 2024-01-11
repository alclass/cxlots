#!/usr/bin/env python3
"""
  This module should not, by design, depend on local system modules
    "import sys" above is fine!
  
  For the functions that do depend on local system modules, they were organized in 
    another module called jogos_function_dependent

sqlite3 database
  nconc
  dezenas_ord_sor
  n_acertos
  n_acertos_unid
  n_acertos_leftdigit
  n_pares
  media100
  dp100
  resto6
  resto10
  n_simmetrical  eg 35 & 53 is 1-simmetrical
  colocurr eg 6000000000 1000400001 etc
  rowocurr 600000 100401
  quadpatt 2112  eg Q1(12 25) Q2(28) Q3(53) Q4(39 58)
  diagpatt 2220000000 d1(01, 12, 23, 34, 45, 56) d2(02, 13, 24, 35, 46, 57)
  coincpatt INT
    # rule n_coinc_concprev1*7^6 + n_coinc_concprev2*7^5 + n_coinc_concprev3*7^4 + ...
  nconcslastoccurstr eg if jogo is 1, 2, 3, 4, 5 & 6 and if nconcslastoccurstr = 010203040506
    # this means dozen 1 happened 1 conc ago, dozen 2, 2 concs' ago, dozen 3, 3 conc's ago etc
"""


def calc_n_coinc_w_prevconc(jogo, dezena_w_gaps_til_repeat_dict):
  """
    # rule n_coinc_concprev1*7**6 + n_coinc_concprev2*7**5 + n_coinc_concprev3*7**4 + ...
  Example with supposition
  Suppose jogo = 1,2,3,4,5,6
    1,2 coincide with the first before last draw
    3,4,5 coincide with the second before last draw
    6 coincide with the fourth before last draw
  That result should be:
    coincpatt = 2*7**6 + 3*7**5 + 1*7**3 = 286062
  meaning:
    the first two happened one conc ago
    the 3 next happened two conc's ago
    the last one happened four conc's ago
  Notice that this indicator has value 0 (zero) if all dozens happened more than 7 conc's ago
  On the other side, if all 6 dozens happened one conc before, it'll have a maximum value of 6*7**6
    which is 705894
  """
  coincpatt = 0
  gapdict = {}
  for dezena in dezena_w_gaps_til_repeat_dict:
    n_gaps = dezena_w_gaps_til_repeat_dict[dezena]
    if n_gaps in gapdict:
      gapdict[n_gaps] += 1
    else:
      gapdict[n_gaps] = 1
  for n_gap in gapdict:
    expo = 7 - n_gap
    coincpatt += gapdict[n_gap] * 7 ** expo
  return coincpatt


def get_diag_n_for_dozen(dezena, diag_matrix=None):
  if diag_matrix is None:
    diag_matrix = form_diag_matrix_positions()
  for i, diag in enumerate(diag_matrix):
    if dezena in diag:
      return i
  return None


def form_diag_matrix_positions():
  """
  diag1 (01, 12, 23, 34, 45, 56)
  diag2 (02, 13, 24, 35, 46, 57)
  diag3 (03, 14, 25, 36, 47, 58)
  diag4 (04, 15, 26, 37, 48, 59)
  diag5 (05, 16, 27, 38, 49, 60)
  diag6 (06, 17, 28, 39, 50, 51)
  diag7 (07, 18, 29, 40, 41, 52)
  diag8 (08, 19, 30, 31, 42, 53)
  diag9 (09, 20, 21, 32, 43, 54)
  diag10 (10, 11, 22, 33, 44, 55)
  Algorithm
    start pos(1, 1) with 1
      going one place to the right, add 11
        if place resultant is diviseable by 10, add 1
      going one place down, add 1 (modulo 60)
        if place resultant is diviseable by 10, subtract 9
  """
  matrix = []
  line = []
  for i in range(1, 11):
    val = i
    for j in range(1, 7):
      if j == 1:
        line.append(i)
        continue
      if val % 10 != 0:
        val += 11
      else:  # val % 10 == 0:
        val += 1
      line.append(val)
    matrix.append(line)
    line = []
  return matrix


def get_n_acertos(jogo, contrajogo):
  n_acertos = 0
  for dezena in jogo:
    if dezena in contrajogo:
      n_acertos += 1
  return n_acertos


def get_coincides_histogram(jogo_dezenas, previous_games_as_dozens, n_sorteadas=6):
  coincides_histogram = {}
  # How many coincides dict-keys are there?  There should be n_sorteadas_mais_nenhuma_coincidencia
  n_sorteadas_mais_nenhuma_coincidencia = n_sorteadas + 1
  for n_coincides in range(n_sorteadas_mais_nenhuma_coincidencia):
    coincides_histogram[n_coincides] = 0
  for previous_game in previous_games_as_dozens:
    n_acertos = get_n_acertos(jogo_dezenas, previous_game)
    coincides_histogram[n_acertos] += 1
  return coincides_histogram 


def has_game_equal_or_more_than_n_acertos(compare_dezenas, all_jogos_as_dezenas, cant_have_n_acertos=3):
  """
  This function is a filter-like operator that runs compare_dezenas (a list of ints) against a history of games
    (each game is a compare_dezenas compatible)
  If, as all games loop up to be compared, more than upToAcertos dozens coincide, False is returned
    right away (no need to expend any extra time!)
  After all games have looped up -- ie, a False not happening before -- True will be returned at the end
  """
  for jogo in all_jogos_as_dezenas:
    n_acertos = 0
    equals = []
    for compare_dezena in compare_dezenas:
      if compare_dezena in jogo:
        n_acertos += 1
        equals.append(compare_dezena)
      if n_acertos >= cant_have_n_acertos:
        return True
  return False


def get_n_impares(jogo):
  return len(filter(lambda n: n % 2 == 1, jogo))


def get_line_pattern_and_drawing(jogo):
  tens_digit_dict = {}
  for line in range(6):
    tens_digit_dict[line] = 0
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


def get_line_drawing(jogo):
  tens_digit_dict = get_line_pattern_and_drawing(jogo)
  quantities = tens_digit_dict.values()
  quantities = filter(lambda n: n != 0, quantities)
  quantities.sort()
  quantities.reverse()
  quantities = map(str, quantities)
  drawing = ''.join(quantities)
  return drawing


def get_column_pattern_and_drawing(jogo):
  unit_minus_one_digit_dict = {}
  for column in range(10):
    unit_minus_one_digit_dict[column] = 0
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
  quantities = filter(lambda e: e != 0, quantities)
  quantities.sort()
  quantities.reverse()
  quantities = map(str, quantities)
  drawing = ''.join(quantities)
  return drawing


def get_consecutive_pattern(jogo, to_sort=False):
  if to_sort:
    jogo.sort()
  n_consecutives, n_groups = 0, 1
  for i, dezena in enumerate(jogo):
    if i == 0:
      continue
    if dezena - 1 == jogo[i-1]:
      n_consecutives += 1
      if n_consecutives > 1:
        if dezena - 2 != jogo[i-2]:
          n_groups += 1
  consecutive_pattern = '%d%d' % (n_consecutives, n_groups)
  return consecutive_pattern 


def get_n_repeats_against_contrajogo(jogo, contrajogo):
  n_repeats = 0
  for dezena in jogo:
    if dezena in contrajogo:
      n_repeats += 1
  return n_repeats 


def get_array_n_repeats_with_m_previous_games(jogo_as_dezenas, contrajogos):
  """
  Suppose the following "small" game history:
    ( 1, 2, 3, 4, 5, 6)
    ( 1, 7, 8, 9, 10, 11)
    ( 1, 12, 13, 14, 15, 16)
  Now we ask how many repeats there are for the game:
    ( 1, 7, 13, 19, 25, 26)
  The repeats are 1, 7 and 13. 1 repeats 3 times, 7 once, 13 once.
  So, the result should be:
    output_array_as_in_documentation = [3,1,1]
  Why?
  Because 3 dozens (1, 7 & 13) repeat at least once.  
  The 1 in the second array position is because 1 repeats at least twice.
  The 1 in the last array position is because 1 repeats 3 times.
  Because there's no dozen repeating a 4th time, the array ends with its 3rd element.
  """
  if jogo_as_dezenas is None or contrajogos is None:
    return []
  each_dozen_repeat_dict = {}
  for dezena in jogo_as_dezenas:
    each_dozen_repeat_dict[dezena] = 0
  for contrajogo_as_dezenas in contrajogos:
    for dezena in contrajogo_as_dezenas:
      if dezena in jogo_as_dezenas:
        each_dozen_repeat_dict[dezena] += 1
  actual_repeats = each_dozen_repeat_dict.values()
  return list(filter(lambda e: e > 0, actual_repeats))


def get_array2_n_repeats_with_m_previous_games(jogo_as_dezenas, contrajogos):
  if len(actual_repeats) == 0:
    return []
  max_repeating = max(actual_repeats)
  output_array_as_in_documentation = []
  for n_repeats in range(1, max_repeating + 1):
    with_this_repeat = [c >= n_repeats for c in actual_repeats]
    total_with_this_repeat = len(with_this_repeat)
    output_array_as_in_documentation.append(total_with_this_repeat)
  return output_array_as_in_documentation


def test_jogo_metrics(jogo):
  print(jogo, get_line_pattern(jogo))
  print(jogo, get_line_drawing(jogo))
  print(jogo, get_column_pattern(jogo))
  print(jogo, get_column_drawing(jogo))
  print(jogo, get_consecutive_pattern(jogo))


def adhoc_test():
  """
  1 (2 3 4 5 6) ==>> 51 meaning 5 consecutive dozens in one group
  1 (2 3 4 5) 7 ==>> 41 means 4 consecutive dozens in one group 
  (...)
  1 (2 3) 5 (6) 8 ==>> 32 means 3 consecutive dozens in two (2) groups 
  (...)
  1(2) 4(5) 7(8) ==>> 33 means 3 consecutive dozens in three (3) groups  
  """
  pass
  jogo = 1, 11, 12, 21, 22, 60
  test_jogo_metrics(jogo)
  jogo = 1, 2, 11, 12, 21, 22, 60
  test_jogo_metrics(jogo)
  jogo = 1, 2, 3, 4, 5, 6
  test_jogo_metrics(jogo)
  jogo = 1, 2, 3, 4, 5, 7
  test_jogo_metrics(jogo)
  jogo = 1, 2, 3, 5, 6, 8
  test_jogo_metrics(jogo)
  jogo = 1, 2, 4, 5, 7, 8
  test_jogo_metrics(jogo)


def adhoctest1():
  contrajogos = []
  contrajogo = (1, 2, 3, 4, 5, 6)
  contrajogos.append(contrajogo)
  contrajogo = (1, 7, 8, 9, 11, 12)
  contrajogos.append(contrajogo)
  contrajogo = (1, 13, 14, 15, 17, 18)
  contrajogos.append(contrajogo)
  jogo_as_dezenas = (1, 7, 13, 19, 25, 26)
  repeats_array = get_array_n_repeats_with_m_previous_games(jogo_as_dezenas, contrajogos)
  print(repeats_array)


def adhoctest2():
  """
  Suppose jogo = 1,2,3,4,5,6
    1,2 coincide with the first before last draw
    3,4,5 coincide with the second before last draw
    6 coincide with the fourth before last draw
  That result should be:
    coincpatt = 2*7**6 + 3*7**5 + 1*7**3 = 286062
  """
  jogo = 1, 2, 3, 4, 5, 6
  dezena_w_gaps_til_repeat_dict = {
    1: 1, 2: 1, 3: 2, 4: 2, 5: 2, 6: 4,
  }
  res = calc_n_coinc_w_prevconc(jogo, dezena_w_gaps_til_repeat_dict)
  print('jogo', jogo, 'dict', dezena_w_gaps_til_repeat_dict)
  print('result', res)
  mtx = form_diag_matrix_positions()
  for line in mtx:
    print(line)
  pdict = {i: get_diag_n_for_dozen(i, mtx) for i in range(1, 61)}
  print(pdict)


if __name__ == '__main__':
  adhoctest2()
