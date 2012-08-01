#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import datetime,
import sys

from sqlalchemy import Column, Date, Integer, Sequence, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Column(Integer, Sequence('user_id_seq'), primary_key=True)

Base = declarative_base()

sys.path.insert(0, '..')
import local_settings as ls
#from models.Jogo import Jogo
from Jogo import Jogo

Base = declarative_base()
# abs paths require 4 bars (ie, ////)
engine_uri = 'sqlite:///' + ls.SQLITE_DATA_FILE_PATH
engine = create_engine(engine_uri) #, echo=True)
#print 'engine_uri', engine_uri 

str02lambda = lambda digit : str(digit).zfill(2)

# sys.exit(0)

class InconsistentTable(ValueError):
  pass


class JogoSlider(object):
  
  def __init__(self):
    Session = sessionmaker(bind=engine)
    self.session = Session() 

  def get_all_jogos(self):
    return self.session.query(Jogo).all()

  def get_total_jogos(self):
    return self.session.query(Jogo).count()
  
  def get_jogo_by_nDoConc(self, nDoConc):
    result_set = self.session.query(Jogo).filter( Jogo.nDoConc == nDoConc )
    if result_set.count() == 0:
      return None 
    elif result_set.count() == 1:
      return result_set[0]
    error_msg = 'nDoConc [nº do concurso) is not unique in db-table :: %d records returned' %result_set.count()
    raise InconsistentTable, error_msg

  def get_jogos_by_date_range(self, data_ini, data_fim):
    result_set = self.session.query(Jogo).filter(Jogo.date >= data_ini, Jogo.date <= data_fim)
    return result_set

  def get_jogo_by_jogoCharOrig(self, jogoCharOrig):
    result_set = self.session.query(Jogo).filter( Jogo.jogoCharOrig == jogoCharOrig )
    if result_set.count() == 0:
      return None 
    elif result_set.count() == 1:
      return result_set[0]
    error_msg = 'nDoConc [nº do concurso) is not unique in db-table :: %d records returned' %result_set.count()
    raise InconsistentTable, error_msg

  def get_jogos_by_dezenas(self, dezenas):
    jogoCharOrig_list = derive_all_jogos_with_dezenas(dezenas)
    jogos = []
    for jogoCharOrig in jogoCharOrig_list:
      jogo = self.get_jogo_by_jogoCharOrig(jogoCharOrig)
      if jogo == None:
        continue
      jogos.append(jogo)
    return jogos

  def get_jogos_by_dezenas_subset(self, dezenas):
    if len(dezenas) == Jogo.N_DE_DEZENAS:
      return self.get_jogos_by_dezenas(dezenas)
    elif len(dezenas) > Jogo.N_DE_DEZENAS:
      raise ValueError, 'error'
    jogos = self.get_all_jogos()
    found_jogos = []
    for jogo in jogos:
      #print 'jogo', jogo
      include_jogo = True
      for dezena in dezenas:
        if dezena not in jogo.get_dezenas():
          include_jogo = False
          break
      if include_jogo:
        found_jogos.append(jogo)
    return found_jogos

from maths.combinatorics.algorithmsForCombinatorics import permute
def derive_all_jogos_with_dezenas(dezenas):
  permuted_jogos = permute(dezenas)
  jogoCharOrig_list = []
  for dezenas in permuted_jogos:
    dezenas_str = ''.join(map(str02lambda, dezenas))
    jogoCharOrig_list.append(dezenas_str)
  return jogoCharOrig_list

def adhoc_test():
  '''Session = sessionmaker(bind=engine)
  session = Session() 
  for jogo in session.query(Jogo).all():
    # print jogo.nDoConc, jogo.date, jogo.jogoCharOrig, jogo.get_dezenas_str(), jogo.get_dezenas_in_orig_order() # instance.id,
    # print jogo.nDoConc, jogo.date, jogo.get_dezenas_str(in_orig_order=False), jogo.jogoCharOrig
    print jogo.nDoConc, jogo.get_dezenas_str(in_orig_order=True), jogo.jogoCharOrig
    # print jogo
  js = JogoSlider()
  print '100 ==>>', js.get_jogo_by_nDoConc(100)  #[0]
  data_ini = datetime.date(2010, 7, 1)
  data_fim = datetime.date(2010, 8, 1)
  jogos = js.get_jogos_by_date_range(data_ini, data_fim)
  for jogo in jogos:
    print jogo.nDoConc, jogo.date, jogo.get_dezenas_str()
  jogos = derive_all_jogos_with_dezenas(range(1,7))
    
    '''
  js = JogoSlider()
  jogo = js.get_jogo_by_nDoConc(100)  #[0]
  print '100 ==>>', jogo
  #dezenas = jogo.get_dezenas_in_orig_order()
  # dezenas = copy.copy(jogo.get_dezenas())
  # dezenas.pop(); dezenas.pop(); dezenas.pop()
  # dezenas = [4, 15, 27]
  dezenas = [4, 17]
  # jogos = js.get_jogos_by_dezenas(dezenas)
  jogos = js.get_jogos_by_dezenas_subset(dezenas)   
  #print 'jogos', jogos
  for jogo in jogos:
    print 'found', jogo
  print 'len(jogos)', len(jogos)
  print 'dezenas', dezenas
  

def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
