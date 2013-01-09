#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 13/11/2011

@author: friend
'''
import sqlite3, sys
a=1
import FieldsAndTypes as fat
import HTMLGrabber as hb
import ClassConcursoEtc as conc
import converterForDateAndCurrency as conv

megasenaMetricsSqliteCreate = '''
CREATE TABLE IF NOT EXISTS `megasenametrics` (
  `nDoConcurso` smallint(6) NOT NULL,
  `iguaisComOAnterior` tinyint(3) DEFAULT NULL,
  `coincsComOs3Anteriores` tinyint(3) DEFAULT NULL,
  `maxDeIguais` tinyint(3) DEFAULT NULL,
  `maxDeIguaisDistAo1o` smallint(5) DEFAULT NULL,
  `maxDeIguaisOcorrencia` tinyint(3) DEFAULT NULL,
  `iguaisMediaComPassado` float DEFAULT NULL,
  `rem2pattern` char(6) DEFAULT NULL,
  `parParImparImpar` char(6) DEFAULT NULL,
  `rem3pattern` char(6) DEFAULT NULL,
  `rem5pattern` char(6) DEFAULT NULL,
  `rem6pattern` char(6) DEFAULT NULL,
  `colpattern` char(6) DEFAULT NULL,
  `til4pattern` char(4) DEFAULT NULL,
  `til5pattern` char(5) DEFAULT NULL,
  `til6pattern` char(6) DEFAULT NULL,
  `til10pattern` char(10) DEFAULT NULL,
  `consecEnc` mediumint(3) DEFAULT NULL,
  `soma1` smallint(5) DEFAULT NULL,
  `soma3` smallint(6) DEFAULT NULL,
  `soma7` smallint(6) DEFAULT NULL,
  `soma15` mediumint(8) DEFAULT NULL,
  `std` float DEFAULT NULL,
  `pathway` smallint(6) DEFAULT NULL,
  `allpaths` smallint(6) DEFAULT NULL,
  `binDecReprSomaDe1s` tinyint(3) DEFAULT NULL,
  `lgiDist` int(11) DEFAULT NULL,
  PRIMARY KEY (`nDoConcurso`)) ;
'''

def sqliteInsert(reinsert=False):
  conn = sqlite3.connect('megasena.sqlite')
  if reinsert:
    sql = 'delete from megasenametrics;'
    conn.execute(sql)
  grabber = hb.HtmlGrabberClass()
  for concurso in grabber.concursos:
    sql = concurso.sqlInsert()
    print sql,
    retVal = conn.execute(sql)
    print retVal
    if retVal:
      conn.commit()
    
def createTable(tablename=megasenaMetricsSqliteCreate):
  conn = sqlite3.connect('megasena.sqlite')
  conn.execute(tablename)
  conn.close()
  
def sqlSelect():
  conn = sqlite3.connect('megasena.sqlite')
  sql = 'select * from `megasenametrics`;'
  rows = conn.execute(sql); concursos = []
  for row in rows:
    row2 = {}; fieldnameCount = 0
    for fieldname in fat.allowedFieldNamesInOriginalOrder:
      value = row[fieldnameCount]
      # this "if" is to be ported to the conc.convertRowListToConcursoObj(row2) function at an opportunity
      if fieldname == 'dataDoSorteio':
        value = str(value)
        value = conv.convertToDatetimeDate(value, 'YYYY-MM-DD')
      row2[fieldname] = value 
      print fieldnameCount, fieldname, value, 'type', type(value)
      fieldnameCount += 1
    print 'row2', row2
    concurso = conc.convertRowListToConcursoObj(row2)
    concursos.append(concurso)
  return concursos

def printConcursos(concursos):
  for concurso in concursos:
    print concurso 

def doCreateTablePlusInsert():
  createTable()
  sqliteInsert(True)

def doShowConcursosData():
  concursos = sqlSelect()
  printConcursos(concursos)
  
cliParameters = {'create':(doCreateTablePlusInsert, 'To create megasena sql table if it does not yet exist and fill it with HTML game result data.'), \
                 'show':(doShowConcursosData, 'To show data in the megasena sql table.')} 

def showCliParameters():
  options = cliParameters.keys()
  options.sort()
  print '='*20
  print sys.argv[0], 'Options:'
  print '='*20
  for option in options:
    description = cliParameters[option][1]
    print option, '==>>', description

def processCliOptions():
  if len(sys.argv) > 1:
    optionIn = sys.argv[1].lower()
    options = cliParameters.keys()
    if optionIn in options:
      func = cliParameters[optionIn][0]
      func()
    else:
      showCliParameters()
  else:
    showCliParameters()

if __name__ == '__main__':
  processCliOptions()
