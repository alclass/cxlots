#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
a=1
import LFClasses
import pprint
import IndicesCombiner as ic
import actions

def testTable(table=None):
  if not table:
    table = cx.readDataIntoTable()
    if not table:
      raise ValueError, 'could not get jogos table'
    elif len(table) < 2:
      raise ValueError, 'jogos table is empty'
  headerFields = table[0]
  '''
  Test to see if data coming from the csv is okay
  '''
  for tableRow in table:
    index = 0
    print '='*30
    for value in tableRow:
      print headerFields[index], '=>', value
      index += 1

def testGetJogoNumero(numero=-1):
  jogosObj = Jogos.getJogosObj()
  print 'last jogos len', jogosObj.getLastConcurso()
  if numero == -1:
    jogo = jogos.getLastJogo()
    pprint.printJogo(jogo)
    return
  jogo = jogosObj.getJogoDoConcurso(numero)
  pprint.printJogo(jogo)
        
def testReadTable():
  table, headerFields = readDataIntoTable()
  testTable(table, headerFields)

def getJogoFromTableRow(tableRow, headerFields):
  '''
  Get jogo list from table row with the help of
  headerFields (they are labeled like 'Bola1', 'Bola2' etc.)
  '''
  jogo=[];index=0;c=0
  for value in tableRow:
    fieldName = headerFields[index]
    index+=1
    if fieldName.startswith('Bola'):
      c+=1
      #print c, index, fieldName, value
      try:
        dezena = int(value)
        if dezena < 1 or dezena > 25:
          raise IndexError, 'dezena fora da faixa 1 a 25. Erro.'
        jogo.append(dezena)
      except ValueError:
        '''
        Well, 
        '''
        continue
  if len(jogo) <> 15:
    print jogo, 'len', len(jogo)
    raise IndexError, 'deveria haver 15 dezenas exatamente.'
  jogo.sort()
  #print jogo  
  return jogo

def getJogosFromTable(table, headerFields):
  '''
  Get all jogos in the table list of lists
  '''
  jogos=[]
  for tableRow in table:
    # well, this 'if' will be unnecessary after avoiding  table[0]==[]
    if len(tableRow)==0:
      continue
    # this is because table[1] is equal to headerFields
    # consequently, table[1  [0]==headerFields[0]='Coluna'
    if tableRow[0] == headerFields[0]:
      continue
    jogo = getJogoFromTableRow(tableRow, headerFields)
    jogos.append(list(jogo))
  return jogos

def testReadTable():
  table, headerFields = readDataIntoTable()
  testTable(table, headerFields)

def makeHistogram(jogos=None):
  '''
  Produce the Histogram, ie, the quantity each dezena has been drawn
  '''
  histG = {}
  if jogos==None:
    table, headerFields  =  fromCsvToTable.readDataIntoTable()
    jogos  = getJogosFromTable(table, headerFields)
  for jogo in jogos:
    for dezena in jogo:
      try:
        histG[dezena]+=1
      except KeyError:
        histG[dezena]=1
  return histG

# global dict
jogosCoincWithJogos = {}  
def testCheckCoincs():
  jogos = ra.getHistoryJogos()
  nOfJogos = len(jogos)
  initializeSetJogoCoincWithJogoDict(nOfJogos)
  checkCoincs(jogos)
  #printSetJogoCoincWithJogoDict()
  printCoincTable()
  checkCoincsWithPrevious(jogos)
  printCoincWithPreviousTable()
def printDict(theDict):
  keys = theDict.keys()
  keys.sort()
  for key in keys:
    value = theDict[key]
    print key, value

import random  
def testGenerateTils():
  '''
  testDict = {}
  for i in range(10):
    dezena = random.randint(1,25)
    testDict[dezena] = random.randint(10,21)
  '''
  #workJogos = fctt.getHistoryJogos()
  #workJogos = ra.getHistoryJogos()
  histG = ra.makeHistogram() #(jogos)
  print '[CALLING] generateTils(histG)'
  points = generateFaixasForTil(histG)
  
def testGetEntireTillFaixas():
  histG = ra.makeHistogram() #(jogos)
  getEntireTillFaixas(histG)
  '''
  TIL = 5
  faixas = generateFaixasForTil(histG, TIL)
  analyzeJogosWithTilFaixas(histG, faixas)
  '''

def testSequenceData():
  table = getTable()
  newTable = getUpTo(table, 10)
  print 'len(table)', len(table)
  newTable = continueTheSequenceBy(table, newTable, 5)
  pprint(newTable)
  workJogos = getJogosUpTo(table, 10)
  print 'len(table)', len(table)
  print 'len(workJogos)', len(workJogos)
  workJogos = continueJogosSequenceBy(table, workJogos, 5)
  printJogos(workJogos)

def testHeaderFields():
  table, headerFields = fctt.readDataIntoTable()
  print headerFields
  print table[0]
  print table[1]

