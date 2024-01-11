#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib, numpy, sys

from Filtre import Filtre
#import CLClasses
#import funcsForSql as fSql
#import LgiCombiner as lc
#import sqlAccessors as sa
#import Stat
import cardprint.pprint as pprint


class ChooserSomaFiltre(Filtre):
  '''
  class SomaChoice

  Observations for soma: (rules are implemented in the method "choose()")

    1) depth should never be greater than 3, ie, it (soma)
       will hardly increase (or decrease) 5 times in a row
       (consider 4 times in a row, the most, this piece will be, at least for the moment, hardwired here)

    2) calculate probabilities that depth will be 0, 1, 2 or 3
      Of course, this should work like a tree node, ie,
      if depth is 2, the next one is either 3 (continues in direction (sobe or desce)
      or 0 (a change in increase/decrease direction occurring)

    3) the probabilities should be sensitive to the sum metric value itself
      ie, if sum is too central (ie, in the middle), these probabilities should be very
      small and, perhaps, the system should advice not going for gambling on it

    4) on the other hand, if soma is very acute (ie, close to upper and lower bounds),
       the system might give out higher probabilities, though limiting bounds represent
       too few jogosfs (at the end, not very helpful anyway, but, as composed with other filters,
       that's something)
  '''

  def __init__(self, standard2LetterName, qualSoma='soma'):
    # Filtre.Filtre.__init__(self, standard2LetterName)
    super(Filtre, self).__init__()
    self.qualSoma = qualSoma
    self.sobeDesceSequence = [] # formerly called sobeDesceList
    self.somas         = []
    self.longestSobe   = 0
    self.longestDesce  = 0
    self.totalSobe     = 0
    self.totalDesce    = 0
    self.somaMax       = 0
    self.somaMin       = self.greatestSum + 1 # it's known, greatest sum is sum(range(55,61))
    #self.somaList = []
    self.avg = 0.0


    # the next two attrs are helper vars
    self.somaAnt = 0
    self.sobeDesceAnt = 0
    self.sobeDesceDepth = 0
    self.somaDasSomas = 0

    self.til = 10
    self.initSomaStats()
    self.calcHistG()
    self.logFile = funcs.mountLogFile(self, self.jogosObj)

  limitLow  = {1:1,3:1,7:1,15:2858}
  limitHigh = {1:1,3:1,7:1,15:2858+159}

  def getLimitLow(self, n):
    return self.limitLow[n]

  def getLimitHigh(self, n):
    return self.limitHigh[n]
      

  def calcHistG(self):
    '''
    self.histG = {}
    for soma in self.somas:
      try:
        self.histG[soma] += 1
      except KeyError:
        self.histG[soma] = 1
    '''
    dist = self.somaMax - self.somaMin + 1
    step     = dist / self.til
    missing  = dist % self.til    
    faixas = [(0,0)]*self.til
    quantFaixaLower = self.somaMin
    for i in range(len(faixas)):
      quantFaixaUpper = quantFaixaLower + step - 1
      '''
      if i==len(faixas)-1 and quantFaixaUpper < self.somaMax:
        quantFaixaUpper = self.somaMax
      '''
      if missing > 0:
        quantFaixaUpper += 1
        missing -= 1
      faixas[i] = (quantFaixaLower, quantFaixaUpper)
      #print 'faixa', quantFaixaLower, quantFaixaUpper
      quantFaixaLower = quantFaixaUpper + 1
    #print 'histG', histG
    #print 'faixas', faixas
    self.faixas = list(faixas)
    self.slices = [0]*self.til
    for soma in self.somas:
      for i in range(self.til):
        faixa = faixas[i]
        quantFaixaLower = faixa[0]
        quantFaixaUpper = faixa[1]
        if soma >= quantFaixaLower and soma <= quantFaixaUpper:
          self.slices[i]+=1
          break

  def initSomaStats(self):
    attr = self.qualSoma
    somasDict, self.somas = sa.getAttr(attr, self.sqlTable)
    for soma in self.somas:
      self.processSoma(soma)
    self.avg = self.somaDasSomas / (0.0 + len(self.somas))

  def processSoma(self, soma):
    print soma,
    self.somaDasSomas += soma
    #self.somaList.append(soma)
    sobeDesce = 0
    if soma > self.somaAnt:
      if self.sobeDesceAnt <> 1: # 1 means SUBINDO
        self.sobeDesceDepth = 0
      else:
        self.sobeDesceDepth += 1
        if self.sobeDesceDepth > self.longestSobe:
          self.longestSobe = self.sobeDesceDepth
      sobeDesce = 1
      self.totalSobe += 1
    elif soma < self.somaAnt:
      if self.sobeDesceAnt <> -1: # -1 means DESCENDO
        self.sobeDesceDepth = 0
      else:
        self.sobeDesceDepth += 1
        if self.sobeDesceDepth > self.longestDesce:
          self.longestDesce = self.sobeDesceDepth
      sobeDesce = -1
      self.totalDesce += 1

    self.sobeDesceAnt = sobeDesce
    self.directionVector.append(sobeDesce)

    print sobeDesce, 'ts =', self.totalSobe, 'td =', self.totalDesce, 'depth', self.sobeDesceDepth,

    if soma > self.somaMax:
      self.somaMax = soma
      print 'MAX',
    if soma < self.somaMin:
      self.somaMin = soma
      print 'min',
    self.somaAnt = soma
    print

  def choose(self, jogo, probCut=None):
    '''
    probCut works like this:
    if probability of jogo is less than probCut, return False "on jogo"
    if probCut is None (the default), only "hardwired" conditions will apply
    '''
    soma = sum(jogo)
    if soma < self.somaMin:
      print 'menor que somaMin, não apostar'
      # return False
    if soma > self.somaMax:
      print 'maior que somaMax, não apostar'
      # return False
    lastSoma = self.somas[-1]
    print jogo, soma, 'last soma', lastSoma
    sobeDesce = 0
    if soma > lastSoma:
      sobeDesce = 1
      print 'SUBINDO'
    elif soma < lastSoma:
      sobeDesce = -1
      print 'DESCENDO'
    else:
      print 'SOMA IGUAL À ANTERIOR'
    # parecer
    
    sobeDesceAnt = self.directionVector[-1]
    
    sameDirection = True; directionDepth = 0; index = len(self.directionVector)
    while sameDirection:
      sameDirection = False
      index -= 1
      if index < 0:
        break
      sobeDesceAnt = self.directionVector[index]
      if sobeDesce == sobeDesceAnt:
        sameDirection = True
        directionDepth += 1

    print 'directionDepth', directionDepth

    if sobeDesce == 1:
      if directionDepth > self.longestSobe:
        print 'directionDepth-SUBINDO maior que longestSobe, não apostar'
    elif sobeDesce == -1:
      if directionDepth < self.longestDesce:
        print 'directionDepth-DESCENDO maior que longestDesce, não apostar'

  def __str__(self):

    longestSobe  = self.longestSobe
    longestDesce = self.longestDesce
    totalSobe    = self.totalSobe
    totalDesce   = self.totalDesce
    somaMax = self.somaMax
    somaMin = self.somaMin
    avg     = self.avg

    outStr = '''Soma Stats:
  self.longestSobe  = %(longestSobe)d
  self.longestDesce = %(longestDesce)d
  self.totalSobe    = %(totalSobe)d
  self.totalDesce   = %(totalDesce)d
  self.somaMax      = %(somaMax)d
  self.somaMin      = %(somaMin)d
  self.avg          = %(avg)f''' \
      %{ \
    'longestSobe' : longestSobe, \
    'longestDesce': longestDesce,\
    'totalSobe'   : totalSobe,\
    'totalDesce'  : totalDesce,\
    'somaMax'     : somaMax,\
    'somaMin'     : somaMin,\
    'avg'         : avg \
      }
    return outStr



