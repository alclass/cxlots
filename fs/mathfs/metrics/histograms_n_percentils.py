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


def calc_dict_percent_freq_of_dozens_from_histogram(accfreqs, dzs_quant_hist_hstgrm_dict):
  total = sum([tupl[1] for tupl in dzs_quant_hist_hstgrm_dict.items()])
  percent_list = []
  for accfreq in accfreqs:
    pct = accfreq * 100 / total
    percent_list.append(pct)
  return percent_list


class MSHistoryHistogram:
  """
  This metric is a "history" metric, ie, it depends on the historical values.

  In this system, most metrics do not depend on history, as this one does,
    this class depends on the existence of a database available.

  Example 'metric': 411530722, ie
    4115 => the maxacertos 4, up to depth 600, at depth 115
    405 => the maxacertos 3, up to 20 depth 60, happening at depth 7 (07)
    22 => the maxacertos 2, up to 2 depth 6, happening at depth 2
  """

  def __init__(self, ms_history_slider=None):
    self._dzs_quant_hist_hstgrm_dict = None
    self._accfreq_ord_sor_conc_asclist = None
    self._pctfreq_ord_sor_conc_asclist = None
    self.hist_slider = ms_history_slider
    self.treat_history_slider_or_default()
    self._curr_intlist_sor_ord = None
    self.has_been_processed = False
    # self.process()

  @property
  def size(self):
    return self.hist_slider.size

  @property
  def dzs_quant_hist_hstgrm_dict(self):
    if self._dzs_quant_hist_hstgrm_dict is None:
      if not self.has_been_processed:
        self.process()
    return self._dzs_quant_hist_hstgrm_dict

  @property
  def accfreq_ord_sor_conc_asclist(self):
    if self._accfreq_ord_sor_conc_asclist is None:
      if not self.has_been_processed:
        self.process()
    return self._accfreq_ord_sor_conc_asclist

  @property
  def pctfreq_ord_sor_conc_asclist(self):
    if self._pctfreq_ord_sor_conc_asclist is None:
      if not self.has_been_processed:
        self.process()
    return self._pctfreq_ord_sor_conc_asclist

  def treat_history_slider_or_default(self):
    """
    Notice hist_slider depends on lh.MSHistorySlider()
      being able to supply the specific data from the database.

    At the time of writing, this piece does not raise an exception
      in case hist_slider is unable to supply data.
    """
    if self.hist_slider is None:
      self.hist_slider = lh.MSHistorySlider()

  def update_history_histogram_count_from_last_counted_on(self):
    """
    This method looks up database to find where the last counting
      happened and, then, continues from there.
    """
    pass

  def count_all_history_into_histogram_from_zero(self):
    """

    """
    self._accfreq_ord_sor_conc_asclist = []
    self._pctfreq_ord_sor_conc_asclist = []
    self._dzs_quant_hist_hstgrm_dict = {}
    for i, intlist in enumerate(self.hist_slider.get_asc_history_as_sor_ord_cardgames()):
      for d in intlist:
        if d in self._dzs_quant_hist_hstgrm_dict:
          self._dzs_quant_hist_hstgrm_dict[d] += 1
        else:
          self._dzs_quant_hist_hstgrm_dict[d] = 1
      accfreqs = [self._dzs_quant_hist_hstgrm_dict[d] for d in intlist]
      accfreq_commasep_str = ','.join(map(str, accfreqs))
      self._accfreq_ord_sor_conc_asclist.append(accfreq_commasep_str)
      cardgame_pctfreq = calc_dict_percent_freq_of_dozens_from_histogram(
        accfreqs, self._dzs_quant_hist_hstgrm_dict
      )
      self._pctfreq_ord_sor_conc_asclist.append(cardgame_pctfreq)

  def process(self):
    self.count_all_history_into_histogram_from_zero()
    self.has_been_processed = True

  def __str__(self):
    outstr = f"MSHistoryHistogram size={self.size}\n"
    intval = 0
    for row in range(6):
      line = ''
      for col in range(10):
        intval += 1
        quant = self.dzs_quant_hist_hstgrm_dict[intval]
        line += f"{intval:02}->{quant} "
      line += "\n"
      outstr += line
    return outstr


class PercentTilCounter(MSHistoryHistogram):
  """
  There are two main ways of counting dozens occurrences:

  w1 one is to follow the histogram field in DB

  w2 the other is to count bottom up from all concursos.

  At this moment, because database completion (the metric fields) is not yet functional,
     w2 (counting bottom up) will firstly be implemented. (Later on [TO-DO] w1 may be included.)
  """

  def __init__(self, ms_history_slider=None):
    super().__init__(ms_history_slider)

  def show_accfreq_conc_by_conc(self):
    for i in range(len(self.accfreq_ord_sor_conc_asclist)):
      nconc = i + 1
      accfreq_str = self.accfreq_ord_sor_conc_asclist[i]
      pctfreqs = self.pctfreq_ord_sor_conc_asclist[i]
      accfreqs = list(map(lambda e: int(e), accfreq_str.split(',')))
      # pctfreqs = list(map(lambda e: int(e), accfreq_str.split(',')))
      soma = sum(accfreqs)
      soma_pct = sum(pctfreqs)
      print(nconc, '=>', accfreqs, soma, pctfreqs, soma_pct)


def adhoctest():
  histo = MSHistoryHistogram()
  histo.process()
  print(histo)
  sorted_histoitems = sorted(histo.dzs_quant_hist_hstgrm_dict.items(), key=lambda e: e[1])
  pdict = dict(sorted_histoitems)
  first = sorted_histoitems[-1]
  last = sorted_histoitems[0]
  print(pdict)
  amplitude = first[1] - last[1]
  print('first', first, 'amplitude', amplitude, len(pdict), 'avg step', amplitude/len(pdict))
  print('last', last)


def adhoctest2():
  freqer = PercentTilCounter()
  freqer.show_accfreq_conc_by_conc()


def process():
  pass


if __name__ == '__main__':
  """
  adhoctest2()
  process()
  """
  adhoctest2()
