#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import localpythonpath
localpythonpath.setlocalpythonpath()

from models.JogoSlider import JogoSlider

from sqlalchemy import Column, Float, Integer, Sequence, String, create_engine # BoundMetaData, mapper 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import local_settings as ls
engine_uri = 'sqlite:///' + ls.SQLITE_DATA_FILE_PATH    # abs paths require 4 bars (ie, ////)
engine = create_engine(engine_uri) #, echo=True)

class InconsistentTable(ValueError):
  pass

Base = declarative_base()
class MetricsDB(Base):
  '''Métricas:
    1) par-ímpar
    2) soma [1. min, 2. max, 3. vetor sobe-e-desce]
    3) desvio-padrão
    4) histograma evolutivo
    5) não-consecutivos num jogo
    6) Nº de repetições e quantos jogos se passaram para isso
    7) variações linha x coluna (ou Dígito da Esquerda x da Direita)
    
  `nDoConc` smallint(6) NOT NULL,
  `iguaisComOAnterior` tinyint(3) DEFAULT NULL,
  `coincsComOs3Anteriores` tinyint(3) DEFAULT NULL,
  `maxDeIguais` tinyint(3) DEFAULT NULL,
  `maxDeIguaisDistAo1o` smallint(5) DEFAULT NULL,
  `maxDeIguaisOcorrencia` tinyint(3) DEFAULT NULL,
  `iguaisMediaComPassado` float DEFAULT NULL,
  `rem2pattern` char(6) DEFAULT NULL,
  `parParImparImpar` char(6) DEFAULT NULL,
  `rem3pattern` char(6) DEFAULT NULL,
  `rem5pattern` char(6) DEFAULT NULL,
  `rem6pattern` char(6) DEFAULT NULL,
  `colpattern` char(6) DEFAULT NULL,
  `til4pattern` char(4) DEFAULT NULL,
  `til5pattern` char(5) DEFAULT NULL,
  `til6pattern` char(6) DEFAULT NULL,
  `til10pattern` char(10) DEFAULT NULL,
  `til12pattern` char(12) DEFAULT NULL,
  `consecEnc` mediumint(3) DEFAULT NULL,
  `soma1` smallint(5) DEFAULT NULL,
  `soma3` smallint(6) DEFAULT NULL,
  `soma7` smallint(6) DEFAULT NULL,
  `soma15` mediumint(8) DEFAULT NULL,
  `std` float DEFAULT NULL,
  `pathway` smallint(6) DEFAULT NULL,
  `allpaths` smallint(6) DEFAULT NULL,
  `binDecReprSomaDe1s` tinyint(3) DEFAULT NULL,
  `lgiDist` int(11) DEFAULT NULL,
  '''

  __tablename__ = 'msstats' # 'megasena'
  
  nDoConc = Column(Integer, Sequence('ms_id_seq'), primary_key=True)
  N_DE_DEZENAS = 6

  iguaisComOAnterior     = Column(Integer(2))
  coincsComOs3Anteriores = Column(Integer(2))
  maxDeIguais            = Column(Integer(2))
  maxDeIguaisDistAo1o    = Column(Integer(2))
  maxDeIguaisOcorrencia  = Column(Integer(2))
  iguaisMediaComPassado  = Column(Float)
  rem2pattern            = Column(String(6))
  parParImparImpar       = Column(String(4))
  rem3pattern            = Column(String(6))
  rem5pattern            = Column(String(6))
  rem6pattern            = Column(String(6))
  colpattern             = Column(String(10))
  til4pattern            = Column(String(4))
  til5pattern            = Column(String(5))
  til6pattern            = Column(String(6))
  til10pattern           = Column(String(10))
  til12pattern           = Column(String(12))
  consecEnc              = Column(Integer(2))
  soma1                  = Column(Integer(2))
  soma3                  = Column(Integer(3))
  soma7                  = Column(Integer(4))
  soma15                 = Column(Integer(4))
  std                    = Column(Float)
  pathway                = Column(Integer(4))
  allpaths               = Column(Integer(4))
  binDecReprSomaDe1s     = Column(Integer(2))
  lgiDist                = Column(Integer(4))
  
  linColDataStru = None
  linColPatternObj = None
  parImparExcludeList = [0,6]

  have_metrics_been_calculed = None

  def __init__(self):
    self.have_metrics_been_calculed = False

  def set_all_metrics_for(self, nDoConc, reprocess=False):
    if self.have_metrics_been_calculed and not reprocess:
      return
    return self.session.query(MetricsDB).count()


class MetricsDBSlider(object):
  '''
  This class...
  '''
  def __init__(self):
    Session = sessionmaker(bind=engine)
    self.session = Session()

  def get_total_records(self):
    return self.session.query(MetricsDB).count()
  
  def get_metrics_for(self, nDoConc):
    result_set = self.session.query(MetricsDB).filter( MetricsDB.nDoConc == nDoConc )
    if result_set.count() == 0:
      return None 
    elif result_set.count() == 1:
      metricsdb = result_set[0]
      return metricsdb
    # if program flow got to here, more than 1 record returned, raise an exception explaining the fact 
    error_msg = 'nDoConc [nº do concurso) is not unique in db-table : MetricsDB :: %d records returned' %result_set.count()
    raise InconsistentTable, error_msg
  
  def update_histfreqs(self, histfreqdbs_to_update):
    for histfreqdb in histfreqdbs_to_update:
      print 'Updating histfreqdb', histfreqdb
      self.session.add(histfreqdb)
    self.session.commit()


