#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''
import sys


import __init__
__init__.setlocalpythonpath()

from fs.jogos import volante_functions

class VolanteCharacteristics(object):

  DEFAULT_N_DEZENAS_NO_SORTEIO = 6
  DEFAULT_N_DEZENAS_NO_VOLANTE = 60
  DEFAULT_INT_RANGE = (1, 60)
  DEFAULT_NOME = 'Megasena'
  
  def __init__(self, n_dezenas_no_volante=None, n_dezenas_no_sorteio=None, int_range=None, nome=None):
    self.set_n_dezenas_no_volante(n_dezenas_no_volante)
    self.set_n_dezenas_no_sorteio(n_dezenas_no_sorteio)
    self.set_int_range(int_range)
    self.set_nome(nome) 
    
  def set_n_dezenas_no_volante(self, n_dezenas_no_volante):
    if n_dezenas_no_volante == None:
      self.n_dezenas_no_volante = self.DEFAULT_N_DEZENAS_NO_VOLANTE
      return
    try:
      int(n_dezenas_no_volante)
    except ValueError:
      self.n_dezenas_no_volante = self.DEFAULT_N_DEZENAS_NO_VOLANTE
      return
    if n_dezenas_no_volante < 1:
      raise ValueError, 'n_dezenas_no_volante (=%d) < 1 ' %(n_dezenas_no_volante)
    self.n_dezenas_no_volante = n_dezenas_no_volante
  
  def set_n_dezenas_no_sorteio(self, n_dezenas_no_sorteio):
    if n_dezenas_no_sorteio == None:
      self.n_dezenas_no_sorteio = self.DEFAULT_N_DEZENAS_NO_SORTEIO
      return
    try:
      int(n_dezenas_no_sorteio)
    except ValueError:
      self.n_dezenas_no_sorteio = self.DEFAULT_N_DEZENAS_NO_SORTEIO
      return
    if n_dezenas_no_sorteio > self.n_dezenas_no_volante:
      raise ValueError, 'n_dezenas_no_sorteio (=%d) > n_dezenas_no_volante (=%d) ' %(n_dezenas_no_sorteio, self.n_dezenas_no_volante)
    if n_dezenas_no_sorteio < 1:
      raise ValueError, 'n_dezenas_no_sorteio (=%d) < 1 ' %(n_dezenas_no_sorteio)
    self.n_dezenas_no_sorteio = n_dezenas_no_sorteio
    
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
  print vc1
  vc2 = VolanteCharacteristics(n_dezenas_no_volante=50, n_dezenas_no_sorteio=5, int_range=(1,50), nome='Quina')
  print vc2
  vc2.equal_attributes_as(vc1)
  print vc2

def process():
  vc1 = VolanteCharacteristics()
  print vc1

