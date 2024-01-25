#!/usr/bin/env python3
"""
fs/mathfs/metrics/triple_simmetrics_n_col_row.py

The "triple simmetrics" (field triplesimm_n_col_row in db [at least at the time of this writing])
  is composed of 3 submetrics (sm), so to say, they are:

  sm1  the 'modulo' simmetric (its explanation below)
  sm2  the 'column' simmetric (explanation below)
  sm3  the 'row' simmetric (definition below)

 => m1  the 'number' simmetric:

  In MS (Megasena) the mtx simmetric is as follows:
    60 is simmetric of 1 and viceversa
    59 is simmetric of 2 and viceversa
    58 is simmetric of 3 and viceversa
    (...)
    31 is simmetric of 30 and viceversa

  The n_simm function is the following:  n_simm(n, m=60) = 61 - n

 => m2  the 'column' simmetric:

  In MS (Megasena) the column simmetric is as follows:
    col 10 is simmetric of col 1 and viceversa
    col 9 is simmetric of col 2 and viceversa
    (...)
    col 6 is simmetric of col 5 and viceversa

Notice that the column simmetry happens through a single row.

However, because numbers are up to 60, the task is a 2-function invocation.
  The first function, separates row and col from a dozen (the number itself).
  The second function returns the simmetric separated above:  n_simm(n, m=10) = 11 - n
  The simmetric then is recomposed from its col, row tuple.

 => m3  the 'row' simmetric (definition below)

  In MS (Megasena) the row simmetric is as follows:
    row 6 is simmetric of col 1 and viceversa
    row 5 is simmetric of col 2 and viceversa
    col 4 is simmetric of col 3 and viceversa

Notice that the row simmetry happens through a single column.

However, because numbers are up to 60, the task is a 2-function invocation.
  The first function, like for column simmetry above, separates row and col from a dozen (the number itself).
  The second function returns the simmetric separated above: n_simm(n, m=6) = 7 - n
  The simmetric then is recomposed from its col, row tuple.

  ---------------------------------------------------------------------
  How the triple simmetrics indicator metric is composed
  ---------------------------------------------------------------------

The triple simmetrics is a 3-digit base-4 number, but it is left as a base10 number, so that
both its str-representation and its appearance as int, both show the 3 simmetrics digit by digit.

---------
If it were chosen to use the base 4, the triplesimmetric number formation function would be as following:
  triplesimm_as_base10 = d2_row*4**2 + d1_col*4**1 + d1_nsimm_*4**0
---------

Example for the triplesimmetric as a metric-indicator:
  if the triplesimmetric is, for an example, '123', that says the following:
    1 pair (2 numbers) is 'modulo simmetric'
    2 pairs (4 numbers, 2 each) is 'column simmetric'
    3 pairs (6 numbers, 2 each) is 'row simmetric'

  @see also example below from the MS history.
    Incidentally, at the time of this writing (conc=2673),
      the MS history has not yet produced the triplesimmetry '123'.
    From the current histogram:
      {'000': 1146}, ie 1146 concs did not have any of the 3 simmetries;
      {'010': 410}, ie 410 concs had the column simmetry but no other;
      followed by {'001': 396}, {'100': 390}, {'111': 79} etc. in diminishing order.

  It's important to notice that if, in a set, no simmetries happen, then its int value will be 0 (zero),
    though its str-representation will be '000' (helping show that the 3 simmetries are absent)

Examples (from MS history):

ex1 conc=2545 TripleSimmetricCalculator [34, 3, 48, 28, 23, 38] => tripsimm = '111'
    111 | inspector = {'NUMSIMMETRY': [(23, 38)], 'COLSIMMETRY': [(28, 38)], 'ROWSIMMETRY': [(28, 23)]}

CURIOSITY:
  in the conc 2545 above, in all 3 simm pairs, one element also belongs to another pair,
  these are:
   23 belongs to MODSIMMETRY and to ROWSIMMETRY
   28 belongs to COLSIMMETRY and to ROWSIMMETRY
   38 belongs to COLSIMMETRY and to MODSIMMETRY

Another triple simmetry in:
ex2 2625 TripleSimmetricCalculator [16, 13, 9, 1, 59, 52] => tripsimm = '111'
    111 | inspector = {'MODSIMMETRY': [(9, 52)], 'COLSIMMETRY': [(9, 59)], 'ROWSIMMETRY': [(59, 52)]}

An example with no simmetries:
ex3 2627 TripleSimmetricCalculator [54, 32, 5, 53, 40, 14] => tripsimm = '000'
    0 | inspector = {}

An example with 3 numbersimmetries:
ex4 2355 TripleSimmetricCalculator [51, 36, 3, 58, 10, 25] => tripsimm = '300'
    300 | inspector = {'MODSIMMETRY': [(51, 10), (36, 25), (3, 58)]}

An example with 2 simmetries of each:
2520 TripleSimmetricCalculator [59, 23, 28, 55, 33, 38] => tripsimm = '222'
    222 | inspector = {'MODIMMETRY': [(23, 38), (28, 33)], 'COLSIMMETRY': [(23, 33), (28, 38)],
                       'ROWSIMMETRY': [(23, 28), (33, 38)]}
CURIOSITY:
  For conc 2520 above, results have 'swapped' elements from one tuple in MODSIMMETRY
    to another in ROWSIMMETRY and viceversa.
"""
import copy
import math
import commands.show.list_ms_history as lh  # lh.get_ms_history_as_list_with_cardgames_in_ord_sor