class MetricsUpdater(object):

  def __init__(self):
    self.jogoSlider = JogoSlider()
    self.metricsdbslider = MetricsDBSlider()    

  def update_db_if_needed(self):
    self.total_jogos = self.jogoSlider.get_total_jogos()
    self.last_n_metrics_record_updated = self.metricsdbslider.get_total_records()
    n_missing_metrics_records = self.total_jogos - self.last_n_metrics_record_updated 
    if n_missing_metrics_records < 0:
      error_msg = 'Inconsistent metricsdb size. It is greater than concursos.  Program execution cannot continue.'
      raise IndexError, error_msg
    elif n_missing_metrics_records == 0:
      # nothing to do! Sizes match.
      return
    print 'Need to update %d hist-freq concursos (from %d to %d)' %(n_missing_metrics_records, self.last_n_histfreq_updated, self.total_jogos)
    self.update_histfreqs_from_last_updated()
       
  def update_metricsdb_from_last_updated(self):
    metricsdbs_to_update = []
    for nDoConc in range(self.last_n_metrics_record_updated + 1, self.total_jogos + 1):
      #jogo = self.jogoSlider.get_jogo_by_nDoConc(nDoConc)
      metricsdb = MetricsDB()
      metricsdb.get_metrics_for(nDoConc)
      metricsdbs_to_update.append(metricsdb)
    self.metricsdbslider.update_histfreqs(metricsdbs_to_update)
    

class X:

  def getSomaStats(self):
    if self.somaStats == None:
      self.gatherSomaEtAlStats()
      if self.somaStats == None:
        msg = ' [Metrics] somaStats continues to be None'
        raise ValueError, msg
    #print self.somaObj
    return self.somaStats

  def getStdStats(self):
    if self.stdStats == None:
      self.gatherSomaEtAlStats()
      if self.stdStats == None:
        msg =  ' [Metrics] stdObj continues to be None'
        raise ValueError, msg
    return self.stdStats

  def getLgiStats(self):
    if self.lgiStats == None:
      self.gatherSomaEtAlStats()
      if self.lgiStats == None:
        msg = ' [Metrics] lgiStats continues to be None'
        raise ValueError, msg
    return self.lgiStats

  def gatherSomaEtAlStats(self):
    tuple3 = gatherSomaEtAlStats()
    self.somaStats = tuple3[0]
    self.stdStats  = tuple3[1]
    self.lgiStats  = tuple3[2]

  def getLinColPatternObj(self):
    if self.linColPatternObj == None:
      self.linColPatternObj = LinColPatternObj() # instantiate LinColPatternObj class
      if self.linColPatternObj == None:
        msg = ' [Metrics] linColPatternObj continues to be None'
        raise ValueError, msg
    return self.linColPatternObj
  def getLinColDataStru(self):
    if self.linColDataStru == None:
      self.linColDataStru = getLinColDataStru()
      if self.linColDataStru == None:
        msg = ' [Metrics] linColPatternObj continues to be None'
        raise ValueError, msg
    print self.linColDataStru
    return self.linColDataStru
  def getParImparExcludeList (self):
    return self.parImparExcludeList
  def __str__(self):
    outStr =  'This is the Metrics class singleton instance:\n'
    outStr += 'somaStats: %s\n' %(self.getSomaStats())
    outStr += 'stdStats: %s\n' %(self.getStdStats())
    outStr += 'lgiStats: %s\n' %(self.getLgiStats())
    outStr += 'linColPatternObj: %s\n' %(self.getLinColPatternObj())
    outStr += 'parImparExcludeList: %s\n' %(self.parImparExcludeList)
    return outStr

def strForSomaEtAlStats(self, oName):
    outStr = '''    %(oName).somaMin = %(somaMin)d
    %(oName).min = %(min)d
    %(oName).max = %(max)d
    %(oName).avg = %(avg)6.1f
    %(oName).std = %(std)5.2f

    %(oName).maxDesce= %(maxDesce)d
    %(oName).maxSobe = %(maxSobe)d
    %(oName).sdAvg   = %(sdAvg)6.1f
    %(oName).sdStd   = %(sdStd)5.2f

    %(oName).difMin  = %(difMin)d
    %(oName).difMax  = %(difMax)d
    %(oName).difAvg  = %(difAvg)6.1f
    %(oName).difStd  = %(difStd)5.2f
    ''' % {'oName':oName, \
    'min':self.min, 'max':self.max, 'avg':self.avg, 'std':self.std, \
    'maxDesce':self.maxDesce, 'maxSobe':self.maxSobe, 'sdAvg':self.sdAvg, 'sdStd':self.sdStd, \
    'difMin':self.difMin, 'difMax':self.difMax, 'difAvg':self.difAvg, 'difStd':self.difStd }
    return outStr

def transferFieldsForSomaEtAlStats(self, obj):
  self.min = obj.min
  self.max = obj.max
  self.avg = obj.avg
  self.std = obj.std

  self.maxDesce= obj.maxDesce
  self.maxSobe = obj.maxSobe
  self.sdAvg   = obj.sdAvg
  self.sdStd   = obj.sdStd

  self.difMin  = obj.difMin
  self.difMax  = obj.difMax
  self.difAvg  = obj.difAvg
  self.difStd  = obj.difStd
  return self

def testMetrics01():
  #piObj = parImparPatternObj()
  #print piObj
  #co=Controller()
  #lgi=co.getLgiStats()
  #print 'lgi.avg', lgi.avg
  #searchingJogosNOSE()
  pass

def adhoc_test():
  print 'Running adhoc_test()'
  #HistFreqUpdater()

def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
