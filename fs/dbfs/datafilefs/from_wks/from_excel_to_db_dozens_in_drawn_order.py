#!/usr/bin/env python3
"""
fs/dbfs/datafilefs/from_wks/from_excel_to_db_dozens_in_drawn_order.py

import fs.jogosfs.jogos_functions as jf
"""
import sqlite3

import pandas as pd

import fs.dbfs.datafilefs.from_wks.ms_excel_read as mer  # for mer.get_pandas_df_from_ms_history_excelfile()
import fs.jogosfs.jogos_metrics as jm
import fs.dbfs.sqlfs.sqlitefs.sqlite_conn_n_createtable as sqlc  # for sqlc.get_sqlite_connection()
TABLENAME = 'ms_concs_n_stats'
SQLITE_DB_FILENAME = 'ms_concs_n_stats.sqlite'


def cut_down_df_above_given_nconc(df, last_nconc):
  """

  # the method below does not work as a filter to the column
  # df = df.filter(lambda e: isinstance(e, int), df['nconc'])
  """
  # first: remove non-numeric (non-int) values in column nconc (in header, there is 'Concurso' there)
  df = df[pd.to_numeric(df['nconc'], errors='coerce').notnull()]
  # second: filter out all rows that were previously inserted into DB
  df = df[df['nconc'] > last_nconc]
  # print(df.to_string())
  # at this point, df only contains (recent) rows that have not yet entered into DB
  return df


class RecentMSRowsFromDataFrameDBInsertor:

  tablename = 'ms_concs_n_stats'

  def __init__(self):
    self.n_inserted = 0
    self.last_nconc = -1  # last one that has been inserted into db
    self.df = None  # placeholoder for a pandas's dataframe
    self.conn = None  # placeholoder for a db connection
    self.cursor = None

  def open_connection(self):
    sqlc.create_table_if_not_exists()
    self.conn = sqlc.get_sqlite_connection()
    self.conn.row_factory = sqlite3.Row
    self.cursor = self.conn.cursor()

  def close_connection(self):
    self.cursor.close()
    self.conn.close()

  def commit(self):
    print('n_inserted', self.n_inserted)
    if self.n_inserted > 0:
      self.conn.commit()
      print('dbcommitted')
    self.close_connection()

  def fetch_last_nconc(self):
    sql = f"""SELECT max(nconc) as maxnconc  FROM {self.tablename}
    WHERE
      ds_ord_sor_str IS NOT null    
    ORDER BY nconc;"""
    self.open_connection()
    fetcho = self.cursor.execute(sql)
    if fetcho:
      last_row = fetcho.fetchone()
      self.last_nconc = last_row['maxnconc']
    print('@fetch_last_nconc, found', self.last_nconc)
    self.close_connection()

  def read_data_as_pandas_df(self):
    self.df = mer.get_pandas_df_from_ms_history_excelfile()
    if self.last_nconc > 0:
      self.df = cut_down_df_above_given_nconc(self.df, self.last_nconc)
    print(self.df.to_string())

  def insert_nconc_n_dezenas_into_db(self, nconc, concdate, ds_ord_sor_str):
    """
    Inserts a row into DB
    The caller must open db-connection before calling this
    A commit will happen later at the caller if at least a row has been inserted
    """
    sql = f"""INSERT OR IGNORE INTO {self.tablename}
      (nconc, concdate, ds_ord_sor_str)
      VALUES (?, ?, ?);
    """
    tuplevalues = (nconc, concdate, ds_ord_sor_str)
    retval = self.cursor.execute(sql, tuplevalues)
    if retval:
      self.n_inserted += 1
      print(self.n_inserted, retval, sql)
    else:
      print(f'Insersion not happened retval={retval}')

  def dbinsert_rows_one_by_one_if_found_in_df(self):
    """
    Insert rows that are in the dataframe but have not yet been inserted into DB
    The db-connection must be opened here and closed at the end
    """
    self.open_connection()
    i = 0
    for row in self.df.iterrows():
      i += 1
      r = row[1]  # the series obj part, ie the part that contains the data
      nconc = r.nconc
      concdate = r.concdate
      tupledozens = r.d1, r.d2, r.d3, r.d4, r.d5, r.d6
      if not isinstance(r.d1, int):
        continue
      if r.d1 < 0:
        continue
      jmetr = jm.JogoMetrics(nconc, tupledozens)
      print(jmetr.nconc, concdate, jmetr.ds_ord_sor_str)
      self.insert_nconc_n_dezenas_into_db(jmetr.nconc, concdate, jmetr.ds_ord_sor_str)
    self.commit_if_needed_n_close_dbconn()

  def commit_if_needed_n_close_dbconn(self):
    if self.n_inserted > 0:
      print('DB committing', self.n_inserted, 'rows.')
      self.commit()
    self.close_connection()

  def process(self):
    self.fetch_last_nconc()
    self.read_data_as_pandas_df()
    self.dbinsert_rows_one_by_one_if_found_in_df()

  def __str__(self):
    outstr = f"RecentMSRowsFromDataFrameDBInsertor n_inserted={self.n_inserted} last={self.last_nconc}"
    return outstr


def adhoctest():
  pass


def process():
  inso = RecentMSRowsFromDataFrameDBInsertor()
  inso.process()
  print(inso)


if __name__ == '__main__':
  adhoctest()
  process()
