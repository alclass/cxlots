#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''
# import numpy, time, sys
import sys

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


def adhoc_test():
  '''
  '''
  testTilElement()
  pass

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
