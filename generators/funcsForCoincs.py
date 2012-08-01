#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

a=1
from cardprint import pprint


def getNOfCoincidences(jogo1, jogo2):
  '''
  Get how many coincidences there are between consecutive jogos
  '''
  nOfCoinc = 0
  for dezena in jogo1:
    if dezena in jogo2:
      nOfCoinc += 1
  return nOfCoinc

#import math
def minNOfBits(n):
  #t = math.log(n) * 1 / log(2)
  if n < 0:
    return None
  if n == 0:
    return 0
  if n == 1 or n == 2: # here, it can only be 1 or 2
    return 1
  n = n - 1
  c = 0
  while n > 0:
    n = n >> 1
    c += 1
  return c

def packJogoToBinaryDecRepr(jogo, nOfBits):
  n = len(jogo)
  #nOfBits = log2(
  stuff = 0
  for dezena in jogo:
    n -= 1
    nc = nOfBits * n
    # print 'nc', nc, 'dezn', dezena, 'n',n
    # shift-left nc bits :: eg. 1 << 5 = 32
    # or 1 << 5 = 1 * 2**5
    # the inverse is 32 >> 5 = 1 or 32 / (2**5) = 1
    trunk = dezena << nc 
    stuff = stuff | trunk
  #print jogo,
  #print stuff
  return stuff

def unpackJogoFromBinaryDecRepr(binaryDecRepr, nDeDezenasSorteadas, nOfBits, maskSortOrReverse=0):
  '''
  The unpack is done in reverse order,
  if order is important, reverse parameter should be passed in as True
  '''
  #print 'binaryDecRepr, nDeDezenasSorteadas, nOfBits'
  #print binaryDecRepr, nDeDezenasSorteadas, nOfBits
  jogo = [-1] * nDeDezenasSorteadas
  # if nOfBits is 5, onesForAndOp should be binary 11111
  # if nOfBits is 3, onesForAndOp should be binary 111, and so on
  onesForAndOp = 2 ** nOfBits - 1
  # parse it backwardly
  for i in range(nDeDezenasSorteadas-1,-1,-1):
    # 31 in binary, is 11111
    # with an AND operation (&), we're throwing everything away except the right-most 5-bits
    # the packing was done in trunks of 5 bits each

    dezena = binaryDecRepr & onesForAndOp
    #print dezena,
    jogo[i] = int(dezena)
    # shift-right 5 bits to get the next 5 bits to the left as loop goes round
    binaryDecRepr = binaryDecRepr >> nOfBits
    #print binaryDecRepr,
  # a first reverse is necess
  return returnJogoTreatingTheOrderOrReverseMask(jogo, maskSortOrReverse)

def returnJogoTreatingTheOrderOrReverseMask(jogo, maskSortOrReverse):
  '''
  maskInOrderAndReverse should be binaries 11 (=3 dec), 10 (=2 dec) or 01 (=1 dec)
  reverse is both a sort() and a reverse()
  '''
  if type(maskSortOrReverse) <> int:
    return jogo
  if maskSortOrReverse not in [0, 1, 2]:
    return jogo
  putInOrder = maskSortOrReverse >> 1 & 1
  reverse    = maskSortOrReverse & 1
  #print 'putInOrder', putInOrder, 'reverse', reverse, 'maskSortOrReverse'
  #print 'jogo', jogo
  if putInOrder:
    jogo.sort()
  if reverse:
    jogo.sort()
    jogo.reverse()
  return jogo

def chargeBetFileIntoBinDecReprDict(fileIn='jogos-bet.txt'):
  nOfLines  = 0
  jogosBetFile = open(fileIn)
  print 'Counting lines and charging jogos into dict, please wait.'
  line = jogosBetFile.readline(); binDecReprJogosDict = {}
  while line:
    nOfLines += 1
    if nOfLines % 100000 == 0:
      print nOfLines, ' ... ',
    jogoLine = JogoLine(line)
    binDecRepr = jogoLine.getBinDecRepr()
    # all binDecReprJogos receive, initially, 1
    binDecReprJogosDict[binDecRepr] = 1
    line = jogosBetFile.readline()
  print 'nOfLines', nOfLines
  print 'len(binDecReprJogosDict)', len(binDecReprJogosDict)
  jogosBetFile.close()
  return binDecReprJogosDict

