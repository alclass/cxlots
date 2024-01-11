#!/usr/bin/env python
# -*- coding: utf-8 -*-

a=1
import CLClasses
import funcsForSql     as fSql
import IndicesCombiner as ic
import Til             as tilc
from cardprint import pprint

def getAttr(field, table='ms', nDoConc=1):
  '''
  getAttr() method
  '''
  tt = type(table)
  if tt == CLClasses.Base:
    table = table.sqlTable
  if tt == CLClasses.Jogos:
    table = table.sqlTable
  sql = "SELECT `%(field)s` FROM `%(table)s` WHERE `nDoConc` >= '%(nDoConc)d';" %{'field':field,'table':table,'nDoConc':nDoConc}
  print sql
  #sys.exit(0)
  conn = fSql.getConnection()
  cursor = conn.cursor()
  cursor.execute(sql)
  rows = []; fields = []; fieldDict = {}
  # fields = map(lambdas.lambdaExtractFirstElem, rows)
  for row in cursor:
    rows.append(row)
  for cols in rows:
    field = cols[0]
    fields.append(field)
    try:
      fieldDict[field]+=1
    except KeyError:
      fieldDict[field]=1
  return fieldDict, fields


def getAttrFor(field, table='ms', nDoConc=1):
  '''
  getAttrFor() method
  '''
  if field == None:
    return None
  sql = "SELECT `%(field)s` FROM `%(table)s` WHERE `nDoConc` = '%(nDoConc)d';" %{'field':field,'table':table,'nDoConc':nDoConc}
  #print sql
  #sys.exit(0)
  conn = fSql.getConnection()
  cursor = conn.cursor()
  cursor.execute(sql)
  rows = []
  for row in cursor:
    rows.append(row)
  # fields = map(lambdas.lambdaExtractFirstElem, rows)
  if len(rows) == 1:
    return rows[0][0]
  return None

def getAttrs(attrs, table='ms', nDoConc=1):
  '''
  getAttrs() method
  '''
  tt = type(table)
  if tt == CLClasses.Base:
    table = table.sqlTable
  if tt == CLClasses.Jogos:
    table = table.sqlTable

  sqlAttrs = ''
  for attr in attrs:
    sqlAttrs += '`%s`,' %(attr)
  sqlAttrs = sqlAttrs[:-1] # to strip the ending ',' (comma)

  sql = '''SELECT %(sqlAttrs)s FROM `%(table)s` 
    WHERE `nDoConc` >= '%(nDoConc)d'
    ORDER BY `nDoConc`;''' %{'sqlAttrs':sqlAttrs,'table':table,'nDoConc':nDoConc}

  print sql

  #sys.exit(0)
  conn = fSql.getConnection()
  cursor = conn.cursor()
  cursor.execute(sql)
  #rows = cursor._rows
  # fields = map(lambdas.lambdaExtractFirstElem, rows)
  outRows = []
  for cols in cursor:
    i=-1; attrDict = {}
    for attr in attrs:
      i+=1
      attrDict[attr] = cols[i]
    outRows.append(attrDict)
  return outRows

def testAccessor():
  jogosObj = CLClasses.Jogos('ms')
  pattDict, patts = getAttr('til10pattern', jogosObj)
  pprint.print_list(patts)

def see456():
  nDoConc = 101
  pattDict, patts = getAttr('til10pattern', 'ms', nDoConc)
  patternSize = 10
  soma = 6
  tpVect = tilc.TilPatternVector(patternSize, soma)
  print 'tpVect.vector ', tpVect.vector[:10]
  print 'patts ', patts[:10]; c=0
  allPattsDict = {}
  for vect in tpVect.vector:
    allPattsDict[vect] = 0
  for patt in patts:
    c += 1
    if patt in tpVect.vector:
      allPattsDict[patt] = 1
      print c, 'i =', tpVect.vector.index(patt), patt, '=>', pattDict[patt],
      if '4' in patt:
        print '*4',
      if '5' in patt:
        print '*4',
      if '6' in patt:
        print '*6',
      print
  print 'len pattDict, len  patts ', len(pattDict), len(patts)
  print 'len tpVect.vector ', len(tpVect.vector)

  print 'patterns that never occurred.'
  allPatts = allPattsDict.keys()
  allPatts.sort()
  for patt in allPatts:
    if allPattsDict[patt] == 0:
      print patt