class TripleSimmetricCalculator:

  MODSIMMETRY = 'MODSIMMETRY'
  COLSIMMETRY = 'COLSIMMETRY'
  ROWSIMMETRY = 'ROWSIMMETRY'

  def __init__(self, numberlist, enable_inspector=False):
    self.numberlist = numberlist
    self.tripsimmlist = []
    self.m_simm_acc, self.col_simm_acc, self.row_simm_acc = 0, 0, 0
    self.enable_inspector = enable_inspector
    self.inspector_dict = {}
    self.triplesimmetric_as_int = -1
    self.process()

  @property
  def triplesimmetric_as_str(self):
    return str(self.triplesimmetric_as_int).zfill(3)

  def get_metric_datum(self):
    return self.triplesimmetric_as_int

  def put_number_as_simmetric_in_inspector_dict(self, n_src, n_trg, typsimm):
    if not self.enable_inspector:
      return
    if typsimm in self.inspector_dict:
      tuplelist = self.inspector_dict[typsimm]
      tuplelist.append((n_src, n_trg))
    else:
      tuplelist = [(n_src, n_trg)]
      self.inspector_dict[typsimm] = tuplelist

  def accumulate_tripsimm_amounts_if_any(self):
    self.m_simm_acc, self.col_simm_acc, self.row_simm_acc = 0, 0, 0
    # 1 accumatate the number_simmetric checking each number in list
    localnumberlist = list(self.numberlist)
    for i, d in enumerate(localnumberlist):
      n_simm = calc_number_simmetric_for_range_1_60(d)
      if n_simm in localnumberlist:
        self.m_simm_acc += 1
        self.put_number_as_simmetric_in_inspector_dict(d, n_simm, self.MODSIMMETRY)
        localnumberlist.remove(n_simm)
    # 2 accumatate the column_simmetric checking each number in list
    localnumberlist = list(self.numberlist)
    for i, d in enumerate(localnumberlist):
      col_simm = calc_the_columnsimmetric_from_1_to_60_along_rows_in_a_10x6matrix(d)
      if col_simm in localnumberlist:
        self.col_simm_acc += 1
        self.put_number_as_simmetric_in_inspector_dict(d, col_simm, self.COLSIMMETRY)
        localnumberlist.remove(col_simm)
    # 3 accumatate the row_simmetric checking each number in list
    localnumberlist = list(self.numberlist)
    for i, d in enumerate(localnumberlist):
      row_simm = calc_the_rowsimmetric_from_1_to_60_along_columns_in_a_10x6matrix(d)
      if row_simm in localnumberlist:
        self.row_simm_acc += 1
        self.put_number_as_simmetric_in_inspector_dict(d, row_simm, self.ROWSIMMETRY)
        localnumberlist.remove(row_simm)

  def calc_the_triplesimmetrics_from_the_accumulated_componentes(self):
    multiplicands_in_power_order = [self.row_simm_acc, self.col_simm_acc, self.m_simm_acc]
    self.triplesimmetric_as_int = compose_as_base10_a_base_b_from_ordered_multiplicands(
      multiplicands_in_power_order, base=10
    )

  def process(self):
    self.accumulate_tripsimm_amounts_if_any()
    self.calc_the_triplesimmetrics_from_the_accumulated_componentes()

  def __str__(self):
    inspector_str = 'off' if not self.enable_inspector else str(self.inspector_dict)
    outstr = f"""TripleSimmetricCalculator {self.numberlist} => tripsimm = '{self.triplesimmetric_as_str}' 
    {self.triplesimmetric_as_int} | inspector = {inspector_str}"""
    return outstr


