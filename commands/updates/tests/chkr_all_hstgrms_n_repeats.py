#!/usr/bin/env python3
"""
commands/updates/tests/chkr_all_hstgrms_n_repeats.py
  Checks histogram & repeat_at_depth consistency upgoing nconc's ascending through history.
  (At the time being, it's only for MS [Megasena])
"""
import commands.show.list_ms_history as msh  # msh.MSHistorySlider
# uhn.get_dict_n_topnconc_map_of_dzs_n_theirnconcs_via_slider_n_topconc
import commands.updates.db_update_histogram_n_repeatdepth as uhn


class HistogramNRepeatChecker:

  def __init__(self, start_from=None):
    self.n_hstgrm_checks = 0
    self.n_repeatatdepth_checks = 0
    self.upgoing_gen_total = 0
    self.upgoing_acc_histogram_dict = {}
    self.upgoing_dz_n_itsnconc_dict = {}
    self.currnconc_histogram_dict = {}
    # the next three are properties derived,
    # the first one by the former,
    # self.currnconc_histogram_str
    # the two others by self.upgoing_dz_n_itsnconc_dict
    # self.currnconc_repeatatdepth_dict = {}
    # self.currnconc_repeatatdepth_str = {}
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
    dzs_repeatatdepth_str = ''
    curr_dzs_sor_ord = self.ms_slider.get_in_sor_ord(self.curr_nconc)
    for dz in curr_dzs_sor_ord:
      repeat_at_depth = self.currnconc_repeatatdepth_dict[dz]
      dzs_repeatatdepth_str += str(repeat_at_depth) + ','
    dzs_repeatatdepth_str = dzs_repeatatdepth_str.rstrip(',')
    return dzs_repeatatdepth_str

  @property
  def currnconc_repeatatdepth_dict(self):
    dzs_repeatatdepth_dict_at_currconc = {}
    curr_dzs_sor_ord = self.ms_slider.get_in_sor_ord(self.curr_nconc)
    for dz in curr_dzs_sor_ord:
      if dz in self.upgoing_dz_n_itsnconc_dict:
        dzs_repeatatdepth_dict_at_currconc[dz] = self.curr_nconc - self.upgoing_dz_n_itsnconc_dict[dz]
      else:
        dzs_repeatatdepth_dict_at_currconc[dz] = -1
    return dzs_repeatatdepth_dict_at_currconc

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

  def get_repeat_at_depth_str_at_currnconc(self):
    dz_n_repeatatdepth_dict, _ = uhn.get_dict_n_topnconc_map_dzs_n_repeatatdepth_w_dznconcdict_n_topconc(
      self.upgoing_dz_n_itsnconc_dict,
      self.curr_nconc
    )
    dzs_ord_sor = self.ms_slider.get_in_sor_ord(self.curr_nconc)
    repeat_at_depth_str = ''
    for dz in dzs_ord_sor:
      r_at_depth = dz_n_repeatatdepth_dict[dz]
      repeat_at_depth_str += str(r_at_depth) + ','
    repeat_at_depth_str = repeat_at_depth_str.rstrip(',')
    return repeat_at_depth_str

  def check_equality_of_calc_repeatatdepth_against_its_indb_counterpart_at_nconc(self):
    calc_repeatatdepth_str = self.currnconc_repeatatdepth_str
    db_repeat_at_depth_str = self.ms_slider.fetch_repeatatdepthstr_at_nconc(self.curr_nconc)
    if calc_repeatatdepth_str != db_repeat_at_depth_str:
      # checking got broken, raise ValueError
      errmsg = (f"Inconsistent repeat_at_depth_str at nconc={self.curr_nconc}:"
                f" the difference is currnconc_histogram_str={calc_repeatatdepth_str}"
                f" != db_repeat_at_depth_str={db_repeat_at_depth_str}")
      raise ValueError(errmsg)
    # check passed
    self.n_repeatatdepth_checks += 1
    dzs_sor_ord = self.ms_slider.get_in_sor_ord(self.curr_nconc)
    scrmsg = (f"okay checked n={self.n_repeatatdepth_checks}: the two equal: repeat@depth_str={calc_repeatatdepth_str}"
              f" @nconc={self.curr_nconc} for {dzs_sor_ord}")
    print(scrmsg)

  def check_equality_of_calc_hstgrm_against_indb_hstgrm_at_nconc(self):
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
    self.n_hstgrm_checks += 1
    dzs_sor_ord = self.ms_slider.get_in_sor_ord(self.curr_nconc)
    scrmsg = (f"\tokay checked n={self.n_hstgrm_checks}: the two equal: histogram_from_slider_str={histogram_from_slider_str}"
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
      # update dz_n_itsnconc dict
      self.upgoing_dz_n_itsnconc_dict[dz] = self.curr_nconc
    self.upgoing_gen_total += len(dzs_sor_ord)

  def go_check_bottom_up(self):
    for self.curr_nconc in range(self.start_from, self.total_concs_in_db + 1):
      # check for repeat_at_depth has to be done before adding freqs, otherwise the dzs's last conc's will be lost
      self.check_equality_of_calc_repeatatdepth_against_its_indb_counterpart_at_nconc()
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

  def init_dict_dz_n_theirnconc(self):
    nconc_upto = self.start_from - 1
    self.upgoing_dz_n_itsnconc_dict, _ = uhn.get_dict_n_topnconc_map_of_dzs_n_theirnconcs_via_slider_n_topconc(
      self.ms_slider, nconc_upto
    )

  def header_before_report(self):
    scrmsg = f"Check of consistency of [1] dz_n_freq histogram & repeat@depth through MS history data"
    print(scrmsg)
    nstart, nend = self.start_from, self.ms_slider.size
    amount = nend - nstart + 1
    print('\t', "="*10, 'start from =', nstart, '| size = ', nend, '| amount = ', amount, '='*20)

  def process(self):
    self.header_before_report()
    self.init_histogram_based_on_n_last_ones()
    self.init_dict_dz_n_theirnconc()
    self.go_check_bottom_up()

  def __str__(self):
    """
    """
    cname = self.__class__.__name__
    t_in_db = self.total_concs_in_db
    ccnc = self.curr_nconc
    outstr = f"""{cname} total_concs={t_in_db} curr_conc={ccnc} | orgstart={self.start_from}
    total dzs in histogram={len(self.upgoing_acc_histogram_dict)} | n_checks={self.n_hstgrm_checks} """
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
