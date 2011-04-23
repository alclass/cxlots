#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, sys
#import numpy
'''
algo
'''

a=1
import NumberSystem as ns

class TilPatternVector(object):
  '''
  This class is a helper around Til Patterns.
  
  Objects can be created two ways:
  
  1) without the 'wordPattern' parameter
  2) with the 'wordPattern' parameter
  
  
  1) without the 'wordPattern' parameter

    Eg.
    1.1) 1233 has 12 permutions
    1.2) the complete set of til pattern for patternSize=10 and soma=6
         is 5005
    
  2) with the 'wordPattern' parameter
  
    Eg. 'xyyzzzzzzz' ie 1 x, 2 y's and 7 z's
    2.1) This is the same as 1223333333 or 0112222222
    2.2) It has 360 permutations
  
  '''

  def __init__(self, patternSize, soma, wordPattern=None):
    self.wordPattern = wordPattern
    if wordPattern == None:
      self.patternSize = patternSize
      self.soma   = soma
      self.vector = None
      self.initVector()
      return
    # second case, a initialPattern was entered
    if type(wordPattern) == list:
      if len(wordPattern) > 0:
        wordPattern = wordPattern[0]
    if type(wordPattern) <> str:
        errorMsg = 'wordPattern should be a str <> ' + str(wordPattern)
        raise ValueError, errorMsg
    if len(wordPattern) == 0:
      errorMsg = 'wordPattern is empty. It should have at least one char'
      raise ValueError, errorMsg
    chrDict = {}
    for c in wordPattern:
      chrDict[c]=1
    self.soma = sum(range(len(chrDict)))
    self.patternSize = len(wordPattern)
    listPattern = [wordPattern]
    self.vector = ns.getPermutations(listPattern)

  def initVector(self):
    self.vector = getTilPatternsFor(self.patternSize, self.soma)
  
  def getVectorSize(self):
    if self.vector:
      return len(self.vector)
    return 0
  
  def getIndex(self, pattern):
    if len(pattern) == self.patternSize:
      return self.vector.index(pattern)
    return -1
  
  def loadDict(self, historyPatterns, baseObj):
    #getDBField('pattern10')
    for pattern in historyPatterns:
      pass
  
  def __str__(self):
    outStr = 'TilPatternVector(patternSize=%d soma=%d vectorSize=%d)' %(self.patternSize, self.soma, self.getVectorSize())
    if self.wordPattern:
      outStr += ' wordPattern=%s' %(self.wordPattern)
    return outStr