def filter11Out(binDecReprJogosDict):
  '''
  Enter dict
  Goes out list
  '''
  binDecReprJogos = binDecReprJogosDict.keys()
  # save some memory if possible
  del binDecReprJogosDict
  print 'start sort binDecReprJogos', time.ctime()
  binDecReprJogos.sort()
  print 'finish sort binDecReprJogos', time.ctime()
  nOfExcluded = 0; i=0
  dynSize = len(binDecReprJogos)
  while i < dynSize - 1:
    binDecReprJogoI = binDecReprJogos[i]
    #if binDecReprJogosDict[binDecReprJogoI] == 0:
      #continue
    jogoLineI = JogoLine(None,None,binDecReprJogoI)
    for j  in range(i+1, dynSize):
      binDecReprJogoJ = binDecReprJogos[j]
      #if binDecReprJogosDict[binDecReprJogoJ] == 0:
        #continue
      jogoLineJ = JogoLine(None,None,binDecReprJogoJ)
      r = has11OrMoreCoincs(jogoLineI.jogo, jogoLineJ.jogo)
      if r:
        del binDecReprJogos[i]
        #binDecReprJogosDict[binDecReprJogoJ] = 0
        nOfExcluded+=1
        #print 0,
        i-=1
        break
      else:
        pass
        #print 1,
      if nOfExcluded % 10000 == 0:
        print 'excl', nOfExcluded,
    dynSize = len(binDecReprJogos)
    i+=1
  print 'nOfExcluded', nOfExcluded
  return binDecReprJogos


def recordNewBetFile(binDecReprJogos, fileOut='jogos-bet-mantidos.txt'):
  mantemFile = open(fileOut,'w')
  nOfExcluded = 0
  for binDecReprJogo in binDecReprJogos:
    jogoLine = JogoLine(None,None,binDecReprJogo)
    line = jogoLine.getLine() + '\n'
    mantemFile.write(line)
  mantemFile.close()

def queueTasks(fileIn='jogos-bet.txt'):
  binDecReprJogosDict = chargeBetFileIntoBinDecReprDict(fileIn)
  binDecReprJogos = filter11OutImpl2(binDecReprJogosDict)
  # save some memory if possible
  del binDecReprJogosDict
  recordNewBetFile(binDecReprJogos)

def generateSampleBet(quant):
  print 'generateSampleBet()'
  jogosBetFile = open('jogos-bet.txt')
  jogosSampleBetFile = open('sample-jogos-bet.txt','w')
  line = jogosBetFile.readline(); nOfLines = 0
  while line and nOfLines < quant:
    nOfLines += 1
    jogosSampleBetFile.write(line)
  jogosSampleBetFile.close()

'''
def testPackAndUnpack():
  jogosObj = LFClasses.getJogosObj()
  jogo = jogosObj.getJogos()[0]
  stuff = packJogoToBinaryDecRepr(jogo)
  dezenas = unpackJogoFromBinaryDecRepr(stuff)
  print dezenas
  jogo = jogosObj.getJogos()[-1]
  stuff = packJogoToBinaryDecRepr(jogo)
  dezenas = unpackJogoFromBinaryDecRepr(stuff)
  print dezenas  
'''
def testMinNOfBits():
  n = 25; expect = 5
  r = minNOfBits(n)
  print 'minNOfBits(',n,') ==>>', r
  assert(r == expect)
  # =====================================
  n = 60; expect = 6
  r = minNOfBits(n)
  print 'minNOfBits(',n,') ==>>', r
  assert(r == expect)
  # =====================================
  n = 1024; expect = 10
  r = minNOfBits(n)
  print 'minNOfBits(',n,') ==>>', r
  assert(r == expect)
  # =====================================
  n = 1; expect = 1
  r = minNOfBits(n)
  print 'minNOfBits(',n,') ==>>', r
  assert(r == expect)
  # =====================================
  n = 0; expect = 0
  r = minNOfBits(n)
  print 'minNOfBits(',n,') ==>>', r
  assert(r == expect)
  # =====================================
  n = -1; expect = None
  r = minNOfBits(n)
  print 'minNOfBits(',n,') ==>>', r
  assert(r == expect)
  # =====================================


