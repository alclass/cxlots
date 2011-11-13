#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy, os, time
'''
 Heuristics:
  histograma linhas x colunas ou dígito-dezena x dígito-unidade
  histograma (acima) dinâmico (como crescem ou diminuem?) (gráficos?)
  
  quantidade de pares/impares (há algum padrão que se sobressai?)
  
  média e desvio padrão (DP) DP mostrará quão disperso ou próximos estão os nºs sorteados
  
  histórico/freqüência em que um nº repete
  
  cruzamento das heurísticas anteriores (triangulação para formar o conjunto de jogos a apostar) (Algoritmos genéticos? Otimização PO?)
  comparar acertos da tarefa acima  (passado longe a passado recente, ambos conhecidos)
  
  Rotinas auxiliares
    gerador de massa de testes/jogos (randômico / parametrizado)
'''

a=1
import analyzer


def petty(sobeDesce):
  '''
  This is a simple petty-print method. When "sobe", print "+<n>", when "desce", it prints "-<n>" n=1,2,...
  '''
  if sobeDesce > 0:
    return '+'+str(sobeDesce)
  return str(sobeDesce)  # minus sign will be there if negative


class DezenasHGSingleton(object):
  _instance = None
  dezenasHG = {}  
  nDoJogo = None
  def __new__(self, *args, **kargs):
    if self._instance is None: 
      self._instance = object.__new__(self, *args, **kargs)
    return self._instance
  def setNDoJogo(self, nDoJogo):
    ''' The next if is just to avoid a second init, mainly when lots of 'setNDoJogo' happen to the same nDoJogo
	In fact, the init should happen in the __new__ method (this is likely to be improved in the future)
    '''
    if len(self.dezenasHG) > 0 and nDoJogo == self.nDoJogo:
      return
    self.nDoJogo = nDoJogo
    self.dezenasHG = obtemHistGDas60(nDoJogo)
    self.getFrequencyFromHistogramaList(True)
    #print 'DezenasHistogramObj init len', len(self.dezenasHG), self.dezenasHG
  def getDezenasHG(self):
    return self.dezenasHG
  frequencyFromHistogramaList = None
  def frequencyFromHistograma(self, quant):
    freqListDescendingOrder = self.getFrequencyFromHistogramaList()
    size = len(freqListDescendingOrder)
    meio =  size / 2
    for index in range(size):
      freqQuant = freqListDescendingOrder[index]
      if freqQuant == quant:
        return index, meio, size
    return None
  def getFrequencyFromHistogramaList(self, reInit = False):
    if self.frequencyFromHistogramaList <> None and not reInit:
      return self.frequencyFromHistogramaList
    self.frequencyFromHistogramaList = []
    histGDas60 = self.getDezenasHG()
    for d in histGDas60.keys():
      quant = histGDas60[d]
      if quant not in self.frequencyFromHistogramaList:
        self.frequencyFromHistogramaList.append(quant)
    if len(self.frequencyFromHistogramaList) == 0:
      raise 'A Problem occurred in frequencyFromHistograma() :: len(frequencyFromHistogramaList) continues == 0'
    self.frequencyFromHistogramaList.sort()
    self.frequencyFromHistogramaList.reverse()
    return self.frequencyFromHistogramaList
  def frequencyWithDezena(self, d):
    quant = self.dezenasHG[d]
    return self.frequencyFromHistograma(quant)
  def frequencyOfDezena(self, d):
    quant = self.dezenasHG[d]
    return quant
  def getDezenasWithFreq(self, freq):
    histGDas60 = self.getDezenasHG()
    dezenasOut = []
    for dezena in histGDas60.keys():
      if histGDas60[dezena] == freq:
	dezenasOut.append(dezena)
    return dezenasOut
  def getDezenasWithOrderOfFreq(self, order):
    quantList = self.getFrequencyFromHistogramaList()
    if order < 0:
      return None
    elif order > len(quantList) - 1:
      return None
    freq = quantList[order]
    return self.getDezenasWithFreq(freq)
  def pickUpFrequencyOrder(self, dezena):
    index, meio, size = self.frequencyWithDezena(dezena)
    indexBackward = size - index - 1
    return index, indexBackward
  def getOrderDigitNumberAndUppercase(self, dezena):
    index, meio, size = self.frequencyWithDezena(dezena)
    return getDigitNumberAndUppercase(index + 1)
  def getHg2PatternForJogo(self, jogo):
    indexList = []	  
    for dezena in jogo.getDezenas():
      index, meio, size = self.frequencyWithDezena(dezena)
      indexList.append(index)
    indexList.sort()
    hg2Pattern = ''
    for index in indexList:
      hg2Pattern += getDigitNumberAndUppercase(index + 1)
    return hg2Pattern

