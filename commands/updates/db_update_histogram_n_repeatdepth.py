#!/usr/bin/env python3
"""
commands/updates/db_update_histogram_n_repeatdepth.py

  Updates the MS db-table in columns:
   `dzs_repeatdepth_ci` & `dzs_acc_hstgrm_n_gentot_cs`

    dzs_repeatdepth_ci TEXT,  # _ci
      _ci means a string composed of integers comma-separated
      hypothetical example:
        e1 '3,1,10,44,21,1'
          that means:
            the first dozen in drawn order repeated 3 concs before
            the second repeated 1 conc before
            the third repeated 10 concs before
            & so on
        e2 '-1,-1,-1,-1,-1,-1'
          the list above, in theory, be the one for the very first conc in the MS history
          for -1 means the dozen not yet repeats
    dzs_acc_hstgrm_n_gentot_cs TEXT,
      _cs means comma-separated
      _gentot means that the general total accumulated is the seventh number
      _ so, in a nutshell, the total of each dozen in drawn order, for the six ones, then the general total
      hypothetical example: '102,55,40,84,21,1,2017'
        that means:
          the first dozen in drawn order has already appeared 102 times (its frequency)
          the second dozen in drawn order has already appeared 55 times (its frequency)
          (...)
          the last number, 2017. as noted above, informs the general accumulated quantities for all dozens

# import fs.dbfs.datafilefs.from_wks.ms_excel_read as mer  # for mer.get_pandas_df_from_ms_history_excelfile()
# import commands.updates.find_for_update_histogram_n_repeatdepth as ffu  # .HistogramNRepeatAtDepthFinder
"""
import sqlite3
import time
import fs.dbfs.sqlfs.sqlitefs.sqlite_conn_n_createtable as sqlc  # for sqlc.get_sqlite_connection()
import commands.show.list_ms_history as msh  # msh.MSHistorySlider
MS_N_ELEMENTS = 60


def get_dict_n_topnconc_map_dzs_n_repeatatdepth_w_dznconcdict_n_topconc(dzs_n_nconc_dict, topnconc):
  dzs_repeatatdepth_dict = {}
  for dz in dzs_n_nconc_dict:
    dzs_repeatatdepth_dict[dz] = topnconc - dzs_n_nconc_dict[dz]
  return dzs_repeatatdepth_dict, topnconc


def get_dict_n_topnconc_map_dzs_n_repeatatdepth_via_slider_n_topconc(ms_slider, topnconc=None):
  dzs_n_nconc_dict, topnconc = get_dict_n_topnconc_map_of_dzs_n_theirnconcs_via_slider_n_topconc(ms_slider, topnconc)
  get_dict_n_topnconc_map_dzs_n_repeatatdepth_w_dznconcdict_n_topconc(dzs_n_nconc_dict, topnconc)
  return get_dict_n_topnconc_map_dzs_n_repeatatdepth_w_dznconcdict_n_topconc(dzs_n_nconc_dict, topnconc)


def get_dict_n_topnconc_map_of_dzs_n_theirnconcs_via_slider_n_topconc(ms_slider, topnconc=None):
  size = ms_slider.size
  topnconc = size if topnconc is None else int(topnconc)
  topnconc = -topnconc if topnconc < 0 else topnconc
  topnconc = topnconc % size if topnconc > size else topnconc
  if topnconc < 1:
    return {}, topnconc
  map_dict = {}
  all_dzs = list(range(1, MS_N_ELEMENTS+1))
  nconc = topnconc
  while len(all_dzs) > 0:
    dzs_ord_sor = ms_slider.get_in_asc_ord(nconc)
    for dz in dzs_ord_sor:
      if nconc < 1:
        break
      if dz in all_dzs:  # and dz not in map_dict:
        map_dict[dz] = nconc
        all_dzs.remove(dz)
    nconc -= 1
  return map_dict, topnconc