import unittest
class MyTest(unittest.TestCase):

  def return_quina_4tuple(self):
    n_dezenas_no_volante = 50;  n_dezenas_no_sorteio = 5;  int_range = (1, 50);  nome = 'Quina'
    return n_dezenas_no_volante, n_dezenas_no_sorteio, int_range, nome

  def setUp(self):
    self.vc_sena_default = VolanteCharacteristics()
    n_dezenas_no_volante, n_dezenas_no_sorteio, int_range, nome = self.return_quina_4tuple()
    self.vc_quina = VolanteCharacteristics(n_dezenas_no_volante, n_dezenas_no_sorteio, int_range, nome)

  def test_1_megasena_is_default(self):
    # subtest 1
    self.assertEquals(self.vc_sena_default.n_dezenas_no_sorteio, VolanteCharacteristics.DEFAULT_N_DEZENAS_NO_SORTEIO)
    # subtest 2
    self.assertEquals(self.vc_sena_default.n_dezenas_no_volante, VolanteCharacteristics.DEFAULT_N_DEZENAS_NO_VOLANTE)
    # subtest 3
    self.assertEquals(self.vc_sena_default.int_range, VolanteCharacteristics.DEFAULT_INT_RANGE)
    # subtest 4
    self.assertEquals(self.vc_sena_default.nome, VolanteCharacteristics.DEFAULT_NOME)
    text = str(self.vc_sena_default)
    # subtest 5
    self.assertIn(VolanteCharacteristics.DEFAULT_NOME, text)
    # subtest 6
    self.assertIn(str(VolanteCharacteristics.DEFAULT_N_DEZENAS_NO_SORTEIO), text)
    # subtest 7
    self.assertIn(str(VolanteCharacteristics.DEFAULT_N_DEZENAS_NO_VOLANTE), text)
    # subtest 8
    self.assertTrue(self.vc_sena_default.has_same_attributes_of(self.vc_sena_default))
    # subtest 9
    self.assertFalse(self.vc_sena_default.has_same_attributes_of(self.vc_quina))

  def test_2_quina_is_quina(self):
    n_dezenas_no_volante, n_dezenas_no_sorteio, int_range, nome = self.return_quina_4tuple()
    # subtest 1
    self.assertEquals(self.vc_quina.n_dezenas_no_sorteio, n_dezenas_no_sorteio)
    # subtest 2
    self.assertEquals(self.vc_quina.n_dezenas_no_volante, n_dezenas_no_volante)
    # subtest 3
    self.assertEquals(self.vc_quina.int_range, int_range)
    # subtest 4
    self.assertEquals(self.vc_quina.nome, nome)
    text = str(self.vc_quina)
    # subtest 5
    self.assertIn(nome, text)
    # subtest 6
    self.assertIn(str(n_dezenas_no_sorteio), text)
    # subtest 7
    self.assertIn(str(n_dezenas_no_volante), text)
    # subtest 8
    self.assertTrue(self.vc_quina.has_same_attributes_of(self.vc_quina))
    # subtest 9
    self.assertFalse(self.vc_quina.has_same_attributes_of(self.vc_sena_default))

  def test_3_change_attributes_work(self):
    vc3 = VolanteCharacteristics()
    # subtest 1
    self.assertTrue(vc3.has_same_attributes_of(self.vc_sena_default))
    # subtest 2
    self.assertFalse(vc3.has_same_attributes_of(self.vc_quina))
    # switch it to quina
    vc3.incorporate_attributes_of(self.vc_quina)
    # subtest 3
    self.assertFalse(vc3.has_same_attributes_of(self.vc_sena_default))
    # subtest 4
    self.assertTrue(vc3.has_same_attributes_of(self.vc_quina))
    # switch it again to megasena
    vc3.incorporate_attributes_of(self.vc_sena_default)
    # subtest 5 == # subtest 1
    self.assertTrue(vc3.has_same_attributes_of(self.vc_sena_default))
    # subtest 6 == # subtest 2
    self.assertFalse(vc3.has_same_attributes_of(self.vc_quina))

  def test_4_raise_ValueError_against_some_inconsistent_attribvalues(self):
    '''
    self.assertRaises(ValueError, VolanteCharacteristics.__init__, cls=VolanteCharacteristics, n_dezenas_no_volante=0)

    Returns: None

    '''
    # unfortunately, we cannot test n_dezenas_no_volante=0 directly because n_dezenas_no_sorteio will default to the Megasena one, and the error caught will be the comparison one (ie, n_dezenas_no_sorteio > n_dezenas_no_volante); not exactly n_dezenas_no_volante = 0; however, ValueError must be raised
    ValueError_raised = False
    try:
      VolanteCharacteristics(n_dezenas_no_volante=0)
    except ValueError: # ValueError will be caught, because not directly because of n_dezenas_no_volante=0, but because n_dezenas_no_sorteio > n_dezenas_no_volante (ie, 6 > 0)
      ValueError_raised = True
    # subtest 1
    self.assertTrue(ValueError_raised)

    # VolanteCharacteristics(n_dezenas_no_volante='a') does NOT raise ValueError, otherwise, it sets attribute to DEFAULT
    ValueError_raised = False
    vc = None
    try:
      vc = VolanteCharacteristics(n_dezenas_no_volante='a')
    except ValueError:
      ValueError_raised = True
    # subtest 2
    self.assertFalse(ValueError_raised)
    # subtest 3
    self.assertEquals(vc.n_dezenas_no_volante, VolanteCharacteristics.DEFAULT_N_DEZENAS_NO_VOLANTE)

    # VolanteCharacteristics(n_dezenas_no_sorteio='a')) does NOT raise ValueError, otherwise, it sets attribute to DEFAULT
    ValueError_raised = False
    vc = None
    try:
      vc = VolanteCharacteristics(n_dezenas_no_sorteio='a')
    except ValueError:
      ValueError_raised = True
    # subtest 4
    self.assertFalse(ValueError_raised)
    # subtest 5
    self.assertEquals(vc.n_dezenas_no_sorteio, VolanteCharacteristics.DEFAULT_N_DEZENAS_NO_SORTEIO)

    # next assert is an inconsistency of having n_dezenas_no_sorteio=2 > n_dezenas_no_volante=1
    # self.assertRaises(ValueError, VolanteCharacteristics(n_dezenas_no_sorteio=2, n_dezenas_no_volante=1))
    ValueError_raised = False
    try:
      VolanteCharacteristics(n_dezenas_no_sorteio=2, n_dezenas_no_volante=1)
    except ValueError:
      ValueError_raised = True
    # subtest 6
    self.assertTrue(ValueError_raised)

    # n_dezenas_no_sorteio=0 must raise ValueError
    ValueError_raised = False
    try:
      VolanteCharacteristics(n_dezenas_no_sorteio=0)
    except ValueError:
      ValueError_raised = True
    # subtest 7
    self.assertTrue(ValueError_raised)

    # int_range = ('a', 1) will not raise an exception, it will otherwise equal int_range to the default
    default_int_range_to = (1,10); int_range = ('a', 1)
    int_range = volante_functions.return_int_range_or_default_or_raise_ValueError(int_range,default_int_range_to)
    # subtest 8
    self.assertEquals(int_range, default_int_range_to)

    # int_range = (2, 1) must raise ValueError in the private function used by the VolanteCharacteristics's Constructor; reason: 2 > 1, ie, first element is greater than the second one
    int_range = (2, 1)
    # subtest 9
    self.assertRaises(ValueError, volante_functions.return_int_range_or_default_or_raise_ValueError, int_range, default_int_range_to)

    # The same test as above, but now via the VolanteCharacteristics's Constructor
    # self.assertRaises(ValueError, VolanteCharacteristics(int_range=(2,1)))
    ValueError_raised = False
    try:
      VolanteCharacteristics(int_range=(2,1))
    except ValueError:
      ValueError_raised = True
    # subtest 10
    self.assertTrue(ValueError_raised)


def look_up_cli_params_for_tests_or_processing():
  if len(sys.argv) < 2:
    process()
    return
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()
    elif arg.startswith('-u'):
      # unittest complains if argument is available, so remove it from sys.argv
      del sys.argv[1]
      unittest.main()
    elif arg.startswith('-p'):
      process()

if __name__ == '__main__':
  look_up_cli_params_for_tests_or_processing()
