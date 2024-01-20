"""
  The triplesimmetrics is an INT has contains 3 numbers
    n1 the first, if it exists, is the row simmetric (or the amount of dozens that are row simmetric)
    n2 the second, if it exists, is the column simmetric (idem)
    n3 the third, if it exists, is the arithmetic simmetric (idem)
    Examples:
        if 01 & 10 happened, it counts 1 row simmetric and also as arithmetic simmetric
        if 01 & 51 happened, it counts 1 column simmetric

    Now, suppose a drawn game is (01, 02, 09, 10, 51, 56)
      There are:
        01 <=> 10 row simmetric
        02 <=> 09 row simmetric
        01 <=> 51 column simmetric
        01 <=> 10 arithmetic simmetric
      Adding up, the triplesimmetry is '121'
"""
import fs.mathfs.metrics.museum.idxshapearea_circle_metric as cm  # .get_col_n_row_1indices_from_dozensarray


def is_pair_column_simmetric(d1, d2, simmsoma=11):
  """
  1 simm 10 | 2 simm 9 | 3 simm 8 | 4 simm 7 |  4 simm 6
  Example: d1=1, d2=10 (both are at row 1 and 1 is column-mirrored, so to say, at 10)
  """
  rid1, cid1 = cm.extract_as_tupl_col1idx_n_row1idx_from_carddozen(d1)
  rid2, cid2 = cm.extract_as_tupl_col1idx_n_row1idx_from_carddozen(d2)
  # both dozens should be at the row
  if rid1 != rid2:
    return False
  if cid1 + cid2 == simmsoma:
    return True
  return False


def is_pair_row_simmetric(d1, d2, simmsoma=7):
  """
  1 simm 6 | 2 simm 5 | 3 simm 4
  Example: d1=1, d2=51 (both are at column 1 and 1 is row-mirrored, so to say, at 51
  """

  rid1, cid1 = cm.extract_as_tupl_col1idx_n_row1idx_from_carddozen(d1)
  rid2, cid2 = cm.extract_as_tupl_col1idx_n_row1idx_from_carddozen(d2)
  # both dozens should be at the column
  if cid1 != cid2:
    return False
  if rid1 + rid2 == simmsoma:
    return True
  return False


def is_pair_arit_simmetric(d1, d2, zfill=2):
  """
  Examples:
    01 <=> 10
    14 <=> 41
    09 <=> None (because there's no 90)
  """
  strd1 = str(d1).zfill(zfill)
  strd2 = str(d2).zfill(zfill)
  rev_str2 = ''.join(reversed(strd2))
  if strd1 == rev_str2:
    return True
  return False


class Simmetrics:

  COLUMN_SIMMSOMA = 11
  ROW_SIMMSOMA = 7
  ZFILL = 2

  def __init__(self, d1, d2):
    self.d1 = d1
    self.d2 = d2
    self.rid1, self.cid1 = cm.extract_as_tupl_col1idx_n_row1idx_from_carddozen(self.d1)
    self.rid2, self.cid2 = cm.extract_as_tupl_col1idx_n_row1idx_from_carddozen(self.d2)

  def is_pair_row_simmetric(self):
    if self.rid1 != self.rid2:
      return False
    if self.cid1 + self.cid2 == self.ROW_SIMMSOMA:
      return True
    return False

  def is_pair_column_simmetric(self):
    if self.rid1 != self.rid2:
      return False
    if self.cid1 + self.cid2 == self.COLUMN_SIMMSOMA:
      return True
    return False

  def is_pair_arit_simmetric(self):
    return is_pair_arit_simmetric(self.d1, self.d2, self.ZFILL)


def count_row_simmetrics(cardarray):
  """
    Now, suppose a drawn game is (01, 02, 09, 10, 51, 56)
      There appeared a second count for row simmetric
      Altogether, the foursimmetrics is '211'
  """
  ca = cardarray
  rowsimm, colsimm, aritsimm = 0, 0, 0
  for i in range(len(ca)-1):
    for j in range(i+1, len(ca)):
      if is_pair_row_simmetric(ca[i], ca[j]):
        rowsimm += 1
      if is_pair_column_simmetric(ca[i], ca[j]):
        colsimm += 1
      if is_pair_arit_simmetric(ca[i], ca[j]):
        aritsimm += 1
  totalindex = rowsimm*10**2 + colsimm*10**1 + aritsimm
  return totalindex


def combine_all_shapes():
  """
  combine_all_shapes()
  """
  pass


def adhoctest():
  """
  """
  d1, d2 = 1, 51
  boolval = is_pair_row_simmetric(d1, d2)
  print(d1, d2, 'is row simm', boolval)
  boolval = is_pair_column_simmetric(d1, d2)
  print(d1, d2, 'is col simm', boolval)
  d1, d2 = 1, 10
  boolval = is_pair_row_simmetric(d1, d2)
  print(d1, d2, 'is row simm', boolval)
  boolval = is_pair_column_simmetric(d1, d2)
  print(d1, d2, 'is col simm', boolval)
  dezenas = (1, 2, 9, 10, 51, 56)
  simm = count_row_simmetrics(dezenas)
  print(dezenas, 'simm', simm)


def process():
  pass


if __name__ == '__main__':
  adhoctest()
  process()
