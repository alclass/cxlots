#!/usr/bin/env python3
"""
pares_dpares_n_percevensum

This metric is composed of three 'submetrics' (sm), they are:

  sm 1: number of even dozens

  sm 2: quantity of even dozen digits, ie, taken the left side digit, how many there are

  sm 2: the percentual, in two digits (rounded from 01 to 99), of the even numbers sum to the total sum

"""
import math
import commands.show.list_ms_history as lh  # lh.get_ms_history_as_list_with_cardgames_in_ord_sor


class EvenNumberTripleMetricCalculator:

  def __init__(self, intlist, listsize=6, intlist_not_repeats=True):
    self.listsize = listsize
    self.intlist_not_repeats = intlist_not_repeats
    self.intlist = intlist
    self.n_pares = None
    self.n_even_leftdigits = None
    self._tripleeven = None
    self.percent_as_int_evensum_by_total = None
    self.has_processed = False
    self.process()

  @property
  def tripleeven(self):
    if self._tripleeven is None:
      if self.has_processed:
        self._tripleeven = self.n_pares * 1000 + self.n_even_leftdigits * 100 + self.percent_as_int_evensum_by_total
    return self._tripleeven

  def get_metric_datum(self):
    return self.tripleeven

  def verify_repeats_n_raises_exception_if_any(self):
    if len(set(self.intlist)) != self.listsize:
      errmsg = (f"verify_repeats_n_raises_exception_if_any intlist {self.intlist}"
                f" has repeats or is malformed, listsize={self.listsize}.")
      raise ValueError(errmsg)

  def process(self):
    if self.intlist_not_repeats:
      self.verify_repeats_n_raises_exception_if_any()
    self.n_pares = calc_n_pares_from_intlist(self.intlist)
    self.n_even_leftdigits = calc_n_even_leftdigits_from_intlist(self.intlist)
    self.percent_as_int_evensum_by_total = calc_percentual_as_int_of_somapares_by_somatotal(self.intlist)
    self.has_processed = True

  def __str__(self):
    outstr = (f"EvenNumberTripleMetricCalculator dzs={self.intlist} tripleeven={self.tripleeven}"
              f" | pares={self.n_pares} | n_even_left_digits {self.n_even_leftdigits}"
              f" | percent = {self.percent_as_int_evensum_by_total}")
    return outstr


def calc_percentual_as_int_of_somapares_by_somatotal(intlist):
  try:
    total_all_ints = sum(intlist)
    even_number_list = list(filter(lambda e: e % 2 == 0, intlist))
    total_even_ints = sum(even_number_list)
    percent_as_int = int(round(100*total_even_ints/total_all_ints, 0))
    return percent_as_int
  except (TypeError, ValueError):
    pass
  return None


def calc_percentual_as_int_of_somapares_by_somatotal_w_size(intlist, listsize=6):
  try:
    if len(intlist) != listsize:
      return None
    return calc_percentual_as_int_of_somapares_by_somatotal(intlist)
  except TypeError:
    pass
  return None


def calc_n_even_leftdigits_from_intlist(intlist):
  try:
    leftdigits_list = list(map(lambda e: int(math.floor(e / 10)), intlist))
    # do not call the 'unique' version, for the left digits may indeed be the same
    return calc_n_pares_from_intlist(leftdigits_list)
  except (TypeError, ValueError):
    pass
  return None


def calc_n_even_leftdigits_from_intlist_w_size(intlist, listsize=6):
  try:
    if len(intlist) != listsize:
      return None
    return calc_n_even_leftdigits_from_intlist(intlist)
  except TypeError:
    pass
  return None


def calc_n_pares_from_intlist(intlist):
  try:
    n_pares = len(list(filter(lambda e: e % 2 == 0, intlist)))
    return n_pares
  except (TypeError, ValueError):
    pass
  return None


def calc_n_pares_from_intlist_w_size(intlist, listsize=6):
  try:
    if len(intlist) != listsize:
      return None
    return calc_n_pares_from_intlist(intlist)
  except TypeError:
    pass
  return None


def calc_n_pares_from_intlist_w_size_n_unique(intlist, listsize=6):
  try:
    intlist = list(set(intlist))
    return calc_n_pares_from_intlist_w_size(intlist, listsize)
  except TypeError:
    pass
  return None


def list_triple_even_metrics_thru_ms_history():
  ms_asc_history_list = lh.get_ms_history_as_list_with_cardgames_in_ord_sor()
  histogram_tripleeven_dict = {}
  for nconc, dozens in enumerate(ms_asc_history_list):
    triple_even_obj = EvenNumberTripleMetricCalculator(dozens)  # , enable_inspector=False (the default)
    tripleeven = triple_even_obj.tripleeven
    if tripleeven in histogram_tripleeven_dict:
      histogram_tripleeven_dict[tripleeven] += 1
    else:
      histogram_tripleeven_dict[tripleeven] = 1
    print(nconc, dozens, tripleeven, 'count up til now', histogram_tripleeven_dict[tripleeven])
  histogram_tripleeven_dict = dict(sorted(histogram_tripleeven_dict.items(), key=lambda e: e[1]))
  print('histogram_tripleeven_dict', histogram_tripleeven_dict)
  print('histogram size', len(histogram_tripleeven_dict))


def adhoctest():
  intlist = [1, 2, 3, 4, 5, 6]
  n_pares = calc_n_pares_from_intlist_w_size_n_unique(intlist, 6)
  scrmsg = f'n_pares from {intlist} is {n_pares}'
  print(scrmsg)
  intlist = [11, 12, 13, 14, 15, 17]
  n_pares = calc_n_pares_from_intlist_w_size_n_unique(intlist)
  scrmsg = f'n_pares from {intlist} is {n_pares}'
  print(scrmsg)
  n_pares = calc_n_even_leftdigits_from_intlist_w_size(intlist)
  scrmsg = f'n_pares leftdigit from {intlist} is {n_pares}'
  print(scrmsg)
  intpercent = calc_percentual_as_int_of_somapares_by_somatotal_w_size(intlist)
  scrmsg = f'intpercent even by total from {intlist} is {intpercent}'
  print(scrmsg)


def adhoctest2():
  intlist = [1, 3, 41, 42, 44, 54]
  obj = EvenNumberTripleMetricCalculator(intlist)
  print(obj)


def process():
  pass


if __name__ == '__main__':
  """
  adhoctest()
  process()
  list_triple_even_metrics_thru_ms_history()
  """
  adhoctest2()
