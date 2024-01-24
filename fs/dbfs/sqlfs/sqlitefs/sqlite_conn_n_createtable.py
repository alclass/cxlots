#!/usr/bin/env python3
"""
fs/dbfs/datafilefs/from_wks/from_excel_to_db_dozens_in_drawn_order.py

There 18 metrics as of the time of this writing. These are:

    soma INT,
    media_mult100 INT,
    dsvpdr_mult100 INT,
    n_consecutivos INT,
    n_8_adjacent_ci INT,
    n_immed_repeats_32123_ci INT,
    up_same_down_seq_ci INT,
    remainder5patt_ci INT,
    resto12patt_b12_b10_ci INT,
    quadrantpatt_ci INT,
    colpatt_ci INT,
    rowpatt_ci INT,
    triple_maxacertos_w_depths_ci INT,
    triple_pares_dpares_n_prct_ci INT,
    triplesimm_num_col_row_ci INT,
    dzs_repeatdepth_ci TEXT,
    xs_ys_distsum_cs TEXT,
    dzs_acc_hstgrm_n_gentot_cs TEXT,

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
  """
  The two sufixes adopted in fieldnames are:

  s1 sufix "_ci" in fieldname means "composed int"
    => a "component" is derived from the whole (the "composed int")
       as a power of 10
    Example: 123 => if each component is a (one) power of 10,
      components will be the sequence-like [100, 20, 3],
      for 100+20+3=123

  s2 sufix "_cs" in fieldname means "comma separated text"
    Example: "1,2,3" => after extraction it's becomes
      the sequence-like [1, 2, 3]
  """
  sql = f"""CREATE TABLE IF NOT EXISTS {MS_TABLENAME} (
    nconc INT PRIMARY KEY,
    ds_ord_sor_str CHAR(12) NOT NULL,
    lexicographicalindex INT,
    soma INT,
    media_mult100 INT,
    dsvpdr_mult100 INT,
    n_consecutivos INT,
    n_8_adjacent_ci INT,
    up_same_down_seq_ci INT,
    remainder5patt_ci INT,
    resto12patt_b12_b10_ci INT,
    quadrantpatt_ci INT,
    colpatt_ci INT,
    rowpatt_ci INT,
    triple_maxacertos_w_depths_ci INT,
    triple_pares_dpares_n_prct_ci INT,
    triplesimm_num_col_row_ci INT,
    n_immed_repeats_32123_ci INT,
    dzs_repeatdepth_ci TEXT,
    xs_ys_distsum_cs TEXT,
    dzs_acc_hstgrm_n_gentot_cs TEXT, 
    created_at DATETIME,
    modified_at DATETIME
  );
  """
  conn = get_sqlite_connection()
  retval = conn.execute(sql)
  print('Creating table if not exists', MS_TABLENAME, 'retval', retval)
  return


def read_raw_last_record_on_ms_table():
  conn = get_sqlite_connection()
  conn.row_factory = sqlite3.Row
  sql = f"SELECT * FROM {MS_TABLENAME} ORDER BY nconc DESC LIMIT 1;"
  cursor = conn.cursor()
  fetchobj = cursor.execute(sql)
  row = fetchobj.fetchone()
  nconc, ds_ord_sor_str = None, None
  if row:
    nconc = row['nconc']
    ds_ord_sor_str = row['ds_ord_sor_str']
  cursor.close()
  conn.close()
  return nconc, ds_ord_sor_str


def fetch_last_ms_nconc_n_cardgame_as_ord_sor_ints_from_db():
  nconc, ds_ord_sor_str = read_raw_last_record_on_ms_table()
  dozens = [int(ds_ord_sor_str[i: i+2]) for i in range(0, 12, 2)]
  return nconc, dozens


def adhoctest():
  nconc, dozens = fetch_last_ms_nconc_n_cardgame_as_ord_sor_ints_from_db()
  scrmsg = f"nconc={nconc}, ds_ord_sorteio={dozens}"
  print(scrmsg)


def process():
  pass


if __name__ == '__main__':
  adhoctest()
  process()
