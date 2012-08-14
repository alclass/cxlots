#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import datetime,
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import localpythonpath
localpythonpath.setlocalpythonpath()

from maths.combinatorics.algorithmsForCombinatorics import permute
from lib import lambdas

import local_settings as ls
engine_uri = 'sqlite:///' + ls.SQLITE_DATA_FILE_PATH # abs paths require 4 bars (ie, ////)
engine = create_engine(engine_uri) #, echo=True)

class InconsistentTable(ValueError):
  pass

class ConcursoSlider(object):
  
  def __init__(self, classref):
    self.CLASSREF = classref
    Session = sessionmaker(bind=engine)
    self.session = Session() 

  def get_all_concursos(self):
    return self.session.query(self.CLASSREF).all()

  def get_total_concursos(self):
    return self.session.query(self.CLASSREF).count()
  
  def get_n_last_concurso(self):
    '''
    to be CHANGED as soon as I can (it involves learning/knowing how to query max(nDoConc) -- must be simple!)
    '''
    return self.get_total_concursos()
    
  def get_last_concurso(self):
    nDoConc = self.get_total_concursos()
    if nDoConc == None or nDoConc == 0:
      return None
    return self.get_concurso_by_nDoConc(nDoConc)
  
  def get_concurso_by_nDoConc(self, nDoConc=None):
    '''
    Convention: is nDoConc is None, last jogo is returned
    '''
    if nDoConc == None:
      return self.get_last_concurso()
    result_set = self.session.query(self.CLASSREF).filter( self.CLASSREF.nDoConc == nDoConc )
    if result_set.count() == 0:
      return None 
    elif result_set.count() == 1:
      return result_set[0]
    error_msg = 'nDoConc [nº do concurso) is not unique in db-table :: %d records returned' %result_set.count()
    raise InconsistentTable, error_msg

  def get_concurso_by_jogoCharOrig(self, jogoCharOrig):
    result_set = self.session.query(self.CLASSREF).filter( self.CLASSREF.jogoCharOrig == jogoCharOrig )
    if result_set.count() == 0:
      return None 
    elif result_set.count() == 1:
      return result_set[0]
    error_msg = 'nDoConc [nº do concurso) is not unique in db-table :: %d records returned' %result_set.count()
    raise InconsistentTable, error_msg

  def get_concursos_by_date_range(self, data_ini, data_fim):
    result_set = self.session.query(self.CLASSREF).filter(self.CLASSREF.date >= data_ini, self.CLASSREF.date <= data_fim)
    return result_set

  def get_concursos_by_dezenas(self, dezenas):
    jogoCharOrig_list = derive_all_concursos_with_dezenas(dezenas)
    concursos = []
    for jogoCharOrig in jogoCharOrig_list:
      concurso = self.get_concurso_by_jogoCharOrig(jogoCharOrig)
      if concurso == None:
        continue
      concursos.append(concurso)
    return concursos

  def get_concursos_by_dezenas_subset(self, dezenas):
    if len(dezenas) == self.CLASSREF.N_DE_DEZENAS:
      return self.get_concursos_by_dezenas(dezenas)
    elif len(dezenas) > self.CLASSREF.N_DE_DEZENAS:
      raise ValueError, 'error'
    concursos = self.get_all_concursos()
    found_concursos = []
    for concurso in concursos:
      #print 'concurso', concurso
      include_concurso = True
      for dezena in dezenas:
        if dezena not in concurso.get_dezenas():
          include_concurso = False
          break
      if include_concurso:
        found_concursos.append(concurso)
    return found_concursos

  def bulk_insert(self, concursos_to_insert):
    for concurso in concursos_to_insert:
      print 'Updating concurso', concurso
      self.session.add(concurso)
    self.session.commit()

# import maths.combinatorics.algorithmsForCombinatorics as combinatorics
def derive_all_concursos_with_dezenas(dezenas):
  permuted_jogos = permute(dezenas)
  jogoCharOrig_list = []
  for dezenas in permuted_jogos:
    dezenas_str = ''.join(map(lambdas.str02lambda, dezenas))
    jogoCharOrig_list.append(dezenas_str)
  return jogoCharOrig_list

def adhoc_test():
  exec('from models.Concurso import ConcursoBase')
  exec('classref = ConcursoBase') #eval('ConcursoHTML')
  classref = eval('classref')
  cs = ConcursoSlider(classref)
  concurso = cs.get_concurso_by_nDoConc(100)  #[0]
  print '100 ==>>', concurso
  #dezenas = concurso.get_dezenas_in_orig_order()
  # dezenas = copy.copy(concurso.get_dezenas())
  # dezenas.pop(); dezenas.pop(); dezenas.pop()
  # dezenas = [4, 15, 27]
  dezenas = [4, 17]
  # concursos = js.get_concursos_by_dezenas(dezenas)
  concursos = cs.get_concursos_by_dezenas_subset(dezenas)   
  print 'cs.get_concursos_by_dezenas_subset(%s)' %str(dezenas)
  #print 'concursos', concursos
  for concurso in concursos:
    print 'found', concurso
  print 'len(concursos)', len(concursos)

def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
