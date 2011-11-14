#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 13/11/2011

@author: friend
'''
import sqlite3, sys
a=1
import ClassConcursoEtc as conc
import converterForDateAndCurrency as conv
import FieldsAndTypes as fat
import HTMLGrabber as hb

megasenaIndividualDzSqlCreateTable  = ''' 
CREATE TABLE IF NOT EXISTS `megasena` (
  `nDoConcurso` smallint(6) NOT NULL,
  `dataDoSorteio` date NOT NULL,
  `dezena1` tinyint(3) NOT NULL,
  `dezena2` tinyint(3) NOT NULL,
  `dezena3` tinyint(3) NOT NULL,
  `dezena4` tinyint(3) NOT NULL,
  `dezena5` tinyint(3) NOT NULL,
  `dezena6` tinyint(3) NOT NULL,
  `arrecadacaoTotal` float DEFAULT NULL,
  `ganhadoresDaSena` tinyint DEFAULT NULL,
  `rateioDaSena` decimal(13,2) DEFAULT NULL,
  `ganhadoresDaQuina` tinyint DEFAULT NULL,
  `rateioDaQuina` decimal(10,2) DEFAULT NULL,
  `ganhadoresDaQuadra` smallint DEFAULT NULL,
  `rateioDaQuadra` decimal(6,2) DEFAULT NULL,
  `acumuladoSimNao` tinyint(1) DEFAULT NULL,
  `valorAcumulado` decimal(12,2) DEFAULT NULL,
  `estimativaDePremio` decimal(13,2) DEFAULT NULL,
  `acumuladoDeNatal` decimal(13,2) DEFAULT NULL,
 PRIMARY KEY (`nDoConcurso`)) ;
'''

def sqliteInsert(reinsert=False):
  conn = sqlite3.connect('megasena.sqlite')
  if reinsert:
    sql = 'delete from megasena;'
    conn.execute(sql)
  grabber = hb.HtmlGrabberClass()
  for concurso in grabber.concursos:
    sql = concurso.sqlInsert()
    print sql,
    retVal = conn.execute(sql)
    print retVal
    if retVal:
      conn.commit()
    
def createTable():
  conn = sqlite3.connect('megasena.sqlite')
  conn.execute(megasenaIndividualDzSqlCreateTable)
  conn.close()
  
def sqlSelect():
  conn = sqlite3.connect('megasena.sqlite')
  sql = 'select * from `megasena`;'
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

def hiddenOldFunctions():
  msCreateForSqlite = '''
CREATE TABLE IF NOT EXISTS `ms` (
  `nDoConc` smallint(6) NOT NULL,
  `jogoCharOrig` char(30) DEFAULT NULL,
  `date` date DEFAULT NULL,
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
  `arrecadacao` decimal(13,2) DEFAULT NULL,
  `ganhadoresSena` tinyint(3) DEFAULT NULL,
  `rateioSena` decimal(13,2) DEFAULT NULL,
  `ganhadoresQuina` smallint(5) DEFAULT NULL,
  `rateioQuina` decimal(10,2) DEFAULT NULL,
  `ganhadoresQuadra` mediumint(8) DEFAULT NULL,
  `rateioQuadra` decimal(6,2) DEFAULT NULL,
  `foiAcumulado` tinyint(1) DEFAULT NULL,
  `acumulado` decimal(12,2) DEFAULT NULL,
  `premioEstimado` decimal(13,2) DEFAULT NULL,
  `premioAcumNatal` decimal(13,2) DEFAULT NULL,
  PRIMARY KEY (`nDoConc`)) ;'''
  print msCreateForSqlite