def varHistograma2():
  filePath = '../Dados/fileHistogram2.txt'
  nDoUltimoJogoNoArq, nDoLastJogo = findOutNOfLastJogoInFile(filePath)
  if nDoUltimoJogoNoArq == None:
    return
  print ' [APPEND] Opening', filePath
  appFile = open(filePath, 'a')
  nOfLastJogo = Sena.getNOfLastJogo()
  hg2Obj = DezenasHGSingleton()
  for nDoJogo in range(nDoUltimoJogoNoArq+1, nOfLastJogo+1):
    jogo = Sena.jogosPool.getJogo(nDoJogo)
    dezenasHistogramObj = DezenasHGSingleton()
    dezenasHistogramObj.setNDoJogo(nDoJogo)
    dezenas = jogo.getSorteadosEmOrdemAscendente()
    line = str(jogo.seqNum) + ' '
    for d in dezenas:
      order, backorder = hg2Obj.pickUpFrequencyOrder(d)
      order += 1    # adjust index (0 -> 1)
      #order = str(order).zfill(2)
      deznFreq = dezenasHistogramObj.frequencyOfDezena(d)
      line += '%2d:%3d:%2d  ' %(d, deznFreq, order)
    line += ' ' + pickUpFrequencyForJogo(jogo)
    appFile.write(line + '\n')

def updateDataFiles():
  variacaoDaSomaEtAl()
  varNsConsecutivos()
  variacaoParImpar()
  variacaoLinhaColuna()
  variacaoRepeats()
  histogramaEvolutivo()
  varHistograma2()

import re
import Sena

def checkIfMoreThanXLettersRepeat(pattern, quantIn=2):
  accDict = {}
  for char in pattern:
    try:
      accDict[char]+=1
    except KeyError:
      accDict[char]=1
  for eachChar in accDict.keys():
    if accDict[eachChar] > quantIn:
      return False
  return True

lettersUppercase = map(chr, range(65, 65+26))
def convertPatternLetter(digit):
  if digit in map(str, range(1,10)):
    return int(digit)
  if digit == '0':
    return 10
  # A is 11, B is 12 and so on
  # calc. ord(A) is 65, so 65 - 54 = 11
  return ord(digit) - 54

def getHg2Patterns():
  filePath = '../Dados/fileHistogram2.txt'
  text=open(filePath).read()
  patt=re.compile('a=(\w+)')
  iter = patt.finditer(text); c = 0
  hgPattDict = {}
  for matchObj in iter:
    c += 1
    if c < 201:
      continue
    hgPattern = matchObj.group(1)
    if hgPattern in hgPattDict.keys():
      hgPattDict[hgPattern] += 1
    else:
      hgPattDict[hgPattern] = 1
    #print c, hgPattern, 'q=', hgPattDict[hgPattern]
  hg2Patterns = hgPattDict.keys()
  hg2Patterns.sort()
  #for patt in patts:
    #print patt
  return hg2Patterns

def getMinMaxIntraFreqs():
  '''
  Eg output
977 seeing pattern 170EMW
978 seeing pattern 380CJL
979 seeing pattern 4DEJKT
980 seeing pattern 68AGHH
(...)
  Min/Max:
Digit 0 :: min 1 max 18
Digit 1 :: min 1 max 21
Digit 2 :: min 2 max 23
Digit 3 :: min 4 max 27
Digit 4 :: min 6 max 30
Digit 5 :: min 9 max 33

  ''' 
  filePath = '../Dados/fileHistogram2.txt'
  lines = open(filePath).readlines()
  # pick up only half of the file, patterns before "half" do not enter into account
  lines = lines[len(lines)/2:]
  text = '\n'.join(lines)
  minIntraDigit = [1000] * 6; maxIntraDigit = [-1] * 6; accDigit = [0] * 6
  import re
  patt = re.compile('a=(\w+)')
  iter = patt.finditer(text)
  for matchObj in iter:
    hg2Pattern = matchObj.group(1); digit = [None] * 6
    for i in range(6):
      digit[i] = convertPatternLetter(hg2Pattern[i])
      #print 'digit i=', i, digit[i],
      #maxAcross[digit[i]] += 1
      if digit[i] < minIntraDigit[i]:
        minIntraDigit[i] = digit[i]
      elif digit[i] > maxIntraDigit[i]:
        maxIntraDigit[i] = digit[i]
  #print 'Min/Max:'
  minMaxIntraListOfTuples = [None] * 6
  for i in range(6):
    #print 'Digit', i, ':: min', minIntraDigit[i], 'max', maxIntraDigit[i]
    minMaxIntraListOfTuples[i] = (minIntraDigit[i], maxIntraDigit[i])
  return minMaxIntraListOfTuples

