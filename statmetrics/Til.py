#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Til.py
'''
# import numpy, time, sys
import sys

a=1
sys.path.insert(0, '..')
import funcsForPermutationEtAl as fsPerm
import datafiller.sqlLayer as sl
# sys.path.insert(0, '../datafiller')
# import sqlLayer as sl
import datafiller.frequencyMounting as fm


class TilPatternVector():
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
    else:
      self.initVectorViaWordPattern(wordPattern)

  def initVector(self):
    self.vector = getTilPatternsFor(self.patternSize, self.soma)
  
  def initVectorViaWordPattern(self, wordPattern):
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
    self.vector = fsPerm.getPermutations(listPattern)

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
      pattern
      pass
  
  def __str__(self):
    outStr = 'TilPatternVector(patternSize=%d soma=%d vectorSize=%d)' %(self.patternSize, self.soma, self.getVectorSize())
    if self.wordPattern:
      outStr += ' wordPattern=%s' %(self.wordPattern)
    return outStr

def testAdHocTilPatternVector():
  patternSize = 5; soma = 6
  tpvObj = TilPatternVector()
  print 'tpvObj', tpvObj 
testAdHocTilPatternVector()

tilObjDict = {}
def getTilObj(tilIn=5):
  if tilIn in tilObjDict.keys():
    return tilObjDict[tilIn]
  tilObj = Til(tilIn)
  tilObjDict[tilIn] = tilObj
  return tilObj

# test adhoc
getTilObj()

class TilMaker():

  def __init__(self, tilNumber=5, nDoConcurso=None):
    '''
    or tilNumber not in [5,6,10,12,15,20]:
    '''
    self.tilNumber = tilNumber
    totalDeConcursos = len(sl.getListAllConcursosObjs())      
    if nDoConcurso == None:
      nDoConcurso = totalDeConcursos
    elif nDoConcurso < 1 or nDoConcurso > totalDeConcursos:
      indexErrorMsg = 'passed in nDoConcurso=%d and range acceptable is 1 to %d' %(nDoConcurso, totalDeConcursos)
      raise IndexError, indexErrorMsg 
    self.nDoConcurso = nDoConcurso
    self.listWithFrequencyFrontiers = None
    self.tilSets = None
    self.freqAtEachConcurso = fm.FrequenciesThruConcursos() 

  def calculateTilOfNUpToConcursoI(self):
    frequenciesAtConcursoN = self.freqAtEachConcurso.getFrequenciesOfAllDezenasByNDoConcurso(self.nDoConcurso)
    minN = min(frequenciesAtConcursoN)
    maxN = max(frequenciesAtConcursoN)
    amplitude = maxN - minN + 1
    incrementSize =  amplitude / self.tilNumber
    # nTotalDeDezenas = self.freqAtEachConcurso.getNTotalDeDezenas() 
    remainder = amplitude % self.tilNumber
    #remainder =  (maxN - minN) % tilNumber
    self.listWithFrequencyFrontiers = [incrementSize] * self.tilNumber
    for i in range(incrementSize):
      if remainder > 0:
        self.listWithFrequencyFrontiers[i] += 1
        remainder -= 1
    # logically list is in ascending order
    if sum(self.listWithFrequencyFrontiers) != amplitude:
      valueErrorMsg = 'sum(listWithFrequencyFrontiers)=%d != amplitude=%d :: The two should be equal' %(sum(self.listWithFrequencyFrontiers), amplitude)
      raise ValueError, valueErrorMsg
    '''
    if sum(self.listWithFrequencyFrontiers) != nTotalDeDezenas:
      valueErrorMsg = 'sum(listWithFrequencyFrontiers)=%d != nTotalDeDezenas=%d :: The two should be equal' %(sum(self.listWithFrequencyFrontiers), nTotalDeDezenas)
      valueErrorMsg += '\n self.listWithFrequencyFrontiers = %s' %(str(self.listWithFrequencyFrontiers))
      valueErrorMsg += '\n tilN = %d  nTotalDeDezenas %d' %(self.tilNumber, nTotalDeDezenas)
      valueErrorMsg += '\n self.nDoConcurso = %d  min %d max %d' %(self.nDoConcurso, minN, maxN)
      raise ValueError, valueErrorMsg
    ''' 
    return self.listWithFrequencyFrontiers

  def getTilSets(self):
    self.separateTilSets()
    self.checkTilSetsBorders()
    return self.tilSets
  
  def separateTilSets(self):
    if self.listWithFrequencyFrontiers == None:
      self.calculateTilOfNUpToConcursoI()
    dezenas = self.freqAtEachConcurso.getAllDezenasInAscendingOrderOfFrequency()
    print 'dezenas', dezenas 
    self.tilSets = [[]] * len(self.listWithFrequencyFrontiers); ini = 0
    for i in range(len(self.listWithFrequencyFrontiers)):
      frontier = self.listWithFrequencyFrontiers[i]
      fim = ini + frontier
      print 'i fim = ini + frontier', i, fim , ini , frontier
      if fim > len(dezenas):
        valueErrorMsg = 'An inconsistency happened, index fim (=%d) is greater than len(dezenas) = %d ' %(fim, len(dezenas)) 
        raise ValueError, valueErrorMsg
      self.tilSets[i] = dezenas[ ini : fim]
      print i, 'tilSets[i]', self.tilSets[i]
      ini = fim
  
  def checkTilSetsBorders(self):
    '''
    This method compares he last element of one tilSet
      with the first element of the next tilSet and if equal, 
      bring the next tilSet element to the previous set and recurse to look for more
    '''
    if self.tilSets == None:
      self.separateTilSets()
    for i in range(len(self.tilSets)-1):
      passingTilSet = self.tilSets[i]
      nextTilSet = self.tilSets[i+1]
      try:
        while passingTilSet[-1] == nextTilSet[0]:
          passingTilSet.append(nextTilSet[0])
          del nextTilSet[0]
      except IndexError:
        pass

def sumUpTilPattern(pattern):
  soma=0
  for c in pattern:
    soma+=int(c)
  return soma

class TilElement():
  '''
  This class covers a Til Element

  A Til Element is instantiated with a pattern (eg '03021')
  From any pattern, length and sum can be derived.  Length is the pattern string size
    ( in the example above len('03021')=5 )
    and sum is the summing up of its digits (in the example above 0+3+0+2+1=6)
  
  It implements a method called getWorkSetsWithQuantities() which does the following:
    it gets the frequency-til-positioned dezenas and joins this set with the quantity expressed in the digit
    
    Let's see this in the example above '03021'
    -- 0, the first digit, means 0 dezenas in the first quintil
    -- 3 means 3 dezenas in the second quintil which may have x dezenas altogether
    -- the pair (tuple) to form is this set of x dezenas, together with the quantity 3
    -- this tuple will be used elsewhere for combinations of this til(size=5, index=1) 3 by 3

    index 1 is because pattern[1]=3
    
    So this method is applied in a calling routine that produces these combinations
    
  '''

  def __init__(self, pattern):
    '''
    init() set the attributes pattern and its two derivatives length and sum
    '''
    self.pattern = pattern
    self.setLengthAndSum()

  def setLengthAndSum(self):
    '''
    called by init() to set the attributes derived by pattern, ie length and sum
    '''
    self.length = len(self.pattern)
    self.sum    = sumUpTilPattern(self.pattern)

  def getWorkSetsWithQuantities(self):
    '''
    This method returns a list of tuples
    -- the 2D-tuple has 1) a list of dezenas and 2) quantity
    -- -- the dezenas are picked up via method tilObj.getTilSets() given the til index (eg. 0123 are indices for the four quartils)
    -- -- the quantity is the digit in the pattern itself (eg. 03021 says 3 dezenas in quintil 2, 2 dezenas in quintil 4 and 1 dezena in quintil 5)    
    '''
    workSetsWithQuantities = []
    tilObj = TilMaker(self.length)
    for i in range(len(self.pattern)):
      quantity = int(self.pattern[i])
      if quantity > 0:
        dezenas = tilObj.getTilSets()[i]
        workSetWithQuantity = (dezenas, quantity)
        workSetsWithQuantities.append(workSetWithQuantity)
    return workSetsWithQuantities

def testTilElement():
  tilElement = TilElement('03021')
  workSetsWithQuantities = tilElement.getWorkSetsWithQuantities()
  print workSetsWithQuantities
#testTilElement()



def stuffStrWithZeros(subtokens, size=10):
  newTokens = []
  for token in subtokens:
    tam = len(token)
    toFill = size - tam
    token = token + '0'*toFill
    newTokefsPerm.append(token)
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
  return fsPerm.getPermutations(subtokens)

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
  pass

'''
# ================================================================================
# ========= Below: Older Alternatives =========
# ================================================================================
'''

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
      i
      workJogos = self.jogosObj.continueJogosSequenceBy(workJogos)
      '''
      lastJogo = jogos[-1]
      histG = sd.incrementalHistogram(histG, lastJogo)
      printJogoWithTils(histG, lastJogo, len(jogos)-1)
      '''


  
'''

  perms = getTilPatternsFor(10,3)
  print perms, len(perms)

  print 'def getPermutations(subtokens):'
  vect = ['xyyzzzzzzz']
  perms = getPermutations(vect)
  print perms, len(perms)

  tpVector = TillPatternVector(-1,-1,vect)
  print tpVector


  #intsToSum(soma=6)
  #testGeraSumComponents()


  perms = getTilPatternsFor()
  print perms, len(perms)

  testSumComponentsGerador()
  print time.ctime()
  prepForPermuteN()
  print time.ctime()

  #expand()
  #testRemaindersComb()
  #testC1()
  #array = [1,2,3,4,5]
  #array = ['a','b','c','d','e']

  tpVector = TilPatternVector(10,6)
  print 'tpVector', tpVector, tpVector.vector
  tpVector = TilPatternVector(10,3)
  print 'tpVector', tpVector
'''