#!/usr/bin/env python
# -*- coding: utf-8 -*-

a=1
import IndicesCombiner as ic
import CLClasses
from carprint import pprint

def somaDict(absorbingDict, dDict):
  for key in dDict.keys():
    try:
      absorbingDict[key] += dDict[key]
    except KeyError:
      absorbingDict[key]  = dDict[key]
  return absorbingDict

fInt = lambda x: int(x)
def analyseJogoInOrderPatterns():
  lines = open('dznUnitPatt.txt').readlines()
  c = 0; usedLinsColsDict = {}
  dSeqRDict    = {}; uSeqRDict    = {}
  dSimpleRDict = {}; uSimpleRDict = {}
  for line in lines:
    patt = ''
    pp = line.split(' ')
    try:
      int(pp[0])
      jogoInOrder = map(fInt, pp[1:7])
      pattExt = pp[7]
      patt = pp[7][3:]
    except IndexError:
      continue
    except ValueError:
      continue
    print 'jogoInOrder', jogoInOrder
    jogoInOrderPatt = JogoInOrderPatt(patt)
    jogoInOrderPatt.report()
    xDict = jogoInOrderPatt.seqRepeatDrawDznDict
    dSeqRDict = somaDict(dSeqRDict, xDict)
    xDict = jogoInOrderPatt.seqRepeatDrawUnitDict
    uSeqRDict = somaDict(uSeqRDict, xDict)
    xDict = jogoInOrderPatt.simpleRepeatDrawDznDict
    dSimpleRDict = somaDict(dSimpleRDict, xDict)
    xDict = jogoInOrderPatt.simpleRepeatDrawUnitDict
    uSimpleRDict = somaDict(uSimpleRDict, xDict)
    c += 1
    usedLinsCols = pattExt.split(':')[0]
    try:
      usedLinsColsDict[usedLinsCols] += 1
    except KeyError:
      usedLinsColsDict[usedLinsCols] = 1
    print c, patt
  print usedLinsColsDict
  usedLinsCols = usedLinsColsDict.keys()
  usedLinsCols.sort()
  for usedLinCol in usedLinsCols:
    print usedLinCol, usedLinsColsDict[usedLinCol]
    try:
      idxAPLC = allPossibleLinsCols.index(usedLinCol)
      del allPossibleLinsCols[idxAPLC]
    except ValueError:
      print 'ValueError: idxAPLC = allPossibleLinsCols.index(usedLinCol)',usedLinCol

  print allPossibleLinsCols

  print 'dSeqRDict', dSeqRDict
  print 'uSeqRDict', uSeqRDict
  print 'dSimpleRDict', dSimpleRDict
  print 'uSimpleRDict', uSimpleRDict
    
allPossibleLinsCols=[\
  '16','23','24','25','26','32','33','34','35','36','42',\
  '43','44','45','46','52','53','54','55','56','61','62',\
  '63','64','65','66']

