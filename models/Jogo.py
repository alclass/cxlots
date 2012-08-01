#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import datetime,
import copy, sys

from sqlalchemy import Column, Date, Integer, Sequence, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker

Column(Integer, Sequence('user_id_seq'), primary_key=True)

Base = declarative_base()

sys.path.insert(0, '..')
import local_settings as ls


Base = declarative_base()
# abs paths require 4 bars (ie, ////)
engine_uri = 'sqlite:///' + ls.SQLITE_DATA_FILE_PATH
engine = create_engine(engine_uri) #, echo=True)
#print 'engine_uri', engine_uri 

str02lambda = lambda digit : str(digit).zfill(2)

# sys.exit(0)

class InconsistentTable(ValueError):
  pass

class Jogo(Base):

  __tablename__ = 'ms' # 'megasena'
  
  # id = Column(Integer, Sequence('ms_id_seq'), primary_key=True)
  nDoConc = Column(Integer, Sequence('ms_id_seq'), primary_key=True)
  # id = nDoConc
  jogoCharOrig = Column(String(12))
  #strdezenas = jogoCharOrig
  date = Column(Date(8))
  #dataDeSorteio = date
  N_DE_DEZENAS = 6
  dezenas = None
  dezenas_in_orig_order = None

  def __init__(self):
    self.dezenas = []
    self.dezenas_in_orig_order = []
  
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

  def __repr__(self):
    return "Jogo %d [%s]" % (self.nDoConc, self.get_dezenas_str())


def adhoc_test():
  pass

def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
