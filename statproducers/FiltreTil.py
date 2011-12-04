#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import statlib
from statlib import stats
#import numpy
'''
algo
'''

a=1
import Filtre
import funcsForSql as fSql
import Til
from cardprint import pprint


def transfHex(ch):
  if ch=='a':
    return 10
  if ch=='b':
    return 11
  if ch=='c':
    return 12
  if ch=='d':
    return 13
  if ch=='e':
    return 14
  if ch=='f':
    return 15


class FiltreTil(Filtre.Filtre):
  '''
  
  '''

  def __init__(self, eitherJogosObjOrS2):
    Filtre.Filtre.__init__(self, eitherJogosObjOrS2)
    self.excludedPatterns = None
    self.patternsDict = {} # to be a 2-D dict
    #tilObj = Til.Til(self.jogosObj, tilN)
    self.patternReg = {}
    self.initPatterns()
    self.tilNs = (4,5,6,10)

  def getExcludedPatterns(self):
    if self.excludedPatterns <> None:
      return self.excludedPatterns

  def initPatterns(self):
    sql = '''SELECT nDoConc, til4pattern, til5pattern, til6pattern, til10pattern FROM `lf` where nDoConc > 100'''
    db = fSql.DB()
    rows = db.doSelect(sql)
    rowToTilN = {1:4, 2:5, 3:6, 4:10}
    for row in rows:
      #nDoConc  = row[0]; tilList = []
      for i in range(1,5):
        self.addPattern(row[i], rowToTilN[i])

  def addPattern(self, pattern, tilN):
    if tilN not in self.patternsDict.keys():
      theDict = {pattern: 1}
      self.patternsDict[tilN] = dict(theDict)
    else:
      theDict = self.patternsDict[tilN]
      try:
        theDict[pattern] += 1
      except KeyError:
        theDict[pattern] = 1
      
  def getPatternsFor(self, tilN):
    theDict = self.patternsDict[tilN]
    patterns = theDict.keys()
    patterns.sort()
    return patterns
  
  def getPatternsDictFor(self, tilN):
    theDict = self.patternsDict[tilN]
    pprint.printDict(theDict)

  def analyze(self):
    
    for tilN in self.tilNs:
      patterns = self.getPatternsFor(tilN)
      qMax = 0
      for patt in patterns:
        for ch in patt:
          if ch not in ['a','b','c','d','e']:
            quant = int(ch)
          else:
            quant = transfHex(ch)
          if quant > qMax:
            qMax = quant
      print 'for tilN', tilN, 'qMax =', qMax

def testFiltre():
  fTilObj = FiltreTil('lf')
  fTilObj.getPatternsDictFor(5)
  fTilObj.analyze()
  patts = fTilObj.getPatternsFor(5)
  print 'len(patts)', len(patts)
  patts = stats.ltrimboth(patts, 0.1) # statlib.
  #patts = statlib.stats.ltrimboth(patts, 0.1) # statlib.
  print 'len(patts)', len(patts)
  #stats.writecc([patts,patts],'test.txt')
  alist = range(1,6)
  print 'sum(alist)', sum(alist)
  print 'cumsum(alist)', stats.cumsum(alist)
  print 'geometricmean(alist)', stats.geometricmean(alist)