class JogoInOrderPatt(object):
  '''
  Attributes:
    self.jogoInOrderPatt = jogoInOrderPatt
    self.seqRepeatDrawDznDict = {}
    self.seqRepeatDrawUnitDict = {}
    self.repeatDrawDznDict = {}
    self.repeatDrawUnitDict = {}
    self.getMaxSimpleRepeatDzn()
    self.getMaxSimpleRepeatUnit()
    
  '''

  def __init__(self, jogoInOrderPatt):
    self.jogoInOrderPatt = jogoInOrderPatt
    self.calculateDigitObjects()
    self.calculateSeqRepeat()
    self.calculateSimpleRepeat()

  def getMaxSimpleRepeatInDzns(self):
    quants = self.simpleRepeatDrawDznDict.values()
    return max(quants)

  def getMaxSimpleRepeatInUnits(self):
    quants = self.simpleRepeatDrawUnitDict.values()
    return max(quants)

  def getMaxSimpleRepeatForDzn(self, dzn):
    if dzn in self.simpleRepeatDrawDznDict.keys():
      return self.simpleRepeatDrawDznDict[dzn]
    else:
      return None

  def getMaxSimpleRepeatForUnit(self, unit):
    if unit in self.simpleRepeatDrawUnitDict.keys():
      return self.simpleRepeatDrawUnitDict[unit]
    else:
      return None

  def calculateDigitObjects(self):
    dznPatts  = []; unitPatts = []
    # first char must be 'd'
    if self.jogoInOrderPatt[0] <> 'd':
      raise ValueError, 'jogoInOrderPatt should start with "d"'
    firstUPos = self.jogoInOrderPatt.find('u')
    if firstUPos < 7:
      raise ValueError, 'jogoInOrderPatt should have "d" start at least 7 positions away'

    dznPatt = ''
    for i in range(1, firstUPos):
      chr = self.jogoInOrderPatt[i]
      if chr == 'd':
        dznPatts.append(dznPatt)
        dznPatt = ''
        continue
      dznPatt += chr
    if len(dznPatt) > 0:
      dznPatts.append(dznPatt)

    unitPatt = ''
    for i in range(firstUPos+1, len(self.jogoInOrderPatt)):
      chr = self.jogoInOrderPatt[i]
      if chr == 'u':
        unitPatts.append(unitPatt)
        unitPatt = ''
        continue
      unitPatt += chr
    if len(unitPatt) > 0:
      unitPatts.append(unitPatt)

    tmpFD = lambda x : DznOrUnitPatt(x,'d')
    tmpFU = lambda x : DznOrUnitPatt(x,'u')
    self.unitPatts = map(tmpFU, unitPatts)
    self.dznPatts  = map(tmpFD, dznPatts)

  def calculateSeqRepeat(self):
    self.seqRepeatDrawDznDict = {}
    self.seqRepeatDrawUnitDict = {}
    for dznPatt in self.dznPatts:
      #print 'dznPatt', dznPatt
      repeat = dznPatt.nOfRepeatedDraw
      try:
        self.seqRepeatDrawDznDict[repeat] += 1
      except KeyError:
        self.seqRepeatDrawDznDict[repeat] = 1
    for unitPatt in self.unitPatts:
      #print 'unitPatt', unitPatt
      repeat = unitPatt.nOfRepeatedDraw
      try:
        self.seqRepeatDrawUnitDict[repeat] += 1
      except KeyError:
        self.seqRepeatDrawUnitDict[repeat] = 1
    
  def calculateSimpleRepeat(self):
    self.simpleRepeatDrawDznDict = {}
    self.simpleRepeatDrawUnitDict = {}
    for dznPatt in self.dznPatts:
      #print 'dznPatt', dznPatt
      simpleRepeat = dznPatt.quant
      try:
        self.simpleRepeatDrawDznDict[simpleRepeat] += 1
      except KeyError:
        self.simpleRepeatDrawDznDict[simpleRepeat] = 1
    for unitPatt in self.unitPatts:
      #print 'unitPatt', unitPatt
      simpleRepeat = unitPatt.quant
      try:
        self.simpleRepeatDrawUnitDict[simpleRepeat] += 1
      except KeyError:
        self.simpleRepeatDrawUnitDict[simpleRepeat] = 1
  
  def report(self):
    print 'seqRepeatDrawDznDict',     self.seqRepeatDrawDznDict
    print 'seqRepeatDrawUnitDict',    self.seqRepeatDrawUnitDict
    print 'simpleRepeatDrawDznDict',  self.simpleRepeatDrawDznDict
    print 'simpleRepeatDrawUnitDict', self.simpleRepeatDrawUnitDict

class DznOrUnitPatt(object):
  '''
  Attributes:
    self.dOrU = dOrU
    self.digit = dznPatt[0]
    self.occurIndices = dznPatt[1:]
    self.quant = len(self.occurIndices)
    self.nOfRepeatedDraw
  '''
  def __init__(self, dznPatt, dOrU='d'):
    self.dOrU = dOrU
    self.digit = dznPatt[0]
    self.occurIndices = dznPatt[1:]
    self.quant = len(self.occurIndices)
    self.calculateRepeatedDraw()
  def calculateRepeatedDraw(self):
    self.nOfRepeatedDraw = 0
    if len(self.occurIndices) < 2:
      return
    previous = self.occurIndices[0]
    for index in self.occurIndices[1:]:
      #print 'index', index, 'prev', previous
      intIndex = int(index)
      intPrevious = int(previous)
      if intIndex == intPrevious + 1:
        self.nOfRepeatedDraw += 1
      previous = index

  def __str__(self):
    outStr = '%s%sq%dr%d' %(self.dOrU, self.digit, self.quant, self.nOfRepeatedDraw)
    return outStr


