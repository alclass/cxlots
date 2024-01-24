#!/usr/bin/env python3
"""
commands/show/list_ms_history.py
  Lists MS (Megasena) concursos' history
"""
import copy
import sqlite3
import fs.dbfs.sqlfs.sqlitefs.sqlite_conn_n_createtable as sqlc  # .get_sqlite_connection


class MSHistorySlider:

  def __init__(self):
    self.ms_asc_history_as_sor_ord_cardgames = get_ms_history_as_list_with_cardgames_in_ord_sor()

  @property
  def size(self):
    return len(self.ms_asc_history_as_sor_ord_cardgames)

  def get_asc_history_as_sor_ord_cardgames(self):
    return self.ms_asc_history_as_sor_ord_cardgames

  def get_desc_history_as_sor_ord_cardgames(self):
    return list(reversed(self.ms_asc_history_as_sor_ord_cardgames))

  def get_most_recent_nconc(self):
    """
    Notice that history, as the available data themselves,
      for consistency reasons, may not have missing conc's,
      ie nconc's must be mapped idx+1 all the way up
    If database is faulty is that respect, the system will not work properly.

    @see function check_nconc_consistency() for a check on that.
    At the time of writing, this has not been included in a kind of bootstrap
      functionality, it may as a TO-DO.)
    """
    return self.size  # notice that size is last_idx + 1

  def get_in_sor_ord(self, trg_nconc):
    idx = trg_nconc - 1
    if idx > self.size - 1:
      errmsg = f'MS nconc {trg_nconc} non-existing.'
      raise ValueError(errmsg)
      # return None  # previously it returned None
    return tuple(self.ms_asc_history_as_sor_ord_cardgames[idx])

  def get_in_asc_ord(self, trg_nconc):
    intlist = self.get_in_sor_ord(trg_nconc)
    if intlist is None:
      return None
    return tuple(sorted(intlist))

  def get(self, trg_nconc):
    return self.get_in_sor_ord(trg_nconc)

  def get_nconc_n_cardgame_sor_ord_as_tuple(self, trg_nconc):
    nconc_n_cardgame_sor_ord_as_tuple = (trg_nconc, self.get_in_sor_ord(trg_nconc))
    return nconc_n_cardgame_sor_ord_as_tuple

  def get_nconc_n_cardgame_sor_ord_as_dict(self, trg_nconc):
    nconc_n_cardgame_sor_ord_as_dict = {trg_nconc: self.get_in_sor_ord(trg_nconc)}
    return nconc_n_cardgame_sor_ord_as_dict

  def is_nconc_n_dezenas_sor_ord_the_same_as(self, trg_nconc, intlist):
    db_intlist = self.get_in_sor_ord(trg_nconc)
    intlist = tuple(intlist)
    if db_intlist == intlist:
      return True
    return False


def check_nconc_consistency():
  ms_slider = MSHistorySlider()
  tablename = sqlc.MS_TABLENAME
  sql = f"SELECT * FROM {tablename} ORDER by nconc;"
  conn = sqlc.get_sqlite_connection()
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()
  fetchobj = cursor.execute(sql)
  counted = 0
  for row in fetchobj:
    nconc = row['nconc']
    counted += 1
    if counted != nconc:
      errmsg = f'Error: integer sequence got broken when reading db records at counted={counted} != nconc={nconc}'
      raise ValueError(errmsg)
    dezenas_str = row['ds_ord_sor_str']
    dezenas_sor_ord = derive_dezenas_list_from_dezenas_str(dezenas_str)
    boolres = ms_slider.is_nconc_n_dezenas_sor_ord_the_same_as(nconc, dezenas_sor_ord)
    if not boolres:
      errmsg = f'Check NOT-PASSED: db-data for the history of MS is inconsistent in the mapping index+1 with nconc at pos {nconc}.'
      raise ValueError(errmsg)
  conn.close()
  scrmsg = 'Passed check: db-data for the history of MS is consistent in the mapping index+1 with nconc.'
  print(scrmsg)
  return


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
  check_nconc_consistency()


if __name__ == '__main__':
  adhoctest()
  process()
