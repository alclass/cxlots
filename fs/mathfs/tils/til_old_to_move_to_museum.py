#!/usr/bin/env python3
"""
fs/mathfs/tils/til_old_to_move_to_museum.py
  Contains class Til_old

  This is no longer used in this system. To move to package "museum".
"""

# ================================================================================
# ========= Below: Older Alternatives =========
# ================================================================================

class Til_old(object):

  def __init__(self, jogosObj, tilIn=5):
    self.til = tilIn
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
      quant_na_faixa = 0
      for dezena in jogo:
        quant = histG[dezena]
        if quant >= quantLower and quant <= quantUpper:
          quant_na_faixa += 1
          #print dezena,
      if quant_na_faixa > 15:
        # well, TIL should be larger
        # it's rare for, eg, til=5
        # it also acts as a protect for the use of hexadecimal numbers in the lgi_b1idx (15=e)
        errmsg = f"'well, TIL should be larger (quant_na_faixa={quant_na_faixa} > 15), program cannot CONTINUE'"
        raise ValueError
      if quant_na_faixa > 9:
        hexadec = hex(quant_na_faixa)
        digit = str(hexadec)[-1]
      else:
        digit = str(quant_na_faixa)
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


def adhoctest():
  pass


if __name__ == '__main__':
  """
  @see the adhoctest module (adhoctest_til_functions.py)
  """
  adhoctest()