class Gerador(CLClasses.Jogo):

  excludeQuantLinColPatt = ['16', '23', '32', '42', '52', '61', '62', '63']
  attrs = ['nMaxOfSimpleRepeatDzn','nMaxOfSimpleRepeatUnit']
  attrsSet = []

  def __init__(self, jogo, standard2LetterName='MS'):
    CLClasses.Jogo.__init__(self, jogo, standard2LetterName)
    # order is not important, because a chosen jogo can be rearranged
    # the seqRepeat is not being checked, but simpleRepeat is
    self.JogoInOrderPatt = JogoInOrderPatt(self.jogo)
    self.conds = []

  def setCond(self, cond):
    '''
    Eg
    'self.nMaxOfSimpleRepeatDzn = 2'
    'self.nMaxOfSimpleRepeatUnit = 3'
    '''
    pos = cond.find('=')
    if pos < 0:
      return
    attr = cond[:pos]
    if attr not in self.attrs:
      return
    # setting the condition dynamically
    exec('self.' + cond)
    self.attrsSet.append(attr)

  def sweep(self):
    '''
    simpleRepeatDrawDznDict
    '''
    print 'sweep(self):', self.jogoInOrder
    for dezena in self.jogoInOrder:
      unit = dezena % 10
      dzn  = dezena / 10
      if dzn == '6' and self.jogoObj.standard2LetterName == 'MS':
        dzn = 0
      if 'nMaxOfSimpleRepeatDzn' in self.attrsSet:
        maxDzn = self.JogoInOrderPatt.getMaxSimpleRepeatForDzn(dzn)
        if maxDzn > self.nMaxOfSimpleRepeatDzn:
          return False
      if 'nMaxOfSimpleRepeatUnit' in self.attrsSet:
        maxUnit = self.JogoInOrderPatt.getMaxSimpleRepeatForUnit(unit)
        if maxUnit > self.nMaxOfSimpleRepeatUnit:
          return False
        

def testGerador():
  jogoObj = CLClasses.Jogo([41, 5, 4, 52, 30, 33])
  ger = Gerador(jogoObj)
  
class Gerador2(object):

  def __init__(self, jogosObj):
    self.jogosObj = jogosObj
    self.initLgisToBeUsed()

  def initLgisToBeUsed(self):
    histGJogosLgisForATilFaixa =     self.jogosObj.getHistGJogosLgisForATilFaixa(5)
    quants = histGJogosLgisForATilFaixa.values()
    quants.sort()
    quantCorte = quants[len(quants)/2]
    self.chosenLgis = []
    for lgi in histGJogosLgisForATilFaixa.keys():
      if histGJogosLgisForATilFaixa[lgi] > quantCorte:
        #print lgi
        self.chosenLgis.append(lgi)

  def mountFirstSets(self):
    betJogos = []; jogosStrDict = {}
    tilObj = LFClasses.Til(5); nOfLgi = 0; totalLgis = len(self.chosenLgis); lgisAlreadyGenerated = []
    for chosenLgi in self.chosenLgis:
      nOfLgi += 1
      print 'chosenLgi', chosenLgi, 'n.', nOfLgi, 'of', totalLgis
      setsForMultiply = []
      faixaIndex = 0
      for char in chosenLgi:
        digit = int(char)
        dezenas = tilObj.getDezenasNaFaixa(faixaIndex)
        faixaIndex += 1
        sets = []
        if digit == 0 or len(dezenas) < digit:
          continue
        elif len(dezenas) == digit:
          sets = [dezenas]
        else:
          sets = ic.setCombine(dezenas, digit)
        if len(sets) > 0:
          setsForMultiply.append(sets)
      icSet = ic.setMultiply(setsForMultiply)
      jogosStrDict = extractJogosFrom3DList(icSet, jogosStrDict)
      #jogosEncDict = extractJogosFrom3DList(icSet, jogosEncDict)
    return jogosStrDict


nLower = 10203040506070809101112131415
def extractJogosFrom3DList(nestedList, jogosStrDict):
  c = 0
  for sublist in nestedList:
    jogo = []
    for dezenas in sublist:
      for dezena in dezenas:
        jogo.append(dezena)
    jogo.sort()
    jogoStr = pprint.jogoListToStrNoPrettyPrint(jogo)
    jogoEnc = int(jogoStr)
    #print jogoStr
    c+=1
    if c % 50000 == 0:
      print c,
    jogosStrDict[jogoStr] = 1
  print 'len jogosStrDict', len(jogosStrDict)
  return jogosStrDict

