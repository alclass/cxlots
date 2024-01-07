#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import datetime,
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import __init__
__init__.setlocalpythonpath()

from maths.combinatorics.combinatoric_algorithms import permute
from fs import system_wide_lambdas as swlambdas

import local_settings as ls
engine_uri = 'sqlite:///' + ls.SQLITE_DATA_FILE_PATH # abs paths require 4 bars (ie, ////)
engine = create_engine(engine_uri) #, echo=True)

class InconsistentTable(ValueError):
  pass

class ConcursoSlider(object):
  
  def __init__(self, classref):
    self.CLASSREF = classref
    self.all_concursos = None
    self.create_session()
    
  def create_session(self):
    Session = sessionmaker(bind=engine)
    self.session = Session() 

  def set_all_concursos(self, refresh=False):
    if self.all_concursos != None and not refresh:
      return
    if self.session == None:
      self.create_session()
    query = self.session.query(self.CLASSREF)
    self.all_concursos = list(query.order_by('nDoConc'))
    # self.check_sequentiality_of_concursos() # 
    # the above method call has been given up as a strategy,
    # this is because, if, in the future, this presumption changed, 
    # code would have to be updated, so let's design it to, when getting concurso by nDoConc,
    # in the case nDoConc is different than concurso.nDoConc, fall back to sql-querying
    # the dict with nDoConc idea was also given up, ie,
    # let the strategy be sql-querying for the right "concurso" 
    if self.all_concursos == None or len(self.all_concursos) == 0:
      self.last_concurso = None
    else: 
      self.last_concurso = self.all_concursos[-1] 

#  def check_sequentiality_of_concursos(self):
#    '''
#    
#    '''
#    self.set_all_concursos()
#    for i, concurso in enumerate(self.all_concursos):
#      sequential = i + 1
#      # print sequential, concurso.nDoConc
#      if sequential != concurso.nDoConc:
#        pass
#        # pass a message to the user?
#        # raise ValueError, 'sequential=%d & concurso.nDoConc=%d are different' %(sequential, concurso.nDoConc)

  def get_all_concursos(self, refresh=False):
    self.set_all_concursos(refresh)
    return self.all_concursos

  def get_total_concursos(self, refresh=False):
    self.set_all_concursos(refresh)
    if self.all_concursos == None:
      return 0
    return len(self.all_concursos)
  
  def get_last_concurso(self, refresh=False):
    self.set_all_concursos(refresh)
    return self.last_concurso

  def get_n_last_concurso(self, refresh=False):
    self.set_all_concursos(refresh)
    if self.last_concurso == None:
      return 0
    return self.last_concurso.n_conc
    
  def get_concurso_by_nDoConc(self, nDoConc=None, refresh=False):
    '''
    Convention: is nDoConc is None, last jogo is returned
    '''
    self.set_all_concursos(refresh)
    if nDoConc == None:
      return self.get_last_concurso()
    if self.all_concursos == None:
      return None
    try:
      int(nDoConc)
    except ValueError:
      # parameter came in not being an int, so return None
      return None
    if nDoConc < 0 or nDoConc > self.get_n_last_concurso():
      return None
    index = nDoConc - 1
    concurso = self.all_concursos[index] 
    if nDoConc == concurso.n_conc:
      # raise ValueError, 'nDoConc=%d pedido é diferente do concurso.nDoConc=%d achado' %(nDoConc, concurso.nDoConc)
      return concurso
    # well, nDoConc != concurso.nDoConc, let's fall back the get it by sql-querying
    result_set = self.session.query(self.CLASSREF).filter(self.CLASSREF.n_conc == nDoConc)
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

# import maths2.combinatorics.algorithmsForCombinatorics as combinatorics
def derive_all_concursos_with_dezenas(dezenas):
  permuted_jogos = permute(dezenas)
  jogoCharOrig_list = []
  for dezenas in permuted_jogos:
    dezenas_str = ''.join(map(swlambdas.zfill2, dezenas))
    jogoCharOrig_list.append(dezenas_str)
  return jogoCharOrig_list

def adhoc_test():
  exec('from models.Concurso import ConcursoBase')
  exec('classref = ConcursoBase') #eval('ConcursoHTML')
  classref = eval('classref')
  slider = ConcursoSlider(classref)
  concurso = slider.get_concurso_by_nDoConc(100)  #[0]
  print '100 ==>>', concurso
  #dezenas = concurso.get_dezenas_in_orig_order()
  # dezenas = copy.copy(concurso.get_dezenas())
  # dezenas.pop(); dezenas.pop(); dezenas.pop()
  # dezenas = [4, 15, 27]
  dezenas = [4, 17]
  # concursos = js.get_concursos_by_dezenas(dezenas)
  concursos = slider.get_concursos_by_dezenas_subset(dezenas)   
  print 'cs.get_concursos_by_dezenas_subset(%s)' %str(dezenas)
  #print 'concursos', concursos
  for concurso in concursos:
    print 'found', concurso
  print 'len(concursos)', len(concursos)
  # slider.check_sequentiality_of_concursos
  print 'last concurso', slider.get_last_concurso()
  print 'n last concurso', slider.get_n_last_concurso()
  print 'total de concursos', slider.get_total_concursos()
  


import unittest
class MyTest(unittest.TestCase):

  def test_1(self):
    pass

def look_up_cli_params_for_tests_or_processing():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()
    elif arg.startswith('-u'):
      # unittest complains if argument is available, so remove it from sys.argv
      del sys.argv[1]
      unittest.main()
    elif arg.startswith('-p'):
      pass
      # process()

if __name__ == '__main__':
  look_up_cli_params_for_tests_or_processing()