#import csv, os, pickle

'''# establish where data file is located
dataDir = '..' + os.sep + 'Dados'
csvFile='D_LOTFAC.csv'
csvPath=os.path.join(dataDir, csvFile)

def readDataIntoTable2():
***
  Main routine to read jogos data from the csv file
***
  pReader = csv.reader(open(csvPath), dialect='excel', delimiter=';', quotechar='|')
  rowCount = 0; fields=None; table = []
  for row in pReader:

'''

def sweepCoincidencesInJogosConsecutives(jogos):
  '''
  Run thru jogos, calculating consecutive coincidences
  '''
  acum = 0; coincMin = 25; coincMax = 0
  for i in range(1,len(jogos)):
    jogo = jogos[i]
    jogoPrevious = jogos[i-1]
    nOfCoinc = getNOfCoincidences(jogo, jogoPrevious)
    print pprint(jogo), 'nOfCoinc', nOfCoinc
    acum += nOfCoinc
    if nOfCoinc < coincMin:
      coincMin = nOfCoinc
    if nOfCoinc > coincMax:
      coincMax = nOfCoinc
  average = acum / (0.0 + len(jogos) - 1)
  print 'average', average
  print 'min coinc', coincMin
  print 'max coinc', coincMax
  import comb as co
  averageInt = int(average) + 1
  nOfCombsWithAverage = co.comb(15,averageInt)
  print 'nOfCombsWithAverage', nOfCombsWithAverage

def initializeSetJogoCoincWithJogoDict(nOfJogos):
  '''
  Just initializes list elems with an empty dict
  This is a coupled method, ie, an extension of another method for zeroing the dict
  '''
  for i in range(nOfJogos):
    jogosCoincWithJogos[i]={}

def setJogoCoincWithJogo(i, j, nOfCoincs):
  '''
  Double set two coincident jogos, one with the other
  '''
  dictOfCoincs = jogosCoincWithJogos[i]
  dictOfCoincs[j]=nOfCoincs
  dictOfCoincs = jogosCoincWithJogos[j]
  dictOfCoincs[i]=nOfCoincs

coincDict = {}
def setCoincs(jogos):
  '''
  Test-like routine
  '''
  for i in range(len(jogos)-1):
    for j in range(i+1,len(jogos)):
      jogoA = jogos[i]
      jogoB = jogos[j]
      nOfCoincs = 0
      for dezena in jogoA:
        if dezena in jogoB:
          nOfCoincs += 1
      setJogoCoincWithJogo(i, j, nOfCoincs)
      try:
        coincDict[nOfCoincs]+=1
      except KeyError:
        coincDict[nOfCoincs]=1

      #if coincs >= 11:
        #print i, j, 'coincs', coincs

coincWithPreviousDict = {}; setJogoCoincWithPrevious = []
def checkCoincsWithPrevious(jogos):
  '''
  Check consecutive jogos for coincidences in a set of jogos
  '''
  nOfJogos = len(jogos)
  setJogoCoincWithPrevious = [0]*nOfJogos
  for i in range(len(jogos)-1):
    jogoA = jogos[i]
    jogoB = jogos[i+1]
    nOfCoincs = 0
    for dezena in jogoA:
      if dezena in jogoB:
        nOfCoincs += 1
    setJogoCoincWithPrevious[i]=nOfCoincs
    try:
      coincWithPreviousDict[nOfCoincs]+=1
    except KeyError:
      coincWithPreviousDict[nOfCoincs]=1


if __name__ == '__main__':
  pass
  '''
  testMinNOfBits()
  # testPackAndUnpack()
  fileIn='sample-jogos-bet.txt'
  print 'queueTasks()'
  #queueTasks(fileIn)
  queueTasks()
  #generateSampleBet(100)
  '''