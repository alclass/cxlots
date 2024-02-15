#!/usr/bin/env python3
"""
commands/updates/db_update_concdates.py
  Updates the MS db-table in column 'concdates'

"""
import pandas as pd
import sqlite3
import fs.dbfs.sqlfs.sqlitefs.sqlite_conn_n_createtable as sqlc  # for sqlc.get_sqlite_connection()
import fs.dbfs.datafilefs.from_wks.ms_excel_read as mer  # for mer.get_pandas_df_from_ms_history_excelfile()
import fs.datefs.date_functions as dtfs  # for dtfs.transform_bar_ddmmyyyy_date_into_datetime


def filter_df_for_those_having_given_nconcs(df, nconcs):
  df = df[pd.to_numeric(df['nconc'], errors='coerce').notnull()]
  df = df[['nconc', 'concdate']]
  # df = df.drop(df['nconc'] not in nconcs)
  # df = df.apply(lambda e: e in nconcs, df['nconc'])
  # df = df['nconc':df.isin({'nconc': nconcs})]
  return df


class ConcDatesDBUpdater:

  tablename = sqlc.MS_TABLENAME

  def __init__(self):
    self.nconcs = []
    self.df = None
    self.nconc_n_date_dict = {}
    # self.nconc_n_date_tuplelist = []
    self.n_updated = 0
    self.conn = None
    self.cursor = None
    self.process()

  def get_concdate_from_df_w_nconc(self, nconc):
    series = self.df[self.df['nconc'] == nconc]
    payload_data = series[1]
    concdate = payload_data['concdate']
    return concdate

  def read_data_as_pandas_df(self):
    self.df = mer.get_pandas_df_from_ms_history_excelfile()
    self.df = filter_df_for_those_having_given_nconcs(self.df, self.nconcs)
    print(self.df.to_string())
    pass

  def convert_dates_if_any(self):
    self.nconc_n_date_dict = {}
    for row in self.df.iterrows():
      series = row[1]
      nconc = series['nconc']
      ddmmyyyy = series['concdate']
      if nconc not in self.nconcs:
        continue
      pdate = dtfs.transform_bar_ddmmyyyy_date_into_datetime(ddmmyyyy)
      self.nconc_n_date_dict[nconc] = pdate
    print('Total items in nconc_n_date_dict', len(self.nconc_n_date_dict))
    pass

  @property
  def fetched_rows(self):
    return len(self.nconcs)

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

  def update_concdate_for_a_row_without_it(self, nconc, concdate):
    sql = f"UPDATE {self.tablename} SET concdate = ? WHERE nconc = ?;"
    sqltuplevalues = (concdate, nconc)
    retval = self.cursor.execute(sql, sqltuplevalues)
    prev_n_upt = self.n_updated
    if retval:
      self.n_updated += 1
    scrmsg = f"Updating concdate={concdate} for nconc={nconc} | prev={prev_n_upt}, n_upd={self.n_updated}"
    print(scrmsg)

  def update_concdate_for_rows_without_it(self):
    """
    Updates all rows, that having dozens and not having its concdate, get it
      ie updates rows setting field concdate if field 'dozenstr' is set
      (@see SELECT sql-query above)
    """
    self.conn = sqlc.get_sqlite_connection()
    self.cursor = self.conn.cursor()
    for nconc in self.nconc_n_date_dict:
      concdate = self.nconc_n_date_dict[nconc]
      print('Updating', nconc, 'with date', concdate)
      self.update_concdate_for_a_row_without_it(nconc, concdate)
    self.db_commit_if_any_update_happened_n_closeconn()

  def db_commit_if_any_update_happened_n_closeconn(self):
    if self.n_updated > 0:
      print(f'committing db with n_updates={self.n_updated} rows')
      self.conn.commit()
    self.conn.close()

  def process(self):
    self.fetch_all_rows_as_nconc_n_dozens_not_having_concdates()
    if self.fetched_rows == 0:
      print('No rows have missing concdates. Nothing to do.')
      return
    self.read_data_as_pandas_df()
    self.convert_dates_if_any()
    self.update_concdate_for_rows_without_it()

  def __str__(self):
    outstr = f"{self.__class__.__name__} fetched_rows={self.fetched_rows} n_updated={self.n_updated}"
    return outstr


def adhoctest():
  co = ConcDatesDBUpdater()
  co.process()
  print(co)


def process():
  pass


if __name__ == '__main__':
  adhoctest()
  process()
