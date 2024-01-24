#!/usr/bin/env python3
"""
fs/mathfs/metrics/immed_repeats_freqs_histograms.py
  Contains class ImmediateRepeatsCounter that produces an
  array with the conc-depth
"""
import commands.show.list_ms_history as lh  # lh.MSHistorySlider
N_DOZENS_IN_CARDGAME = 6
MAX_DIGITS_IMMED_REPEATS = 2
DIVIDER_FOR_IMMED_REPEATS = 10 ** MAX_DIGITS_IMMED_REPEATS


class ImmediateRepeatsCounter:
  """
  This metric is a "history" metric, ie, it depends on the historical values.

  In this system, most metrics do not depend on history, as this one does,
    this class depends on the existence of a database available.

  Example 'metric': 411530722, ie
    4115 => the maxacertos 4, up to depth 600, at depth 115
    405 => the maxacertos 3, up to 20 depth 60, happening at depth 7 (07)
    22 => the maxacertos 2, up to 2 depth 6, happening at depth 2
  """

  def __init__(self, nconc=None, ms_history_slider=None):
    self.nconc = nconc
    self.hist_slider = ms_history_slider
    self.treat_nconc_n_history_or_default()
    self._curr_intlist_sor_ord = None
    self.repeat_depth_list = []  # it's assumed that cardgame is in sor ord
    self._repeat_depth_str = None
    self._repeat_depth_int = None
    self.has_been_processed = False
    self.process()

  def treat_nconc_n_history_or_default(self):
    """
    Notice hist_slider depends on lh.MSHistorySlider()
      being able to supply the specific data from the database.

    At the time of writing, this piece does not raise an exception
      in case hist_slider is unable to supply data.
    """
    if self.hist_slider is None:
      self.hist_slider = lh.MSHistorySlider()
    if self.nconc is None:
      self.nconc = self.hist_slider.get_most_recent_nconc()

  @property
  def current_intlist_in_sor_ord(self):
    if self._curr_intlist_sor_ord is None:
      self._curr_intlist_sor_ord = self.hist_slider.get_in_sor_ord(self.nconc)
    return self._curr_intlist_sor_ord

  @property
  def current_intlist_in_asc_ord(self):
    if self._curr_intlist_sor_ord is None:
      self._curr_intlist_sor_ord = sorted(self.current_intlist_in_sor_ord)
    return self._curr_intlist_sor_ord

  @property
  def repeat_depth_int(self):
    if self._repeat_depth_int is None:
      if not self.has_been_processed:
        self.process()
      reversedlist = list(reversed(self.repeat_depth_list))
      summing_seq = [n * 10 ** (2*i+1) for i, n in enumerate(reversedlist)]
      # adjust the last position dividing the sum by 10
      # this is needed, because the last postision was multiplied by 10**1 (instead of 10**0)
      self._repeat_depth_int = sum(summing_seq) // 10

    return self._repeat_depth_int

  @property
  def repeat_depth_str(self):
    """
    This property (repeat_depth_str) is not derived directly from repeat_depth_int.
      both are derived from repeat_depth_list.

    There is one particular different between the two
      when the first repeat amount is less than 10. This will be noted below.

    IMPORTANT: it's (strongly) supposed that a repeat amount is
               never greater than 99.

    Suppose, as a hypothesis, such a repeat list: [4, 5, 7, 9, 10, 19]
    In fact, we are only concerned about the first amount being less than 10.
      Its repeat_depth_int is 40507091019
      However, its str counterpart is 040507091019
    ie, in this case, repeat_depth_str has a leading 0 (zero) that repeat_depth_int does not.
    """
    if self._repeat_depth_str is None:
      if not self.has_been_processed:
        self.process()
      self._repeat_depth_str = ''
      for repeat_amount in self.repeat_depth_list:
        amount_str = str(repeat_amount)
        amount_str = '0' + amount_str if len(amount_str) < 2 else amount_str
        self._repeat_depth_str += amount_str
    return self._repeat_depth_str

  def get_metric_datum(self):
    return self.repeat_depth_int

  def dive_deep_until_all_found(self):
    downgoing_nconc = self.nconc - 1
    # list is necessary, for it will be deleted one by one and original is a tuple
    curr_intlist_sor_ord = list(self.current_intlist_in_sor_ord)
    while downgoing_nconc > 0:
      if len(curr_intlist_sor_ord) == 0:
        break
      for d in curr_intlist_sor_ord:
        past_intlist = self.hist_slider.get(downgoing_nconc)
        if d in past_intlist:
          depth = self.nconc - downgoing_nconc
          self.repeat_depth_list.append(depth)
          curr_intlist_sor_ord.remove(d)
      downgoing_nconc -= 1

  def process(self):
    self.dive_deep_until_all_found()
    self.has_been_processed = True

  def __str__(self):
    outstr = (f"Immediate Repeats {self.nconc} | {self.current_intlist_in_sor_ord} |"
              f" repeatpatt={self.get_metric_datum()} | "
              f"{self.repeat_depth_list} | {self.repeat_depth_str}")
    return outstr


def recover_immed_repeats_from_intpatt(intpatt, immed_repeats=None):
  """
  Decomposes the n parcels of the immediate repeats of a cardgame
    (n-sized array)
  Obs:
    1) this function is recursive;
    2) it divides up the original intval by the power of ten built-in in
       the orginal composition summation, stores the remainder
       and recurse sending on the quotient and the results list.
  ANALOGY:
    this function is a number-system decomposer applied to the case
      here where composition is based by powers of 10 incremented by 2 at a time:
      ie 10**2, 10**4, ... up to 10**12
  Args:
    intpatt: the integer pattern composed of the immediate repeats
    immed_repeats: the list with the decomposed parcels from intpatt
  Returns: the list immed_repeats completed at the end of recursion

  """
  immed_repeats = [] if immed_repeats is None else immed_repeats
  quotient = intpatt // DIVIDER_FOR_IMMED_REPEATS
  remainder = intpatt % DIVIDER_FOR_IMMED_REPEATS
  immed_repeats.append(remainder)
  if quotient == 0:
    # decomposition has ended, return without recursing
    return list(reversed(immed_repeats))
  return recover_immed_repeats_from_intpatt(quotient, immed_repeats)


def adhoctest():
  pass


def process():
  repeatcounter = ImmediateRepeatsCounter()
  print(repeatcounter)
  repeats_int = 40507091019
  recovered_list = recover_immed_repeats_from_intpatt(repeats_int)
  print(repeats_int, 'recovered_list', recovered_list)


if __name__ == '__main__':
  """
  adhoctest2()
  """
  process()
  adhoctest()
