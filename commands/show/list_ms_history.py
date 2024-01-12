#!/usr/bin/env python3
"""
commands/show/list_ms_history.py
  Lists MS (Megasena) concursos' history
"""
import sqlite3
import fs.dbfs.sqlfs.sqlitefs.sqlite_conn_n_createtable as sqlc  # .get_sqlite_connection


def derive_dezenas_list_from_dezenas_str(dezenas_str):
  dezenas = [int(dezenas_str[i:i+2]) for i in range(0, 12, 2)]
  return dezenas


def list_ms_history():
  tablename = sqlc.MS_TABLENAME
  sql = f"SELECT * FROM {tablename} ORDER by nconc;"
  conn = sqlc.get_sqlite_connection()
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()
  fetchobj = cursor.execute(sql)
  for row in fetchobj:
    nconc = row['nconc']
    dezenas_str = row['ds_ord_sor_str']
    dezenas = derive_dezenas_list_from_dezenas_str(dezenas_str)
    scrmsg = f"{nconc} | {dezenas}"
    print(scrmsg)


def adhoctest():
  pass


def process():
  list_ms_history()


if __name__ == '__main__':
  adhoctest()
  process()
