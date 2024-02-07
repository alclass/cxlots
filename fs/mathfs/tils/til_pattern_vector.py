#!/usr/bin/env python3
"""
fs/mathfs/tils/til_pattern_vector.py
  Contains class TilPatternVector
"""
# import numpy, time, sys
import os, sys
import fs.mathfs.tils.til_element as te  # te.TilElement
folder_relpath = os.path.dirname(__file__)
folder_abspath = os.path.abspath(folder_relpath)
app_root_abspath = folder_abspath [ : -len('maths2/frequencies') ]
# print 'app_root_abspath', app_root_abspath
sys.path.insert(0, app_root_abspath)
from models.JogoSlider import JogoSlider
# from models.JogoTil import JogoTil
import maths.combinatorics.combinatoric_algorithms as fsPerm
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



class TilPatternVector:
  """
  This class is a helper around Til Patterns.
  
  Objects can be created two ways:
    1) without the 'wordPattern' parameter
    2) with the 'wordPattern' parameter

  1) without the 'wordPattern' parameter
    Eg
    1.1) 1233 has 12 permutions
    1.2) the complete set of til pattern for patternSize=10 and soma=6
         is 5005
    
  2) with the 'wordPattern' parameter
    Eg 'xyyzzzzzzz' ie 1 x, 2 y's and 7 z's
    2.1) This is the same as 1223333333 or 0112222222
    2.2) It has 360 permutations
  """

  def __init__(self, pattern_size, soma, word_pattern=None):
    self.wordPattern = word_pattern
    if word_pattern is None:
      self.patternSize = pattern_size
      self.soma   = soma
      self.vector = None
      self.init_vector()
    else:
      self.init_vector_via_word_pattern(word_pattern)

  def init_vector(self):
    self.vector = fsPerm.getTilPatternsFor(self.patternSize, self.soma)
  
  def init_vector_via_word_pattern(self, word_pattern):
    # second case, a initialPattern was entered
    if type(word_pattern) == list:
      if len(word_pattern) > 0:
        word_pattern = word_pattern[0]
    if type(word_pattern) != str:
        errmsg = 'wordPattern should be a str <> ' + str(word_pattern)
        raise ValueError(errmsg)
    if len(word_pattern) == 0:
      errmsg = 'wordPattern is empty. It should have at least one char'
      raise ValueError(errmsg)
    chr_dict = {}
    for c in word_pattern:
      chr_dict[c] = 1
    self.soma = sum(range(len(chr_dict)))
    self.patternSize = len(word_pattern)
    list_pattern = [word_pattern]
    self.vector = fsPerm.get_permutations(list_pattern)

  def get_vector_size(self):
    if self.vector:
      return len(self.vector)
    return 0
  
  def get_index(self, pattern):
    if len(pattern) == self.patternSize:
      return self.vector.index(pattern)
    return -1
  
  def load_dict(self, history_patterns, baseObj):
    #getDBField('pattern10')
    for pattern in history_patterns:
      pattern
      pass
  
  def __str__(self):
    out_str = ('TilPatternVector(patternSize=%d soma=%d vectorSize=%d)'
               %(self.patternSize, self.soma, self.get_vector_size()))
    if self.wordPattern:
      out_str += ' wordPattern=%s' % self.wordPattern
    return out_str

def test_ad_hoc_til_pattern_vector():
  pattern_size, soma = 5, 6
  tpv_obj = TilPatternVector(pattern_size, soma)
  print('tpv_obj', tpv_obj)
  # test_ad_hoc_til_pattern_vector()


def spread2_d_list_to1_d_list(list2_d):
  new_set = []
  for list1D in list2_d:
    for element in list1D:
      new_set.append(element)
  return new_set

def sum_up_til_pattern(pattern):
  soma=0
  for c in pattern:
    soma+=int(c)
  return soma


def test_til_element():
  til_element = te.TilElement('03021')
  work_sets_with_quantities = til_element.get_worksets_w_quantities()
  for ws in work_sets_with_quantities:
    print(ws[0], 'size', len(ws[0]), 'ncomb', ws[1])  # work_sets_with_quantities
  #test_til_element()
  

def adhoctest():
  test_til_element()


if __name__ == '__main__':
  adhoctest()

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
  
  lgi_b1idx is the LexicoGraphical Index
  Eg.
  1c5a203   101010   32001   etc.
    '''
    # lgi_b1idx is the LexicoGraphical Index
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
        # it also acts as a protect for the use of hexadecimal numbers in the lgi_b1idx (15=e)
        raise ValueError, 'well, TIL should be larger, IT CAN NOT CONTINUE'
      if quantNaFaixa > 9:
        hexadec = hex(quantNaFaixa)
        digit = str(hexadec)[-1]
      else:
        digit = str(quantNaFaixa)
      lgi += digit
      #print
    # print 'lgi_b1idx', lgi_b1idx
    return lgi

  def tilJogoAJogo(self):
    startAt = 100
    workJogos = self.jogosObj.getJogosAteConcurso(startAt)
    upToOneMore = self.jogosObj.getLastConcurso()+1
    for i in range(startAt, upToOneMore):
      i
      workJogos = self.jogosObj.continueJogosSequenceBy(workJogos)

#      lastJogo = jogosfs[-1]
#      histG = sd.incrementalHistogram(histG, lastJogo)
#      printJogoWithTils(histG, lastJogo, len(jogosfs)-1)

tilObjDict = {}
def getTilObj(tilIn=5):
  if tilIn in tilObjDict.keys():
    return tilObjDict[tilIn]
  tilObj = Til(tilIn)
  tilObjDict[tilIn] = tilObj
  return tilObj

# test adhoc
# getTilObj()
