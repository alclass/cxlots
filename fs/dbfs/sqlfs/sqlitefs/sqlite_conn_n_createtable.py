#!/usr/bin/env python3
"""
fs/dbfs/datafilefs/from_wks/from_excel_to_db_dozens_in_drawn_order.py

import fs.jogosfs.jogos_functions as jf
import fs.dbfs.datafilefs.from_wks.ms_excel_read as mer  # get_pandas_df_from_ms_history_excelfile
import fs.jogosfs.jogos_metrics as jm
"""
import os
import sqlite3
import local_settings as ls
MS_TABLENAME = 'ms_concs_n_stats'
SQLITE_MS_DB_FILENAME = 'ms_concs_n_stats.sqlite'


def get_sqlite_connection():
  appsdata_basedirpath = ls.get_appsdata_basedirpath()
  sqlitefilepath = os.path.join(appsdata_basedirpath, SQLITE_MS_DB_FILENAME)
  return sqlite3.connect(sqlitefilepath)


def create_table_if_not_exists():
  sql = f"""CREATE TABLE IF NOT EXISTS {MS_TABLENAME} (
    nconc INT PRIMARY KEY,
    ds_ord_sor_str CHAR(12) NOT NULL,
    comb_idx INT,
    soma INT,
    n_primos INT,
    n_pares INT,
    nconsecutivos INT,
    adjacente1 INT,
    n_immed_repeat INT,
    binary_up_down_vector INT,
    media100 INT,
    dp100 INT,
    resto5patt INT,
    restobase12intpatt INT,
    quadrantpatt INT,
    colpatt INT,
    rowpatt INT,
    idxshapearea INT,
    triplesimmetrics INT,
    dzs_imedrepeat_semicommasep TEXT,
    dzs_hstgrm_semicommasep TEXT, 
    created_at DATETIME,
    modified_at DATETIME
  );
  """
  conn = get_sqlite_connection()
  retval = conn.execute(sql)
  print('Creating table if not exists', MS_TABLENAME, 'retval', retval)
  return


def adhoctest():
  pass


def process():
  pass


if __name__ == '__main__':
  adhoctest()
  process()