def find_repeat_at_depth_of(dz, nconc, ms_slider):
  """
  A historical note when writing this function:
    using the debugger, there appeared a bug describing "_PyEval_EvalFrameDefault returned NULL"
      when trying to break-point before the return after "if dz in dz_ord_sor:"
    the associated GitHub entry for this bug is sort of difficult to understand (in part because it's C++)
      and points to a solved issue
    because of that, we gave up the debugger and put some prints here, later on commented-out
      we wanted to check what happened at the moment of the first 'repeat' in the MS history
      with the help of 'prints', it seems to be correctly getting the first 'repeat'
  """
  top_to_bottom_idx = nconc - 2
  repeat_at_depth = - 1  # if no repeat is found
  if top_to_bottom_idx < 0:
    return repeat_at_depth
  repeat_at_depth = 1  #
  allconcs_in_hist_order = ms_slider.get_asc_history_as_sor_ord_cardgames()
  for idx in range(top_to_bottom_idx, -1, -1):  # search downwards
    dz_ord_sor = allconcs_in_hist_order[idx]
    # print(dz, 'idx', idx, dz_ord_sor)
    if dz in dz_ord_sor:
      # print('Caught dz', dz, 'repeat found', repeat_found)
      return repeat_at_depth
    repeat_at_depth += 1
  # if program-flow falls down here, a depth was not found
  # notice that at some point in the MS history, when histogram of every dozen goes to 2 or above,
  # there will always be a depth at which a repeat happens
  return -1


