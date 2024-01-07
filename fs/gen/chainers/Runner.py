#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime, sys, time
import sqlite3

a=1
import Controller as contr
import CLClasses
import funcs
#import funcsForSql as fSql
import lambdas
import LgiCombiner as lc
import Stat
import Stream
import Til as tilc
from cardprint import pprint


class Runner(contr.Ruler):

  def __init__(self, eitherJogosObjOrS2):
    jogosObj = funcs.returnJogosObj(eitherJogosObjOrS2)
    contr.Ruler.__init__(self, jogosObj)

    self.beginAt = datetime.datetime.now()
    print 'Start at', self.beginAt
    #self.apostasConnIn = createSqliteTest()

  def setStreamObj(self, streamObj):
    '''
    in and out
    '''
    self.streamObj = streamObj

  def setCheckerObj(self, checkerObj):
    self.checkerObj = checkerObj

  def run(self):
    '''
    '''
    self.jogoObj = self.streamObj.first(); c=0; self.rCount = 0
    '''
    if type(self.jogoObj) == list:
      jogo = self.jogoObj
    else:
      jogo = self.jogoObj.jogo
    '''
    print 'Please, wait'
    while self.jogoObj:
      c+=1
      jogo = self.jogoObj
      r = self.checkerObj.check(jogo)
      if r:
        self.amass()
      self.jogoObj = self.streamObj.next()
      if c % 10000 == 0:
        print 'c/rCount', c, self.rCount
  def amass(self):
    self.rCount += 1
    self.streamObj.write(self.jogoObj)

  def close(self):
    self.streamObj.close()
    print 'Started at', self.beginAt
    now = datetime.datetime.now()
    print 'Finished at', now



def runRunner():
  jogosObj = CLClasses.getJogosObj('lf')
  print 'instantiating Runner'
  ru = Runner(jogosObj)
  print 'instantiating Stream'
  streamObj = Stream.Stream(jogosObj)
  print 'setStreamInLgiCombiner()'
  streamObj.setStreamInLgiCombiner()
  print 'setStreamOutBinFile()'
  streamObj.setStreamOutBinFile()
  ru.setStreamObj(streamObj)
  checkerObj = contr.CheckerSoma3(jogosObj)
  ru.setCheckerObj(checkerObj)
  print 'Run Runner ru.run()'
  ru.run()
  nowInFilename = ru.outBinFilename
  print 'setStreamOutBinFile()'
  streamObj.setStreamInBinFile(nowInFilename)
  print 'Close Runner ru.close()'
  
  ru.close()


def a1():
  consecDictHist = seeConsecutives(jogosObj, tipoJogo)
  consecDict = getAllConsecs()
  #consecDict = seeConsecutives(lgiObj, tipoJogo)
  print 'patterns that never happened.'
  patts = consecDict.keys()
  pattsHist = consecDictHist.keys()
  #pattsNeverHappened = []
  totalNeverHappened = 0
  for patt in patts:
    if patt not in pattsHist:
      print 'patt', patt, 'never happened.'
      #pattsNeverHappened.append(patt) 
      totalNeverHappened += consecDict[patt]
      print 'totalNeverHappened', totalNeverHappened, 'patt', patt, consecDict[patt]
  #seeTils(lgiObj, tipoJogo)

def seeTil5inLF():
  jogosObj = CLClasses.getJogosObj('lf')
  til5obj = tilc.Til(jogosObj, 5)
  lgiObj = lc.LgiCombiner(24, 15)
  jogo = lgiObj.first(); c=0
  print 'Please, wait ::'#, tipoJogo,'nOfCombines =' #, lgiObj.nOfCombines
  passed = 0
  while jogo:
    #if type(jogo) == CLClasses.Jogo:
      #jogo = jogo.jogo
    patt = til5obj.generateLgiForJogoVsTilFaixas(jogo)
    if int(patt[0]) < 2:
      if int(patt[1]) < 3:
        if int(patt[2]) < 8:
          if int(patt[4]) < 8:
            passed += 1
    c = printOutMultiples(c)
    jogo = lgiObj.next()
  print 'passed', passed 

if __name__ == '__main__':
  runRunner()
  '''
  seeTil5inLF()
  sys.exit(0)
  tipoJogo = sys.argv[1]
  prepLgi(tipoJogo)
  '''
def testLgi():
  jogo = lgiObj.first(); c=0
  print 'first', jogo
  print 'move to 200', lgiObj.move_to(200, False, False)
  print 'last', lgiObj.last()
  iArray = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 18]
  iArray = map(lambdas.minus_one, iArray)
  iArray.reverse()
  print iArray
  lgiObj = lc.LgiCombiner(24,-1,iArray)
  print 'lgi', lgiObj.get_lgi(), lgiObj
  print 'ok'
  sys.exit(0)