class TilController(object):
  _instance = None
  patternsOccurred = []
  patternsOccurredDict= {}
  patternsNotOccurred = []
  quantMax = 0
  patternMax = None
  minOccurrencesForAPattern = 2    # not used for now, think about a dynamic changing value dependant on what's going on in the history
  maxOccurrencesForAPattern = None 
  forbiddenPatterns = None
  def __new__(self, *args, **kargs):
    # print 'inside SixtilController new'
    if self._instance is None: 
      self._instance = object.__new__(self, *args, **kargs)
      self._instance.initializeAttributes()
    return self._instance
  def initializeAttributes(self): # , reInit=False
    '''
    Note: dictJogoEPatternEHistG goes accumulating jogo upwardly, ie, jogo by jogo as seqNum increases.
    Eg. {1: ('600000', 1), 2: ('600000', 2), 3: ('600000', 3), ...
     23: ('600000', 23), 24: ('600000', 24), 25: ('031011', 1), 26: ('022200', 1), 27: ('102021', 1), ... 
    '''
    dictJogoEPatternEHistG, patternsNotOccurred, patternsDict = generateSixtilPatternsControlObject()
    self.dictJogoEPatternEHistG = dictJogoEPatternEHistG
    self.patternsNotOccurred = patternsNotOccurred
    self.getForbiddenPatterns()
    self.initPatternsOccurredDict()
    #print 'SixtilController initializeAttributes len patternsOccurredDict', len(self.patternsOccurredDict)

  def initPatternsOccurredDict(self):
    nsDeJogos = self.dictJogoEPatternEHistG.keys()
    for nDoJogo in nsDeJogos:
      tuple = self.dictJogoEPatternEHistG[nDoJogo]
      pattern = tuple[0]
      if pattern in self.forbiddenPatterns:
        continue
      try:
        self.patternsOccurredDict[pattern] += 1
      except KeyError:
        self.patternsOccurredDict[pattern] = 1
    self.patternsOccurred = self.patternsOccurredDict.keys()
    self.patternsOccurred.sort()
       
  def getSixtilPatternOfJogo(self, jogoObjOuN):
    if jogoObjOuN == None:
      return None
    nDoJogo = None
    if type(jogoObjOuN) == type(1):
      nDoJogo = jogoObjOuN
    else:
      nDoJogo = jogoObjOuN.getSeqNum()
    if type(nDoJogo) != type(1):
      return None
    tuple =  self.dictJogoEPatternEHistG[nDoJogo]
    pattern = tuple[0]
    return pattern

  def getSixtilPatternAndQuantOfJogo(self, jogoObjOuN):
    if jogoObjOuN == None:
      return None
    nDoJogo = None
    if type(jogoObjOuN) == type(1):
      nDoJogo = jogoObjOuN
    else:
      nDoJogo = jogoObjOuN.getSeqNum()
    if type(nDoJogo) != type(1):
      return None
    if nDoJogo not in self.dictJogoEPatternEHistG.keys():
      return None
    tuple2 =  self.dictJogoEPatternEHistG[nDoJogo]
    pattern = tuple2[0]
    quant   = tuple2[1]
    return quant, pattern

  def getSixtilPatternAndQuantOfJogoMax(self, update=False):
    if not update or self.quantMax == 0:
      self.quantMax = 0  # in case update is True but quantMax is not 0
      patterns = self.patternsOccurredDict.keys()
      for pattern in patterns:
        quant =  self.patternsOccurredDict[pattern]
        if quant > self.quantMax:
          self.quantMax = quant
          self.patternMax = pattern
    return self.quantMax, self.patternMax

  def getPatternsNotOccurred(self):
    return self.patternsNotOccurred
  
  def hasPatternOccurred(self, pattern):
    if pattern not in self.patternsNotOccurred:
      return True
    return False

  def howManyTimesHasPatternOccurred(self, pattern):
    if not self.hasPatternOccurred(pattern):
      return 0
    # if logic of this class is consistent, a KeyError exception will not happen here
    if pattern in self.patternsOccurredDict.keys():
      quant =  self.patternsOccurredDict[pattern] 
      return quant
    return 0
  
  def getPatternMax(self):
    if self.patternMax == None:
      quant, patt = self.getSixtilPatternAndQuantOfJogoMax()
      return patt # it will also go as an attribute inside the class (side-effect of getSixtilPatternAndQuantOfJogoMax())
    return self.patternMax

  def resetPatternsDict(self, patternsDict):
    self.dictJogoEPatternEHistG = dict(patternsDict)  # hard-copy patternsDict 
    self.initPatternsOccurredDict()

  def getSixtilPatternOfGeneralizedJogo(self, jogo):
    return getSixtilPatternOfGeneralizedJogo(jogo)
    
  def whatIsQuantAccOfPatternInJogo(self, jogo):
    pattern = calculateSixtilPattern(jogo)
    quant = 0
    if not self.hasPatternOccurred(pattern):
      return 0
    nDoJogo = jogo.getSeqNum()
    nDosJogos = self.dictJogoEPatternEHistG.keys()
    if nDoJogo in nDosJogos:
      tuple = self.dictJogoEPatternEHistG[nDoJogo]
      patternHere = tuple[0]
      if patternHere != pattern:
        return 0
      quant = tuple[1]
    return quant

  def isPatternInJogo(self, jogo, pattern):
    quant = self.whatIsQuantAccOfPatternInJogo(jogo, pattern)
    if quant <= 0:
      return False
    return True

  def initMaxOccurrencesForAPattern(self):
    quantMax, patternMax = self.getSixtilPatternAndQuantOfJogoMax()
    #print 'initMaxOccurrencesForAPattern quantMax, patternMax', quantMax, patternMax
    self.maxOccurrencesForAPattern = int(quantMax * 0.8)   # 80% of the value of max freq sixtil pattern

  def isPatternAboveMinImposed(self, thisSixtilPattern):
    howManyTimesHasPatternOccurred = self.howManyTimesHasPatternOccurred(thisSixtilPattern)
    #print thisSixtilPattern, 'howManyTimesHasPatternOccurred', howManyTimesHasPatternOccurred
    if howManyTimesHasPatternOccurred < self.minOccurrencesForAPattern:
      return False
    return True    
  
  def isPatternBelowMaxImposed(self, someSixtilPattern):
    howManyTimesHasPatternOccurred = self.howManyTimesHasPatternOccurred(someSixtilPattern)
    #print 'sc isPatternBelowMaxImposed howManyTimesHasPatternOccurred', howManyTimesHasPatternOccurred
    if self.maxOccurrencesForAPattern == None:
      self.initMaxOccurrencesForAPattern()
    #print 'sc maxOccurrencesForAPattern ', self.maxOccurrencesForAPattern
    if howManyTimesHasPatternOccurred > self.maxOccurrencesForAPattern:
      return False
    return True   
  
  def getNOfBackwardJogosForCompare(self):
    return 10  
  
  def getForbiddenPatterns(self):
     '''
     These (forbidden patterns) are the first occurred patterns in history which do not repeat after the 100th jogo.
     This rule/policy/heuristics may change in the future.
     '''
     if self.forbiddenPatterns == None:
       self.forbiddenPatterns = generateForbiddenPatterns() 
     if self.forbiddenPatterns == None or len(self.forbiddenPatterns) == 0:
       raise IndexError, 'forbiddenPatterns is still either None or empty, some problem (eg: it failed reading the Histogram file) has occurred.'
     return self.forbiddenPatterns 

