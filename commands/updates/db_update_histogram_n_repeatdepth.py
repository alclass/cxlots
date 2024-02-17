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


class HistogramNRepeatsUpdater:

  tablename = sqlc.MS_TABLENAME

  def __init__(self):
    self.bottom_nconc = None
    self.top_nconc = None
    self.dzs_in_updt_range = None
    self.most_recent_nconc = -1
    self.ms_slider = msh.MSHistorySlider()
    self.conc_n_hstgrmstr_dict = {}
    self.repeat_at_depth_dict = {}
    self.general_total = None
    self.df = None
    self.hstgrm_per_dozen = {}
    self.nconc_n_date_dict = {}
    # self.nconc_n_date_tuplelist = []
    self.n_updated = 0
    self.conn = None
    self.cursor = None
    self.process()

  @property
  def opsize(self):
    return len(self.conc_n_hstgrmstr_dict)

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
    # self.conn.row_factory = sqlite3.Row
    self.cursor = self.conn.cursor()

  def close_connection(self):
    print('Closing connection', self.conn)
    self.cursor.close()
    self.conn.close()

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
    concs = sorted(self.conc_n_hstgrmstr_dict.keys())
    for nconc in concs:
      dzs_acc_hstgrm_n_gentot_cs = self.conc_n_hstgrmstr_dict[nconc]
      dzs_repeatdepth_ci = self.repeat_at_depth_dict[nconc]
      self.dbupdate_row_w_histogram_n_repeat_at_depth_if_needed(nconc, dzs_acc_hstgrm_n_gentot_cs, dzs_repeatdepth_ci)
    if self.n_updated > 0:
      print('DB-Committing', self.n_updated, 'records')
      self.conn.commit()
    self.close_connection()

  def make_hstgrm_dbfield(self, dz_ord_sor):
    hstgrm_str = ''
    for dz in dz_ord_sor:
      hstgrm_str += str(self.hstgrm_per_dozen[dz]) + ','
    hstgrm_str += str(self.general_total)
    return hstgrm_str

  def update_hstgrm_per_dozen_w_concdzs(self, upnext_dzs):
    for dz in self.hstgrm_per_dozen:
      if dz in upnext_dzs:
        self.hstgrm_per_dozen[dz] += 1
      else:
        # self slider.get_hstgrm_for_dz
        self.hstgrm_per_dozen[dz] += 1

  def gather_n_set_all_dzs_in_range_bottom_top(self):
    # 1st: find all dozens in range
    self.dzs_in_updt_range = []
    for nconc in range(self.bottom_nconc, self.top_nconc+1):
      curr_dzs = self.ms_slider.get_in_asc_ord(nconc)
      self.dzs_in_updt_range += curr_dzs
    self.dzs_in_updt_range = sorted(list(set(self.dzs_in_updt_range)))

  def gather_n_set_hstgrm_from_appeardepth_for_all_dzs_in_range_bottom_top(self):
    last_nconc_wo_freqs = self.bottom_nconc - 1
    dz_depth_dict = self.ms_slider.make_dz_n_appearance_depth_dict_for_dozenlist(
      last_nconc_wo_freqs, self.dzs_in_updt_range
    )
    depths = sorted(dz_depth_dict.values())
    for each_depth in depths:
      nconc = last_nconc_wo_freqs - each_depth
      freqdict, _ = self.ms_slider.read_histogram_at_nconc(nconc)
      for dz in freqdict:
        if dz in self.conc_n_hstgrmstr_dict:
          continue
        self.conc_n_hstgrmstr_dict[dz] = freqdict[dz]

  def gather_n_set_last_available_freqs_n_gentotal(self):
    last_available_hist_nconc = self.bottom_nconc - 1
    freqdict, self.general_total = self.ms_slider.read_histogram_at_nconc(last_available_hist_nconc)
    self.conc_n_hstgrmstr_dict = freqdict

  def mount_histogram_n_repeat_at_depth_bottom_up(self):
    # limit_count = 0
    for nconc in range(self.bottom_nconc, self.top_nconc+1):
      dz_ord_sor = self.ms_slider.get_in_sor_ord(nconc)
      repeat_at_depth_str = ''
      for dz in dz_ord_sor:  # at this point, dz_ord_sor must be used (instead of dz_asc_ord) because repeat_at_depth
        self.general_total += 1
        self.hstgrm_per_dozen[dz] += 1
        depth = find_repeat_at_depth_of(dz, nconc, self.ms_slider)
        repeat_at_depth_str += str(depth) + ','
      hstgrm_str = self.make_hstgrm_dbfield(dz_ord_sor)
      self.conc_n_hstgrmstr_dict[nconc] = hstgrm_str
      # print(nconc, dz_asc_ord, dz_ord_sor, 'hstgrm_str', hstgrm_str)
      repeat_at_depth_str = repeat_at_depth_str.rstrip(',')
      self.repeat_at_depth_dict[nconc] = repeat_at_depth_str
      # print(nconc, dz_asc_ord, dz_ord_sor, 'repeat_at_depth_str', repeat_at_depth_str)

  def find_most_recent_nconc(self):
    self.most_recent_nconc = self.ms_slider.get_most_recent_nconc()
    print('most_recent_nconc', self.most_recent_nconc)

  def find_nconcs_without_hstgrm_n_repeat_at_depth(self):
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
    if nconcs or len(nconcs) < 1:
      print('No histograms are missing at this point.')
      return
    dist_last_to_first_without = self.most_recent_nconc - nconcs[0] + 1
    n_of_rows_missing_hstgrm = len(nconcs)
    if dist_last_to_first_without != n_of_rows_missing_hstgrm:
      dist = dist_last_to_first_without
      miss = n_of_rows_missing_hstgrm
      errmsg = f"dist_last_to_first_without (={dist}) != n_of_rows_missing_hstgrm (={miss})"
      raise ValueError(errmsg)
    self.bottom_nconc = nconcs[0]
    self.top_nconc = nconcs[-1]

  @property
  def is_there_conc_yet_to_get_histogram(self):
    try:
      if self.bottom_nconc <= self.top_nconc:
        return True
    except TypeError:
      pass
    return False

  def process(self):
    """
    self.fetch_all_rows_as_nconc_n_dozens_not_having_concdates()
    if self.fetched_rows == 0:
      print('No rows have missing concdates. Nothing to do.')
      return
    self.read_data_as_pandas_df()
    self.convert_dates_if_any()
    self.update_concdate_for_rows_without_it()

    print(self.hstgrm_per_dozen)
    print(self.repeat_at_depth_dict)
    """
    # 1 fetch most recent nconc
    self.find_most_recent_nconc()
    # 2 find nconcs without histogram (an exception may be raised if missing histograms are discontiguous)
    self.find_nconcs_without_hstgrm_n_repeat_at_depth()
    # 3 if histogram is complete, ie nothing to do, return
    if not self.is_there_conc_yet_to_get_histogram:
      print('There is no conc with its histogram. Returning.')
      return
    # 4 recup last available general_total (gather also all 6 dzs_freqs even if they are not needed)
    self.gather_n_set_last_available_freqs_n_gentotal()
    # 5 gather dzs within the range bottom to top
    self.gather_n_set_all_dzs_in_range_bottom_top()
    # 6 knowing dzs within bottom & top, get their freqs via depths down to history
    self.gather_n_set_hstgrm_from_appeardepth_for_all_dzs_in_range_bottom_top()
    # 7 mount histogram & repeat@depth bottom up
    self.mount_histogram_n_repeat_at_depth_bottom_up()
    # 8 finally, update db with histogram & repeat@depth
    # self.dbupdate_histogram_n_repeat_at_depth_if_needed()

  def __str__(self):
    outstr = f"""{self.__class__.__name__} updt={self.n_updated} opsize={self.opsize} last={self.most_recent_nconc}
    concs missing histogram/repeat@depth: from {self.bottom_nconc} up to {self.top_nconc}
    gentotal {self.general_total} : hstgrm_per_dozen={self.hstgrm_per_dozen}"""
    return outstr


def adhoctest():
  """
  hst = HistogramNRepeatsUpdater()
  hst.process()
  print(hst)
  """
  histo = HistogramNRepeatsUpdater()
  print(histo)


def process():
  pass


if __name__ == '__main__':
  adhoctest()
  process()
