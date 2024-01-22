#!/usr/bin/env python3
"""
fs/mathfs/metrics/max_acertos_backward.py
  Contains the max_acertos_backward metric.

This metric looks for max_acertos down to a certain backward depth of cardgames, ie
  every cardgame looks up n past cardgames.

Similar to other metrics (e.g. tripleeven or triplesimm), this one is also a triple.

  Obs: original depths of 50, 100, 200 were changed to 6, 60, 600

The six coordinates (submetrics sm) are:
  sm1 looks for max_acertos down to a max cardgames backward depth of 600,
  sm2 the first depth, within 600, to maxacertos above, having 3 digits
  sm3 looks for max_acertos down to a max cardgames backward depth of 60,
  sm4 the first depth, within 60, to maxacertos above, having 2 digits
  sm5 looks for max_acertos down to a max cardgames backward depth of 6
  sm6 the first depth, within 6, to maxacertos above, having 1 digits

Example 'metric': 411530722, ie
====================================
    4115 => the maxacertos 4, up to depth 600, at depth 115
    405 => the maxacertos 3, up to 20 depth 60, happening at depth 7 (07)
    22 => the maxacertos 2, up to 2 depth 6, happening at depth 2

Motivation for the triple 6, 60, 600
====================================
The choice was due to an empirical observation that showed,
  at this 'spreading', each maxacerto, for a higher depth,
  was probably greater than its counterpart for a lower depth.

This metrics starts at conc=601, so it does not exist for the first 600 concs.
(At the time of this writing, nconc = 2764.)


"""
import math
import commands.show.list_ms_history as lh  # lh.get_ms_history_as_list_with_cardgames_in_ord_sor
LAST_DOWNWARD_LIMIT_600 = 600


class TripleBackwardMaxAcertos:
  """
  Example 'metric': 411530722, ie
    4115 => the maxacertos 4, up to depth 600, at depth 115
    405 => the maxacertos 3, up to 20 depth 60, happening at depth 7 (07)
    22 => the maxacertos 2, up to 2 depth 6, happening at depth 2
  """

  BACKWARD_DEPTH_CONC_SIZES = [6, 60, LAST_DOWNWARD_LIMIT_600]

  def __init__(self, nconc, ms_asc_history_list):
    self.nconc = nconc
    self._ordered_intlist = None
    self._triplemaxacertos = None
    self.maxacertos_dict = {}  # key is depth, value is tuple with maxacertos and depth_to_it
    self.ms_asc_history_list = ms_asc_history_list
    self.has_been_process = False
    self.process()

  @property
  def intlist(self):
    if self._ordered_intlist is None:
      idx = self.nconc - 1
      self._ordered_intlist = sorted(self.ms_asc_history_list[idx])
    return self._ordered_intlist

  @property
  def maxacertos_50bw(self):
    return self.maxacertos_dict[50]

  @property
  def maxacertos_100bw(self):
    return self.maxacertos_dict[100]

  @property
  def maxacertos_200bw(self):
    return self.maxacertos_dict[200]

  @property
  def triplemaxacertos_int(self):
    """
    To facilitate its formation, we've used str instead of power summation,
      ie s = n1*10**pos1 + n2*10**pos2 + ... + nN
    The string takes care of the positioning, ie:
      = max_acertos for 200bw + its_ocorrence_depth (zfill=3) : a 4-digit chunk
      = max_acertos for 20bw + its_ocorrence_depth (zfill=2) : a 3-digit chunk
      + max_acertos for 2bw + its_ocorrence_depth (zfill=1) : a 2-digit chunk
      Obs: zfill (1, 2 or 3) is controlled by log10 of depth
    A 9-digit metric
    @see also above (docstring for the module) for an example.
    """
    tmpstr = ''
    if self._triplemaxacertos is None:
      if self.has_been_process:
        for depth in reversed(self.BACKWARD_DEPTH_CONC_SIZES):
          quant, at_depth = self.maxacertos_dict[depth]
          zfill = int(math.ceil(math.log10(depth)))
          tmpstr += str(quant) + str(at_depth).zfill(zfill)
        self._triplemaxacertos = int(tmpstr)
    return self._triplemaxacertos

  @property
  def triplemaxacertos_str(self):
    try:
      return str(self.triplemaxacertos_int)
    except (TypeError, ValueError):
      pass
    return ''

  def process(self):
    for backward_depth in self.BACKWARD_DEPTH_CONC_SIZES:
      result_maxacs_n_nconccompared = compare_maxacertos_from_nconc_down_to(
        self.nconc, self.ms_asc_history_list, backward_depth
      )
      maxacertos, nconc_compared = result_maxacs_n_nconccompared
      depth_to = self.nconc - nconc_compared + 1
      self.maxacertos_dict[backward_depth] = (maxacertos, depth_to)
    self.has_been_process = True

  def __str__(self):
    outstr = f"TripleMaxAcertos nconc={self.nconc} dzs={self.intlist} triplemax_int={self.triplemaxacertos_int}"
    return outstr