class TilPatternsChoice(CLClasses.Base):
  '''
  class TilPatternsChoice

  Rules for choice: (the rules are implemented in the method "choose()")

    1) if a single digit is higher than the highest one ever occurred,
      return False "on jogo"


  '''

  def __init__(self, standard2LetterName, tilN=5):
    CLClasses.Base.__init__(self, standard2LetterName)
    self.directionVector = [] # formerly called sobeDesceList
    self.somas           = []
    self.highestDigit    = 0
    self.patternsOccured = 0
    self.allPatterns     = 0
    self.tilN = tilN
    self.initTilPatternsStats()
    # the next two attrs are helper vars

  def initTilPatternsStats(self):
    field = 'til%dpattern' %(self.tilN)
    pDict, pList = sa.getAttr(field, self.sqlTable)
    #print pList

  def getAllPatterns(self):
    pass

  def choose(self, jogo):
    jogoObj = CLClasses.Jogo(jogo, self.standard2LetterName)
    tilPattern = jogoObj.getTilPattern(self.tilN)
    print 'tilPattern', tilPattern


class TilPatternsComposer(CLClasses.Base):
  '''
  class TilPatternsChoice

  Rules for choice: (the rules are implemented in the method "choose()")

    1) if a single digit is higher than the highest one ever occurred,
      return False "on jogo"


  '''

  def __init__(self, standard2LetterName, tilN=5):
    CLClasses.Base.__init__(self, standard2LetterName)
    self.directionVector = [] # formerly called sobeDesceList

  def run(self):
    for pattern in self.tilPatternsChoosen:
      pass


