#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

'''
# import copy
import numpy
import sys
import localpythonpath
localpythonpath.setlocalpythonpath()
from models.ConcursoSlider import ConcursoSlider
from models.Concurso import ConcursoBase

from sqlalchemy import Column, Integer, Sequence, String, create_engine # BoundMetaData, mapper 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import local_settings as ls
engine_uri = 'sqlite:///' + ls.SQLITE_DATA_FILE_PATH    # abs paths require 4 bars (ie, ////)
engine = create_engine(engine_uri) #, echo=True)

class InconsistentTable(ValueError):
  pass

Base = declarative_base()
class HistFreqDB(Base):

  __tablename__ = 'mshistfreqs' # 'megasena'
  
  nDoConc = Column(Integer, Sequence('mshistfreqs_id_seq'), primary_key=True)
  charfreqs = Column(String(300)) # 5*60 = 300
  N_DE_DEZENAS_NO_VOLANTE = 60
  histfreq = None
  
  def __init__(self):
    self.histfreq = None
  
  def set_histfreq_within_concursorange(self):
    str_freq_array = self.charfreqs.split(';')
    if len(str_freq_array) <> self.N_DE_DEZENAS_NO_VOLANTE:
      error_msg = 'len(str_freq_array)=%d <> self.N_DE_DEZENAS_NO_VOLANTE=%d :: freq array = %s' %(len(str_freq_array), self.N_DE_DEZENAS_NO_VOLANTE, str_freq_array)
      raise ValueError, error_msg
    self.histfreq = map(int, str_freq_array)
    self.histfreq = numpy.array(self.histfreq)

  def get_histfreq(self):
    if self.histfreq == None:
      self.set_histfreq_within_concursorange()
    return self.histfreq
  
  def set_charfreqs(self, p_histfreq, nDoConc):
    str_freq_array = map(str, p_histfreq)
    self.charfreqs  = ';'.join(str_freq_array)
    self.nDoConc = nDoConc

  def __repr__(self):
    return '<%d %s>' %(self.nDoConc, self.get_histfreq())

class HistFreqDBSlider(object):
  '''
  This class reads individual histfreq arrays and is capable of inserting a bulk of histfreq arrays via a db-transaction

  Notice:
     It's important to notice that this class does not trigger histfreqs update on its own, due to the dependency the update
    class has upon this one. (Otherwise one class would call the other ad infinitum, resulting in a deadlock.)
    However, get_histfreq_at(nDoConc) returns None when the corresponding histfreq is not found.
    The caller can then decide to trigger the update class if context is appropriate (ie, if count() for both tables do differ),
    which will update histfreqs and, after that, the caller may retry get_histfreq_at(nDoConc) just a second time.
  '''
  def __init__(self):
    Session = sessionmaker(bind=engine)
    self.session = Session()

  def get_total_histfreqs(self):
    return self.session.query(HistFreqDB).count()
  
  def get_histfreq_at(self, nDoConc):
    result_set = self.session.query(HistFreqDB).filter( HistFreqDB.nDoConc == nDoConc )
    if result_set.count() == 0:
      return None 
    elif result_set.count() == 1:
      histfreqdb = result_set[0]
      return histfreqdb.get_histfreq()
    # if program flow got to here, more than 1 record returned, raise an exception explaining the fact 
    error_msg = 'nDoConc [nº do concurso) is not unique in db-table : HistFreqDB :: %d records returned' %result_set.count()
    raise InconsistentTable, error_msg
  
  def update_histfreqs(self, histfreqdbs_to_update):
    for histfreqdb in histfreqdbs_to_update:
      print 'Updating histfreqdb', histfreqdb
      self.session.add(histfreqdb)
    self.session.commit()

class HistFreqUpdater(object):
  '''
  '''
  def __init__(self): # concurso_range
    self.concursoSlider = ConcursoSlider(ConcursoBase)
    self.histfreqdbslider = HistFreqDBSlider()
    self.update_db_if_needed()
    self.verify_histfreqs_consistency()

  def update_db_if_needed(self):
    self.total_concursos = self.concursoSlider.get_total_concursos()
    self.last_n_histfreq_updated = self.histfreqdbslider.get_total_histfreqs()
    n_missing_histfreqs = self.total_concursos - self.last_n_histfreq_updated 
    if n_missing_histfreqs < 0:
      error_msg = 'Inconsistent histfreqs size. It is greater than concursos.  Program execution cannot continue.'
      raise IndexError, error_msg
    elif n_missing_histfreqs == 0:
      # nothing to do! Sizes match.
      return
    print 'Need to update %d hist-freq concursos (from %d to %d)' %(n_missing_histfreqs, self.last_n_histfreq_updated, self.total_Concursos)
    self.update_histfreqs_from_last_updated()
       
  def update_histfreqs_from_last_updated(self):
    histfreqdbs_to_update = []
    if self.last_n_histfreq_updated == 0:
      numpy_histfreq = numpy.zeros(60,int)
    else:
      numpy_histfreq = self.histfreqdbslider.get_histfreq_at(self.last_n_histfreq_updated)
    for nDoConc in range(self.last_n_histfreq_updated + 1, self.total_jogos + 1):
      jogo = self.jogoSlider.get_jogo_by_nDoConc(nDoConc)
      for dezena in jogo.get_dezenas():
        index = dezena - 1 
        numpy_histfreq[index] += 1 
      histfreqdb = HistFreqDB()
      histfreqdb.set_charfreqs(numpy_histfreq, nDoConc)
      histfreqdbs_to_update.append(histfreqdb)
    self.histfreqdbslider.update_histfreqs(histfreqdbs_to_update)

  def verify_histfreqs_consistency(self):
    print 'About to verify histfreqs consistency of %d concursos : Please, wait. ' %(self.total_concursos)  
    numpy_histfreq = numpy.array([0]*60)
    for nDoConc in range(1, self.total_concursos + 1):
      jogo = self.concursoSlider.get_concurso_by_nDoConc(nDoConc)
      for dezena in jogo.get_dezenas():
        index = dezena - 1 
        numpy_histfreq[index] += 1
      self.compare_calc_histfreq_with_db(nDoConc, numpy_histfreq)
    print 'Verified histfreqs consistency of %d concursos : ok! ' %(self.total_concursos)  
    
  def compare_calc_histfreq_with_db(self, nDoConc, numpy_histfreq):
    histfreqdb = self.histfreqdbslider.get_histfreq_at(nDoConc)
    bool_array = histfreqdb == numpy_histfreq
    # unfortunately, comparison of numpy arrays should compare element by element
    # old implementation 
    # one_to_one = zip(histfreqdb, numpy_histfreq)
    # for pair in one_to_one:
      # if pair[0] != pair[1]:
    if False in bool_array:
      error_msg = ' at nDoConc=%d histfreqdb != numpy_histfreq \n db = %s \n calculated = %s' %(nDoConc, histfreqdb, numpy_histfreq)
      raise ValueError, error_msg
      

def adhoc_test2():
  Session = sessionmaker(bind=engine)
  session = Session()
  # metadata = BoundMetaData(engine)
  # tablehistfreqs = Table('mshistfreqs', metadata, autoload=True)
  # mapper(DBHistFreq, tablehistfreqs)  
  histfreqDb = HistFreqDB()
  nDoConc = 1 
  freq_array = ['1']*60
  histfreqDb.set_charfreqs(freq_array, nDoConc)
  print 'session add', histfreqDb 
  session.add(histfreqDb)
  session.commit()

def adhoc_test():
  print 'Running (Updating) HistFreqUpdater() '
  HistFreqUpdater()

def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
