#!/usr/bin/env python3
"""
This module contains calculation for the following metrics:

    completed m1 soma INT,
    completed m2 media_mult100 INT,
    completed m3 dsvpdr_mult100 INT,
    completed m4 n_consecutivos INT,
    completed m5 n_8_adjacent INT,
    completed m6 n_immed_repeats INT,
    completed m7 up_same_down_seq INT,
    completed m8 remainder5patt INT,
    completed m9 resto12patt_b12_to_b10 INT,
    completed m10 quadrantpatt INT,

"""
import copy
import statistics as sta
import fs.mathfs.metrics.distance_xs_ys_sums_metric as ds  # ds.extract_xcol_yrow_from_dozen_intval_10columns
import commands.show.list_ms_history as lh  # lh.get_ms_history_as_list_with_cardgames_in_ord_sor


class EightAdjacentSurroundingNumberFinder:
  """
  This class calculates and stores the surrounding integers of a specific value in a cardmatrix.

    Example:
      intval=35 is surrounded, in a 10x6 cardmatrix, by:
        {'east': 36, 'west': 34, 'south': 45, 'north': 25,
         'southeast': 46, 'southwest': 44, 'northeast': 26, 'northwest': 24}

  Metric Implemented
  ==================

  The metric that is implemented sideways to its main functionality described above
    is called the 'n_8_adjacent'. This metric tells how many items in a
      comparing set are surrounding ones.

    Example:
      suppose cardgame = [1, 5, 7, 35, 36, 37]
    One has seen above thet 35, 36 & 37 are interrelated as surrounding items.
      (If 36 surrounds 35, also 35 surrounds 36, it's a bijection relation.)
    So let's do it by parts.
      p1 Dozens 1, 5 & 7 are not surrounding-related.
      p2 Dozens 35, 36 & 37 are related, but the relation is the following:
        36 surrounds 35 => it counts one surrounding, not two
        37 surrounds 36 => again, it counts one surrounding, not two
    Thus, the result is cardgame = [1, 5, 7, 35, 36, 37] has n_8_adjacent = 2.
  """

  def __init__(self, intval, maxcol=10, maxrow=6):
    self.intval = intval
    self._col, self._row = None, None
    self.maxcol, self.maxrow = maxcol, maxrow
    self._surrounding_ints = None
    self._surrounding_dict = None
    self._east, self._west, self._south, self._north = None, None, None, None
    self._southeast, self._southwest, self._northeast, self._northwest = None, None, None, None

  @property
  def surrounding_ints(self):
    if self._surrounding_ints is None:
      self._surrounding_ints = sorted(self.surrounding_dict.values())
    return self._surrounding_ints

  @property
  def surrounding_dict(self):
    if self._surrounding_dict is None:
      self.process()
    return self._surrounding_dict

  @property
  def col(self):
    if self._col is None:
      self._col, self._row = ds.extract_xcol_yrow_from_dozen_intval_10columns(self.intval)
    return self._col

  @property
  def row(self):
    if self._row is None:
      self._col, self._row = ds.extract_xcol_yrow_from_dozen_intval_10columns(self.intval)
    return self._row

  @property
  def east(self):
    if self._east is None:
      self.process()
    return self._east

  @property
  def west(self):
    if self._west is None:
      self.process()
    return self._west

  @property
  def south(self):
    if self._south is None:
      self.process()
    return self._south

  @property
  def north(self):
    if self._north is None:
      self.process()
    return self._north

  @property
  def southeast(self):
    if self._southeast is None:
      self.process()
    return self._southeast

  @property
  def southwest(self):
    if self._southwest is None:
      self.process()
    return self._southwest

  @property
  def northeast(self):
    if self._northeast is None:
      self.process()
    return self._northeast

  @property
  def northwest(self):
    if self._northwest is None:
      self.process()
    return self._northwest

  def get_int_by_moving_unit_eastward(self):
    newcol = self.col + 1
    newcol = newcol if newcol <= self.maxcol else newcol - self.maxcol
    newrow = self.row
    # recompose moved int by its coordinates
    moved_intval = ds.recompose_dozen_from_xcol_yrow_10columns(newcol, newrow)
    return moved_intval

  def get_int_by_moving_unit_westward(self):
    newcol = self.col - 1
    newcol = newcol if newcol > 0 else self.maxcol - newcol
    newrow = self.row
    # recompose moved int by its coordinates
    moved_intval = ds.recompose_dozen_from_xcol_yrow_10columns(newcol, newrow)
    return moved_intval

  def get_int_by_moving_unit_southward(self):
    newcol = self.col
    newrow = self.row + 1
    newrow = newrow if newrow <= self.maxrow else newrow - self.maxrow
    # recompose moved int by its coordinates
    moved_intval = ds.recompose_dozen_from_xcol_yrow_10columns(newcol, newrow)
    return moved_intval

  def get_int_by_moving_unit_northward(self):
    newcol = self.col
    newrow = self.row - 1
    newrow = newrow if newrow > 0 else self.maxrow - newrow
    # recompose moved int by its coordinates
    moved_intval = ds.recompose_dozen_from_xcol_yrow_10columns(newcol, newrow)
    return moved_intval

  def get_int_by_moving_unit_southeastward(self):
    newcol = self.col + 1
    newcol = newcol if newcol <= self.maxcol else newcol - self.maxcol
    newrow = self.row + 1
    newrow = newrow if newrow <= self.maxrow else newrow - self.maxrow
    # recompose moved int by its coordinates
    moved_intval = ds.recompose_dozen_from_xcol_yrow_10columns(newcol, newrow)
    return moved_intval

  def get_int_by_moving_unit_southwestward(self):
    newcol = self.col - 1
    newcol = newcol if newcol > 0 else self.maxcol - newcol
    newrow = self.row + 1
    newrow = newrow if newrow <= self.maxrow else newrow - self.maxrow
    # recompose moved int by its coordinates
    moved_intval = ds.recompose_dozen_from_xcol_yrow_10columns(newcol, newrow)
    return moved_intval

  def get_int_by_moving_unit_northeastward(self):
    newcol = self.col + 1
    newcol = newcol if newcol <= self.maxcol else newcol - self.maxcol
    newrow = self.row - 1
    newrow = newrow if newrow > 0 else self.maxrow - newrow
    # recompose moved int by its coordinates
    moved_intval = ds.recompose_dozen_from_xcol_yrow_10columns(newcol, newrow)
    return moved_intval

  def get_int_by_moving_unit_northwestward(self):
    newcol = self.col - 1
    newcol = newcol if newcol > 0 else self.maxcol - newcol
    newrow = self.row - 1
    newrow = newrow if newrow > 0 else self.maxrow - newrow
    # recompose moved int by its coordinates
    moved_intval = ds.recompose_dozen_from_xcol_yrow_10columns(newcol, newrow)
    return moved_intval

  def gather_the_8_surrounding_ints(self):
    self._surrounding_dict = {}
    # 1
    self._east = self.get_int_by_moving_unit_eastward()
    self._surrounding_dict['east'] = self._east
    # 2
    self._west = self.get_int_by_moving_unit_westward()
    self._surrounding_dict['west'] = self._west
    # 3
    self._south = self.get_int_by_moving_unit_southward()
    self._surrounding_dict['south'] = self._south
    # 4
    self._north = self.get_int_by_moving_unit_northward()
    self._surrounding_dict['north'] = self._north
    # 5
    self._southeast = self.get_int_by_moving_unit_southeastward()
    self._surrounding_dict['southeast'] = self._southeast
    # 6
    self._southwest = self.get_int_by_moving_unit_southwestward()
    self._surrounding_dict['southwest'] = self._southwest
    # 7
    self._northeast = self.get_int_by_moving_unit_northeastward()
    self._surrounding_dict['northeast'] = self._northeast
    # 8
    self._northwest = self.get_int_by_moving_unit_northwestward()
    self._surrounding_dict['northwest'] = self._northwest

  def process(self):
    self.gather_the_8_surrounding_ints()

  def __str__(self):
    outstr = f"""intval={self.intval} surrounding_ints={self.surrounding_ints}
    {self.surrounding_dict}"""
    return outstr