#import atualizaStatisticsEtAl
def pickUpDezenasWithHg2(orders):
  orders = [1, 4, 6, 8]
  for order in range(32):
    hg2Obj = atualizaStatisticsEtAl.DezenasHGSingleton()
    hg2Obj.setNDoJogo(Sena.getNOfLastJogo())
    ds = hg2Obj.getDezenasWithOrderOfFreq(order)
    #print 'order', order, 'dezenas', ds

def balanceSets(setsToBalance):
  # balance sizes
  maxSize = 0; minSize = 1000; maxIndex = None; minIndex = None
  for i in range(0, len(setsToBalance)):
    if len(setsToBalance[i]) > maxSize:
      maxSize = len(setsToBalance[i])
      maxIndex = i
    if len(setsToBalance[i]) < minSize:
      minSize = len(setsToBalance[i])
      minIndex = i
  dif = maxSize - minSize
  #print 'maxIndex', maxIndex, 'minIndex', minIndex
  if dif < 2 or minIndex == maxIndex:
    return setsToBalance
  passToOtherSide = dif/2
  for i in range(passToOtherSide):
    elem = setsToBalance[maxIndex][i]
    #print 'balancing',i, 'elem', elem
    setsToBalance[minIndex].append(elem)
  setsToBalance[maxIndex] = setsToBalance[maxIndex][passToOtherSide:]
  #print 'new sizes: ex-max=',len(setsToBalance[maxIndex]), 'ex-min',len(setsToBalance[minIndex])
  return balanceSets(setsToBalance)

def cleanUpRepeatingDezenas(setsToCleanIntersection):
  '''
  setComb has various sets (list of lists)
  '''
  if len(setsToCleanIntersection) < 2:
    return setsToCleanIntersection
  newSet = [None] * len(setsToCleanIntersection)
  for i in range(0, len(setsToCleanIntersection)-1):
    for j in range(i+1, len(setsToCleanIntersection)):
      newSet[j] = []
      for elem in setsToCleanIntersection[j]:
        if elem not in setsToCleanIntersection[i]:
          newSet[j].append(elem)
  for i in range(len(setsToCleanIntersection)):
    if newSet[i] <> None:
      setsToCleanIntersection[i] = list(newSet[i])
  #setsToCleanIntersection = balanceSets(setsToCleanIntersection)
  return setsToCleanIntersection

def getSubSetsForCombination():
  minMaxIntraListOfTuples = getMinMaxIntraFreqs(); setsForComb = [None] * 6
  hg2Obj = atualizaStatisticsEtAl.DezenasHGSingleton()
  hg2Obj.setNDoJogo(Sena.getNOfLastJogo())
  for i in range(6):
    minIntraDigit, maxIntraDigit = minMaxIntraListOfTuples[i]
    dif = maxIntraDigit - minIntraDigit
    if i > 0 and dif >= 5:
      minIntraDigit = int(minIntraDigit + dif * 0.2)
    if i < 5 and dif >= 5:
      maxIntraDigit = int(maxIntraDigit - dif * 0.2)
    setsForComb[i] = []
    for order in range(minIntraDigit, maxIntraDigit + 1):
      dezenas = hg2Obj.getDezenasWithOrderOfFreq(order)
      if dezenas == None:
        continue
      setsForComb[i] += dezenas
    setsForComb[i].sort()
  setsForComb = cleanUpRepeatingDezenas(setsForComb)
  setsForComb = balanceSets(setsForComb)
  print '='*40    
  for i in range(len(setsForComb)):
    setsForComb[i].sort()
    print 'Comb', i, 'size', len(setsForComb[i]), setsForComb[i]
  print '='*40    
  return setsForComb