def find_n_acertos_intlist_to_another(intlist, another_intlist):
  coincide_ints = list(filter(lambda e: e in another_intlist, intlist))
  return len(coincide_ints)


def compare_maxacertos_from_nconc_down_to(nconc, ms_asc_history_list, backward_depth_conc_size=50):
  result_maxacs_n_nconccompared = None
  max_acertos = -1
  top_position_idx = nconc - 1
  topone_intlist = sorted(ms_asc_history_list[top_position_idx])
  if top_position_idx - backward_depth_conc_size + 1 <= 0:
    return None
  second_downward_start_from = top_position_idx - 1
  downto = second_downward_start_from - backward_depth_conc_size - 1
  for second_downward_i in range(second_downward_start_from, downto, -1):
    downone_intlist = sorted(ms_asc_history_list[second_downward_i])
    n_acertos = find_n_acertos_intlist_to_another(topone_intlist, downone_intlist)
    if n_acertos > max_acertos:
      max_acertos = n_acertos
      nconc_compared = second_downward_i + 1
      result_maxacs_n_nconccompared = (max_acertos, nconc_compared)
  return result_maxacs_n_nconccompared


def list_max_acertos_from_top_concs_downward(down_to_nconc=None):
  histogram_triplemax = {}
  ms_asc_history_list = lh.get_ms_history_as_list_with_cardgames_in_ord_sor()
  histogram_conc_n_maxhistacertos_dict = {}
  coinc_quants = [tupl[1] for tupl in histogram_conc_n_maxhistacertos_dict.items()]
  total_coincs = sum(coinc_quants)
  downward_start_from = len(ms_asc_history_list) - 1
  down_to = LAST_DOWNWARD_LIMIT_600 - 1 if down_to_nconc is None else down_to_nconc - 1
  for downward_idx in range(downward_start_from, down_to, -1):
    nconc = downward_idx + 1
    triplemax_obj = TripleBackwardMaxAcertos(nconc, ms_asc_history_list)
    print(triplemax_obj)
    tri_int = triplemax_obj.triplemaxacertos_int
    if tri_int in histogram_triplemax:
      histogram_triplemax[tri_int] += 1
    else:
      histogram_triplemax[tri_int] = 1
  print('total concs', len(histogram_triplemax), 'histogram', histogram_triplemax)
  totalitems = sum(map(lambda e: e[1], histogram_triplemax.items()))
  repeated = totalitems - len(histogram_triplemax)
  print('totalitems', totalitems, 'repeated', repeated)


def adhoctest():
  pass


def adhoctest2():
  pass


def process():
  down_to_nconc = None
  total_concs = lh.count_total_concs_in_ms_history_db()
  scrmsg = f"Total concs in ms history = {total_concs}"
  print(scrmsg)
  if total_concs and total_concs > LAST_DOWNWARD_LIMIT_600 + 5:
    down_to_nconc = total_concs - 5
  if down_to_nconc is not None:
    list_max_acertos_from_top_concs_downward(down_to_nconc)
  else:
    scrmsg = (f"It could not process maxacertos due to possible database missing:"
              f" total_concs = {total_concs} and downward limit = {LAST_DOWNWARD_LIMIT_600}")
    print(scrmsg)


if __name__ == '__main__':
  """
  adhoctest()
  adhoctest2()
  adhoctest()
  """
  process()

