#!/usr/bin/env python3
"""
commands/updates/db_update_metrics_into_db.py

    soma INT,
    media_mult100 INT,
    dsvpdr_mult100 INT,
    n_consecutivos INT,
    n_8_adjacent_ci INT,
    up_same_down_seq_ci INT,
    remainder5patt_ci INT,
    resto12patt_b12_b10_ci INT,
    quadrantpatt_ci INT,
    colpatt_str CHAR(10),
    rowpatt_str CHAR(6),
    triple_maxacertos_w_depths_ci INT,
    triple_pares_dpares_n_prct_ci INT,
    triplesimm_mtx_col_row_ci INT,
    n_immed_repeats_12312_ci INT,
    xs_ys_distsum_cs TEXT,
    dzs_repeatdepth_ci TEXT,
    dzs_acc_hstgrm_n_gentot_cs TEXT,

import fs.mathfs.metrics.histograms_n_percentils as hp  # hp.MSHistoryHistogram
 => metric histogram is to be done separately!
"""
import sqlite3
import time
import commands.show.list_ms_history as lh  # lh.get_ms_history_as_list_with_cardgames_in_ord_sor
import fs.mathfs.metrics.soma_media_dsvpdr_etal as smd  # .calc_soma_from_intlist_or_none
import fs.mathfs.metrics.max_acertos_backward as mab  # mab.TripleBackwardMaxAcertos
import fs.mathfs.metrics.pares_dpares_n_percevensum as pdp  # pdp.EvenNumberTripleMetricCalculator
import fs.mathfs.metrics.triple_simmetrics_n_col_row as tsmcr  # tsmcr.TripleSimmetricCalculator
import fs.mathfs.metrics.immed_repeats_freqs_histograms as rfh  # rfh.ImmediateRepeatsCounter
import fs.mathfs.metrics.distance_xs_ys_sums_metric as xysums  # xysums.MetricDistanceXsYsSummer
import fs.dbfs.sqlfs.sqlitefs.sqlite_conn_n_createtable as sqli  # sqli.get_sqlite_connection
import fs.mathfs.numberfs.numberfunctions as nfs  # nfs.transf_6number12charstr_into_dozenlist