def seeSoma():
  aListOfDicts = sa.getAttrs(['jogoCharOrig', 'soma'])
  nDoConc = 0
  somaMin = 1000
  somaMax = 0
  somaDasSomas = 0
  totalSobe  = 0; totalDesce = 0; sobeDesceDepth = 0
  somaList = []; sobeDesceList = []
  for attrDict in aListOfDicts:
    attrs = attrDict.keys()
    # the SELECT is ORDERed BY nDoConc
    nDoConc += 1
    print nDoConc, 
    jogoCharOrig = attrDict['jogoCharOrig']
    jogoObj = CLClasses.Jogo(jogoCharOrig, 'ms')
    jogo = jogoObj.jogo # jogoAsEntered
    print pprint.number_list_to_str_commaless(jogo, 2),

    soma = attrDict['soma']

    print soma,

    shouldBeSoma = sum(jogo)
    assert(soma == shouldBeSoma)

    somaDasSomas += soma
    somaList.append(soma)

    sobeDesce = 0
    if nDoConc > 1:
      if soma > somaAnt:
        if sobeDesceAnt <> 1:
          sobeDesceDepth = 0
        else:
          sobeDesceDepth += 1
        sobeDesce = 1
        totalSobe += 1
      elif soma < somaAnt:
        if sobeDesceAnt <> -1:
          sobeDesceDepth = 0
        else:
          sobeDesceDepth += 1
        sobeDesce = -1
        totalDesce += 1

    sobeDesceAnt = sobeDesce

    sobeDesceList.append(sobeDesce)

    print sobeDesce, 'ts =', totalSobe, 'td =', totalDesce, 'depth',  sobeDesceDepth,

    if soma > somaMax:
      somaMax = soma
      print 'MAX',
    if soma < somaMin:
      somaMin = soma
      print 'min',
    somaAnt = soma
    print

  print 'somaMax', somaMax
  print 'somaMin', somaMin
  mostMax = sum(range(55,61))
  print 'mostMax', mostMax
  leastMin = sum(range(1,7))
  print 'leastMin', leastMin
  avg = somaDasSomas / (nDoConc + 0.0)
  print 'avg', avg


  #matplotlib.plot(somaList)
  #print sobeDesceList
  sobeDesceDict = {}
  for sd in sobeDesceList:
    try:
      sobeDesceDict[sd] += 1
    except KeyError:
      sobeDesceDict[sd] = 1
  print sobeDesceDict