def writeOutSubSets(setsForComb, nOfNextConc):
  outFilename = '../Apostas/setsForComb-%d.txt' %(nOfNextConc)
  outFile = open(outFilename, 'w')
  line = 'Sets for Combination (Megasena concurso %d)' %(nOfNextConc)
  print line
  outFile.write(line + '\n')
  line = '='*40
  print line
  outFile.write(line + '\n')
  for i in range(len(setsForComb)):
    setsForComb[i].sort()
    line = 'Comb %d size %d %s' %(i, len(setsForComb[i]), str(setsForComb[i]))
    print line
    outFile.write(line + '\n')
  outFile.close()

def doCombinations(nOfNextConc=Sena.getNOfLastJogo()+1):
  filePath = '../Apostas/CombinationsChain-level-1-%s.txt'  %(nOfNextConc)
  dumpFile = open(filePath, 'w')
  subSets = getSubSetsForCombination(); c=0; d=[None]*6
  writeOutSubSets(subSets, nOfNextConc)
  hg2Patterns = getHg2Patterns()
  for d[0] in subSets[0]:
    for d[1] in subSets[1]:
      if d[1] == d[0]:
        continue
      for d[2] in subSets[2]:
        if d[2] == d[0] or d[2] == d[1]:
          continue
        for d[3] in subSets[3]:
          if d[3] == d[0] or d[3] == d[1] or d[3] == d[2]:
            continue
          for d[4] in subSets[4]:
            doContinue = False
            for j in range(4):
              if d[4] == d[j]:
                doContinue = True
                break
            if doContinue:
              continue
            for d[5] in subSets[5]:
              doContinue = False
              for j in range(5):
                if d[5] == d[j]:
                  doContinue = True
                  break
              if doContinue:
                continue
              line = ''; c+=1
        # DO NOT d.sort()
        dCopy = d[:] # hard copying "d"
        dCopy.sort()
        for j in range(6):
          line += '%s ' %(str(dCopy[j]).zfill(2))
        jogo = Sena.Jogo(-c)
        jogo.setDezenas(dCopy)
        hg2Pattern = jogo.getHg2Pattern()
        ok = False
        resp = checkIfMoreThanXLettersRepeat(hg2Pattern, 2)
        if not resp:
          print 'hg2Pattern (',hg2Pattern,') has more than 2 repeats.'
        hg2Conform = True
        if hg2Pattern in hg2Patterns:
          print 'hg2Pattern (',hg2Pattern,') in hg2Patterns, filtering out'
        hg2Conform = False
        if resp and hg2Conform:
          ok = True
        if ok:
            #line = line + hg2Pattern
            dumpFile.write(line + '\n')
        if c % 1000 == 0:
          print c  #, line, hg2Pattern, 'ok', ok

def dezenasIntFromTextLine(line):
  try:
    dezenas = map(int, line.split(' ')[:6])
  except ValueError:
    return None
  except IndexError:
    return None
  return dezenas

import filters
tmpF = lambda x: str(x).zfill(2)
def chainLevel1to2(nOfNextConc=Sena.getNOfLastJogo()+1):
  filePath = '../Apostas/CombinationsChain-level-1-%s.txt' %(nOfNextConc)
  inFile = open(filePath)
  filePathOutput = '../Apostas/CombinationsChain-level-2-%s.txt' %(nOfNextConc)
  outFile = open(filePathOutput, 'w')
  line = inFile.readline(); c = 0
  while line:
    dezenas = dezenasIntFromTextLine(line)
    if dezenas == None:
      line = inFile.readline()
      continue
    c += 1
    jogo = Sena.Jogo(-c)
    jogo.setDezenas(dezenas)
    tuple2 = filters.passThruFilters(jogo)
    hasPassed = tuple2[0]
    if not hasPassed:
      msgCode = tuple2[1]
      print jogo, filters.getMessageStrFromFilterReturnNumberCode(msgCode)
    else:
      dezenasStrList = map(tmpF, dezenas)
      dezenasStr = ' '.join(dezenasStrList)
      outLine = '%s' %(dezenasStr)
      outFile.write(outLine + '\n')
    line = inFile.readline()
  outFile.close()

