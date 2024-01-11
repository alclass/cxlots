#!/usr/bin/env python3
"""
fs/jogosfs/jogos_metrics.py
  Calculates the available / planned metrics for a drawn dozens game.
"""
import fs.jogosfs.jogos_functions as jf


class JogoMetrics:
  NDOZENS = 6

  def __init__(self, nconc, tupledezenas):
    self.diag_matrix = jf.form_diag_matrix_positions()
    self.nconc = nconc
    self._tup_dez_ord_sor = None
    self._ds_ord_sor_str = None
    self.d1, self.d2, self.d3, self.d4, self.d5, self.d6 = tuple([-1]*self.NDOZENS)
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
      try:
        exec(assignment_comm)
      except ValueError:
        pass

  @property
  def dezenas(self):
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