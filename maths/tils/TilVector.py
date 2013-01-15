#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Til.py
'''
# import numpy, time, sys
import os, sys
folder_relpath = os.path.dirname(__file__)
folder_abspath = os.path.abspath(folder_relpath)
app_root_abspath = folder_abspath [ : -len('maths/frequencies') ] 
# print 'app_root_abspath', app_root_abspath
sys.path.insert(0, app_root_abspath)
from models.JogoSlider import JogoSlider
# from models.JogoTil import JogoTil
import maths.combinatorics.algorithmsForCombinatorics as fsPerm
import TilSets as ts
import HistoryFrequency as hf
#===============================================================================
# sys.path.insert(0, '..')
# import funcsForFrequencies as ffFreq
# import datafiller.sqlLayer as sl
# # sys.path.insert(0, '../datafiller')
# # import sqlLayer as sl
# import datafiller.frequencyMounting as fm
#===============================================================================



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
    self.vector = fsPerm.getTilPatternsFor(self.patternSize, self.soma)
  
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
  tpvObj = TilPatternVector(patternSize, soma)
  print 'tpvObj', tpvObj 
#testAdHocTilPatternVector()


def spread2DListTo1DList(list2D):
  newSet = []
  for list1D in list2D:
    for element in list1D:
      newSet.append(element)
  return newSet

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
  for ws in workSetsWithQuantities:
    print ws[0], 'size', len(ws[0]), 'ncomb', ws[1] # workSetsWithQuantities
#testTilElement()
  
def adhoc_test():
  testTilElement()

def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()

# ================================================================================
# ========= Below: Older Alternatives =========
# ================================================================================

class Til_old(object):

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
    aprint

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

#      lastJogo = jogos[-1]
#      histG = sd.incrementalHistogram(histG, lastJogo)
#      printJogoWithTils(histG, lastJogo, len(jogos)-1)

tilObjDict = {}
def getTilObj(tilIn=5):
  if tilIn in tilObjDict.keys():
    return tilObjDict[tilIn]
  tilObj = Til(tilIn)
  tilObjDict[tilIn] = tilObj
  return tilObj

# test adhoc
# getTilObj()