class Til(object):

  def __init__(self, jogosObj, tilIn=5):
    self.til      = tilIn
    self.jogosObj = jogosObj
    # initiates: self.faixas
    self.initFaixasForTil()
    # initiates: self.dezenasNasFaixas
    self.initEntireTilFaixas()

  def getTil(self):
    return self.til

  def getDezenasNasFaixas(self):
    '''
    Returns the dezenas in each faixa
    '''
    return self.dezenasNasFaixas

  def getDezenasNaFaixa(self, faixaIn):
    if faixaIn < 0:
      # change it to the first faixa
      faixa = 0
    elif faixaIn > len(self.dezenasNasFaixas) - 1:
      # change it to the last faixa
      faixa = len(self.dezenasNasFaixas) - 1
    else:
      faixa = faixaIn
    return self.dezenasNasFaixas[faixa]

  def getFaixas(self):
    '''
    Returns the faixas ((quantMin1,quantMax1),(quantMin2,quantMax2) etc.) according to the 'til'
    '''
    return self.faixas

  def initFaixasForTil(self):
    '''
    The 'tils', so to say, are a generic denomination
    for frequency classes (percentils, quartils, sixtils, etc.)
    The routine/method accepts the number of classes to calculate:
    if tilIn is 4, for instance, the output will be a list with
    the 4-interval points
    '''
    histG  = self.jogosObj.getHistG()
    # print 'initFaixasForTil(self) jogosObj', self.jogosObj, 'size', self.jogosObj.size()
    values = histG.values()
    values.sort()
    soma     = sum(values)
    quantMin = min(values)
    quantMax = max(values)
    dist     = quantMax - quantMin + 1
    step     = dist / self.til
    missing  = dist % self.til

    aprint = '''  til = %(til)d
  values = %(values)s
  soma = %(soma)d
  quantMin = %(quantMin)d
  quantMax = %(quantMax)d
  dist = %(dist)d
  step = %(step)d
  missing = %(missing)d''' %{'til':self.til, 'values':values,
  'soma':soma, 'quantMin':quantMin, 'quantMax':quantMax,'dist':dist,
  'step':step, 'missing':missing}

    faixas = [(0,0)]*self.til
    quantFaixaLower = quantMin
    for i in range(len(faixas)):
      quantFaixaUpper = quantFaixaLower + step - 1
      if missing > 0:
        quantFaixaUpper += 1
        missing -= 1
      faixas[i] = (quantFaixaLower, quantFaixaUpper)
      #print 'faixa', quantFaixaLower, quantFaixaUpper
      quantFaixaLower = quantFaixaUpper + 1
    #print 'histG', histG
    #print 'faixas', faixas
    self.faixas = list(faixas)

  def initEntireTilFaixas(self):
    dezenasNasFaixas = [[]]*self.til
    histG = self.jogosObj.getHistG()
    DEZENA_UPPER = self.jogosObj.totalDeDezenasNoVolante
    for dezena in range(1, DEZENA_UPPER + 1):
      try:
        quant = histG[dezena]
      except KeyError:
        quant = 0
      for i in range(len(self.faixas)):
        faixa = self.faixas[i]
        quantLower = faixa[0]
        quantUpper = faixa[1]
        if quant >= quantLower and quant <= quantUpper:
          dezns = list(dezenasNasFaixas[i])
          dezns.append(dezena)
          dezenasNasFaixas[i] = list(dezns)
          break
    '''for faixa in dezenasNasFaixas:
      print 'faixa',
      for dezena in faixa:
        print dezena,
      print'''
    self.dezenasNasFaixas = list(dezenasNasFaixas)

  def generateLgiForJogoVsTilFaixas(self, jogo):
    '''
  Each jogo has a pattern of frequency distribution, ie,
  some dezenas have occurred more than others
  some others have occurred less
  
  lgi is the LexicoGraphical Index
  Eg.
  1c5a203   101010   32001   etc.
    '''
    # lgi is the LexicoGraphical Index
    lgi = ''
    histG = self.jogosObj.getHistG()
    for faixa in self.faixas:
      quantLower = faixa[0]
      quantUpper = faixa[1]
      #print 'faixa', faixa,
      quantNaFaixa = 0
      for dezena in jogo:
        quant = histG[dezena]
        if quant >= quantLower and quant <= quantUpper:
          quantNaFaixa += 1
          #print dezena,
      if quantNaFaixa > 15:
        # well, TIL should be larger
        # it's rare for, eg, til=5
        # it also acts as a protect for the use of hexadecimal numbers in the lgi (15=e)
        raise ValueError, 'well, TIL should be larger, IT CAN NOT CONTINUE'
      if quantNaFaixa > 9:
        hexadec = hex(quantNaFaixa)
        digit = str(hexadec)[-1]
      else:
        digit = str(quantNaFaixa)
      lgi += digit
      #print
    # print 'lgi', lgi
    return lgi

  def tilJogoAJogo(self):
    startAt = 100
    workJogos = self.jogosObj.getJogosAteConcurso(startAt)
    upToOneMore = self.jogosObj.getLastConcurso()+1
    for i in range(startAt, upToOneMore):
      workJogos = self.jogosObj.continueJogosSequenceBy(workJogos)
      lastJogo = jogos[-1]
      histG = sd.incrementalHistogram(histG, lastJogo)
      printJogoWithTils(histG, lastJogo, len(jogos)-1)


tilObjDict = {}
def getTilObj(tilIn=5):
  if tilIn in tilObjDict.keys():
    return tilObjDict[tilIn]
  tilObj = Til(tilIn)
  tilObjDict[tilIn] = tilObj
  return tilObj


class TilHist(object):
  def __init__(self):
    pass
  