class MetricsMSUpdater:

  TABLENAME = sqli.MS_TABLENAME

  def __init__(self):
    self.conn = None
    self.cursor = None
    self.nconc = -1
    self.nconc_n_dozenstr_tuplelist = []
    self.ms_hist_slider = lh.MSHistorySlider()
    self.tablename = self.TABLENAME
    self.dozens_ord_sor_list = None
    self._dozens_asc_ord_list = None
    self.soma = None
    self.media_mult100 = None
    self.dsvpdr_mult100 = None
    self.n_consecutivos = None
    self.n_8_adjacent_ci = None
    self.up_same_down_seq_ci = None
    self.remainder5patt_ci = None
    self.resto12patt_b12_b10_ci = None
    self.quadrantpatt_ci = None
    self.quadrantpatt_ci = None
    self.colpatt_str, self.rowpatt_str = None, None
    self.triple_maxacertos_w_depths_ci = None
    self.triple_pares_dpares_n_prct_ci = None
    self.triplesimm_mtx_col_row_ci = None
    self.n_immed_repeats_12312_ci = None
    self.dzs_repeatdepth_ci = None
    self.xs_ys_distsum_cs = None

  @property
  def dozens_asc_ord_list(self):
    if self._dozens_asc_ord_list is None:
      if self.dozens_ord_sor_list:
        self._dozens_asc_ord_list = sorted(self.dozens_ord_sor_list)
      else:
        self._dozens_asc_ord_list = None
    return self._dozens_asc_ord_list

  @property
  def fetched_rows(self):
    return len(self.nconc_n_dozenstr_tuplelist)

  def gather_metrics_for_nconc(self):
    # soma INT,
    self.soma = smd.calc_soma_from_intlist_or_none(self.dozens_ord_sor_list)
    # media_mult100 INT,
    self.media_mult100 = smd.calc_mediamult100_from_intlist_or_none(self.dozens_ord_sor_list)
    # dsvpdr_mult100 INT,
    self.dsvpdr_mult100 = smd.calc_desviopadraomult100_from_intlist_none(self.dozens_ord_sor_list)
    # n_consecutivos INT,
    self.n_consecutivos = smd.calc_n_consecutivos(self.dozens_ord_sor_list)
    # n_8_adjacent_ci INT,
    eac = smd.EightAdjacentFromIntListCalculator(self.dozens_ord_sor_list)
    self.n_8_adjacent_ci = eac.get_metric_datum()
    # up_same_down_seq_ci INT,
    usd = smd.UpSameDownFromIntlistDeriver(self.dozens_ord_sor_list)
    self.up_same_down_seq_ci = usd.get_metric_datum()
    # remainder5patt_ci INT,
    self.remainder5patt_ci = smd.calc_resto5patt_from_intlist(self.dozens_ord_sor_list)
    # resto12patt_b12_b10_ci INT,
    self.resto12patt_b12_b10_ci = smd.calc_resto12patt_as_a_base10int_from_intlist(self.dozens_ord_sor_list)
    # quadrantpatt_ci INT,
    self.quadrantpatt_ci = smd.calc_quadrantpattern_from_intlist_n_maxcol_maxrow(self.dozens_ord_sor_list)
    # colpatt_str CHAR(10),
    # rowpatt_str CHAR(6),
    self.colpatt_str, self.rowpatt_str = smd.calc_column_n_row_str_patterns(self.dozens_ord_sor_list)
    # triple_maxacertos_w_depths_ci INT,
    triple_maxacertos_w_depths_ci = None
    if self.nconc > mab.LAST_DOWNWARD_LIMIT_600 + 1:
      tbma = mab.TripleBackwardMaxAcertos(self.nconc, self.ms_hist_slider.ms_asc_history_as_sor_ord_cardgames)
      self.triple_maxacertos_w_depths_ci = tbma.get_metric_datum()
    # triple_pares_dpares_n_prct_ci INT,
    eventriple = pdp.EvenNumberTripleMetricCalculator(self.dozens_ord_sor_list)
    self.triple_pares_dpares_n_prct_ci = eventriple.get_metric_datum()
    # triplesimm_mtx_col_row_ci INT,
    tri_simm = tsmcr.TripleSimmetricCalculator(self.dozens_ord_sor_list)
    self.triplesimm_mtx_col_row_ci = tri_simm.get_metric_datum()
    # n_immed_repeats_12312_ci INT,
    irc_o = rfh.ImmediateRepeatsCounter(self.nconc, self.ms_hist_slider)
    self.n_immed_repeats_12312_ci = irc_o.get_metric_datum()
    # dzs_repeatdepth_ci TEXT,
    drc_o = rfh.DepthRepeatsCounter(self.nconc, self.ms_hist_slider)
    self.dzs_repeatdepth_ci = drc_o.get_metric_datum()
    # xs_ys_distsum_cs TEXT,
    xysums_o = xysums.MetricDistanceXsYsSummer(self.dozens_ord_sor_list)
    self.xs_ys_distsum_cs = xysums_o.get_metric_datum()
    # dzs_acc_hstgrm_n_gentot_cs TEXT,
    # histogram must be done separately! hp.MSHistoryHistogram()

  def get_tuplevalues(self):
    modified_at = time.time()
    return (
      self.soma,
      self.media_mult100,
      self.dsvpdr_mult100,
      self.n_consecutivos,
      self.n_8_adjacent_ci,
      self.up_same_down_seq_ci,
      self.remainder5patt_ci,
      self.resto12patt_b12_b10_ci,
      self.quadrantpatt_ci,
      self.colpatt_str,
      self.rowpatt_str,
      self.triple_maxacertos_w_depths_ci,
      self.triple_pares_dpares_n_prct_ci,
      self.triplesimm_mtx_col_row_ci,
      self.n_immed_repeats_12312_ci,
      self.xs_ys_distsum_cs,
      modified_at,
      # the last one is for the WHERE-clause
      self.nconc,
    )

  def sql_update(self):
    sql = f"""UPDATE {self.tablename} SET
      soma=?,
      media_mult100=?,
      dsvpdr_mult100=?,
      n_consecutivos=?,
      n_8_adjacent_ci=?,
      up_same_down_seq_ci=?,
      remainder5patt_ci=?,
      resto12patt_b12_b10_ci=?,
      quadrantpatt_ci=?,
      colpatt_str=?,
      rowpatt_str=?,
      triple_maxacertos_w_depths_ci=?,
      triple_pares_dpares_n_prct_ci=?,
      triplesimm_mtx_col_row_ci=?,
      n_immed_repeats_12312_ci=?,
      xs_ys_distsum_cs=?,
      modified_at=? 
    WHERE nconc=?;
    """
    conn = sqli.get_sqlite_connection()
    cursor = conn.cursor()
    retval = cursor.execute(sql, self.get_tuplevalues())
    if retval:
      conn.commit()
    conn.close()

  def fetch_rows_missing_metrics(self):
    """
    Though there are many metrics for updating, the guide-one (as the pivot-one) is 'soma',
      ie, if soma is missing, it is (strongly) supposed that all the metrics in here are missing.
      Because of this supposition, only 'soma IS null' is in the WHERE-clause.
    """
    self.nconc_n_dozenstr_tuplelist = []
    self.conn = sqli.get_sqlite_connection()
    sql = f"""SELECT nconc, ds_ord_sor_str  FROM {self.tablename}
    WHERE
      soma IS null and
      ds_ord_sor_str IS NOT null    
    ORDER BY nconc;"""
    # print(sql)
    self.conn.row_factory = sqlite3.Row
    self.cursor = self.conn.cursor()
    fetch_o = self.cursor.execute(sql)
    if fetch_o:
      for row in fetch_o.fetchall():
        nconc = row['nconc']
        ds_ord_sor_str = row['ds_ord_sor_str']
        print('Found nconc', nconc, 'ds_ord_sor_str', ds_ord_sor_str)
        nconc_n_dozenstr_tuple = (nconc, ds_ord_sor_str)
        self.nconc_n_dozenstr_tuplelist.append(nconc_n_dozenstr_tuple)
    self.conn.close()
    return

  def gather_metrics_for_all_missing_rows(self):
    for nconc_n_dozenstr_tuple in self.nconc_n_dozenstr_tuplelist:
      self.nconc, n6ch12_dozens_str = nconc_n_dozenstr_tuple[0], nconc_n_dozenstr_tuple[1]
      self.dozens_ord_sor_list = nfs.transf_6number12charstr_into_dozenlist(n6ch12_dozens_str)
      self.gather_metrics_for_nconc()
      self.sql_update()

  def process(self):
    """
    """
    print('Searching rows without metrics (based on field soma')
    self.fetch_rows_missing_metrics()
    print('Number of rows found', self.fetched_rows)
    self.gather_metrics_for_all_missing_rows()
    return
    # print(self.nconc, 'inserting updating')
    # print(self.)
    # # self..sql_update()

  def __str__(self):
    outstr = f"""{self.__class__.__name__} 
    nconc {self.nconc} = nconc | cardgame = {self.dozens_ord_sor_list} | {self.dozens_asc_ord_list}
    soma = {self.soma} | media = {self.media_mult100} | desvio padrão = {self.dsvpdr_mult100}
    n_consecutivos = {self.n_consecutivos} | n_8_adjacent_ci = {self.n_8_adjacent_ci}
    up_same_down_seq_ci = {self.up_same_down_seq_ci} | quadrantpatt_ci = {self.quadrantpatt_ci}
    remainder5patt_ci = {self.remainder5patt_ci} | resto12patt_b12_b10_ci = {self.resto12patt_b12_b10_ci}
    quadrantpatt_ci = {self.quadrantpatt_ci}
    colpatt_str, rowpatt_str = {self.colpatt_str}, {self.rowpatt_str}
    triple_maxacertos_w_depths_ci = {self.triple_maxacertos_w_depths_ci}
    triple_pares_dpares_n_prct_ci= {self.triple_pares_dpares_n_prct_ci}
    triplesimm_mtx_col_row_ci= {self.triplesimm_mtx_col_row_ci}
    n_immed_repeats_12312_ci = {self.n_immed_repeats_12312_ci}
    dzs_repeatdepth_ci = {self.dzs_repeatdepth_ci}
    xs_ys_distsum_cs = {self.xs_ys_distsum_cs}
    """
    return outstr


def adhoc_test():
  pass


def insert_update():
  """
  ms_slider = lh.MSHistorySlider()
  for i, cardgame in enumerate(ms_slider.ms_asc_history_as_sor_ord_cardgames):
    nconc = i + 1
  """
  miu_o = MetricsMSUpdater()
  miu_o.process()


def process():
  """
  """
  insert_update()


if __name__ == '__main__':
  """
  adhoctest()
  """
  process()
