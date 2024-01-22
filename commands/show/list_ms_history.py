#!/usr/bin/env python3
"""
commands/show/list_ms_history.py
  Lists MS (Megasena) concursos' history
"""
import copy
import sqlite3
import fs.dbfs.sqlfs.sqlitefs.sqlite_conn_n_createtable as sqlc  # .get_sqlite_connection


def derive_dezenas_list_from_dezenas_str(dezenas_str):
  dezenas = [int(dezenas_str[i:i+2]) for i in range(0, 12, 2)]
  return dezenas


def get_ms_history_as_list_with_cardgames_in_ord_sor():
  tablename = sqlc.MS_TABLENAME
  sql = f"SELECT * FROM {tablename} ORDER by nconc;"
  conn = sqlc.get_sqlite_connection()
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()
  fetchobj = cursor.execute(sql)
  ms_history_as_list = []
  counted = 0
  for row in fetchobj:
    nconc = row['nconc']
    counted += 1
    if counted != nconc:
      errmsg = f'Error: integer sequence got broken when reading db records at counted={counted} != nconc={nconc}'
      raise ValueError(errmsg)
    dezenas_str = row['ds_ord_sor_str']
    dezenas = derive_dezenas_list_from_dezenas_str(dezenas_str)
    ms_history_as_list.append(dezenas)  # copy.copy(dezenas)
  conn.close()
  return ms_history_as_list


def count_total_concs_in_ms_history_db():
  tablename = sqlc.MS_TABLENAME
  conn = sqlc.get_sqlite_connection()
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()
  sql = f"SELECT count(*) AS total FROM {tablename};"
  fetchobj = cursor.execute(sql)
  total_recs_in_dbtable = 0
  if fetchobj:
    rec = fetchobj.fetchone()
    total_recs_in_dbtable = rec['total']
  conn.close()
  return total_recs_in_dbtable


def list_ms_history():
  msgame_history_list = get_ms_history_as_list_with_cardgames_in_ord_sor()
  for i, dezenas in enumerate(msgame_history_list):
    nconc = i + 1
    scrmsg = f"{nconc} | {dezenas}"
    print(scrmsg)


def adhoctest():
  pass


def process():
  """
  list_ms_history()
  """
  total = count_total_concs_in_ms_history_db()
  scrmsg = f"count_total_concs_in_ms_history_db {total}"
  print(scrmsg)


if __name__ == '__main__':
  adhoctest()
  process()
