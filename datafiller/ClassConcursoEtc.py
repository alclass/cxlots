#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime, sys

sys.path.insert(0, '..')
a=1
import FieldsAndTypes as fat
import converterForDateAndCurrency as conv
#import frequencyMounting as fm
# the next line produces a circular reference problem in Python, so a third module will be created to join functionalities that cannot be joint here
#import statmetrics.TilModule as tilMod

class Concurso():
  def __init__(self):
    self.concursoDict = {}
    self.fieldnamesInOrder = [] # this extra attribute will not be necessary in Python 3, for in Py3 it's possible to maintain order in a dict
  def __setitem__(self, fieldname, value):
    shouldBeType = fat.getFieldType(fieldname)
    if type(value) != shouldBeType:
      raise TypeError, 'type error in __setitem__ attrName=%s and attrValue=%s ' %(fieldname, str(value))
    self.concursoDict[fieldname] = value
    self.insertFieldnameInOrder(fieldname)
  def insertFieldnameInOrder(self, fieldname):
    # first case: if self.fieldnamesInOrder is empty, append it right away and return
    if len(self.fieldnamesInOrder) == 0:
      self.fieldnamesInOrder.append(fieldname)
      return
    indexPositionOfEnteringOne = fat.allowedFieldNamesInOriginalOrder.index(fieldname)
    indexPositionOfLastElement = fat.allowedFieldNamesInOriginalOrder.index(self.fieldnamesInOrder[-1])
    if indexPositionOfEnteringOne > indexPositionOfLastElement:
      # okay, problem solved, it can be appended (ie, inserted at the end) and routine should return
      self.fieldnamesInOrder.append(fieldname)
      return
    # the optimum time condition above did not happen, so let's loop thru it (it's not that big, so time is not a problem here)
    for i in range(0, len(self.fieldnamesInOrder)): 
      indexPositionOfCurrentElement = fat.allowedFieldNamesInOriginalOrder.index(self.fieldnamesInOrder[i])
      if indexPositionOfEnteringOne < indexPositionOfCurrentElement:
        self.fieldnamesInOrder.insert(i, fieldname)
        return
    # well, if program flow got to here, a exception should be raised
    raise IndexError, "could not insertFieldnameInOrder :: fieldname = %s " %fieldname 
  def __getitem__(self, fieldname):
    if fieldname in self.concursoDict.keys():
      return self.concursoDict[fieldname]
    return None
  def getDezenas(self):
    dezenas = []
    for i in range(1,7):
      fieldname = 'dezena%d' %i
      dezenas.append(self[fieldname])
    return dezenas

  def getTilN(self, tilN=None):
    nDoConcurso = self.concursoDict['nDoConcurso']
    tilObj = tilMod.TilMaker(tilN, nDoConcurso)
    tilSets = tilObj.getTilSets() 
    dezenas = self.getDezenas()
    tilPatternDict = {}
    for i in range(len(tilSets)):
      tilPatternDict[i+1]=0
    tilSets = tilObj.getTilSets()
    for dezena in dezenas:
      for i in range(len(tilSets)):
        tilSet = tilSets[i] 
        if dezena in tilSet:
          tilPatternDict[i+1] += 1
          break
    tilPatternStr = ''
    patterns = tilPatternDict.keys()
    patterns.sort()
    for pattern in patterns:
      tilPatternStr += str(tilPatternDict[pattern]) 
    return tilPatternStr

  def sqlInsert(self):
    sqlInsertStr = 'INSERT INTO `megasena` ('
    for fieldname in self.fieldnamesInOrder:
      sqlInsertStr += '`%s`, ' %fieldname
    sqlInsertStr = sqlInsertStr[:-2] + ') VALUES ('
    for fieldname in self.fieldnamesInOrder:
      sqlInsertStr += "'%s', " %str(self.concursoDict[fieldname])
    sqlInsertStr = sqlInsertStr[:-2] + ');'
    return sqlInsertStr 
  def isEqualTo(self, concurso2):
    for fieldname in self.fieldnamesInOrder:
      if self.concursoDict[fieldname] != concurso2[fieldname]:
        return False
    return True
  def __str__(self):
    outStr = ''
    for fieldname in self.fieldnamesInOrder:
      outStr += fieldname + ':' + str(self.concursoDict[fieldname]) + '; '
    outStr = outStr[ : -2]
    return outStr 

def convertRowListToConcursoObj(row):
  # the HTML nDoConcurso field must be an int number first of all, check this first
  try:
    value = row['nDoConcurso']
    try:
      value = int(value)
    except ValueError:
      return None
  except KeyError:
    return None
  concurso = Concurso()
  for fieldname in row.keys():
    value = row[fieldname]
    shouldBeType = fat.getFieldType(fieldname)
    if type(value) == shouldBeType:
      concurso[fieldname]=value
      continue
    # special case of 
    if fieldname == 'acumuladoSimNao':
      if value.lower().startswith('s'): # s = sim
        value = 1
      elif value.lower().startswith('n'): # n = não
        value = 0
      else:
        # dirty value
        raise ValueError, "dirty value in fieldname %s = %s" %(fieldname, str(value))
      concurso[fieldname]=value
      continue
    elif shouldBeType == int:
      value = int(value)
      concurso[fieldname]=value
      continue
    elif shouldBeType == float:
      value = conv.convertToFloatAMoneyCurrencyNotInEnglishFormat(value)
      concurso[fieldname]=value
    elif shouldBeType == datetime.date:
      value = conv.convertToDatetimeDate(value)
      concurso[fieldname]=value
    else:
      # last try: see if it will enter as a string
      if type(value) == str:
        concurso[fieldname]=value
        continue
      raise ValueError, "could not enter value in a fieldname according the type rules :: value = %s type=%s" %(str(value), str(type(value)))
  return concurso

def testConcursoSample():
  c = Concurso()
  c['valorAcumulado']=1000000.00
  c['dezena6']=15
  c['nDoConcurso']=200
  c['dezena1']=25
  print c
  
if __name__ == '__main__':
  testConcursoSample()


def hidden():
  textForOld_sqlInsert = '''
    def sqlInsert(self):
    sqlInsertStr = 'INSERT INTO `megasena` ('
    for fieldname in self.fieldnamesInOrder:
      sqlfieldname = fieldname
      if sqlfieldname == 'dezena6':
        sqlfieldname = '***dezenas***'
      if sqlfieldname.startswith('dezena') and len(sqlfieldname) == 7:
        continue
      if sqlfieldname == '***dezenas***':
        sqlfieldname = 'dezenas'
      sqlInsertStr += '`%s`, ' %sqlfieldname
    sqlInsertStr = sqlInsertStr[:-2] + ') VALUES ('
    dezenasStr = ''
    for fieldname in self.fieldnamesInOrder:
      if fieldname.startswith('dezena') and len(fieldname) == 7:
        dezenasStr += '%s' %str(self.concursoDict[fieldname]).zfill(2)
        if fieldname == 'dezena6':
          sqlInsertStr += "'%s', " %dezenasStr
      else:
        sqlInsertStr += "'%s', " %str(self.concursoDict[fieldname])
    sqlInsertStr = sqlInsertStr[:-2] + ');'
    return sqlInsertStr'''
  print textForOld_sqlInsert 
