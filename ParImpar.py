#!/usr/bin/env python
#-*-coding:utf8-*-

class ParImpar(object):
  # singleton
  _instance = None
  def __new__(self, *args, **kargs):
    if self._instance is None: 
      self._instance = object.__new__(self, *args, **kargs)
      self._instance.initParImparPatternObj()
    return self._instance
  def initParImparPatternObj(self):
    tuple9 = verPatternsOfCombinationsOfRemainder5()
    # return sobrando5, foundP5, patterns5, sobrando3, foundP3, patterns3, sobrandoPI, foundPI, patternsPI
    self.sobrando5, self.foundP5, self.patterns5, self.sobrando3, self.foundP3, self.patterns3, self.sobrandoPI, self.foundPI, self.patternsPI = tuple9
  def lookUpDivergePattern(self, jogo):
    nDePares = jogo.getNDePares()
    if nDePares == 3:
      goBackwards = 4
    elif nDePares in [2, 4]:
      goBackwards = 2
    #elif nDePares in [1,5]:
    else:
      goBackwards = 1
    nDoLastJogo = Sena.getNOfLastJogo();  coincide = 0
    for i in range(goBackwards):
      nDoJogo = nDoLastJogo - i
      jogoN = Sena.jogosPool.getJogo(nDoJogo)
      if nDePares == jogoN.getNDePares():
        coincide += 1
    if coincide == goBackwards:
      return False
    return True

  maxPattern3Deja = False
  maxPatternP3 = ''; maxOccurOfPattern3 = 0
  def getMaxPattern3(self):
    if self.maxPattern3Deja:
      return self.maxPattern3, self.maxOccurOfPattern3
    for patt in self.foundP3:
      quant = self.patterns3[patt]
      if quant > self.maxOccurOfPattern3:
        self.maxOccurOfPattern3 = quant
        self.maxPattern3 = patt
    self.maxPattern3Deja = True
    return self.maxPattern3, self.maxOccurOfPattern3
  def equalsMaxP3Occurs(self, pattIn):
    tuple2 = self.getMaxPattern3()
    if tuple2[0] == pattIn:
      return True
    return False
  
  maxPattern5Deja = False
  maxPatternP5 = ''; maxOccurOfPattern5 = 0
  def getMaxPattern5(self):
    if self.maxPattern5Deja:
      return self.maxPattern5, self.maxOccurOfPattern5
    for patt in self.foundP5:
      quant = self.patterns5[patt]
      if quant > self.maxOccurOfPattern5:
        self.maxOccurOfPattern5 = quant
        self.maxPattern5 = patt
    self.maxPattern5Deja = True
    return self.maxPattern5, self.maxOccurOfPattern5
  def equalsMaxP5Occurs(self, pattIn):
    tuple2 = self.getMaxPattern5()
    if tuple2[0] == pattIn:
      return True
    return False

  maxPatternPIDeja = False
  maxPatternPI = ''; maxOccurOfPatternPI = 0
  def getMaxPatternPI(self):
    if self.maxPatternPIDeja:
      return self.maxPatternPI, self.maxOccurOfPatternPI
    for patt in self.foundPI:
      quant = self.patternsPI[patt]
      if quant > self.maxOccurOfPatternPI:
        self.maxOccurOfPatternPI = quant
        self.maxPatternPI = patt
    self.maxPatternPIDeja = True
    return self.maxPatternPI, self.maxOccurOfPatternPI
  def equalsMaxPIOccurs(self, pattIn):
    tuple2 = self.getMaxPatternPI()
    if tuple2[0] == pattIn:
      return True
    return False

  def __str__(self):
    outStr = ''
    outStr += 'sobrando5' + str(self.sobrando5) + '\n'
    outStr += 'sobrando3' + str(self.sobrando3) + '\n'
    outStr += 'sobrandoPI' + str(self.sobrandoPI) + '\n'
    return outStr

if __name__ == '__main__':
  # testParImpar()
  pass