def compose_as_base10_the_base_4_triplesimmetrics(n_simm, col_simm, row_simm):
  """
  @see also __doc__ for the next function below.
  """
  multiplicands_in_power_order = [row_simm, col_simm, n_simm]
  return compose_as_base10_a_base_b_from_ordered_multiplicands(multiplicands_in_power_order, base=4)


def compose_as_base10_a_base_b_from_ordered_multiplicands(multiplicands_in_power_order, base=4):
  """
  This function was originally written for composing the triplesimmetrics, but, later one,
    it's been decided to left it as its own base10 form.
  """
  base10_equivant = 0
  for exponent, multiplicand in enumerate(multiplicands_in_power_order):
    base10_equivant += multiplicand * base ** exponent
  return base10_equivant


def calc_number_simmetric_for_range_1_60(n):
  try:
    n = int(n)
  except (TypeError, ValueError):
    return None
  if n < 1 or n > 60:
    return None
  return calc_number_simmetric_for_range_1_m(n, upto=60)


def extract_row_n_col_tuple_from_a_10x6_dozen(dozen):
  try:
    dozen = int(dozen)
  except (TypeError, ValueError):
    return None, None
  if dozen < 1 or dozen > 60:
    return None, None
  row = math.floor((dozen-1)/10) + 1
  col = dozen % 10
  col = col if col > 0 else 10
  return row, col


def recompose_dozen_with_row_n_col_tuple_for_a_10x6_matrix_1_to_60(row, col):
  try:
    row, col = int(row), int(col)
  except (TypeError, ValueError):
    return None
  if row < 1 or row > 6 or col < 0 or col > 10:
    return None
  recomposed_dozen = (row-1) * 10 + col
  return recomposed_dozen


def calc_the_rowsimmetric_from_1_to_60_along_columns_in_a_10x6matrix(dozen):
  """
  To be row simmetric, the numbers must be in the same row
  Examples:
    row 1: 02 is row-simmetrical to 08 (viceversa 8 to 2)
    row 2: 17 is row-simmetrical to 14 (viceversa 14 to 17)
    row 3: 22 is row-simmetrical to 29 (viceversa 29 to 22)
    and so on
  """
  row, col = extract_row_n_col_tuple_from_a_10x6_dozen(dozen)
  col_of_the_row_simm = calc_the_rowsimmetric_w_column_within_1_to_10_for_a_10x6matrix(col)
  thesimm = recompose_dozen_with_row_n_col_tuple_for_a_10x6_matrix_1_to_60(row, col_of_the_row_simm)
  return thesimm


def calc_the_columnsimmetric_from_1_to_60_along_rows_in_a_10x6matrix(dozen):
  """
  To be column simmetric, the numbers must be in the same column
  Examples:
    column 1: 01 is column-simmetrical to 51 (viceversa 51 to 1)
    column 2: 22 is column-simmetrical to 32 (viceversa 32 to 22)
    column 3: 44 is column-simmetrical to 14 (viceversa 14 to 44)
    and so on
  """
  row, col = extract_row_n_col_tuple_from_a_10x6_dozen(dozen)
  row_of_the_col_simm = calc_the_columnsimmetric_w_row_within_1_to_6_for_a_10x6matrix(row)
  thesimm = recompose_dozen_with_row_n_col_tuple_for_a_10x6_matrix_1_to_60(row_of_the_col_simm, col)
  return thesimm