def investigateTils():
  tils = getAttrInDB()
  tilDict = {}
  for til in tils:
    try:
      tilDict[til]+=1
    except KeyError:
      tilDict[til]=1
  return tilDict

digits = '0112222222'
# swap the last 1 with the first 2
# go swapping the 1 with each remaining 2 to the right
# swap the first 1 with the first 2
# go swapping the 1 with each remaining 2 to the right
def swap(posX, posY, digits):
  outDigits = list(digits)
  tmp = outDigits[posX]
  outDigits[posX] = outDigits[posY]
  outDigits[posY] = tmp
  print 'swap x', posX, 'y', posY, 'dx1', tmp, 'dy1',outDigits[posX]
  return outDigits

def sweep(posX, posY, digits):
  if posY == len(digits):
    depth += 1
    if posX == len(digits)-1:
      return
    posY = posX + 1
    return sweep(posX, posY, digits)
  modifiedDigits = swap(posX, posY, digits)
  print ''.join(modifiedDigits)
  return sweep(posX, posY+1, digits)

'''def trans_list_to_nonspace_jointstr(lista):
  return ''.join(lista)
'''

digitsOrig = pprint.strToCharList('0122')
def prepForSweep():
  print 'prepForSweep() digitsOrig =', digitsOrig
  digits = list(digitsOrig)
  print ''.join(digits)
  posX     = 0
  depth    = 0
  posY     = posX + 1
  sweep(posX, posY, digits)


def removeNoneFromList(lista):
  outList = []
  for elem in lista:
    if elem <> None:
      outList.append(elem)
  return outList


def analyzeSomaN(n):
  jogosObj = CLClasses.getJogosObj('lf')
  attr = 'soma%d' %(n)
  somaNDict, somaNList = sa.getAttr(attr, jogosObj.sqlTable)
  # Remeber: the first 14 values are None, so let's remove them
  somaNList = removeNoneFromList(somaNList)

  somaAnt = somaNList[0]
  directionAnt = 0 # defaults to a 'plateau' position
  desce   = 0; desceDist   = 0; desceDistMax   = 0; desceAmount   = 0; desceAmountMin = 0
  plateau = 0; plateauDist = 0; plateauDistMax = 0; plateauAmount = 0; plateauAmountMax = 0
  sobe    = 0; sobeDist    = 0; sobeDistMax    = 0; sobeAmount    = 0; sobeAmountMax = 0
  i=0
  for somaElem in somaNList[1:]:
    i+=1
    delta = somaElem - somaAnt
    if delta < 0:
      pText = 'DESC'
      desce += 1
      if directionAnt == -1:
        desceDist += 1
        desceAmount += delta
      else: # broke direction
        desceDist = 1
        desceAmount = delta
      if desceDist > desceDistMax:
        desceDistMax = desceDist
      if desceAmount < desceAmountMin:
        desceAmountMin = desceAmount

      tupleAmount = desceAmount, desceAmountMin
      directionAnt = -1
      #print 'desce', desce, 'desceDist', desceDist, 'desceDistMax', desceDistMax
    elif delta > 0:
      pText = 'SOBE'
      sobe += 1
      if directionAnt == 1:
        sobeDist += 1
        sobeAmount += delta
      else: # broke direction
        sobeDist = 1
        sobeAmount = delta
      if sobeDist > sobeDistMax:
        sobeDistMax = sobeDist
      if sobeAmount > sobeAmountMax:
        sobeAmountMax = sobeAmount

      tupleAmount = sobeAmount, sobeAmountMax
      directionAnt = 1

    else: #  somaElem == somaAnt:
      pText = 'PLAT'
      plateau += 1
      if directionAnt == 0:
        plateauDist += 1
        plateauAmount += delta
      else:
        plateauDist = 1
        plateauAmount = delta
      if plateauDist > plateauDistMax:
        plateauDistMax = plateauDist
      if plateauAmount > plateauAmountMax:
        plateauAmountMax = plateauAmount

      tupleAmount = plateauAmount, plateauAmountMax
      directionAnt = 0


    print '%03d %s ant=%d this=%d delta=%d %s' %(i, pText, somaAnt, somaElem, delta, tupleAmount)

    somaAnt = somaElem
  print 'desce', desce, 'desceDistMax', desceDistMax
  print 'sobe', sobe, 'sobeDistMax', sobeDistMax
  print 'plateau', plateau, 'plateauDistMax', plateauDistMax


  na = numpy.array(somaNList, int)
  soma = na.sum()
  avg = float(soma) / len(somaNList)
  print 'avg', avg
  print 'std', na.std()
  #histG = Stat.makeHistogram(soma15Dict)
  pprint.print_dict(somaNDict)


