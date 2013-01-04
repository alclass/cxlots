#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import datetime,
# import copy
import sys

from sqlalchemy import Column, Date, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base

import localpythonpath
localpythonpath.setlocalpythonpath()

from ConcursoSlider import ConcursoSlider

Base = declarative_base()
class ConcursoBase(Base):

  __tablename__ = 'ms' # 'megasena'
  
  nDoConc = Column(Integer, Sequence('ms_id_seq'), primary_key=True)
  # id = nDoConc
  jogoCharOrig = Column(String(12))
  date = Column(Date(8))   #dataDeSorteio = date
  N_DE_DEZENAS = 6
  N_DE_DEZENAS_NO_VOLANTE = 60
  dezenas = None
  dezenas_in_orig_order = None
  concursoSlider = None

  def __init__(self):
    self.dezenas = []
    self.dezenas_in_orig_order = []
    self.set_concursoSlider()
  
  def set_concursoSlider(self):
    if self.concursoSlider == None:
      self.concursoSlider = ConcursoSlider(self.__class__)  
  
  def get_all_concursos(self):
    self.set_concursoSlider()
    if self.concursoSlider != None:
      return self.concursoSlider.get_all_concursos()
    return []

  def get_last_concurso(self):
    self.set_concursoSlider()
    if self.concursoSlider != None:
      return self.concursoSlider.get_last_concurso()
    return None

  def get_n_last_concurso(self):
    last_concurso = self.get_last_concurso()
    if last_concurso != None:
      return last_concurso.nDoConc
    return 0
  
  def set_dezenas_in_orig_order(self):
    if len(self.jogoCharOrig) <> self.N_DE_DEZENAS * 2:
      error_msg = 'jogoCharOrig has not size %d [%s has size %d]' %(self.N_DE_DEZENAS * 2, self.jogoCharOrig, len(self.jogoCharOrig))
      raise ValueError, error_msg
    self.dezenas_in_orig_order = []
    for pos in range(0, 12, 2):
      dezena = int( self.jogoCharOrig[pos : pos+2] )
      self.dezenas_in_orig_order.append(dezena)
    
  def get_dezenas_in_orig_order(self):
    if self.dezenas_in_orig_order == None:
      self.set_dezenas_in_orig_order()
      if self.dezenas_in_orig_order == None:
        error_msg = 'Unable to derive jogoCharOrig [=%s] into dezenas_in_orig_order ' %(self.jogoCharOrig)
        raise ValueError, error_msg
    return self.dezenas_in_orig_order

  def set_dezenas(self):
    self.dezenas = self.get_dezenas_in_orig_order()
    if self.dezenas == None: 
      error_msg = 'Unable to derive dezenas from dezenas_in_orig_order :: jogoCharOrig [=%s] ' %(self.jogoCharOrig)
      raise ValueError, error_msg
    # need to hard copy it
    self.dezenas = self.dezenas[:]
    self.dezenas.sort()

  def get_dezenas(self):
    if self.dezenas == None:
      self.set_dezenas()
    return self.dezenas

  def get_dezenas_str(self, in_orig_order=False):
    if in_orig_order:
      dezenas = self.get_dezenas_in_orig_order()
    else:
      dezenas = self.get_dezenas()
    dezenas_str  = ' '.join(map(str02lambda, dezenas))
    return dezenas_str
  
  def get_previous(self):
    if self.nDoConc <= 2:
      return None
    self.set_concursoSlider()    
    return self.concursoSlider.get_concurso_by_nDoConc(self.nDoConc - 1)
  
  def get_next(self):
    self.set_concursoSlider()    
    if self.concursoSlider != None:
      if self.nDoConc >= self.get_n_last_concurso():
        return None    
      return self.concursoSlider.get_concurso_by_nDoConc(self.nDoConc + 1)
    return None

  def get_concurso_by_nDoConc(self, nDoConc_to_compare=None):
    self.set_concursoSlider()    
    if self.concursoSlider != None:
      return self.concursoSlider.get_concurso_by_nDoConc(nDoConc_to_compare)
    return None

  def get_total_concursos(self):
    self.set_concursoSlider()    
    if self.concursoSlider != None:
      return self.concursoSlider.get_total_concursos()
    try:
      int(self.nDoConc)
      return 1
    except ValueError:
      pass
    return 1

  def __repr__(self):
    return "Concurso %d [%s]" % (self.nDoConc, self.get_dezenas_str())

str02lambda = lambda digit : str(digit).zfill(2)

def adhoc_test():
  pass

import unittest
class MyTest(unittest.TestCase):

  def test_nDoConc_sequentiallity(self):
    pass
  
def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()
    elif arg.startswith('-u'):
      # unittest complains if argument is available, so remove it from sys.argv
      del sys.argv[1]
      unittest.main()


if __name__ == '__main__':
  look_for_adhoctest_arg()