def genLastLineTotalDeApostas(quantToBuy):
 return 'Total de Apostas: %d (x 1.75 = R$ %5.2f)' %(quantToBuy, 1.75*quantToBuy)

tmpF = lambda x:str(x).zfill(2)
def generateOutputJogosToBuy(jogosToBuy, nOfNextJogo=None):
  if nOfNextJogo == None:
    nOfNextJogo = Sena.getNOfLastJogo() + 1
  filePath = '../Apostas/apostas-%s.txt' %(str(nOfNextJogo).zfill(4))
  print 'Writing file', filePath
  appFile = open(filePath, 'w')
  line = '%d:' %(nOfNextJogo)
  appFile.write(line + '\n')
  for jogo in jogosToBuy:
    dezenas = map(tmpF, jogo.getDezenas())
    dezenasStr = ' '.join(dezenas)
    line = '%s' %(dezenasStr)
    appFile.write(line + '\n')
  quantToBuy = len(jogosToBuy)
  line = genLastLineTotalDeApostas(quantToBuy)
  appFile.write(line + '\n')
  print quantToBuy, 'apostas recorded.'
  appFile.close()

def recursiveDelCoincidentOnes(allJogos, nOfCoincIn=3):
  i=0; hasDeleted = False
  while i < len(allJogos)-1:
    print i, '/', len(allJogos)
    j = i + 1
    while j < len(allJogos):
      jogoI = allJogos[i]; jogoJ = allJogos[j]; nOfCoinc = 0
      for dI in jogoI.getDezenas():
        if dI in jogoJ.getDezenas():
          nOfCoinc += 1
    if nOfCoinc >= nOfCoincIn:
      #print 'deleting', j, 'size', len(allJogos)
      hasDeleted = True
      del allJogos[j]
      break
    j += 1
    #print 'j =', j,
    if j==len(allJogos):
      i+=1
  if hasDeleted:
    return recursiveDelCoincidentOnes(allJogos, nOfCoincIn)
  return allJogos

def chainLevel2toApostas(nOfNextConc=Sena.getNOfLastJogo()+1, nOfCoincIn=3):
  # read in all jogos
  filePath = '../Apostas/CombinationsChain-level-2-%d.txt' %(nOfNextConc)
  inFile = open(filePath)
  line = inFile.readline(); c = 0
  allJogos = []
  while line:
    dezenas = dezenasIntFromTextLine(line)
    if dezenas == None:
      line = inFile.readline()
      continue
    c += 1
    jogo = Sena.Jogo(-c)
    jogo.setDezenas(dezenas)
    allJogos.append(jogo)
    line = inFile.readline()
  takeOutList = []
  originalSize = len(allJogos)
  allJogos = recursiveDelCoincidentOnes(allJogos, nOfCoincIn)
  print 'allJogos orig size', originalSize
  print 'after del, allJogos size', len(allJogos)
  jogosToBuy = []
  for i in range(len(allJogos)):
    jogo = allJogos[i]
    jogosToBuy.append(jogo)
    print jogo
  generateOutputJogosToBuy(jogosToBuy)

def putInAscendingOrder(allDezenas):
  for i in range(len(allDezenas)-1):
    for j in range(i+1,len(allDezenas)):
      if allDezenas[i] > allDezenas[j]:
        tmpList = list(allDezenas[i]) # hard copy
  allDezenas[i] = list(allDezenas[j])
  allDezenas[j] = tmpList
  return allDezenas

def putInAscendingOrderInFile2(filePath):
  lines = open(filePath).readlines(); allDezenas = []
  #line1 = lines[0]
  orderedFile = open(filePath, 'w')
  #print line1
  #orderedFile.write(line1)  # line1 already has \n at the end (see above, it's lines[0])
  for line in lines:
    dezenas = dezenasIntFromTextLine(line)
    if dezenas == None:
      continue
    allDezenas.append(dezenas)
  putInAscendingOrder(allDezenas)
  for dezenasInt in allDezenas:
    dezenas = map(tmpF, dezenasInt)
    dezenasStr = ' '.join(dezenas)
    line = '%s' %(dezenasStr)
    print line
    orderedFile.write(line + '\n')
  line = genLastLineTotalDeApostas(len(allDezenas))
  orderedFile.write(line + '\n')
  orderedFile.close()