def stuffStrWithZeros(subtokens, size=10):
  newTokens = []
  for token in subtokens:
    tam = len(token)
    toFill = size - tam
    token = token + '0'*toFill
    newTokens.append(token)
    #print token
  return newTokens

def strToList(s):
  lista = []
  for c in s:
    lista.append(c)
  return lista

def sumComponentsToListOfStrs(intLists):
  outList = []
  for elem in intLists:
    strList = map(str, elem)
    outList.append(''.join(strList))
  return outList

def testSumComponentsGerador():
  subtokensHandMade=['6','51','42','411','33','321','3111',\
    '222','2211','21111','111111']
  subtokens = geraSumComponents(6)
  subtokens = sumComponentsToListOfStrs(subtokens)
  #print 'subtokensHandMade', subtokensHandMade
  #print 'subtokens', subtokens
  #print 'subtokensHandMade == subtokens', subtokensHandMade == subtokens

def getTilPatternsFor(patternSize=10, patternSoma=6):
  #array = range(1,4)
  #wordForArray = 'xyyzzzzzzz'
  subtokens = geraSumComponents(6)
  subtokens = sumComponentsToListOfStrs(subtokens)
  subtokens = stuffStrWithZeros(subtokens, patternSize)
  #print subtokens
  #wordForArray = '222000000'
  #sys.exit(0)
  return ns.getPermutations(subtokens)

passa=0
def geraSumComponents(soma, parcel=-1, acc=[]):
  global passa
  passa += 1
  if soma == 1:
    acc += [[1]]
    #dif=-1
    #print 'passa', passa, 'RET parcel,soma,acc', parcel, soma, acc
    return acc
  if parcel == 1:
    acc += [[1]*soma]
    #dif=-1
    #print 'passa', passa, 'RET parcel,soma,acc', parcel, soma, acc
    return acc
  # case where caller leaves 'parcel' to its initial supposed condition, ie, it's equal to 'soma'
  if parcel == -1:
    parcel = soma
  if parcel == soma:
    acc += [[parcel]]
    #dif=-1
    #print 'passa', passa, 'REC soma=%d parcel=%d dif=%d acc=%s' %(soma,parcel,dif,str(acc))
    return geraSumComponents(soma, parcel-1, acc)
  # dif NOW
  dif = soma - parcel
  if dif == 1:
    acc += [[parcel, 1]]
    #print 'passa', passa, 'REC soma=%d parcel=%d dif=%d acc=%s' %(soma,parcel,dif,str(acc))
    return geraSumComponents(soma, parcel-1, acc)

  keptAcc = list(acc)
  newAcc = []
  #print 'passa', passa, 'ATT soma=%d parcel=%d dif=%d acc=%s' %(soma,parcel,dif,str(acc))
  subAcc = geraSumComponents(dif, dif, [])
  for sub in subAcc:
    # well, the 'if' below was a tough decision to correct a repeat
    # eg. gera(5) was having [3,2] and [2,3]
    if parcel < sub[0]:
      continue
    #print 'adding', parcel, 'to', sub,
    sublista = [parcel] + sub
    #print '=', sublista
    newAcc.append(sublista)
  keptAcc += newAcc
  acc = keptAcc
  if parcel > 1:
    #print 'passa', passa, 'REC soma=%d parcel=%d dif=%d acc=%s' %(soma,parcel,dif,str(acc))
    return geraSumComponents(soma, parcel-1, acc)
    #print 'passa', passa, 'RF  soma=%d parcel=%d dif=%d acc=%s' %(soma,parcel,dif,str(acc))
  return acc


def testGeraSumComponents():
  for soma in range(5,6):
    acc = geraSumComponents(soma, soma, [])
    # check it up
    for elem in acc:
      calcSoma = sum(elem)
      if soma <> calcSoma:
        print 'soma <> sum(elem):', soma, calcSoma
    print soma, 'R:', acc
   
if __name__ == '__main__':
  tpVector = TilPatternVector(10,6)
  print 'tpVector', tpVector, tpVector.vector
  tpVector = TilPatternVector(10,3)
  print 'tpVector', tpVector