class HistogramNRepeatsFollower:
  """
  Does the evolving of frequencies (histogram) & repeat@depth from the last one available upward.

  Explanation of the case when no histogram data is available and the case where it's parcially available:

  Case 1: no histogram data is available
    if db has only the history of dozencards (the n integers in a volant conc by conc) and
      histogram & repeat@depth (db-fields `dzs_repeatdepth_ci` & `dzs_acc_hstgrm_n_gentot_cs`)
      this class gathers the two, conc by conc, upwardly, ie historically, ascending through time.

  Case 2: histogram is partial
    when it is partial, the 'formation' of the complement data uses the last available one to build it upward,
    ie, conc by conc in ascending time order.

  The two uses of this class (at the moment of creation 2024-02):

  Use 1:
    The first use is to check consistency in the two fields (histogram & repeat@depth)
  Use 2:
    The second use is to db-update when new concs become available.
    (This is done by class (inherited or composed): HistogramNRepeatsUpdater
  """

  tablename = sqlc.MS_TABLENAME

  def __init__(self):
    """
    This class operates in two modes, ie:
      m1 checking_mode &
      m2 update_mode
    The base class (this one), because it performs checking/verifying function, keeps this as False
    The inheriting class, for db-update, below, sets update_mode to True
      (per complementarity, in this, checking_mode is False)
    """
    self.update_mode = None  # set later on because of inherited class HistogramNRepeatsUpdater
    self.most_recent_nconc = None
    self._bottom_chk_nconc = None
    self._top_chk_nconc = None
    self.bottom_upt_nconc = None
    self.top_upt_nconc = None
    self.dzs_in_gather_range = []
    self.nconc_n_hstgramstr_for_range_dict = {}
    self.nconc_n_repeatdepthstr_for_range_dict = {}
    self.dz_n_freq_acc_hstgrm_upgoing_dict = {}
    self.general_total = None
    self.ms_slider = msh.MSHistorySlider()
    self.conn = None
    self.cursor = None
    self.eq_chknconcs_w_uptnconcs_as_default()
    # process() should not be issued from here because the user has yet to choose chk_mode or update
    # self.process()

  def eq_chknconcs_w_uptnconcs_as_default(self):
    self.find_most_recent_nconc()
    self.find_nconcs_within_gather_range_f_hstgrm_n_repeat()
    # establish equality as a default, user may set a different range after construction (__init__)
    self.bottom_chk_nconc = self.bottom_upt_nconc
    self.top_chk_nconc = self.top_upt_nconc

  def set_topmost_general_total(self):
    dz_freq_dict, self.general_total = self.ms_slider.fetch_n_derive_dzsfreqhstgrm_n_gentotal_at_nconc(
      self.most_recent_nconc
    )
    for dz in dz_freq_dict:
      if dz in self.dz_n_freq_acc_hstgrm_upgoing_dict:
        self.dz_n_freq_acc_hstgrm_upgoing_dict[dz] += dz_freq_dict[dz]
      else:
        self.dz_n_freq_acc_hstgrm_upgoing_dict[dz] = dz_freq_dict[dz]

  @property
  def dzs_mr_sor_ord(self):
    """
    most recent dzs_sor_ord
    """
    return self.ms_slider.get_in_sor_ord(self.most_recent_nconc)

  @property
  def bottom_chk_nconc(self):
    if self._bottom_chk_nconc is None:
      # default to bottom_upt_nconc
      self._bottom_chk_nconc = self.bottom_upt_nconc
    return self._bottom_chk_nconc

  @bottom_chk_nconc.setter
  def bottom_chk_nconc(self, bottom_nconc):
    if bottom_nconc is None:
      self._bottom_chk_nconc = 1
      return
    if bottom_nconc < 0:
      self._bottom_chk_nconc = self.most_recent_nconc - bottom_nconc + 1
    else:
      self._bottom_chk_nconc = bottom_nconc
    if self._bottom_chk_nconc > self.most_recent_nconc:
      self._bottom_chk_nconc = self._bottom_chk_nconc % self.most_recent_nconc

  @property
  def top_chk_nconc(self):
    if self._top_chk_nconc is None:
      # default to bottom_upt_nconc
      self._top_chk_nconc = self.top_upt_nconc
    return self._top_chk_nconc

  @top_chk_nconc.setter
  def top_chk_nconc(self, top_nconc):
    if top_nconc is None:
      # this may not make much sense, also not making much sense a setting it None from somewhere
      # unless it means the most_recent
      self._top_chk_nconc = self.most_recent_nconc
      return
    if top_nconc < 0:
      self._top_chk_nconc = self.most_recent_nconc - top_nconc + 1
    else:
      self._top_chk_nconc = top_nconc
    if self._top_chk_nconc > self.most_recent_nconc:
      self._top_chk_nconc = self.most_recent_nconc
    if self._bottom_chk_nconc > self._top_chk_nconc:
      self._top_chk_nconc = self._bottom_chk_nconc
    # if a setting is happening here, necessarily update_mode should be False
    # self.update_mode = False

  @property
  def concs_size(self):
    """
    concs_size is short for "number of concs that need checking or updating"
      it refers to the number of concs in nconc_n_hstgramstr_for_range_dict

    How many are they?
      Let's see it as an example:
        e1 if history has 100 concs and all of them miss histogram, concs_size, in this case, is 100
        e2 if history has 101 concs and only the last one misses histogram, concs_size, in this case, is 1
        e3 if history has 101 concs none misses histogram, concs_size, in this case, is 0
    """
    return len(self.nconc_n_hstgramstr_for_range_dict)

  def fetch_all_rows_as_nconc_n_dozens_not_having_concdates(self):
    """
    Fetches all rows in which field `concdate` is null and ds_ord_sor_str is not null
      The purpose is to update all rows that need to receive the concdate value
      (the concdate values are present in the Excel that comes up via a pandas' dataframe)
    """
    self.conn = sqlc.get_sqlite_connection()
    sql = f"""SELECT nconc FROM {self.tablename}
    WHERE
      concdate is null and
      ds_ord_sor_str is not null
    ORDER BY nconc;"""
    print(sql)
    self.conn.row_factory = sqlite3.Row
    self.cursor = self.conn.cursor()
    fetch_o = self.cursor.execute(sql)
    nconcs = []
    if fetch_o:
      for row in fetch_o.fetchall():
        nconc = row['nconc']
        print('Found nconc', nconc, 'without concdate')
        nconcs.append(nconc)
    self.conn.close()
    return nconcs

  def open_connection(self):
    self.conn = sqlc.get_sqlite_connection()
    self.conn.row_factory = sqlite3.Row
    self.cursor = self.conn.cursor()

  def close_connection(self):
    # print('Closing connection', self.conn)
    self.cursor.close()
    self.conn.close()

  def make_hstgrm_dbfield(self, dz_ord_sor):
    # all dzs should be in self.hstgrm_dozen_n_freq_for_range_dict.keys()
    dzs_in_dict = list(self.dz_n_freq_acc_hstgrm_upgoing_dict.keys())
    total_keys_in_lst = sum(map(lambda e: 1 if e in dzs_in_dict else 0, dz_ord_sor))
    if total_keys_in_lst != len(dz_ord_sor):
      # cannot build the histogram, one or more dz_keys are missing
      return None
    hstgrm_str = ''
    for dz in dz_ord_sor:
      # the check above guarantees all keys are present (not raising KeyError)
      hstgrm_str += str(self.dz_n_freq_acc_hstgrm_upgoing_dict[dz]) + ','
    hstgrm_str += str(self.general_total)
    return hstgrm_str

  def gather_n_set_all_dzs_in_range_bottom_top(self):
    nconc_from, nconc_to = self.pick_up_nconc_from_to()
    for nconc in range(nconc_from, nconc_to + 1):
      curr_dzs = self.ms_slider.get_in_asc_ord(nconc)
      self.dzs_in_gather_range += curr_dzs
    # make the dzs list have unique items and in ascending order
    self.dzs_in_gather_range = sorted(list(set(self.dzs_in_gather_range)))

  def gather_n_set_hstgrm_from_appeardepth_for_all_dzs_in_range_bottom_top(self):
    nconc_from, nconc_to = self.pick_up_nconc_from_to()
    last_nconc_wo_freqs = nconc_from - 2  # it's minus 2 before it read the last available one above
    if last_nconc_wo_freqs < 1:
      return
    nconcs = [nconc_from - 1]  # idem
    # remove coinciding dzs
    dzs_yet_to_get_its_freq = list(self.dzs_in_gather_range)
    for dz_in_freq_dict in self.dz_n_freq_acc_hstgrm_upgoing_dict:
      if dz_in_freq_dict in dzs_yet_to_get_its_freq:
        dzs_yet_to_get_its_freq.remove(dz_in_freq_dict)
    dz_n_conc_at_which_it_last_occurred_dict = self.ms_slider.makedict_dz_n_conc_at_which_it_last_occurred(
      last_nconc_wo_freqs, dzs_yet_to_get_its_freq
    )
    nconcs += list(set(dz_n_conc_at_which_it_last_occurred_dict.values()))
    # get it in descending order
    nconcs = list(reversed(sorted(nconcs)))
    for nconc in nconcs:
      freqdict, _ = self.ms_slider.fetch_n_derive_dzsfreqhstgrm_n_gentotal_at_nconc(nconc)
      for dz in freqdict:
        if dz in self.dz_n_freq_acc_hstgrm_upgoing_dict:
          continue
        self.dz_n_freq_acc_hstgrm_upgoing_dict[dz] = freqdict[dz]

  def gather_n_set_last_available_freqs_n_gentotal(self):
    """
    Gets the frequencies of the immediate last available conc in db
      If info is not present in db, zero 'histogram' (with {}) and general_total
    """
    last_available_hist_nconc = self.bottom_upt_nconc - 1
    if last_available_hist_nconc < 1:
      freqdict, self.general_total = {}, 0
    else:
      freqdict, self.general_total = self.ms_slider.fetch_n_derive_dzsfreqhstgrm_n_gentotal_at_nconc(
        last_available_hist_nconc
      )
    # this is the first setting for hstgrm_dozen_n_freq_for_range_dict
    self.dz_n_freq_acc_hstgrm_upgoing_dict = freqdict

  def pick_up_nconc_from_to(self):
    if not self.update_mode:
      nconc_from = self.bottom_upt_nconc
      nconc_to = self.top_upt_nconc
    else:
      nconc_from = self.bottom_chk_nconc
      nconc_to = self.top_chk_nconc
    return nconc_from, nconc_to

  def mount_histogram_n_repeat_at_depth_bottom_up(self):
    nconc_from, nconc_to = self.pick_up_nconc_from_to()
    for nconc in range(nconc_from, nconc_to + 1):
      dz_ord_sor = self.ms_slider.get_in_sor_ord(nconc)
      repeat_at_depth_str = ''
      histogram_str = ''
      for dz in dz_ord_sor:  # at this point, dz_ord_sor must be used (instead of dz_asc_ord) because repeat_at_depth
        if dz in self.dz_n_freq_acc_hstgrm_upgoing_dict:
          self.dz_n_freq_acc_hstgrm_upgoing_dict[dz] += 1
        else:
          # 'else' should occur only when no histogram data was gathered before for 'small' nconc's
          self.dz_n_freq_acc_hstgrm_upgoing_dict[dz] = 1
        histogram_str += str(self.dz_n_freq_acc_hstgrm_upgoing_dict[dz]) + ','
        depth = find_repeat_at_depth_of(dz, nconc, self.ms_slider)
        repeat_at_depth_str += str(depth) + ','
      repeat_at_depth_str = repeat_at_depth_str.rstrip(',')
      # hstgrm_str = self.make_hstgrm_dbfield(dz_ord_sor)
      self.general_total += len(dz_ord_sor)
      histogram_str += str(self.general_total)
      self.nconc_n_hstgramstr_for_range_dict[nconc] = histogram_str
      self.nconc_n_repeatdepthstr_for_range_dict[nconc] = repeat_at_depth_str

  def find_most_recent_nconc(self):
    self.most_recent_nconc = self.ms_slider.get_most_recent_nconc()
    print('most_recent_nconc', self.most_recent_nconc)

  def find_nconcs_within_gather_range_f_hstgrm_n_repeat(self):
    nconcs = []
    sql = f"SELECT nconc FROM {self.tablename} WHERE dzs_acc_hstgrm_n_gentot_cs is null ORDER BY nconc;"
    self.open_connection()
    fetch_o = self.cursor.execute(sql)
    if fetch_o:
      for row in fetch_o.fetchall():
        nconc = row['nconc']
        nconcs.append(nconc)
    self.close_connection()
    sorted(nconcs)
    self.set_range_or_raise_if_nconcs_are_discontiguous(nconcs)

  def set_range_or_raise_if_nconcs_are_discontiguous(self, nconcs):
    """
    histogram, more than repeat@depth, cannot exist discontiguously because any one
      above nconc=1 depends on its previous ones
    """
    if nconcs is None:
      return
    if len(nconcs) < 1:
      print('No histograms are missing at this point.')
      return
    dist_last_to_first_without = self.most_recent_nconc - nconcs[0] + 1
    n_of_rows_missing_hstgrm = len(nconcs)
    if dist_last_to_first_without != n_of_rows_missing_hstgrm:
      dist = dist_last_to_first_without
      miss = n_of_rows_missing_hstgrm
      errmsg = f"dist_last_to_first_without (={dist}) != n_of_rows_missing_hstgrm (={miss})"
      raise ValueError(errmsg)
    # notice that the two properties below are used in the inherited class HistogramNRepeatsUpdater,
    # however, they are set here because they correspond to the nconc range that have missing histogram
    # and will be a default (the user can reset them) to self.bottom_chk_nconc & self.top_chk_nconc
    self.bottom_upt_nconc = nconcs[0]
    self.top_upt_nconc = nconcs[-1]

  @property
  def describe_mode(self):
    chk_mode_str = '[check mode]'
    upd_mode_str = '[update mode]'
    if self.update_mode:
      return upd_mode_str
    return chk_mode_str

  @property
  def is_there_conc_yet_to_get_histogram(self):
    try:
      if self.bottom_upt_nconc <= self.top_upt_nconc:
        return True
    except TypeError:
      pass
    return False

  def process(self):
    """
    These two operations were taken from __init__()
    # step 2
    self.find_most_recent_nconc()
    # step 3
    self.find_nconcs_within_gather_range_f_hstgrm_n_repeat()
    """
    # this is because the inheriting class HistogramNRepeatsUpdater sets mode at __init__() after super().__init__()
    if self.update_mode is None:  # at this inherited class and at process(), this is not None
      self.update_mode = False
    # step 4 if histogram is complete, ie nothing to do, return
    if not self.is_there_conc_yet_to_get_histogram:
      print('At this point, there is no conc yet to get its histogram. Returning.')
      self.set_topmost_general_total()
      return
    # step 5 recup last available general_total (gather also all 6 dzs_freqs even if they are not needed)
    self.gather_n_set_last_available_freqs_n_gentotal()
    # step 6 gather dzs within the range bottom to top
    self.gather_n_set_all_dzs_in_range_bottom_top()
    # step 7 knowing dzs within bottom & top, get their freqs via depths down to history
    self.gather_n_set_hstgrm_from_appeardepth_for_all_dzs_in_range_bottom_top()
    # step 8 mount histogram & repeat@depth bottom up
    self.mount_histogram_n_repeat_at_depth_bottom_up()
    # the 9th (ninth) step (update db with histogram & repeat@depth) is taken by
    # the inheriting class HistogramNRepeatsUpdater (below or elsewhere)
    # the base class functions as a data-gatherer & a checker

  def __str__(self):
    """
    updt={self.n_updated}
    """
    cname = self.__class__.__name__
    recent = self.most_recent_nconc
    outstr = f"""{cname} mode={self.describe_mode} n_to_upd={self.concs_size} last={recent} dzs={self.dzs_mr_sor_ord}
    concs missing histogram/repeat@depth: from {self.bottom_upt_nconc} up to {self.top_upt_nconc}
    gentotal {self.general_total} : topmost_hstgrm={self.dz_n_freq_acc_hstgrm_upgoing_dict}"""
    return outstr