import random  
def testGenerateTils():
  '''
  testDict = {}
  for i in range(10):
    dezena = random.randint(1,25)
    testDict[dezena] = random.randint(10,21)
  '''
  #workJogos = fctt.getHistoryJogos()
  #workJogos = ra.getHistoryJogos()
  histG = ra.makeHistogram() #(jogos)
  print '[CALLING] generateTils(histG)'
  points = generateFaixasForTil(histG)

def testGetEntireTillFaixas():
  histG = ra.makeHistogram() #(jogos)
  getEntireTillFaixas(histG)
  '''
  TIL = 5
  faixas = generateFaixasForTil(histG, TIL)
  analyzeJogosWithTilFaixas(histG, faixas)
  '''

def testRandomJogosFilterOut11Coincs():
  nOfJogosToGen=1000
  jogos = generateRandomJogos(nOfJogosToGen)
  #sequenceData.printJogos(jogos)
  newJogos=filterOut11Coincs(jogos)
  sequenceData.printJogos(newJogos)

def testJogoAgainstCoincFilter():
  jogo = generateRandomJogo()
  nOfCoincs=14
  print jogo, 
  ans, jogoIndex = filterOutAgainstHistoryWithNCoincs(jogo, nOfCoincs)
  if ans:
    print 'NOT PASSED', 'against jogo n.', jogoIndex
  else:
    print 'PASSED'

#arrays=[([1,2,3],2),([4,5],1),[(6,7,8],2),[(9],1)]
'''
combs
1 2 4 6 7 9
1 2 4 6 8 9
1 2 4 7 8 9
1 2 5 6 7 9
1 2 5 6 8 9
1 2 5 7 8 9

1 3 4 6 7 9
1 3 4 6 8 9
1 3 4 7 8 9
1 3 5 6 8 9
1 3 5 7 8 9

2 3 4 6 7 9
2 3 4 6 8 9
2 3 4 7 8 9
2 3 5 6 7 9
2 3 5 6 8 9
2 3 5 7 8 9

a1a2 b1b2

a1b1
a1b2
a2b1
a2b2ee
...
'''

def setMultiply(collected, cadeia, combineArray):
  listElem = list(combineArray[0])
  for elem in listElem:
    #print elem, cadeia, collected
    if len(combineArray) == 1:
      collected.append(list(cadeia)+[elem])
    else:
      nothing = setMultiply(collected, list(cadeia)+[elem], combineArray[1:])
  return collected

def prepSetMultiply():
  combineArray = [[1,2,5],[3,4],[6]]
  print combineArray
  result = setMultiply([], [], combineArray)
  print result
  #testGenerateTils()

def testSequenceData():
  table = getTable()
  newTable = getUpTo(table, 10)
  print 'len(table)', len(table)
  newTable = continueTheSequenceBy(table, newTable, 5)
  pprint(newTable)
  workJogos = getJogosUpTo(table, 10)
  print 'len(table)', len(table)
  print 'len(workJogos)', len(workJogos)
  workJogos = continueJogosSequenceBy(table, workJogos, 5)
  printJogos(workJogos)

def testHeaderFields():
  table, headerFields = fctt.readDataIntoTable()
  print headerFields
  print table[0]
  print table[1]

def testTilObj():
  tilObj = LFClasses.getTilObj(7)
  print tilObj.getFaixas()
  print tilObj.getDezenasNasFaixas()

def testGetJogosLgisForATilFaixa():
  jogosObj  = LFClasses.Jogos()
  lgis = jogosObj.getJogosLgisForATilFaixa(5)
  print lgis
  print jogosObj.getHistGJogosLgisForATilFaixa(5)

def getLgisToBeUsed():
  jogosObj  = LFClasses.Jogos()
  histGJogosLgisForATilFaixa =     jogosObj.getHistGJogosLgisForATilFaixa(5)
  quants = histGJogosLgisForATilFaixa.values()
  quants.sort()
  quantCorte = quants[len(quants)/2]
  for lgi in histGJogosLgisForATilFaixa.keys():
    quant = histGJogosLgisForATilFaixa[lgi]
    if quant > quantCorte:
      print lgi, '=>', quant

def testSetCombine():
  sets = ic.testSetCombine([10,12,15,17, 3],3)
  print sets

def testGerador():
  gerador = actions.Gerador()
  # gerador.mountFirstSets()
  fDict = gerador.jogosObj.getHistGJogosLgisForATilFaixa(5)
  print fDict
  print 'len', len(fDict)
  lgis = gerador.chosenLgis
  print lgis
  print 'len', len(lgis)

def testMultiply():
  s = [1, 2, 11, 15, 23, 25]

def baseClass():
  o = LFClasses.getJogosObj('LF')
  print o.getLastConcurso()
  print o

if __name__ == '__main__':
  baseClass()

  '''
  testGerador()
  testSetCombine()
  getLgisToBeUsed()
  testGetJogosLgisForATilFaixa()
  testTilObj()
  testGetJogoNumero(440)
  testTable()
  testGetJogoNumero(int(sys.argv[1]))
  '''