def isNumberWithinRegion(n, nMin, nMax):
  if n > nMin - 1 and n < nMax + 1:
    return True
  return False

def somaOfNJogosBefore(theJogosBefore):
  somaParcel = 0
  lgisPassed = []
  for jogo in theJogosBefore:
    somaParcel += sum(jogo)
  print 'theJogosBefore size', len(theJogosBefore), 'somaParcel', somaParcel
  return somaParcel

def seeHowManyPassFilterForSomaN(n=1, somaMin=0, somaMax=10000):
  jogosObj = CLClasses.getJogosObj('lf')
  jogos = jogosObj.getJogos()
  lgiComb = lc.LgiCombiner(24, 15)

  oneLess = 15 - 1
  theJogosBefore = jogos [-oneLess: ]
  somaParcel = somaOfNJogosBefore(theJogosBefore)

  somaMin = 2858 + 15
  somaMax = 2858 + 15 + 45

  jogo = lgiComb.first(); nOfPassed = 0; i=0; lgisPassed = []
  while jogo:
    somaN = sum(jogo) + somaParcel
    if isNumberWithinRegion(somaN, somaMin, somaMax):
      nOfPassed += 1
      lgisPassed.append(i)
    jogo = lgiComb.next()
    i+=1
    if  i % 100000 == 0:
      print 'nOfPassed =', nOfPassed, 'i =', i
  dif = i - nOfPassed
  print 'nOfPassed =', nOfPassed, 'i =', i, 'excluded', dif, 'len(lgisPassed)', len(lgisPassed)

  oneLess = 7 - 1
  theJogosBefore = jogos [-oneLess: ]
  somaParcel = somaOfNJogosBefore(theJogosBefore)

  somaMin = 1304 + 10
  somaMax = somaMin + 50
  nOfPassed = 0; nextLgisPassed = []; c=0
  for i in lgisPassed:
    jogo = lgiComb.move_to(i)
    somaN = sum(jogo) + somaParcel
    if isNumberWithinRegion(somaN, somaMin, somaMax):
      nOfPassed += 1
      #nextLgisPassed.append(i)
    if  c % 100000 == 0:
      print 'nOfPassed =', nOfPassed, 'i =', i, 'c =', c
    c+=1

  dif = c - nOfPassed
  print 'nOfPassed =', nOfPassed, 'c =', c, 'excluded', dif


def adhoc_test():
  seeHowManyPassFilterForSomaN()
  '''
  o = TilPatternsChoice('ms')
  jogo = range(1, 7)
  o.choose(jogo)
  #print o.histG

  o=SomaChoice('ms')
  #print o.directionVector
  print o
  jogo = range(1, 7)
  o.choose(jogo)
  print o.faixas
  print o.slices

  prepForSweep()
  tilDict = investigateTils()
  pprint.print_dict(tilDict)
  '''
   

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