'''
back

def extractJogosFrom3DList(nestedList, chosenLgi, lgisAlreadyGenerated):
  outFilename = chosenLgi + '.dat'
  print 'Writing', outFilename
  jogosOutfile = open(outFilename,'w')
  c=0; nOfEquals = 0
  for sublist in nestedList:
    jogo = []
    #print 'jogo',
    for dezenas in sublist:
      for dezena in dezenas:
        jogo.append(dezena)
    jogo.sort()
    if len(lgisAlreadyGenerated) > 0:
      r = checkIfJogoHasAlreadyHappened(jogo, lgisAlreadyGenerated)
      if r:
        nOfEquals += 1
        print 'nOfEquals', nOfEquals
        #print nOfEquals, 'jogo already exists, continuing...'
        continue
    line = pprint.jogoListToStr(jogo) + '\n'
    jogosOutfile.write(line)
    c+=1
    #print c,
    #pprint.printJogo(jogo)
  jogosOutfile.close()
  print 'Closing', outFilename, c, 'jogosfs written.'
  return

'''

def getJogoFromLine(line):
  if line.find('\n') > -1:
    line = line[:-1]
    jogo = map(lambdas.to_int, line.split(' '))
    return jogo

def compare(jogo1, jogo2):
  equals = 0
  for i in range(len(jogo1)):
    dezena = jogo1[i]
    if dezena == jogo2[i] and i==equals:
      equals += 1
      if equals == 15:
        return True
    else:
      #print False, 'equals', equals, 'i', i
      return False
  return False

def checkIfJogoHasAlreadyHappened(jogo, lgisAlreadyGenerated):
  #print 'Checking/sweeping for equals', jogo,
  for filenameGenerated in lgisAlreadyGenerated:
    fileGenerated = open(filenameGenerated)
    jogoLine = fileGenerated.readline()
    while jogoLine:
      jogoThere = getJogoFromLine(jogoLine)
      r = compare(jogo, jogoThere)
      if r:
        #print True
        return True
      jogoLine = fileGenerated.readline()
  return False

def checkIfJogoHasAlreadyHappened2(jogo, lgisAlreadyGenerated):
  #print 'Checking/sweeping for equals', jogo,
  for filenameGenerated in lgisAlreadyGenerated:
    text = open(filenameGenerated).read()
    jogoStr = pprint.jogoListToStr(jogo)
    pos = text.find(jogoStr)
    if pos > -1:
      return True
  return False

def extractJogoFromListsNested(nestedList, unNested=[]):
  for elem in nestedList:
    if type(elem) == type([]):
      unNested += extractJogoFromListsNested(elem, unNested)
    else:
      unNested.append(elem)
  return unNested
  '''
      for l1 in icSet:
        print 'l1'
        if type(l1) <> type([]):
          print 'l1', l1,
        else:
          for l2 in l1:
            print 'l2'
            if type(l2) <> type([]):
              print 'l2', l2,
            else:
              for l3 in l2:
                print l3,
  '''

   
def analyzeJogosWithTilFaixas(histG, faixas):
  jogos = ra.getHistoryJogos()
  index = 99; lgiDict = {}
  for jogo in jogos[index:]:
    nOfJogo = index + 1
    print nOfJogo, jogo
    lgi = generateLgiForJogoVsTilFaixas(histG, faixas, jogo)
    index += 1
    try:
      lgiDict[lgi] += 1
    except KeyError:
      lgiDict[lgi] = 1
  printDict(lgiDict)

def combine(dezenasNasFaixas, sizeNow, combination):
  dezenasNow = dezenasNasFaixas[0]
  for dezena in dezenasNow:
    combination.append(dezena)

   
def geradorDeJogos(dezenasNasFaixas, lgis):
  for lgiToUse in lgis:
    useThisLgi = True 
    for faixa in dezenasNasFaixas:
      faixa = list(dezenasNasFaixas[i])
      if len(faixa) < int(lgiToUse[i]):
        # lgi can not be used
        useThisLgi = False
        break
    if useThisLgi:
      combineFaixaWithLgi(faixa, lgiToUse)

def combineFaixaWithLgi(faixa, lgiToUse):
  workFaixas = []
  for quantStr in lgiToUse:
    quant = int(quantStr)
    arrayPieces = generateCombs(workFaixa, quant)
    arrayFaixas.append(arrayPieces)
  combineFaixas(arrayFaixas)
  
def combineFaixas(workFaixas):
  '''
  Under development
  '''
  if len(workFaixas) == 1:
    for faixa in workFaixas:
      return
  innerWorkFaixas = workFaixas[1:]
  for workFaixa in workFaixas:
    faixa = list(workFaixa[0])
    combineFaixas(subWorkFaixas)
    

    useThisLgi = True 
    for faixa in dezenasNasFaixas:
      faixa = list(dezenasNasFaixas[i])
      if len(faixa) < int(lgiToUse[i]):
        # lgi can not be used
        useThisLgi = False
        break
    if useThisLgi:
      combineFaixaWithLgi(faixa, lgiToUse)
  
  
  combine(dezenasNasFaixas, len(dezenasNasFaixas))
  for conj in dezenasNasFaixas:
    pass