def calc_soma_from_intlist_or_none(intlist):
  try:
    return sum(intlist)
  except (TypeError, ValueError):
    pass
  return None


def calc_mediamult100_from_intlist_or_none(intlist):
  try:
    afloat = sta.mean(intlist)
    return int(round(afloat*100, 0))
  except (TypeError, ValueError):
    pass
  return None


def calc_desviopadraomult100_from_intlist_none(intlist):
  try:
    afloat = sta.stdev(intlist)
    return int(round(afloat*100, 0))
  except (TypeError, ValueError):
    pass
  return None


class UpSameDownFromIntlistDeriver:

  NEXT_MOVE_DOWN, NEXT_MOVE_SAME, NEXT_MOVE_UP = 0, 1, 2

  def __init__(self, intlist):
    self.sor_ord_intlist = intlist
    self.treat_n_asc_ord_intlist()
    self.up_same_down_array = []
    self._up_same_down_int = None
    self.has_been_processed = False
    self.process()

  def treat_n_asc_ord_intlist(self):
    """
    Obs: the guarantee that the order of intlist is the one original should
      be taken by the caller.
    """
    try:
      self.sor_ord_intlist = list(self.sor_ord_intlist)
    except (TypeError, ValueError):
      errmsg = f'intlist {self.sor_ord_intlist} for DownSameUpFromIntlistDeriver is not valid.'
      raise ValueError(errmsg)

  @property
  def up_same_down_str(self):
    zfillsize = len(self.sor_ord_intlist)
    _upsamedown_str = str(self.up_same_down_int).zfill(zfillsize)
    return _upsamedown_str

  @property
  def up_same_down_int(self):
    if self._up_same_down_int is None:
      if not self.has_been_processed:
        self.process()
      upsamedown_str = ''.join(map(str, self.up_same_down_array))
      self._up_same_down_int = int(upsamedown_str)
    return self._up_same_down_int

  def get_metric_datum(self):
    return self.up_same_down_int

  def derive_n_set_upsamedown_array_from_asc_ord_intlist_none(self):
    """
    ord_sor means "in the order of drawing"
    This function guarantees int's are ordered by sorted()
    """
    for left_i in range(len(self.sor_ord_intlist)):
      right_i = left_i + 1
      if right_i == len(self.sor_ord_intlist):
        right_i = 0
      if self.sor_ord_intlist[left_i] > self.sor_ord_intlist[right_i]:
        self.up_same_down_array.append(self.NEXT_MOVE_DOWN)
      elif self.sor_ord_intlist[left_i] == self.sor_ord_intlist[right_i]:
        self.up_same_down_array.append(self.NEXT_MOVE_SAME)
      else:  # ie, ord_sor_intlist[left_i] < ord_sor_intlist[right_i]
        self.up_same_down_array.append(self.NEXT_MOVE_UP)
    return

  def process(self):
    self.derive_n_set_upsamedown_array_from_asc_ord_intlist_none()
    self.has_been_processed = True

  def __str__(self):
    outstr = f'DownSameUpFromIntlistDeriver f{self.sor_ord_intlist} metric={self.get_metric_datum()}'
    return outstr