forbiddenSixtilPatterns = None
def generateForbiddenPatterns():
  global forbiddenSixtilPatterns
  if forbiddenSixtilPatterns != None:
    return forbiddenSixtilPatterns
  forbiddenSixtilPatterns = []; patternList = pickUpSixtilHistoryInHistogramFile()
  cutOffLimit = int(len(patternList)*0.15)  # this may change in the future
  for i in range(cutOffLimit):
    if patternList[i] not in patternList[cutOffLimit:]:
      if patternList[i] not in forbiddenSixtilPatterns:
        forbiddenSixtilPatterns.append(patternList[i])
  return forbiddenSixtilPatterns

def getSixtilPatternOfGeneralizedJogo(jogo):
  dezenas = jogo.getDezenas()
  sixtilAcc = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
  sixtils = analyzer.generateSixtils()
  for d in dezenas:
    for i in range(1,7): # sixtils:
      if d in sixtils[i]:
        sixtilAcc[i]+=1
        #print d, 'in sixtil', i, 'sixtilAcc[i]', sixtilAcc[i]
  strPattern = ''
  for i in range(1,7): # sixtils:
    strPattern += str(sixtilAcc[i])
  return strPattern

def calculateSixtilPattern(jogoExt):
  sixtilHistGPattern = ''
  sixtilHistG = ()
  # test jogoExt
  for sixtil in jogoExt.getSixtils():
    sixtilHistG[sixtil] += 1
    sixtilHistGTotal[sixtil] += 1
  for i in range(1,7):
    sixtilHistGPattern += '%d' %(sixtilHistG[i])
  try:
    patternsDict[sixtilHistGPattern] += 1
  except KeyError:
    patternsDict[sixtilHistGPattern] = 1
  return sixtilHistGPattern

