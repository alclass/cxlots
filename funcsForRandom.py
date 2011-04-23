#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import shutil
import sys
import time

PRIMES_TILL_60 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59] 

def randomSet(n):
  dezenasToCombine = []
  for i in range(n):
    goAhead = False
    while not goAhead:
      d = random.randint(1,60)
      if d not in dezenasToCombine:
        dezenasToCombine.append(d)
        goAhead = True
  dezenasToCombine.sort()
  return dezenasToCombine

def xRandomDezenas():
  #dezenas = [1,2,3,4,5,6,7]
  #dezenas = range(1,16)
  dezenasToCombine = randomSet(20)
  comb6Conv(dezenasToCombine)

def d60MinusXLastJogos(nOfLastJogosToNotConsider=2):
  nOfLastJogo = Sena.getNOfLastJogo(); dezenasToStrip = []
  for i in range(nOfLastJogosToNotConsider):
    nOfJogo = nOfLastJogo - i
    jogo = Sena.jogosPool.getJogo(nOfJogo)
    dezenasToStrip += jogo.getDezenas()
  setWithStripped2Jogos = []
  d60=range(1,61)
  for d in d60:
    if d in dezenasToStrip:
      continue
    setWithStripped2Jogos.append(d)
  return setWithStripped2Jogos

filtroDict = {1:0, 2:0, 3:0, 4:0}; filtroKeys = filtroDict.keys()
filtroKeys.sort()

OneMillion = 10 ** 6
passing = 1; nOfFailPass = 0; nOfPass = 0
def runCombinations(startAt, endAt, nOfLastJogosToNotConsider=2):
  print ' [runCombinations()] with the following data:'
  setWithStripped2Jogos = d60MinusXLastJogos(nOfLastJogosToNotConsider)
  print 'Dezenas a combinar: ', setWithStripped2Jogos
  tam = len(setWithStripped2Jogos)
  nDeComb = comb(tam, 6)
  if endAt == None or endAt < 1:
    endAt = nDeComb
  print 'O número de combinações para %d dezenas é de %d' %(tam, nDeComb)  
  print 'Relatively long processing, some messages will appear.  Please wait.'
  combObj = Comb6IterativeGenerator(setWithStripped2Jogos, startAt, endAt)
  combObj.run()

def runCombinationsWithD60Minus():
  setWithStripped2Jogos = d60MinusXLastJogos()
  d60MinusSize = len(setWithStripped2Jogos); c = 0; allDrawns = []
  for i in range(11):
    hasPassed = False
    while not hasPassed:
      dezenas = []
      while len(dezenas) < 6:
        index = random.randint(1,d60MinusSize)
        d = setWithStripped2Jogos[index-1]
        if d not in dezenas:
          dezenas.append(d)
      c += 1
      jogo = Sena.Jogo(-c)
      dezenas.sort()
      jogo.setDezenas(dezenas)
      tuple2 = filters.passThruFilters(jogo)
      hasPassed = tuple2[0]
      if not hasPassed:
        print jogo, filters.getMessageStrFromFilterReturnNumberCode(tuple2[1])
    allDrawns.append(jogo.getDezenas())
  allDrawns.sort()
  print 'Tirados:', len(allDrawns), 'Tentativas totais:', c
  for drawnList in allDrawns:
    tmpF = lambda x: str(x).zfill(2)
    drawnStrList = map(tmpF, drawnList)
    line = ' '.join(drawnStrList)
    print line

def main2():
  #  startAt = 10*OneMillion + 1; endAt = 20*OneMillion
  startAt = 1
  endAt   = 2000
  try:
    startAt = int(sys.argv[1])
    endAt = int(sys.argv[2])
    print ' *** Using startAt =', startAt, 'and endAt =', endAt
  except:
    pass
  runCombinations(startAt, endAt)

def main1():
  nOfCombs48a6 = comb(48, 6)
  endAt = nOfCombs48a6
  for i in range(10):
    drawn = random.randint(1,nOfCombs48a6)
    startAt = drawn
    print ' *** Using startAt =', startAt, 'and endAt =', endAt
    runCombinations(startAt, endAt)

def testComb6():
  c=0
  comb = Comb6(comb=[59,50,40,30,20,10])
  c+=1; print c, '==>>', comb
  comb = Comb6(lgi=100)
  c+=1; print c, '==>>', comb
  comb = Comb6(comb=[9,6,5,4,2,0])
  c+=1; print c, '==>>', comb


alphabet = map(chr, range(65, 65+28))
if __name__ == '__main__':
  #runCombinationsWithD60Minus()
  testComb6()
