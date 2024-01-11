#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
import sys
from fs.jogosfs import volante_functions


class VolanteCharacteristics(object):

  DEFAULT_N_DEZENAS_NO_SORTEIO = 6
  DEFAULT_N_DEZENAS_NO_VOLANTE = 60
  DEFAULT_INT_RANGE = (1, 60)
  DEFAULT_NOME = 'Megasena'

  def __init__(self, n_dezenas_no_volante=None, n_dezenas_no_sorteio=None, int_range=None, nome=None):
    self.n_dezenas_no_volante = n_dezenas_no_volante
    self.treat_n_dezenas_no_volante(n_dezenas_no_volante)
    self.set_n_dezenas_no_sorteio(n_dezenas_no_sorteio)
    self.set_int_range(int_range)
    self.set_nome(nome) 
    
  def treat_n_dezenas_no_volante(self):
    if self.n_dezenas_no_volante is None:
      self.n_dezenas_no_volante = self.DEFAULT_N_DEZENAS_NO_VOLANTE
      return
    try:
      int(self.n_dezenas_no_volante)
    except ValueError:
      self.n_dezenas_no_volante = self.DEFAULT_N_DEZENAS_NO_VOLANTE
      return
    if self.n_dezenas_no_volante < 1:
      errmsg = 'n_dezenas_no_volante (=%d) < 1 ' % self.n_dezenas_no_volante
      raise ValueError(errmsg)

  def set_n_dezenas_no_sorteio(self, n_dezenas_no_sorteio):
    if n_dezenas_no_sorteio is None:
      self.n_dezenas_no_sorteio = self.DEFAULT_N_DEZENAS_NO_SORTEIO
      return
    try:
      int(n_dezenas_no_sorteio)
    except ValueError:
      self.n_dezenas_no_sorteio = self.DEFAULT_N_DEZENAS_NO_SORTEIO
      return
    if n_dezenas_no_sorteio > self.n_dezenas_no_volante:
      errmsg = 'n_dezenas_no_sorteio (=%d) > n_dezenas_no_volante (=%d) ' % self.n_dezenas_no_volante
      raise ValueError(errmsg)
    if n_dezenas_no_sorteio < 1:
      errmsg = 'n_dezenas_no_sorteio (=%d) < 1 ' % (self.n_dezenas_no_sorteio)
      raise ValueError(errmsg)

  def set_int_range(self, int_range):
    self.int_range = volante_functions.return_int_range_or_default_or_raise_ValueError(int_range, self.DEFAULT_INT_RANGE)

  def set_nome(self, nome):
    if nome == None or type(nome) not in [str, unicode]:
      self.nome = self.DEFAULT_NOME
      return
    self.nome = nome
    
  def incorporate_attributes_of(self, volante_caract):
    if volante_caract == None or type(volante_caract) != VolanteCharacteristics:
      self = VolanteCharacteristics()
      return
    self.n_dezenas_no_volante = volante_caract.n_dezenas_no_volante
    self.n_dezenas_no_sorteio = volante_caract.n_dezenas_no_sorteio
    self.int_range            = volante_caract.int_range
    self.nome                 = volante_caract.nome

  def has_same_attributes_of(self, volante_caract):
    if volante_caract == None or type(volante_caract) != VolanteCharacteristics:
      return False
    if self.n_dezenas_no_volante != volante_caract.n_dezenas_no_volante:
      return False
    if self.n_dezenas_no_sorteio != volante_caract.n_dezenas_no_sorteio:
      return False
    if self.int_range != volante_caract.int_range:
      return False
    if self.nome != volante_caract.nome:
      return False
    return True

  def __str__(self):
    str_dict = {'nome':self.nome,'n_dezenas_no_sorteio':self.n_dezenas_no_sorteio, 'n_dezenas_no_volante':self.n_dezenas_no_volante,'str_int_range':str(self.int_range)}
    outstr = '''Nome = %(nome)s
    N_DEZENAS_NO_SORTEIO = %(n_dezenas_no_sorteio)d
    N_DEZENAS_NO_VOLANTE = %(n_dezenas_no_volante)d
    INT_RANGE = %(str_int_range)s''' %str_dict
    return outstr


def adhoc_test():
  vc1 = VolanteCharacteristics()
  print(vc1)
  vc2 = VolanteCharacteristics(n_dezenas_no_volante=50, n_dezenas_no_sorteio=5, int_range=(1,50), nome='Quina')
  print(vc2)
  vc2.equal_attributes_as(vc1)
  print(vc2)


def process():
  vc1 = VolanteCharacteristics()
  print(vc1)


if __name__ == '__main__':
  process()
  adhoc_test()