def one():
  """
    n_8_adjacent INT,
    n_immed_repeats INT,
    down_same_up_array INT,
    remainder5patt INT,
    resto12patt_b12_to_b10 INT,
    quadrantpatt INT,
  """
  pass


def calc_n_consecutivos(ord_sor_intlist):
  try:
    ord_sor_intlist = sorted(ord_sor_intlist)
  except (TypeError, ValueError):
    return None
  n_consecutivos = 0
  for left_i in range(len(ord_sor_intlist)):
    right_i = left_i + 1
    if right_i == len(ord_sor_intlist):
      break
    if ord_sor_intlist[left_i] + 1 == ord_sor_intlist[right_i]:
      n_consecutivos += 1
  return n_consecutivos


class EightAdjacentFromIntListCalculator:

  def __init__(self, intlist, maxcol=10, maxrow=6):
    self.intlist = intlist
    self.treat_intlist()
    self._n_8_adjacent = None
    self.maxcol, self.maxrow = maxcol, maxrow

  def treat_intlist(self):
    try:
      self.intlist = list(self.intlist)
    except (TypeError, ValueError):
      errmsg = (f'intlist={self.intlist} should be a list with integers with'
                f' maxcol={self.maxcol} and maxrow={self.maxrow}')
      raise ValueError(errmsg)

  @property
  def n_8_adjacent(self):
    if self._n_8_adjacent is None:
      self.process()
    return self._n_8_adjacent

  def calc_n_set_metric_8_adjacent(self):
    self._n_8_adjacent = 0
    for i in range(len(self.intlist)-1):
      for j in range(i+1, len(self.intlist)):
        doz1 = self.intlist[i]
        doz2 = self.intlist[j]
        eas = EightAdjacentSurroundingNumberFinder(doz1)
        if doz2 in eas.surrounding_ints:
          self._n_8_adjacent += 1

  def get_metric_datum(self):
    return self.n_8_adjacent

  def process(self):
    self.calc_n_set_metric_8_adjacent()

  def __str__(self):
    return f'intlist={self.intlist} | n_8_adjacent={self.n_8_adjacent}'