def geraSixtilStrusAndPatterns():
  '''
  Line example:
  970    5:115x:6s  21: 89x:3s  28: 96x:4s  34:104x:5s  54:110x:6s  57: 98x:4s
  '''
  filePath = '../Dados/fileHistogramaEvolutivo.txt'
  
  lines = open(filePath).readlines(); jogoExt = None
  for line in lines:
    pp = line.split(' ')
    if len(pp) < 7:
      contine
    try:
      nDoJogo = int(pp[0])
      jogoExt = JogoExt(nDoJogo)
    except ValueError:
      continue
    c = 0
    for p in pp[1:]:
      pos = p.find('s') # s stands for "sixtil"
      if pos > -1:
        sixtil = int(p[pos-1:pos])
        c += 1
        jogoExt.setSixtil(c, sixtil)
    msg = '%s ' %(jogoExt)
    ##print 'msg', msg
    sixtilHistGPattern = calculateSixtilPattern(jogoExt)
    msg += ' ' + sixtilHistGPattern
    for i in range(1,7):
      msg += '%d:' %(sixtilHistGTotal[i])
    ##print msg

  patternsKeys = patternsDict.keys()
  patternsKeys.sort()
  #for patt in patternsKeys:
    ##print patt, patternsDict[patt]
  ##print 'Quant of patterns:', len(patternsKeys)
  return patter


class JogoExt(Sena.Jogo):
  '''
  What's the purpose of the class extension?
  Line example:
  970    5:115x:6s  21: 89x:3s  28: 96x:4s  34:104x:5s  54:110x:6s  57: 98x:4s
  pattern above is 001212 ie sixtil1=0 sixtil2=0 sixtil3=1 sixtil4=2 sixtil5=1 sixtil6=2
  
  The idea of the class extension is to add/manage the sixtil pattern to the jogo object. 
  '''
  sixtils = [-1]*7 # index 0 not used
  sixtilsAcc = [-1]*7
  def __init__(self, nDoJogo=None, jogo=None):
    if jogo == None:
      if nDoJogo == None:
        Sena.Jogo.__init__(self, -1)
        return
      else:
        jogo = jogosPool.getJogo(nDoJogo)
        # if it continues to be None, return
        if jogo == None:
          Sena.Jogo.__init__(self, nDoJogo)
          return
    # if control flow gets here, parameter nDoJogo will be ignored but obviously getSeqNum() will equal it
    Sena.Jogo.__init__(self, jogo.getSeqNum())
    self.setDezenas(jogo.getDezenas())
    ##print self.getDezenas()
    if len(self.dezenas) > 6:
      raise IndexError, 'Error: dezenas has more than 6 elements.'
  def setSixtil(self, index, sixtilQuant):
    if index < 1 or index > 6:
      raise IndexError, 'IndexError in setSixtil(self, index, sixtilQuant) index should be in [1,6].'
    self.sixtils[index] = sixtilQuant
  def getSixtil(self, index):
    if index < 1 or index > 6:
      return None
    return self.sixtils[index]
  def goGetSixtils(self):
    pass
  def getSixtils(self):
    if -1 not in self.sixtils[1:]:
      return self.sixtils
    return self.goGetSixtils()
  def setSixtilAcc(self, index, sixtilQuantAcc):
    if index < 1 or index > 6:
      raise IndexError, 'IndexError in setSixtilAcc(self, index, sixtilQuant) index should be in [1,6].'
    self.sixtilsAcc[index] = sixtilQuantAcc
  def getSixtilAcc(self, index):
    if index < 1 or index > 6:
      return None
    return self.sixtilsAcc[index]
  def getSixtilsAcc(self):
    if -1 not in self.sixtilsAcc[1:]:
      return self.sixtilsAcc
    return None

patternsDict = {}
sixtilHistGTotal = {}
for i in range(7):
  sixtilHistGTotal[i]=0

def zeraSixtil():
  sixtilHistG = {}
  for i in range(7):
    sixtilHistG[i]=0
  return sixtilHistG