def calc_the_columnsimmetric_w_row_within_1_to_6_for_a_10x6matrix(n):
  """
  To be column simmetric, the numbers must be in the same column
  Examples:
    column 1: 01 is simmetrical to 51 (viceversa 51 to 1)
    column 2: 22 is simmetrical to 32 (viceversa 32 to 22)
    column 3: 44 is simmetrical to 14 (viceversa 14 to 44)
    and so on
  """
  try:
    n = int(n)
  except (TypeError, ValueError):
    return None
  if n < 1 or n > 6:
    return None
  simm = 6 + 1 - n
  return simm


def calc_the_rowsimmetric_w_column_within_1_to_10_for_a_10x6matrix(col):
  """
  To be row simmetric, the numbers must be in the same row
  Examples:
    row 1: 02 is simmetrical to 08 (viceversa 8 to 2)
    row 2: 17 is simmetrical to 14 (viceversa 14 to 17)
    row 3: 22 is simmetrical to 29 (viceversa 29 to 22)
    and so on
  """
  try:
    col = int(col)
  except (TypeError, ValueError):
    return None
  if col < 1 or col > 10:
    return None
  thesimm = 10 + 1 - col
  return thesimm


def calc_number_simmetric_for_range_1_m(n, upto=60):
  """
  Examples:
    if upto=60
      f(60) = 1 (and viceversa)
      f(31) = 30 (and viceversa)
    if upto=10
      f(10) = 1 (and viceversa)
      f(6) = 5 (and viceversa)
  """
  if n < 1 or n > upto:
    return None
  return upto + 1 - n


def list_triplesimmetrics_thru_ms_history():
  ms_asc_history_list = lh.get_ms_history_as_list_with_cardgames_in_ord_sor()
  histogram_triplestr_dict = {}
  for nconc, dozens in enumerate(ms_asc_history_list):
    trisimmobj = TripleSimmetricCalculator(dozens)  # , enable_inspector=False (the default)
    triplestr = trisimmobj.triplesimmetric_as_str
    if triplestr in histogram_triplestr_dict:
      histogram_triplestr_dict[triplestr] += 1
    else:
      histogram_triplestr_dict[triplestr] = 1
    print(nconc, dozens, triplestr, 'count up til now', histogram_triplestr_dict[triplestr])
  histogram_triplestr_dict = dict(sorted(histogram_triplestr_dict.items(), key=lambda e: e[1]))
  print('histogram_triplestr_dict', histogram_triplestr_dict)
  print('histogram size', len(histogram_triplestr_dict))


def adhoc_test():
  """

  """
  dozen = 12
  rowsimm = calc_the_rowsimmetric_from_1_to_60_along_columns_in_a_10x6matrix(dozen)
  print(dozen, 'row simm is', rowsimm)
  dozen = 14
  rowsimm = calc_the_rowsimmetric_from_1_to_60_along_columns_in_a_10x6matrix(dozen)
  print(dozen, 'row simm is', rowsimm)
  dozen = 1
  colsimm = calc_the_columnsimmetric_from_1_to_60_along_rows_in_a_10x6matrix(dozen)
  print(dozen, 'column simm is', colsimm)
  dozen = 55
  colsimm = calc_the_columnsimmetric_from_1_to_60_along_rows_in_a_10x6matrix(dozen)
  print(dozen, 'column simm is', colsimm)
  dozen = 47
  colsimm = calc_the_columnsimmetric_from_1_to_60_along_rows_in_a_10x6matrix(dozen)
  print(dozen, 'column simm is', colsimm)


def adhoc_test2():
  """
  dozens = [1, 12, 23, 34, 45, 60]
  trisimmobj = TripleSimmetricCalculator(dozens)
  print(trisimmobj)
  """
  dozens = [1, 14, 17, 34, 47, 60]
  trisimmobj = TripleSimmetricCalculator(dozens, enable_inspector=True)
  print(trisimmobj)


if __name__ == '__main__':
  """
  adhoctest()
  list_triple_even_metrics_thru_ms_history()
  """
  adhoc_test2()