def calc_immed_repeats_w_intlist():
  """
    (depends on history) m6 n_immed_repeats INT,
  """
  pass


def calc_resto5patt_from_intlist(intlist):
  r5_patt_str = ''
  for d in intlist:
    remainder = d % 5
    r5_patt_str += str(remainder)
  resto5_seq_as_int = int(r5_patt_str)
  return resto5_seq_as_int


def calc_quadrantpattern_from_intlist_n_maxcol_maxrow(intlist, maxcol=10, maxrow=6):
  col_mid_to_left = maxcol // 2
  row_mid_to_up = maxrow // 2
  quadrant_list = []
  for d in intlist:
    xcol, yrow = ds.extract_xcol_yrow_from_dozen_intval(d, maxcol)
    if xcol <= col_mid_to_left:
      if yrow <= row_mid_to_up:
        quadrant = 1
      else:
        quadrant = 3
    else:
      if yrow <= row_mid_to_up:
        quadrant = 2
      else:
        quadrant = 4
    quadrant_list.append(quadrant)
  quadrant_str = ''.join(map(str, quadrant_list))
  return quadrant_str


def calc_resto12patt_as_a_base10int_from_intlist(intlist):
  """

  """
  intlist = sorted(intlist)
  remainders_list = []
  soma_as_resto12_patt = 0
  exponent = 0
  for d in intlist:
    remainder = d % 12
    remainders_list.append(remainder)
    soma_as_resto12_patt += remainder * 12 ** exponent
    exponent += 1
  return soma_as_resto12_patt


def recover_remainders12_from_its_base10int(intval, remainders=None):
  remainders = [] if remainders is None else remainders
  divided = intval // 12
  remainder = intval % 12
  remainders.append(remainder)
  if divided == 0:
    return remainders
  return recover_remainders12_from_its_base10int(divided, remainders)


