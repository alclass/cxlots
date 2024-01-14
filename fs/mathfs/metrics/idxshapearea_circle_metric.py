#!/usr/bin/env python3
"""
fs/mathfs/metrics/idxshapearea_circle_metric.py
  Implements the abstract circle metric
"""
import math
import statistics


class Jogo:

  def __init__(self, points):
    self.points = points
    self.calculate_center_n_radius()
    self._mid_x = (10 + 1) / 2
    self._mid_y = (6 + 1) / 2

  @property
  def card_mid_x(self):
    return self._mid_x

  @property
  def card_mid_y(self):
    return self._mid_y

  @property
  def mid_x(self):
    return self._mid_x

  @property
  def mid_y(self):
    return self._mid_y

  def calculate_center_n_radius(self):
    pass


def get_abstract_card_radius(center, array):
  total_distances = 0
  ccol, crow = center
  for d in array:
    # x is col
    col, row = extract_as_tupl_row1idx_n_col1idx_from_carddozen(d)
    dist = math.sqrt((col - ccol) ** 2 + (row - crow) ** 2)
    total_distances += dist
  mean_distance = total_distances / (len(array))
  radius = round(mean_distance*100, 0)
  print(center, array, mean_distance, radius)
  return radius


def extract_as_tupl_row1idx_n_col1idx_from_carddozen(n, low_high_limit=(1, 60)):
  """
  Example:
    dozen = 15 => row_idx = 2, col_idx = 5
    dozen = 10 => row_idx = 1, col_idx = 0
    dozen = 1 => row_idx = 1, col_idx = 1
    dozen = 11 => row_idx = 2, col_idx = 1
    dozen = 60 => row_idx = 6, col_idx = 0
  """
  try:
    n = int(n)
  except (TypeError, ValueError):
    return None, None
  if n < low_high_limit[0] or n > low_high_limit[1]:
    return None, None
  row1idx = math.ceil(n/10)  # notice that row1idx(10)=1 & row1idx(11)=2
  col1idx = ((n-1) % 10) + 1  # it's the same as the unit-digit
  return row1idx, col1idx


def separate_as_tupl_dozen_n_unit_from_carddozen(n, low_high_limit=(1, 60)):
  """
  Example:
    dozen = 15 => left_digit = 1, right_digit = 5
    dozen = 1 => left_digit = 0, right_digit = 1
    dozen = 60 => left_digit = 6, right_digit = 0
  """
  try:
    n = int(n)
  except (TypeError, ValueError):
    return None, None
  if n < low_high_limit[0] or n > low_high_limit[1]:
    return None, None
  rowdigit = math.floor((n-1)/10) + 1
  coldigit = ((n-1) % 10) + 1
  return rowdigit, coldigit


def get_rowpatt_n_colpatt_from_dozensarray(dozens):
  rowpatt = []
  colpatt = []
  for d in dozens:
    rowdigit, coldigit = extract_as_tupl_row1idx_n_col1idx_from_carddozen(d)
    rowpatt.append(rowdigit)
    colpatt.append(coldigit)
  return rowpatt, colpatt


def get_x_y_row_column_6x10pairs():
  tuplelist = [(math.floor(n / 10 + 1), (n % 10) + 1) for n in range(0, 60)]
  return tuplelist


def calc_abstract_card_radius_of_cardarray(cardarray):
  """
  01 02 03 04 05 06 07 08 09 10
  11 12 13 14 15 16 17 18 19 20
  21 22 23 24 25 26 27 28 29 30
  31 32 33 34 35 36 37 38 39 40
  41 42 43 44 45 46 47 48 49 50
  51 52 53 54 55 56 57 58 59 60

  Example: (14, 16, 18, 54, 56, 58)
  center should be (visually) 36
  radius should be (visually) > 2 (in implementation, it's > 2*100=200
    (the integer is to calculated-interpolated)

  bool_has_true_if_some_different = list(map(lambda e: e != rows[0], rows[1:]))
  if True not in bool_has_true_if_some_different:
    print('radius is None', bool_has_true_if_some_different, 'rows', rows)
    return None
  bool_has_true_if_some_different = list(map(lambda e: e != columns[0], columns[1:]))
  if True not in bool_has_true_if_some_different:
    print('radius is None', bool_has_true_if_some_different, 'columns', columns)
    return None


  """
  dezenas = cardarray
  columns, rows = [], []
  # tuplelist = get_x_y_row_column_6x10pairs()
  # print(len(tuplelist), tuplelist)
  rows = [math.floor(d / 10) for d in dezenas]
  columns = [d % 10 for d in dezenas]
  mid_col = statistics.mean(columns)
  mid_row = statistics.mean(rows)
  print('midrow', mid_row,  'rows', rows, 'midcol', mid_col,  'columns', columns)
  center = (mid_row, mid_col)
  radius = get_abstract_card_radius(center, dezenas)
  print('center', center, 'radius', radius)


