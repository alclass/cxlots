#!/usr/bin/env python
# -*- coding: utf-8 -*-

a=1
import Sena
jogosPool = Sena.JogosPool()
nOfLastJogoParam=Sena.getNOfLastJogo()

class Metrics(object):
  '''Métricas:
    1) par-ímpar
    2) soma [1. min, 2. max, 3. vetor sobe-e-desce]
    3) desvio-padrão
    4) histograma evolutivo
    5) não-consecutivos num jogo
    6) Nº de repetições e quantos jogos se passaram para isso
    7) variações linha x coluna (ou Dígito da Esquerda x da Direita)
  '''
  _instance = None
  somaStats = None
  stdStats  = None
  lgiStats  = None
  #linColPatternObj = None
  linColDataStru = None
  linColPatternObj = None
  parImparExcludeList = [0,6]

  def __new__(self, *args, **kargs):
    #print 'inside Controller new'
    if self._instance is None: 
      self._instance = object.__new__(self, *args, **kargs)
    return self._instance

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

if __name__ == '__main__':
  pass
  searchingPrimes()