def list_metrics_soma_media_dp_consec_etc_thru_ms_history(nrecords=5):
  """
    m1 soma INT,
    m2 media_mult100 INT,
    m3 dsvpdr_mult100 INT,
    m4 n_consecutivos INT,
    m5 n_8_adjacent INT,
    (depends on history) m6 n_immed_repeats INT,
    m7 up_same_down_seq INT,
    m8 remainder5patt INT,
    m9 resto12patt_b12_to_b10 INT,
    m10 quadrantpatt INT,
  """
  ms_asc_history_list = lh.get_ms_history_as_list_with_cardgames_in_ord_sor()
  downto = len(ms_asc_history_list) - nrecords
  for i in range(len(ms_asc_history_list)-1, downto, -1):
    nconc = i + 1
    dozens = ms_asc_history_list[i]
    dozen_ord_sor = copy.copy(dozens)
    soma = calc_soma_from_intlist_or_none(dozens)
    med100 = calc_mediamult100_from_intlist_or_none(dozens)
    dp100 = calc_desviopadraomult100_from_intlist_none(dozens)
    consec = calc_n_consecutivos(dozens)
    eac = EightAdjacentFromIntListCalculator(dozens)
    n_8_adjacent = eac.get_metric_datum()
    upsamedown = UpSameDownFromIntlistDeriver(dozen_ord_sor)
    upsamedown_seq = upsamedown.get_metric_datum()
    upsamedown_str = upsamedown.up_same_down_str
    dozens = sorted(dozens)
    r5patt = calc_resto5patt_from_intlist(dozens)
    r12patt = calc_resto12patt_as_a_base10int_from_intlist(dozens)
    quad = calc_quadrantpattern_from_intlist_n_maxcol_maxrow(dozen_ord_sor)
    scrmsg = (
      f"nconc={nconc} | {dozen_ord_sor} | s={soma} | md={med100} | dp={dp100}"
      f" | consec={consec} | 8_adj={n_8_adjacent} | up0down={upsamedown_seq}"
      f" {upsamedown_str} | r5={r5patt} | r12={r12patt} | quad={quad}"
    )
    print(scrmsg)


def adhoctest():
  dozens = [1, 23, 15, 28, 34, 60]
  soma = calc_soma_from_intlist_or_none(dozens)
  print(dozens, 'soma', soma)
  media = calc_mediamult100_from_intlist_or_none(dozens)
  print(dozens, 'media', media)
  dsvpdr = calc_desviopadraomult100_from_intlist_none(dozens)
  print(dozens, 'desvio padrão', dsvpdr)
  upsamedown = UpSameDownFromIntlistDeriver(dozens)
  print(upsamedown)
  dozens = [1, 5, 7, 35, 36, 37]
  eight_adj = EightAdjacentFromIntListCalculator(dozens)
  print(dozens, eight_adj)
  resto12int = calc_resto12patt_as_a_base10int_from_intlist(dozens)
  print(dozens, 'resto12', resto12int)
  remainders = recover_remainders12_from_its_base10int(resto12int)
  print('resto12', resto12int, 'remainders', remainders)


def adhoctest2():
  dozen = 35
  expected_surrounding_dict = {
    'east': 36, 'west': 34, 'south': 45, 'north': 25,
    'southeast': 46, 'southwest': 44, 'northeast': 26, 'northwest': 24,
  }
  surround_finder = EightAdjacentSurroundingNumberFinder(dozen)
  returned_surrounding_dict = surround_finder.surrounding_dict
  print('expected', expected_surrounding_dict)
  print('returned', returned_surrounding_dict)
  print(surround_finder)


def adhoctest3():
  intlist = [40, 10, 13, 20, 56, 43]
  quad = calc_quadrantpattern_from_intlist_n_maxcol_maxrow(intlist)
  print(intlist, 'quad', quad)


if __name__ == '__main__':
  """
  adhoctest2()
  adhoctest()
  list_metrics_soma_media_dp_consec_etc_thru_ms_history()
  """
  adhoctest3()
  list_metrics_soma_media_dp_consec_etc_thru_ms_history()