def get_as_pattstr_col_n_row_stretches(dozenarray):
  rowstretch, colstretch = get_col_n_row_stretches(dozenarray)
  if (rowstretch, colstretch) == ([], []):
    return '', ''
  rowstretch_pattstr = ''.join(map(lambda e: str(e), rowstretch))
  colstretch_pattstr = ''.join(map(lambda e: str(e), colstretch))
  return rowstretch_pattstr, colstretch_pattstr


def get_col_n_row_stretches(dozenarray):
  """

  The "stretches" may be explained by an example:
  Suppose card = (1, 2, 3, 4, 5, 6)
    Its colstretch is '111111' and its rowstretch is '6'
  Now, put some gaps in the previous card = (1, 2, 3, 4, 5, 6), such that card = (1, 3, 5, 7, 9, 10)
    Its colstretch is '1010101011' and its rowstretch is still '6'
  Notice the 0's (zeroes) stuffed into colstretch, the first one is '111111', the second is '1010101011'
  The rule here is that zeroes can only be inserted in between the non-zeroes, not before or after.
  """
  nrows = []
  ncolumns = []
  for d in dozenarray:
    lrtuple = extract_as_tupl_row1idx_n_col1idx_from_carddozen(d)
    if lrtuple[0] is None:
      return [], []
    ncolumns.append(lrtuple[0])
    nrows.append(lrtuple[1])
  rowstretch = nrows[:]
  colstretch = ncolumns[:]
  # sweep rows
  indices_before_the_first = []
  for r in range(6):
    boolarray = list(map(lambda e: r < e, nrows))
    if False not in boolarray:
      continue
    boolarray = list(map(lambda e: r > e, nrows))
    if False not in boolarray:
      continue
    boolarray = list(map(lambda e: r == e, nrows))
    if True in boolarray:
      continue
    #
    rowstretch.insert(r, 0)
  for c in range(10):
    boolarray = list(map(lambda e: r < e, ncolumns))
    if False not in boolarray:
      continue
    boolarray = list(map(lambda e: r > e, ncolumns))
    if False not in boolarray:
      continue
    boolarray = list(map(lambda e: r == e, ncolumns))
    if True in boolarray:
      continue
    #
    colstretch.insert(c, 0)
  print()
  print(ncolumns, 'colstretch', colstretch, nrows, 'rowstretch', rowstretch)
  return rowstretch, colstretch


def adhoctest():
  jogos = []
  dezenas = (14, 16, 18, 54, 56, 58)
  jogos.append(dezenas)
  dezenas = (12, 14, 25, 16, 17, 18)
  jogos.append(dezenas)
  dezenas = (12, 14, 15, 16, 17, 18)
  jogos.append(dezenas)
  dezenas = (22, 24, 25, 26, 27, 28)
  jogos.append(dezenas)
  dezenas = (1, 2, 3, 4, 5, 6)
  jogos.append(dezenas)
  dezenas = (1, 11, 21, 31, 41, 51)
  jogos.append(dezenas)
  dezenas = (1, 2, 3, 11, 12, 13)
  jogos.append(dezenas)
  dezenas = (4, 5, 6, 14, 15, 16)
  jogos.append(dezenas)
  for i, cardarray in enumerate(jogos):
    print('jogo', i+1, '=>', cardarray)
    colstretch, rowstretch = get_col_n_row_stretches(cardarray)
    calc_abstract_card_radius_of_cardarray(cardarray)


def process():
  pass


if __name__ == '__main__':
  adhoctest()
  process()

