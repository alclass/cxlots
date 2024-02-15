#!/usr/bin/env python3
"""
fs/jogosfs/jogos_metrics.py
  Calculates the available / planned metrics for a drawn n-dozens cardgame.

The n in n-dozen mostly used here is 6 as the MS has 6 drawn dozens for each 'conccur'.

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

TO-DO: unit-tests!
"""
import fs.jogosfs.jogos_functions as jf
import fs.datefs.date_functions as dtfs


class JogoMetrics:
  NDOZENS = 6

  def __init__(self, nconc, concdate, tupledezenas):
    self.diag_matrix = jf.form_diag_matrix_positions()
    self.nconc = nconc
    self.concdate = dtfs.transform_bar_ddmmyyyy_date_into_datetime(concdate)
    self._tup_dez_ord_sor = None
    self._tupledezenas = None
    self._ds_ord_sor_str = None
    self.d1, self.d2, self.d3, self.d4, self.d5, self.d6 = tuple([-1]*self.NDOZENS)
    self.n_dezenas = -1
    self.treat_dezenas(tupledezenas)
    self.colpatt = ''
    self.diagpatt = ''
    self.gather_metrics()

  @property
  def ds_ord_sor_str(self):
    if self._ds_ord_sor_str is None:
      strds = map(lambda e: str(e).zfill(2), list(self.tup_dez_ord_sor))
      self._ds_ord_sor_str = ''.join(strds)
    return self._ds_ord_sor_str

  @property
  def tupledezenas(self):
    if self._tupledezenas is None:
      self._tupledezenas = (self.d1, self.d2, self.d3, self.d4, self.d5, self.d6)
    return self._tupledezenas

  def treat_dezenas(self, tupledezenas):
    """
      self.d1, self.d2, self.d3, self.d4, self.d5, self.d6 = tuple([-1] * self.NDOZENS)

    Args:
      tupledezenas:

    Returns:  None
    """
    for i, dozen in enumerate(tupledezenas):
      fieldname = 'self.d' + str(i+1)  # notice that d1 is tupledezenas[0] ie the first is index+1
      assignment_comm = fieldname + ' = int(tupledezenas[' + str(i) + '])'
      self.n_dezenas += 1
      try:
        exec(assignment_comm)
      except ValueError:
        pass

  @property
  def dezenas_list(self):
    return list(self.tupledezenas)

  @property
  def tup_dez_ord_sor(self):
    """
    Returns the dozends n-tuple
      In MS, it's a 6-tuple with integers from 1 to 60
    """
    if self._tup_dez_ord_sor is None:
      self._tup_dez_ord_sor = self.d1, self.d2, self.d3, self.d4, self.d5, self.d6
    return self._tup_dez_ord_sor

  @property
  def jogo(self):
    """
    Same as @property tup_dez_ord_sor()

    """
    return self.tup_dez_ord_sor

  def gather_metrics(self):
    """

    Returns:

    """
    # n pares
    # diag
    if self.d1 > -1:
      self.colpatt = jf.get_column_pattern(self.jogo)
      self.diagpatt = jf.get_diag_n_for_dozen(self.jogo, self.diag_matrix)

  def __str__(self):
    outstr = f"""Jogo Metrics nconc={self.nconc} dz={self.jogo}
    coluna pattern {self.colpatt}
    diagonal pattern {self.diagpatt}
    """
    return outstr


def adhoctest():
  pass


def process():
  pass


if __name__ == '__main__':
  adhoctest()
  process()
