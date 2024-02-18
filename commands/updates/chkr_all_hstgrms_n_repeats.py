#!/usr/bin/env python3
"""
commands/updates/chkr_all_hstgrms_n_repeats.py
"""
import commands.show.list_ms_history as msh  # msh.MSHistorySlider


class HistogramNRepeatChecker:

  def __init__(self, start_from=None):
    self.n_checks = 0
    self.upgoing_gen_total = 0
    self.upgoing_acc_histogram_dict = {}
    self.currnconc_histogram_dict = {}
    self.currnconc_repeatatdepth_dict = {}
    self.ms_slider = msh.MSHistorySlider()
    self.curr_nconc = None
    self.start_from = start_from
    self.treat_start_from_n_currnconc()
    self.process()

  @property
  def currnconc_histogram_str(self):
    """
    Derivable attribute from self.currnconc_histogram_dict
    """
    dzs_ord_sor = self.ms_slider.get_in_sor_ord(self.curr_nconc)
    histogram_str = ''
    if self.currnconc_histogram_dict is None or len(self.currnconc_histogram_dict) == 0:
      return ''
    for dz in dzs_ord_sor:
      histogram_str += str(self.currnconc_histogram_dict[dz]) + ','
    histogram_str += str(self.upgoing_gen_total)
    return histogram_str

  @property
  def currnconc_repeatatdepth_str(self):
    """
    Derivable attribute from self.currnconc_repeatatdepth_dict
    """
    dzs_ord_sor = self.ms_slider.get_in_sor_ord(self.curr_nconc)
    currnconc_repeatatdepth_str = ''
    if self.currnconc_repeatatdepth_dict is None or len(self.currnconc_repeatatdepth_dict) == 0:
      return ''
    for dz in dzs_ord_sor:
      currnconc_repeatatdepth_str += str(self.currnconc_repeatatdepth_dict[dz]) + ','
    currnconc_repeatatdepth_str = currnconc_repeatatdepth_str.rstrip(',')
    return currnconc_repeatatdepth_str

  @property
  def total_concs_in_db(self):
      return self.ms_slider.size

  def treat_start_from_n_currnconc(self):
    self.curr_nconc = 1
    if self.start_from is None:
      return
    if self.start_from < 0:
      self.start_from = -self.start_from
      self.start_from = self.total_concs_in_db - self.start_from + 1
      # advance self.curr_nconc
      self.curr_nconc = self.start_from
      return
    if 1 <= self.start_from <= self.total_concs_in_db - 1:
      # advance self.curr_nconc
      self.curr_nconc = self.start_from
      return
    self.start_from = None

  def check_equality_of_calc_hstgrm_against_indb_hstgrm_at_nconc(self):
    scrmsg = f"@nconc={self.curr_nconc}: about to check equality of calculated hstgrm against indb hstgrm"
    print(scrmsg)
    histogram_from_slider_str = self.ms_slider.fetch_histogramstr_at_nconc(self.curr_nconc)
    if histogram_from_slider_str is None or histogram_from_slider_str == '':
      scrmsg = f"Got empty histogram_from_slider_str at nconc={self.curr_nconc}. Continuing."
      print(scrmsg)
      return
    if self.currnconc_histogram_str != histogram_from_slider_str:
      # checking got broken, raise ValueError
      errmsg = (f"Inconsistent hstgrm_str at nconc={self.curr_nconc}:"
                f" the difference is currnconc_histogram_str={self.currnconc_histogram_str}"
                f" != histogram_from_slider_str={histogram_from_slider_str}")
      raise ValueError(errmsg)
    # check passed
    self.n_checks += 1
    dzs_sor_ord = self.ms_slider.get_in_sor_ord(self.curr_nconc)
    scrmsg = (f"okay checked n={self.n_checks}: the two equal: histogram_from_slider_str={histogram_from_slider_str}"
              f" @nconc={self.curr_nconc} for {dzs_sor_ord}")
    print(scrmsg)

  def add_freqs_to_dict_n_set_upgoing_histogram_str_at_nconc(self):
    dzs_sor_ord = self.ms_slider.get_in_sor_ord(self.curr_nconc)
    self.currnconc_histogram_dict = {}
    for dz in dzs_sor_ord:
      if dz in self.upgoing_acc_histogram_dict:
        self.upgoing_acc_histogram_dict[dz] += 1
      else:
        self.upgoing_acc_histogram_dict[dz] = 1
      # copy freqs to curr_dict
      self.currnconc_histogram_dict[dz] = self.upgoing_acc_histogram_dict[dz]
    self.upgoing_gen_total += len(dzs_sor_ord)

  def go_check_bottom_up(self):
    for self.curr_nconc in range(self.start_from, self.total_concs_in_db + 1):
      self.add_freqs_to_dict_n_set_upgoing_histogram_str_at_nconc()
      self.check_equality_of_calc_hstgrm_against_indb_hstgrm_at_nconc()

  def init_histogram_based_on_n_last_ones(self):
    if self.start_from is None:
      return
    if self.start_from < 2:
      return
    nconc_upto = self.start_from - 1
    histogram_dict, gentotal_upto_nconc = self.ms_slider.fetch_dzsfreqhstgrm_n_gentotal_downgoing_from_nconc(
      nconc_upto
    )
    # test consistency of gentotal by multiplication
    shouldbe_gentotal = (self.start_from - 1) * self.ms_slider.N_DOZENS_PER_CARD
    if shouldbe_gentotal != gentotal_upto_nconc:
      errmsg = f"shouldbe_gentotal={shouldbe_gentotal} != gentotal_upto_nconc={gentotal_upto_nconc}"
      raise ValueError(errmsg)
    self.upgoing_acc_histogram_dict, self.upgoing_gen_total = histogram_dict, gentotal_upto_nconc
    self.curr_nconc = self.start_from

  def process(self):
    self.init_histogram_based_on_n_last_ones()
    self.go_check_bottom_up()

  def __str__(self):
    """
    """
    cname = self.__class__.__name__
    t_in_db = self.total_concs_in_db
    ccnc = self.curr_nconc
    outstr = f"""{cname} total_concs={t_in_db} curr_conc={ccnc} | orgstart={self.start_from}
    total dzs in histogram={len(self.upgoing_acc_histogram_dict)} | n_checks={self.n_checks} """
    return outstr


def adhoctest():
  """
  """
  pass


def process():
  chker = HistogramNRepeatChecker(start_from=-2)
  print(chker)


if __name__ == '__main__':
  adhoctest()
  process()
