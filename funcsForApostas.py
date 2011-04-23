#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time  # for timing purposes
#import math

a=1
from cardprint import pprint


def findStandard2LetterNameInFilename(apostasFilename):
  '''
  Apostas filename are standardized
  yyyy-mm-dd-s2LN-apostas.txt[.n]
  where n, if exists, is a int number equal or greater than one
  Eg.
  2009-10-04-ms-apostas.txt.3
  '''
  pp = apostasFilename.split('-')
  standard2LetterName = pp[3]
  standard2LetterName = standard2LetterName.upper()
  return standard2LetterName

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