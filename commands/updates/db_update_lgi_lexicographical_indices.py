#!/usr/bin/env python3
"""
commands/updates/db_update_lgi_lexicographical_indices.py
  Updates the MS db-table in column 'lexicographicalindex'

"""
import sqlite3
import fs.dbfs.sqlfs.sqlitefs.sqlite_conn_n_createtable as sqlc  # for sqlc.get_sqlite_connection()
# for lgim.calc_lgi_b0idx_from_comb_where_ints_start_at_1()
import fs.mathfs.combinatorics.lgi_lexicographical_indices_to_from as lgim
import fs.mathfs.numberfs.numberfunctions as nfs  # nfs.transf_6number12charstr_into_dozenlist


class LgiDBUpdater:

  tablename = sqlc.MS_TABLENAME

  def __init__(self):
    self.nconc_n_dozenstr_tuplelist = []
    self.n_updated = 0
    self.conn = None
    self.cursor = None
    self.process()

  @property
  def fetched_rows(self):
    if not self.nconc_n_dozenstr_tuplelist:
      return 0
    return len(self.nconc_n_dozenstr_tuplelist)

  def fetch_all_rows_as_nconc_n_dozens_not_having_lgi(self):
    """
    Fetches all rows in which field `lexicographicalindex` is null and ds_ord_sor_str is not null
      The purpose is to get all rows that can receive the lexicographicalindex associated
        with the dozen combination
    Example:
      nconc=2679	has dozenstr = '260738511820'
      This dozenstr represents the following ordered number list: [7, 18, 20, 26 38, 51]
      In turn, this number list as a combination has lgi=26158097 (a number above 26MM)
    """
    self.conn = sqlc.get_sqlite_connection()
    sql = f"""SELECT nconc, ds_ord_sor_str FROM {self.tablename}
    WHERE
      lexicographicalindex is null and
      ds_ord_sor_str is not null
    ORDER BY nconc;"""
    print(sql)
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

  def update_lgi_for_a_row_without_it(self, nconc, b0lgisimm):
    sql = f"UPDATE {self.tablename} SET lexicographicalindex = ? WHERE nconc = ?;"
    sqltuplevalues = (b0lgisimm, nconc)
    retval = self.cursor.execute(sql, sqltuplevalues)
    prev_n_upt = self.n_updated
    if retval:
      self.n_updated += 1
    scrmsg = f"Updating lgi={b0lgisimm} for nconc={nconc} | prev={prev_n_upt}, n_upd={self.n_updated}"
    print(scrmsg)

  def update_lgi_for_rows_without_it(self):
    """
    Updates all rows, that having dozens and not have its associated lgi, get it
      ie updates rows setting field lgi if field 'dozenstr' is set

    A note about the 'kind of lgi' is used here:
      This 'kind of lgi' is the b0_simm_idx
      (ie, index starts at 0 and is ascending with the lexicographical ascending combinations)
    (the canonical algorithm does the inverse, ie the indices are descending in relation to the ascending combinations)
    Using the 'simmetrical index':
      the first combination should have lgi = 0
      the last combination should have the highest lgi, ie lgi = total_combinations - 1
      (in the canonical algorithm it's the other way around)
    This can be seen in code:
      dezenas = list(range(1, 7))
      b0_lgi = lgim.calc_lgisimm_b0idx_from_comb_where_ints_start_at_1(dezenas, n_elements=60)
      print(dezenas, b0_lgi)
      dezenas = list(range(55, 61))  # the last combination idem
      b0_lgi = lgim.calc_lgisimm_b0idx_from_comb_where_ints_start_at_1(dezenas, n_elements=60)
      print(dezenas, b0_lgi)

    Another observation (startsat1=True)
    The first combination, in the example above, happens with (n_elements=60, n_slots=6, startsat1=True)
      o1 the startsat1 only exists in the lgi functions, not in the 'IndicesCombinators' classes
      o2 the startsat1 tells the first combination does not start with zero:
        noting:
          n1 with startsat1=False, first combination is [0,1,2]
          n2 with startsat1=True, first combination is [1,2,3] (but only in the lgi functions, not in the combiners)
    """
    self.conn = sqlc.get_sqlite_connection()
    self.cursor = self.conn.cursor()
    if self.fetched_rows == 0:
      print(f"No rows ({self.fetched_rows}) were found. Returning")
      return
    for nconc_n_dozenstr_tuple in self.nconc_n_dozenstr_tuplelist:
      nconc = nconc_n_dozenstr_tuple[0]
      dozens_str = nconc_n_dozenstr_tuple[1]
      dezenas = nfs.transf_6number12charstr_into_dozenlist(dozens_str)
      dezenas.sort()
      b0lgisimm = lgim.calc_lgisimm_b0idx_from_comb_where_ints_start_at_1(dezenas, n_elements=60)
      print('Updating', nconc, dezenas, dozens_str, b0lgisimm)
      self.update_lgi_for_a_row_without_it(nconc, b0lgisimm)

  def db_commit_if_any_update_happened_n_closeconn(self):
    if self.n_updated > 0:
      print(f'committing db with n_updates={self.n_updated} rows')
      self.conn.commit()
    self.conn.close()

  def process(self):
    self.fetch_all_rows_as_nconc_n_dozens_not_having_lgi()
    self.update_lgi_for_rows_without_it()
    self.db_commit_if_any_update_happened_n_closeconn()

  def __str__(self):
    outstr = f"{self.__class__.__name__} fetched_rows={self.fetched_rows} n_updated={self.n_updated}"
    return outstr


def adhoctest():
  lo = LgiDBUpdater()
  print(lo)


def process():
  pass


if __name__ == '__main__':
  adhoctest()
  process()
