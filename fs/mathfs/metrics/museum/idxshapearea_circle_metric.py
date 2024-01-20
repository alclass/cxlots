#!/usr/bin/env python3
"""
fs/mathfs/metrics/idxshapearea_circle_metric.py
  Implements the abstract circle metric
"""
import math
import statistics
import fs.mathfs.combinatorics.combinatoric_algorithms as ca  # ca.RCombiner
COLUMN_POSITION_SIZE, ROW_POSITION_SIZE = 10, 6


class ShapeAreaCircleCalculator:

  def __init__(self, cardarray):
    self.cardarray = cardarray
    self.radius = None
    self.center_x_y = None
    self.dozen_col_indices, self.dozen_row_indices = get_col_n_row_1indices_from_dozensarray(self.cardarray)
    self.rowstretch, self.colstretch = get_col_n_row_1indices_inbetweenzerografted_from_cardarray(self.cardarray)
    self.calculate_center_n_radius()

  @property
  def dozen_col_indices_str(self):
    return ''.join(map(lambda e: str(e), self.dozen_col_indices))

  @property
  def dozen_row_indices_str(self):
    return ''.join(map(lambda e: str(e), self.dozen_row_indices))

  @property
  def colstretch_str(self):
    return ''.join(map(lambda e: str(e), self.colstretch))

  @property
  def rowstretch_str(self):
    return ''.join(map(lambda e: str(e), self.rowstretch))

  def calculate_center_n_radius(self):
    self.center_x_y = get_center_x_y_from_cardarray(self.cardarray)
    self.radius = get_abstract_card_radius(self.center_x_y, self.cardarray)

  def calc_col_n_row_1idx_zerografted(self):
    pass

  def __str__(self):
    ro1idpttstr = self.dozen_row_indices_str
    co1idpttstr = self.dozen_col_indices_str
    outstr = f"""  ShapeAreaCircleCalculator cardarray={self.cardarray} 
      center={self.center_x_y} radius={self.radius}
      rowpatt={ro1idpttstr} colpatt={co1idpttstr}
      rowstretch={self.rowstretch_str} colpatt={self.colstretch_str}"""
    return outstr


def prune_beginning_n_ending_zeros_from_intlist(intlist):
  while len(intlist) > 0:
    if intlist[-1] == 0:
      del intlist[-1]
    else:
      break
  while len(intlist) > 0:
    if intlist[0] == 0:
      del intlist[0]
    else:
      break
  return intlist


def get_abstract_card_radius(center, array):
  total_distances = 0
  ccol, crow = center
  for d in array:
    # x is col
    col, row = extract_as_tupl_col1idx_n_row1idx_from_carddozen(d)
    dist = math.sqrt((col - ccol) ** 2 + (row - crow) ** 2)
    total_distances += dist
  mean_distance = total_distances / (len(array))
  radius = round(mean_distance*100, 0)
  print(center, array, mean_distance, radius)
  return radius


def extract_as_tupl_col1idx_n_row1idx_from_carddozen(n, low_high_limit=(1, 60)):
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
  col1idx = ((n-1) % 10) + 1  # it's the same as the unit-digit
  row1idx = math.ceil(n/10)  # notice that row1idx(10)=1 & row1idx(11)=2
  return col1idx, row1idx


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


def get_col_n_row_1indices_from_dozensarray(dozens):
  rowpatt = []
  colpatt = []
  for d in dozens:
    coldigit, rowdigit = extract_as_tupl_col1idx_n_row1idx_from_carddozen(d)
    colpatt.append(coldigit)
    rowpatt.append(rowdigit)
  return colpatt, rowpatt


def get_x_y_row_column_6x10pairs():
  tuplelist = [(math.floor(n / 10 + 1), (n % 10) + 1) for n in range(0, 60)]
  return tuplelist


def get_center_x_y_from_cardarray(cardarray):
  """
  01 02 03 04 05 06 07 08 09 10
  11 12 13 14 15 16 17 18 19 20
  21 22 23 24 25 26 27 28 29 30
  31 32 33 34 35 36 37 38 39 40
  41 42 43 44 45 46 47 48 49 50
  51 52 53 54 55 56 57 58 59 60

  Example: (14, 16, 18, 54, 56, 58)
  center should be (visually) 36
  radius should be (visually) > 2 (in implementation, it's > 2*100=200)
    (the integer is to calculated-interpolated)

  bool_has_true_if_some_different = list(map(lambda e: e != rows[0], rows[1:]))
  if True not in bool_has_true_if_some_different:
    print('radius is None', bool_has_true_if_some_different, 'rows', rows)
    return None
  bool_has_true_if_some_different = list(map(lambda e: e != columns[0], columns[1:]))
  if True not in bool_has_true_if_some_different:
    print('radius is None', bool_has_true_if_some_different, 'columns', columns)
    return None

  radius = get_abstract_card_radius(center, dezenas)
  print('center', center, 'radius', radius)
  """
  dezenas = cardarray
  rows = [math.floor(d / 10) for d in dezenas]
  columns = [d % 10 for d in dezenas]
  mid_col = statistics.mean(columns)
  mid_row = statistics.mean(rows)
  center = (mid_row, mid_col)
  return center