class HistogramNRepeatsUpdater(HistogramNRepeatsFollower):

  def __init__(self):
    """
    # self.histo = HistogramNRepeatsFollower()

    The two properties below have been set in the constructor (__init__()) for the base class
      p1 self.bottom_upt_nconc
      p2 self.top_upt_nconc
    """
    super().__init__()
    self.update_mode = True
    self.n_updated = 0

  def dbupdate_row_w_histogram_n_repeat_at_depth_if_needed(self, nconc, dzs_acc_hstgrm_n_gentot_cs, dzs_repeatdepth_ci):
    modified_at = time.time()
    sql = f"""UPDATE {self.tablename} 
    SET 
      dzs_acc_hstgrm_n_gentot_cs = ?,
      dzs_repeatdepth_ci = ?,
      modified_at = ?
    WHERE
      nconc = ?;
    """
    tuplevalues = (dzs_acc_hstgrm_n_gentot_cs, dzs_repeatdepth_ci, modified_at, nconc)
    retval = self.cursor.execute(sql, tuplevalues)
    if retval:
      self.n_updated += 1
      print('updated', self.n_updated, tuplevalues)
      return True
    return False

  def dbupdate_histogram_n_repeat_at_depth_if_needed(self):
    self.open_connection()
    concs = sorted(self.nconc_n_hstgramstr_for_range_dict.keys())
    for nconc in concs:
      dzs_acc_hstgrm_n_gentot_cs = self.nconc_n_hstgramstr_for_range_dict[nconc]
      dzs_repeatdepth_ci = self.nconc_n_repeatdepthstr_for_range_dict[nconc]
      self.dbupdate_row_w_histogram_n_repeat_at_depth_if_needed(nconc, dzs_acc_hstgrm_n_gentot_cs, dzs_repeatdepth_ci)
    if self.n_updated > 0:
      self.conn.commit()
    print('DB-Committed', self.n_updated, 'records')
    self.close_connection()

  def update_hstgrm_per_dozen_w_concdzs(self, upnext_dzs):
    for dz in self.dz_n_freq_acc_hstgrm_upgoing_dict:
      if dz in upnext_dzs:
        self.dz_n_freq_acc_hstgrm_upgoing_dict[dz] += 1
      else:
        # self slider.get_hstgrm_for_dz
        self.dz_n_freq_acc_hstgrm_upgoing_dict[dz] += 1

  def process(self):
    super().process()
    self.dbupdate_histogram_n_repeat_at_depth_if_needed()


def adhoctest():
  """
  hst = HistogramNRepeatsUpdater()
  hst.process()
  print(hst)
  """
  ms_slider = msh.MSHistorySlider()
  dzs_n_nconc_dict, topnconc = get_dict_n_topnconc_map_of_dzs_n_theirnconcs_via_slider_n_topconc(
    ms_slider, topnconc=None
  )
  print('topnconc', topnconc, dzs_n_nconc_dict)
  dzs_n_depth_dict, topnconc = get_dict_n_topnconc_map_dzs_n_repeatatdepth_w_dznconcdict_n_topconc(
    dzs_n_nconc_dict, topnconc
  )
  print('topnconc', topnconc, dzs_n_depth_dict)


def process():
  histo = HistogramNRepeatsUpdater()
  histo.process()
  print('Finishing:', histo)


if __name__ == '__main__':
  process()
  adhoctest()
