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

import fs.dbfs.datafilefs.from_wks.ms_excel_read as mer  # for mer.get_pandas_df_from_ms_history_excelfile()
"""
import sqlite3
import fs.dbfs.sqlfs.sqlitefs.sqlite_conn_n_createtable as sqlc  # for sqlc.get_sqlite_connection()
import commands.show.list_ms_history as msh  # msh.MSHistorySlider
MS_N_ELEMENTS = 60


def trans_dzs6number12charstr_into_dzslist(dzs6number12charstr):
  try:
    dzslist = [int(dzs6number12charstr[i:i + 1]) for i in range(0, 12, 2)]
    return dzslist
  except (TypeError, ValueError):
    pass
  return []


class HistogramNRepeatAtDepthFinder:
  """
  This class aims to find the following two 'metrics' of a conc, ie:
    dzs_acc_hstgrm_n_gentot_cs & dzs_repeatdepth_ci
    In terms of db-fetching them, the two are connected,
      ie fetching histogram also fetches repeat_at_depth.

  Testing notice:
    Because this class and its methods depend on a database (at the time of this writing it's a sqlite db)
      an adhoctest module will be elaborated for testing correctness of sql-selection/data fetching routines
      instead of a unit-test approach, this is due to the fact that one doesn't have
      a mock-interface that could unit-test it in case db is empty
      or unaccessible from where the unit-tests are run.
  """

  def __init__(self, curr_nconc):
    self.conn = None
    self.dzs_w_freq_hstgrm_dict = {}
    self.dz_n_appearance_depth_dict = {}
    self.curr_nconc = curr_nconc
    self._gentotal_updated = -1
    self.ms_hist_slider = msh.MSHistorySlider()
    self.dzs_sor_ord = self.ms_hist_slider.get_in_sor_ord(self.curr_nconc)
    self.process()

  def fetch_hstgrm_from_known_repeat_at_depth_for_nconc(self, nconc):
    self.conn = sqlc.get_sqlite_connection()
    self.conn.row_factory = sqlite3.Row
    cursor = self.conn.cursor()
    # dzs_sor_ord is not needed because the ms_hist_slider has it
    sql = f"""
    SELECT dzs_acc_hstgrm_n_gentot_cs  FROM {sqlc.MS_TABLENAME}
    WHERE nconc = ?;
    """
    dzs_acc_hstgrm_n_gentot_cs = None
    sqltuplevalues = (nconc, )
    ro = cursor.execute(sql, sqltuplevalues)
    if ro:
      row = ro.fetchone()
      dzs_acc_hstgrm_n_gentot_cs = row['dzs_acc_hstgrm_n_gentot_cs']
      if nconc == self.curr_nconc - 1:
        self.set_generaltotal_w_dzs_acc_hstgrm_n_gentot_cs(dzs_acc_hstgrm_n_gentot_cs)
    cursor.close()
    self.conn.close()
    return dzs_acc_hstgrm_n_gentot_cs

  def set_generaltotal_w_dzs_acc_hstgrm_n_gentot_cs(self, dzs_acc_hstgrm_n_gentot_cs):
    """
    This set-method is called when the SELECT method meets the immediate previous nconc
    """
    dzs_acc_hstgrm_n_gentot_intstrs = dzs_acc_hstgrm_n_gentot_cs.split(',')
    dzs_acc_hstgrm_n_gentot_ints = list(map(int, dzs_acc_hstgrm_n_gentot_intstrs))
    previous_gentotal = dzs_acc_hstgrm_n_gentot_ints[-1]
    self._gentotal_updated = previous_gentotal + 6

  @property
  def gentotal_updated(self):
    if self._gentotal_updated == -1:
      self.fetch_hstgrm_from_known_repeat_at_depth_for_nconc(self.curr_nconc - 1)
    return self._gentotal_updated

  @property
  def dzs_w_freq_known_list(self):
    return list(self.dzs_w_freq_hstgrm_dict.keys())

  @property
  def dzs_asc_ord(self):
    return sorted(self.dzs_sor_ord)

  @property
  def dzs_repeatdepth_ci(self):
    _repeat_at_depth_ci = ''
    for dz in self.dzs_sor_ord:
      repeat_at_depth = self.dz_n_appearance_depth_dict[dz]
      _repeat_at_depth_ci += str(repeat_at_depth) + ','
    _repeat_at_depth_ci = _repeat_at_depth_ci.rstrip(',')
    return _repeat_at_depth_ci

  @property
  def dzs_acc_hstgrm_n_gentot_cs(self):
    _dzs_acc_hstgrm_n_gentot_cs = ''
    for dz in self.dzs_sor_ord:
      dz_freq = self.dzs_w_freq_hstgrm_dict[dz]
      _dzs_acc_hstgrm_n_gentot_cs += str(dz_freq) + ','
    _dzs_acc_hstgrm_n_gentot_cs += str(self.gentotal_updated)
    return _dzs_acc_hstgrm_n_gentot_cs

  def accumulate_dict_of_dzs_acc_hstgrm_n_gentot_cs_w_dzs_sor_ord(
      self, nconc, dzs_sor_ord, dzs_acc_hstgrm_n_gentot_cs, dzs_repeatdepth_ci
  ):
    hstgrm_n_gentot_list = list(map(int, dzs_acc_hstgrm_n_gentot_cs.split(',')))
    repeat_at_depth_n_gentot_list = list(map(int, dzs_repeatdepth_ci.split(',')))
    for i in range(len(dzs_sor_ord)):
      if dzs_sor_ord[i] not in self.dzs_asc_ord:
        continue
      self.dzs_w_freq_hstgrm_dict[dzs_sor_ord[i]] = hstgrm_n_gentot_list[i]
    if nconc == self.curr_nconc - 1:
      self.gentotal_updated = hstgrm_n_gentot_list[-1] + 6
    return

  def fetch_acumfreq_for_dz_at_nconc(self, dz, nconc, pos):
    dzs_acc_hstgrm_n_gentot_cs = self.fetch_hstgrm_from_known_repeat_at_depth_for_nconc(nconc)
    acumfreqs_as_str = dzs_acc_hstgrm_n_gentot_cs.split(',')
    acumfreqs = list(map(int, acumfreqs_as_str))
    acumfreq = acumfreqs[pos]
    self.dzs_w_freq_hstgrm_dict[dz] = acumfreq

  def fetch_histogram_from_history_for_each_curr_dozenlist(self):
    for pos, dz in enumerate(self.dzs_sor_ord):
      repeat_at_depth = self.dz_n_appearance_depth_dict[dz]
      trg_nconc = self.curr_nconc - repeat_at_depth
      self.fetch_acumfreq_for_dz_at_nconc(dz, trg_nconc, pos)

  def get_dz_n_appearance_depth_dict_for_curr_conc(self):
    self.dz_n_appearance_depth_dict = self.ms_hist_slider.make_dz_n_appearance_depth_dict_for_dozenlist(
      self.curr_nconc-1, self.dzs_sor_ord
    )

  def process(self):
    self.get_dz_n_appearance_depth_dict_for_curr_conc()
    self.fetch_histogram_from_history_for_each_curr_dozenlist()

  def __str__(self):
    outstr = f"""{self.__class__.__name__} | nconc={self.curr_nconc} dzs={self.dzs_sor_ord} dzs={self.dzs_asc_ord}   
    histogram={self.dzs_acc_hstgrm_n_gentot_cs} | repeat@depth={self.dzs_repeatdepth_ci}"""
    return outstr


def find_repeat_at_depth_of(dz, nconc, allconcs_in_hist_order):
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
    self.nconcs = []
    self.conc_n_hstgrmstr_dict = {}
    self.repeat_at_depth_dict = {}
    self.general_total = 0
    self.df = None
    self.hstgrm_per_dozen = {}
    self.nconc_n_date_dict = {}
    # self.nconc_n_date_tuplelist = []
    self.n_updated = 0
    self.conn = None
    self.cursor = None
    # self.process()

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
    if fetch_o:
      for row in fetch_o.fetchall():
        nconc = row['nconc']
        print('Found nconc', nconc, 'without concdate')
        self.nconcs.append(nconc)
    self.conn.close()
    return

  def open_connection(self):
    self.conn = sqlc.get_sqlite_connection()
    # self.conn.row_factory = sqlite3.Row
    self.cursor = self.conn.cursor()

  def close_connection(self):
    print('Closing connection', self.conn)
    self.cursor.close()
    self.conn.close()

  def dbupdate_row_w_histogram_n_repeat_at_depth_if_needed(self, nconc, dzs_repeatdepth_ci, dzs_acc_hstgrm_n_gentot_cs):
    sql = f"""UPDATE {self.tablename} 
    SET 
      dzs_repeatdepth_ci = ?,
      dzs_acc_hstgrm_n_gentot_cs = ?
    WHERE
      nconc = ?;
    """
    tuplevalues = (dzs_repeatdepth_ci, dzs_acc_hstgrm_n_gentot_cs, nconc)
    retval = self.cursor.execute(sql, tuplevalues)
    if retval:
      self.n_updated += 1
      print('updated', self.n_updated)

  def dbupdate_histogram_n_repeat_at_depth_if_needed(self):
    self.open_connection()
    concs = sorted(self.conc_n_hstgrmstr_dict.keys())
    for nconc in concs:
      dzs_repeatdepth_ci = self.repeat_at_depth_dict[nconc]
      dzs_acc_hstgrm_n_gentot_cs = self.conc_n_hstgrmstr_dict[nconc]
      self.dbupdate_row_w_histogram_n_repeat_at_depth_if_needed(nconc, dzs_repeatdepth_ci, dzs_acc_hstgrm_n_gentot_cs)
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

  def form_histogram_n_repeat_at_depth_bottom_up(self):
    sli = msh.MSHistorySlider()
    allconcs_in_hist_order = sli.get_asc_history_as_sor_ord_cardgames()
    self.general_total = 0
    # limit_count = 0
    for i, dz_ord_sor in enumerate(allconcs_in_hist_order):
      # limit_count += 1
      # if limit_count > 50:
      #   break
      # dz_asc_ord = sorted(dz_ord_sor)  # used for the prints below that were commented-out
      nconc = i + 1  # this correspondence is tested by a checker (bootstrapper-to-be) module in this system
      repeat_at_depth_str = ''
      for dz in dz_ord_sor:  # at this point, dz_ord_sor must be used (instead of dz_asc_ord) because repeat_at_depth
        self.general_total += 1
        if dz not in self.hstgrm_per_dozen:
          self.hstgrm_per_dozen[dz] = 1
        else:
          self.hstgrm_per_dozen[dz] += 1
        depth = find_repeat_at_depth_of(dz, nconc, allconcs_in_hist_order)
        repeat_at_depth_str += str(depth) + ','
      hstgrm_str = self.make_hstgrm_dbfield(dz_ord_sor)
      self.conc_n_hstgrmstr_dict[nconc] = hstgrm_str
      # print(nconc, dz_asc_ord, dz_ord_sor, 'hstgrm_str', hstgrm_str)
      repeat_at_depth_str = repeat_at_depth_str.rstrip(',')
      self.repeat_at_depth_dict[nconc] = repeat_at_depth_str
      # print(nconc, dz_asc_ord, dz_ord_sor, 'repeat_at_depth_str', repeat_at_depth_str)

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
    self.form_histogram_n_repeat_at_depth_bottom_up()
    # TO-DO: before uncommenting out next line, it's necessary to sql-query db
    # for knowing which rows having missing histogram & repeat_at_depth
    # self.dbupdate_histogram_n_repeat_at_depth_if_needed()

  def __str__(self):
    return f"{self.__class__.__name__} updt={self.n_updated} opsize={self.opsize}"


def adhoctest():
  """
  hst = HistogramNRepeatsUpdater()
  hst.process()
  print(hst)
  """
  histo = HistogramNRepeatAtDepthFinder(curr_nconc=2500)
  print(histo)


def process():
  pass


if __name__ == '__main__':
  adhoctest()
  process()