def generateFaixasForTil(histG, tilIn=5):
  '''
  The 'tils', so to say, are a generic denomination
  for frequency classes (percentils, quartils, sixtils, etc.)
  The routine/method accepts the number of classes to calculate:
  if tilIn is 4, for instance, the output will be a list with
  the 4-interval points
  '''
  TIL = tilIn
  values = histG.values()
  values.sort()
  soma = sum(values)
  quantMin = min(values)
  quantMax = max(values)
  dist = quantMax - quantMin + 1
  step = dist / TIL
  missing = dist % TIL

  print '''  TIL = %(TIL)d
  values = %(values)s
  soma = %(soma)d
  quantMin = %(quantMin)d
  quantMax = %(quantMax)d
  dist = %(dist)d
  step = %(step)d
  missing = %(missing)d''' %{'TIL':TIL, 'values':values,
  'soma':soma, 'quantMin':quantMin, 'quantMax':quantMax,'dist':dist,
  'step':step, 'missing':missing}

  faixas = [(0,0)]*TIL
  quantFaixaLower = quantMin
  for i in range(len(faixas)):
    quantFaixaUpper = quantFaixaLower + step - 1
    if missing > 0:
      quantFaixaUpper += 1
      missing -= 1
    faixas[i] = (quantFaixaLower, quantFaixaUpper)
    print 'faixa', quantFaixaLower, quantFaixaUpper
    quantFaixaLower = quantFaixaUpper + 1
  print 'histG', histG
  print 'faixas', faixas
  return faixas

def generateLgiForJogoVsTilFaixas(histG, faixas, jogo):
  '''
  Each jogo has a pattern of frequency distribution, ie,
  some dezenas have occurred more than others
  some others have occurred less
  
  lgi is the LexicoGraphical Index
  Eg.
  1c5a203   101010   32001   etc.
  '''
  TIL = len(faixas)
  # lgi is the LexicoGraphical Index
  lgi = ''
  for faixa in faixas:
    quantLower = faixa[0]
    quantUpper = faixa[1]
    print 'faixa', faixa,
    quantNaFaixa = 0
    for dezena in jogo:
      quant = histG[dezena]
      if quant >= quantLower and quant <= quantUpper:
        quantNaFaixa += 1
        print dezena,
    if quantNaFaixa > 15:
      # well, TIL should be larger
      raise ValueError, 'well, TIL should be larger, IT CAN NOT CONTINUE'
    if quantNaFaixa > 9:
      hexadec = hex(quantNaFaixa)
      digit = str(hexadec)[-1]
    else:
      digit = str(quantNaFaixa)
    lgi += digit
    print
  print 'lgi', lgi
  return lgi
  
def tilJogoAJogo():
  startAt = 100
  workJogos = getJogosUpTo(table, startAt)
  histG = makeHistogram(jogos)
  for i in range(startAt,len(table)+1):
    workJogos = sd.continueJogosSequenceBy(table, workJogos)
    lastJogo = jogos[-1]
    histG = sd.incrementalHistogram(histG, lastJogo)
    printJogoWithTils(histG, lastJogo, len(jogos)-1)

def geraCombinacoes(faixaDeDezenas, quant):
  indexCombs = IndicesCombiner.combine(len(faixaDeDezenas), quant)
  outCombs = []
  for indices in indexCombs:
    outComb = []
    for index in indices:
      outComb.append(faixaDeDezenas[index])
    outCombs.append(outComb)
  return outCombs

def combineFaixaDeDezenasWithLgi(faixaDeDezenas, lgiToUse):
  workFaixas = []
  for quantStr in lgiToUse:
    quant = int(quantStr)
    workSets = geraCombinacoes(faixaDeDezenas, quant)
    workFaixas.append(workSets)
  multiplySet(arrayFaixas)

def gera(jogosObj):
  gerador = Gerador(jogosObj)
  jogosStrDict = gerador.mountFirstSets()
  jogosStrList = jogosStrDict.keys()
  outFile = open('jogosfs-bet.txt','w')
  for jogosStr in jogosStrList:
    outFile.write(jogosStr + '\n')
  outFile.close()

if __name__ == '__main__':
  jogosObj = getJogosObj('LF')
  gera(jogosObj)

'''  
if __name__ == '__main__':
  pass
  #analyseJogoInOrderPatterns()
  testGerador()
  dp = DznOrUnitPatt('312','d')
  print 'dp', dp,
  print dp.nOfRepeatedDraw
'''
  