def putInAscendingOrderInFile(filePath=None):
  if filePath == None:
    nOfNextJogo = Sena.getNOfLastJogo() + 1
    filePath = '../Apostas/apostas-%s.txt' %(str(nOfNextJogo).zfill(4))
  return putInAscendingOrderInFile2(filePath)

import volantePrintingFunctions as volante
def checkAcertosInCombinationsChainFile(nOfRefJogo=Sena.getNOfLastJogo(), chainN=2, changeChainRefNumberTo=None):
  jogoRef = Sena.jogosPool.getJogo(nOfRefJogo)
  dezenasSorteadas = jogoRef.getDezenas()
  nOfRefForChain = nOfRefJogo
  if changeChainRefNumberTo != None:
    nOfRefForChain = changeChainRefNumberTo
  filePath = '../Apostas/CombinationsChain-level-%d-%s.txt'  %(chainN, nOfRefForChain)
  jogoFile = open(filePath)
  line = jogoFile.readline(); nOfAcertosDict = {}
  while line:
    pp = line.split(' ')
    if len(pp) >= 6:
      try:
        dezenasApostadas = map(int, pp[:6])
        nOfAcertosDict = volante.compareJogosForAcertos(dezenasApostadas, dezenasSorteadas, nOfAcertosDict)
      except ValueError:
        pass
    line = jogoFile.readline()
  volante.showStatsForCheckAcertosThruJogos(nOfAcertosDict)

def getQuadrasFromDezenasList(dezenas, quadrasIn=[]):
  if len(dezenas) < 6:
    return []
  i = [None]*4; quadras = quadrasIn[:]
  for i[0] in range(3):
    for i[1] in range(i[0]+1,4):
      for i[2] in range(i[1]+1,5):
        for i[3] in range(i[2]+1,6):
          quadra = []
          for j in range(4):
            #print i, j
            quadra.append(dezenas[i[j]])
  quadras.append(quadra)
  quadras.sort()
  return quadras

def getQuinasFromDezenasList(dezenas, quinasIn=[]):
  if len(dezenas) < 6:
    return []
  i = [None]*5; quinas = quinasIn[:]
  for i[0] in range(2):
    for i[1] in range(i[0]+1,3):
      for i[2] in range(i[1]+1,4):
        for i[3] in range(i[2]+1,5):
          for i[4] in range(i[3]+1,6):
            quina = []
            for j in range(5):
              #print i, j
              quina.append(dezenas[i[j]])
              quinas.append(quina)
  quinas.sort()
  return quinas

def accumulateQuadras(quadras, quadrasRec, recNo, quadrasRecNos):
  for quadra in quadras:
    if quadra not in quadrasRec:
      print len(quadrasRecNos), 'Acc quad', quadra, recNo
      quadrasRec.append(quadra)
      quadrasRecNos.append(recNo)
  return quadrasRec

def extractQuadrasFromJogos(jogosList):
  quadrasRec = []; quadrasRecNos = []
  for i in range(len(jogosList)):
    dezenas    = jogo.getDezenas()
    quadras    = getQuadrasFromDezenasList(dezenas)
    quadrasRec = accumulateQuadras(quadras, quadrasRec, i, quadrasRecNos)
    #print quadraRec

def extractQuadrasFromApostaFile(apostaFilename):
  quadrasRec = []; quadrasRecNos = []; c=0
  apostaFile = open(apostaFilename)
  line = apostaFile.readline(); discoveredHasRecNo = False; hasRecNo = False
  while line:
    try:
      if not discoveredHasRecNo:
        pp = line.split(' ')
        dezenas = map(int, pp[:6])
        if dezenas[0] < 0:
          sixthDezena = int(pp[6])
          discoveredHasRecNo = True
        if sixthDezena >=1 and sixthDezena <= 60:
          hasRecNo = True
      if hasRecNo:
        dezenas = map(int, line.split(' ')[1:7])
      else:
        dezenas = map(int, line.split(' ')[:6])
      c+=1
      quadras    = getQuadrasFromDezenasList(dezenas)
      quadrasRec = accumulateQuadras(quadras, quadrasRec, c, quadrasRecNos)
    except ValueError:
      continue
    except IndexError:
      continue
    line = apostaFile.readline()
  for i in range(len(quadrasRec)):
    recNo  = quadrasRecNos[i]
    quadra = quadrasRec[i]
    print recNo, quadra