def get_asstr_col_n_row_1indices_inbetweenzerografted(dozenarray):
  rowstretch, colstretch = get_col_n_row_1indices_inbetweenzerografted_from_cardarray(dozenarray)
  if (rowstretch, colstretch) == ([], []):
    return '', ''
  rowstretch_pattstr = ''.join(map(lambda e: str(e), rowstretch))
  colstretch_pattstr = ''.join(map(lambda e: str(e), colstretch))
  return rowstretch_pattstr, colstretch_pattstr


def get_col_n_row_1indices_from_cardarray(dozenarray):
  row_1indices, column_1indices = [], []
  for d in dozenarray:
    col1idx, row1idx = extract_as_tupl_col1idx_n_row1idx_from_carddozen(d)
    if col1idx is None or row1idx is None:
      return [], []
    column_1indices.append(col1idx)
    row_1indices.append(row1idx)
  return column_1indices, row_1indices


def get_col_n_row_counted_pos_dict_from_cardarray(dozenarray):
  col1indices, row1indices = get_col_n_row_1indices_from_cardarray(dozenarray)
  col_count_dict, row_count_dict = {}, {}
  for pos1idx in col1indices:
    if pos1idx in col_count_dict:
      col_count_dict[pos1idx] += 1
    else:
      col_count_dict[pos1idx] = 1
  for pos1idx in row1indices:
    if pos1idx in row_count_dict:
      row_count_dict[pos1idx] += 1
    else:
      row_count_dict[pos1idx] = 1
  return col_count_dict, row_count_dict


def get_col_n_row_1indices_inbetweenzerografted_from_cardarray(dozenarray):
  """

  The "stretches" may be explained by an example:
  Suppose card = (1, 2, 3, 4, 5, 6)
    Its colstretch is '111111' and its rowstretch is '6'
  Now, put some gaps in the previous card = (1, 2, 3, 4, 5, 6), such that card = (1, 3, 5, 7, 9, 10)
    Its colstretch is '1010101011' and its rowstretch is still '6'
  Notice the 0's (zeroes) stuffed into colstretch, the first one is '111111', the second is '1010101011'
  The rule here is that zeroes can only be inserted in between the non-zeroes, not before or after.
  """
  zero, columnsize, rowsize = 0, COLUMN_POSITION_SIZE, ROW_POSITION_SIZE
  col_count_dict, row_count_dict = get_col_n_row_counted_pos_dict_from_cardarray(dozenarray)
  column_counts = []
  for idx1 in range(1, columnsize+1):
    if idx1 in col_count_dict:
      column_counts.append(col_count_dict[idx1])
    else:
      column_counts.append(zero)
  prune_beginning_n_ending_zeros_from_intlist(column_counts)
  row_counts = []
  for idx1 in range(1, rowsize+1):
    if idx1 in row_count_dict:
      row_counts.append(row_count_dict[idx1])
    else:
      row_counts.append(zero)
  prune_beginning_n_ending_zeros_from_intlist(row_counts)
  return column_counts, row_counts


def stretch_inbetween(alist):
  """

  """
  if len(alist) < 1 or len(alist) > 6:
    errmsg = f'alist has size {len(alist)}, ie not within set [1, 6]'
    raise ValueError(errmsg)
  if len(alist) in [1, 6]:
    return []
  possible_grafts = 6 - len(alist)
  for i in range(1, possible_grafts+1):
    grafts = '0'*i


def gen_all_comb_for_col1idx_zerografted():
  """
  fs.mathfs.combinatorics.combinatoric_algorithms.RCombiner

  """
  for asize in range(1, 7):
    combiner = ca.RCombiner(a_size=asize, up_int=6)
    print(asize, combiner.base_intpartitions)


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
    colstretch, rowstretch = get_col_n_row_1indices_inbetweenzerografted_from_cardarray(cardarray)
    center = get_center_x_y_from_cardarray(cardarray)
    print(center, colstretch, rowstretch)


def adhoctest2():
  dezenas = (14, 16, 18, 54, 56, 58)
  calcor = ShapeAreaCircleCalculator(dezenas)
  print(calcor)
  dezenas = (4, 6, 8, 44, 46, 48)
  calcor = ShapeAreaCircleCalculator(dezenas)
  print(calcor)


def adhoctest3():
  dezenas = (14, 16, 18, 54, 56, 58)
  col, row = get_col_n_row_1indices_inbetweenzerografted_from_cardarray(dezenas)
  print(dezenas, col, row)


def process():
  pass


if __name__ == '__main__':
  """
  adhoctest3()
  adhoctest2()
  process()
  """
  gen_all_comb_for_col1idx_zerografted()