PRINT_EVERY = 10000; booleanTrueCounter = 0; exclCodHistG = {}
def printAndJump(jogo, c, count, exclCod):
  global booleanTrueCounter
  if count:
    booleanTrueCounter += 1
    try:
      exclCodHistG[exclCod]+=1
    except KeyError:
      exclCodHistG[exclCod]=1
  if c % PRINT_EVERY == 0:
    line = '%d %s booleanTrueCounter=%d exclCod=%s' %(c, jogo, booleanTrueCounter, exclCodHistG)
    print line


class Ruler(object):
  def __init__(self):
    self.rules = []
    # tilN, patternPos, least, greatest
  def setRule(self, tilN, patternPos, least, greatest):
    self.rules.append((tilN, patternPos, least, greatest))
  def applyRules(self, pattern):
    for rule in self.rules:
      tilN, patternPos, least, greatest = rule
      digit = int(pattern[patternPos])
      if greatest <> None:
        if digit < least:
          return False
        if digit > greatest:
          return False
      else: # ie greatest == None:
        if digit == least:
          return False
    

def verifyAllCombsWith4OrMoreInAPattern(tilN=10):
  '''
  Eg patterns with 4 or more
  
  0041100000
  5000000001
  etc
  '''
  print 'instantiating jogosObj ms'
  jogosObj = CLClasses.getJogosObj('ms')
  print 'instantiated'

  til4  = tilc.Til(jogosObj, 4)
  til5  = tilc.Til(jogosObj, 5)
  til6  = tilc.Til(jogosObj, 6)
  til10 = tilc.Til(jogosObj, 10)

  combObj = ic.IndicesCombiner(59, 6, False)
  jogo = combObj.first_zeroless()
  c = 0; booleanTrueCounter = 0; exclCod = 0; count = False
  while jogo:
    printAndJump(jogo, c, count, exclCod)
    c+=1
    jogo = combObj.next_zeroless()
    #print jogo
    count = False
    exclCod = 0

    patt = til4.generateLgiForJogoVsTilFaixas(jogo)
    # first digit (least occurring dezenas) cannot be greater than 3
    digit = int(patt[0])
    exclCod += 1 # 1
    if digit > 3:
      count = True
      continue

    # second and last digit cannot be greater than 5 (or, it cannot be 6)
    digit1 = int(patt[1])
    digit3 = int(patt[3])
    exclCod += 1 # 2
    if digit1 == 6 or digit3 == 6:
      count = True
      continue
    # patt 0060 has occurred 5 times until nDoConc 1113

    patt = til5.generateLgiForJogoVsTilFaixas(jogo)
    # first digit (least occurring dezenas) cannot be greater than 2
    digit = int(patt[0])
    exclCod += 1 # 3
    if digit > 2:
      count = True
      continue
    # last digit (most occurring dezenas) cannot be greater than 5 (though 5 has really happened in history)
    digit = int(patt[0])
    exclCod += 1 # 4
    if digit >= 5:
      count = True
      continue

    exclCod += 1 # 5
    if '6' in patt:
      count = True
      continue

    patt = til6.generateLgiForJogoVsTilFaixas(jogo)
    # first digit (least occurring dezenas) cannot be greater than 2
    digit = int(patt[0])
    exclCod += 1 # 6
    if digit > 2:
      count = True
      continue

    # last digit (most occurring dezenas) cannot be greater than 5 (though 5 has really happened in history)
    digit = int(patt[0])
    exclCod += 1 # 7
    if '5' in patt:
      count = True
      continue

    exclCod += 1 # 8
    if '6' in patt:
      count = True
      continue

    patt = til10.generateLgiForJogoVsTilFaixas(jogo)
    exclCod += 1 # 9
    if '4' in patt:
      count = True
      continue

    exclCod += 1 # 10
    if '5' in patt:
      count = True
      continue

    exclCod += 1 # 11
    if '6' in patt:
      count = True
      continue

    exclCod = 0



def process2():
  for tilN in [5, 6, 10]:
    verifyAllCombsWith4OrMoreInAPattern(tilN)

def process():
  verifyAllCombsWith4OrMoreInAPattern()


def lookUpPatterns():
  table='ms'; nDoConc=101
  for tilN in [4, 5, 6, 10]:
    pattDict, patts = getAttr('til%dpattern' %(tilN), table, nDoConc)
    print 'tilN', tilN
    pprint.print_dict(pattDict)

if __name__ == '__main__':
  #lookUpPatterns()
  #process()
  testAccessor()