def extractQuadrasLexGraphIndexFromApostaFile(apostaFilename, EQUALSN=4):
  quadrasDict = {}; apostaFile = open(apostaFilename)
  import combinadics
  line = apostaFile.readline(); c=0
  while line:
    dezenas = dezenasIntFromTextLine(line)
    if dezenas == None:
      line = apostaFile.readline()
      continue
    c+=1
    if EQUALSN == 4:
      quadras    = getQuadrasFromDezenasList(dezenas)
    elif EQUALSN == 5:
      quadras    = getQuinasFromDezenasList(dezenas)
    # lgi6 = combinadics.findIndexFromCombination(dezenas)
    print c,#'::', dezenas, 'len dict', len(quadrasDict)
    for quadra in quadras:
      lexGraphIndex = combinadics.findIndexFromCombination(quadra, EQUALSN)
      try:
        quadrasDict[lexGraphIndex] += 1
      except KeyError:
        quadrasDict[lexGraphIndex] = 1
      #print quadra, lexGraphIndex, 'q=%d' %(quadrasDict[lexGraphIndex])
      print '%2d' %(quadrasDict[lexGraphIndex]),
    print
    line = apostaFile.readline()
  indices = quadrasDict.keys()
  print 'len', len(quadrasDict)
  #for lexGraphIndex in indices:
    #print lexGraphIndex, quadrasDict[lexGraphIndex],'|',

def crossCheckingBackwardApostas():
  for i in range(10):
    nConcRef = 980-i
    print 'nConcRef',nConcRef,'chain-1 is 982.'
    checkAcertosInCombinationsChainFile(nConcRef, 1, 982)

def fileToQuadras(nDoConcurso):
  #apostaFilename = '../Apostas/CombinationsChain-level-2-986.txt'
  apostaFilename = '../Apostas/apostas-%04d.txt' %(nDoConcurso)
  print apostaFilename
  extractQuadrasLexGraphIndexFromApostaFile(apostaFilename, 4)

import volantePrintingFunctions
def checkApostasFileThruFilters():
  nOfLastJogo = Sena.getNOfLastJogo()
  filePath = '../Apostas/apostas-%04d.txt' %(nOfLastJogo)
  fileIn = open(filePath)
  line = fileIn.readline(); c=0; falsesDict = {}; nOfOks = 0
  while line:
    dezenas = volantePrintingFunctions.transformLineToDezenasList(line)
    if dezenas != None:
      c+=1
      jogo = Sena.Jogo(-c)
      jogo.setDezenas(dezenas)
      resp, cod = filters.passThruFilters(jogo)
      dezenasStrList = map(tmpF, dezenas)
      dezenasStr = ' '.join(dezenasStrList)
      print dezenasStr,
      if not resp:
        print 'fail pass', cod, filters.getMessageStrFromFilterReturnNumberCode(cod)
      else:
        nOfOks += 1
      print 'ok'
      if not resp:
        try:
          falsesDict[cod] += 1
        except KeyError:
          falsesDict[cod] = 1
  line = fileIn.readline()
  cods = falsesDict.keys()
  cods.sort()
  print '='*40
  print 'Histogram for falses from filters:'
  print '='*40
  for cod in cods:
    print '%2dx %d:%s' %(falsesDict[cod],cod, filters.getMessageStrFromFilterReturnNumberCode(cod))
  print '-'*40
  percentOfOks = nOfOks * 100 / (0.0 + c)
  print 'Total', c, ':: ok/total = %5.2f' %(percentOfOks), '%'


def processChain2():
  nOfCoincIn=3
  chainLevel2toApostas(Sena.getNOfLastJogo()+1, nOfCoincIn)
  putInAscendingOrderInFile()

def processChain():
  doCombinations()
  chainLevel1to2()
  nOfCoincIn=3
  chainLevel2toApostas(Sena.getNOfLastJogo()+1, nOfCoincIn)
  putInAscendingOrderInFile()


if __name__ == '__main__':
  print 'Sena.getNOfLastJogo()', Sena.getNOfLastJogo()
  print 'Running updateDataFiles()'
  updateDataFiles()
