#!/usr/bin/env python3
"""
fs/dbfs/datafilefs/from_wks/from_excel_to_db_dozens_in_drawn_order.py

import fs.jogosfs.jogos_functions as jf
"""
import fs.dbfs.datafilefs.from_wks.ms_excel_read as mer  # get_pandas_df_from_ms_history_excelfile
import fs.jogosfs.jogos_metrics as jm
import fs.dbfs.sqlfs.sqlitefs.sqlite_conn_n_createtable as sqlc  # .get_sqlite_connection
TABLENAME = 'ms_concs_n_stats'
SQLITE_DB_FILENAME = 'ms_concs_n_stats.sqlite'


class Insertor:

  tablename = 'ms_concs_n_stats'

  def __init__(self):
    self.n_inserted = 0
    sqlc.create_table_if_not_exists()
    self.conn = sqlc.get_sqlite_connection()
    self.cursor = self.conn.cursor()

  def insert_nconc_n_dezenas_into_db(self, nconc, ds_ord_sor_str):
    sql = f"INSERT INTO {self.tablename} (nconc, ds_ord_sor_str) VALUES (?, ?);"
    tuplevalues = (nconc, ds_ord_sor_str)
    retval = self.cursor.execute(sql, tuplevalues)
    self.n_inserted += 1
    print(self.n_inserted, retval, sql)

  def commit(self):
    print('n_inserted', self.n_inserted)
    if self.n_inserted > 0:
      self.conn.commit()
      print('dbcommitted')
    self.conn.close()


def get_data_n_build_metrics():
  df = mer.get_pandas_df_from_ms_history_excelfile()
  i = 0
  insertor = Insertor()
  for row in df.iterrows():
    i += 1
    r = row[1]  # the series part
    nconc = r.nconc
    tupledozens = r.d1, r.d2, r.d3, r.d4, r.d5, r.d6
    if not isinstance(r.d1, int):
      continue
    if r.d1 < 0:
      continue
    jmetr = jm.JogoMetrics(nconc, tupledozens)
    print(jmetr.nconc, jmetr.ds_ord_sor_str)
    insertor.insert_nconc_n_dezenas_into_db(jmetr.nconc, jmetr.ds_ord_sor_str)
  insertor.commit()


def adhoctest():
  pass


def process():
  get_data_n_build_metrics()


if __name__ == '__main__':
  adhoctest()
  process()