def generateSixtilPatternsControlObject(upTo=None):
  '''
  This method reads out fileHistogramaEvolutivo.txt and extracts the sixtil pattern for every jogo.
  Furthermore, it generates a sixtil pattern histogram and compares every pattern with all possible
  combinations of patterns, creating a list with patterns that never occurred.
  '''
  sixtilPatternHistG = {}; dictJogoEPatternEHistG = {}
  filePath = '../Dados/fileHistogramaEvolutivo.txt'
  lines = open(filePath).readlines()
  for line in lines:
    if line[0]=='#':
      continue
    if line[-1]=='\n':
      line=line[:-1]
    pp=line.split(' ')
    if len(pp) > 2:
      nDoJogo = int(pp[0])
      if upTo != None:
        if nDoJogo > upTo:
          break
      sixtilPattern = pp[-2]
      try:
        sixtilPatternHistG[sixtilPattern]+=1
      except KeyError:
        sixtilPatternHistG[sixtilPattern]=1
      #print nDoJogo, 'pattern', sixtilPattern,'x', sixtilPatternHistG[sixtilPattern]  
      dictJogoEPatternEHistG[nDoJogo]=(sixtilPattern, sixtilPatternHistG[sixtilPattern])
  #print 'Now comparing patterns with all patterns existing to see those that never occurred.'
  allPatternCombinations = arrangeSixtilPatternsSoma6()
  #print 'len(allPatterns)', len(allPatterns) 
  occurredPatterns = sixtilPatternHistG.keys()
  #print 'len(occurredPatterns)', len(occurredPatterns) 
  occurredPatterns.sort(); patternsNotOccurred = []
  for pattern in allPatternCombinations:
    if pattern not in occurredPatterns:
      patternsNotOccurred.append(pattern)
  #print 'those that never occurred:', len(allPatterns), 'x', allPatterns
  # instantiate a sixtil control object and return all data via it
  # dictJogoEPatternEHistG = { nDoJogo, (pattern, quant) }, patternsNotOccurred is a list
  # sixtilControl = SixtilControl(dictJogoEPatternEHistG, patternsNotOccurred)
  return dictJogoEPatternEHistG, patternsNotOccurred, sixtilPatternHistG

def sixtilDepth():  
  sixCo =sixtilFunctions.SixtilController()
  dictPatterns = sixCo.dictJogoEPatternEHistG
  nsDoJogo = dictPatterns.keys()
  nsDoJogo.sort()
  nOfLastJogo = nsDoJogo[-1]
  pattAnt, quantAcc = dictPatterns[nsDoJogo[0]]
  dictDepthMax = {}; dictDepthMin = {}
  depth = 1; depthMax = 0; depthMin = 1000; nOfDepthMin = 0; whereMin = 0
  patternsDone = []
  for lockNDoJogo in range(nOfLastJogo, 401, -1):
    pattLock, quantLock = dictPatterns[lockNDoJogo]
    if quantLock == 1:
      continue
    if pattLock in patternsDone:
      continue
    depth = 0; depthMax = 0; depthMin = 1000; nOfDepthMin = 0
    for nDoJogo in range(lockNDoJogo - 1, 400, -1):
      patt, quantAcc = dictPatterns[nDoJogo]
      #print 'nDoJogo', nDoJogo, patt, quantAcc, 'depth', depth
      if pattLock == patt:
        if depth < depthMin and nDoJogo > 300:
          depthMin = depth
          #print '*** found depthMin', depthMin, 'nOfDepthMin', nOfDepthMin
          nOfDepthMin += 1
        whereMin = nDoJogo
        if depth > depthMax:
          #print '*** found depthMax', depthMax, 'lockN', lockNDoJogo, 'nDoJogo', nDoJogo
          depthMax = depth
        depth = 1
      else:
        depth += 1
    patternsDone.append(pattLock)
    dictDepthMax[pattLock] = depthMax
    dictDepthMin[pattLock] = depthMin
    print lockNDoJogo, 'pattLock', pattLock, quantLock, 'depthMax', depthMax, 'depthMin', depthMin, 'nOfDepthMin', nOfDepthMin, 'whereMin', whereMin
  
def testSixtilsObj():
  sObj = SixtilStrusAndPatterns(jogo)
  #print 'jogo', jogo, 'sObj', sObj


if __name__ == '__main__':
  testFiltre()