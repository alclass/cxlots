#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3, sys


'''
-- DROP TABLE IF EXISTS `ms`;
'''
import funcsForSql as fSql
import HistoricoUpdater as hu
import Stat

msCreateForMySql = '''
CREATE TABLE IF NOT EXISTS `ms` (
  `nDoConc` smallint(6) unsigned NOT NULL,
  `jogoCharOrig` char(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `date` date DEFAULT NULL,
  `iguaisComOAnterior` tinyint(3) unsigned DEFAULT NULL,
  `coincsComOs3Anteriores` tinyint(3) unsigned DEFAULT NULL,
  `maxDeIguais` tinyint(3) unsigned DEFAULT NULL,
  `maxDeIguaisDistAo1o` smallint(5) unsigned DEFAULT NULL,
  `maxDeIguaisOcorrencia` tinyint(3) unsigned DEFAULT NULL,
  `iguaisMediaComPassado` float unsigned DEFAULT NULL,
  `rem2pattern` char(6) COLLATE utf8_unicode_ci DEFAULT NULL,
  `parParImparImpar` char(6) COLLATE utf8_unicode_ci DEFAULT NULL,
  `rem3pattern` char(6) COLLATE utf8_unicode_ci DEFAULT NULL,
  `rem5pattern` char(6) COLLATE utf8_unicode_ci DEFAULT NULL,
  `rem6pattern` char(6) COLLATE utf8_unicode_ci DEFAULT NULL,
  `colpattern` char(6) COLLATE utf8_unicode_ci DEFAULT NULL,
  `til4pattern` char(4) COLLATE utf8_unicode_ci DEFAULT NULL,
  `til5pattern` char(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `til6pattern` char(6) COLLATE utf8_unicode_ci DEFAULT NULL,
  `til10pattern` char(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `consecEnc` mediumint(3) unsigned DEFAULT NULL COMMENT 'int encoding for consecutives',
  `soma1` smallint(5) unsigned DEFAULT NULL,
  `soma3` smallint(6) unsigned DEFAULT NULL,
  `soma7` smallint(6) unsigned DEFAULT NULL,
  `soma15` mediumint(8) unsigned DEFAULT NULL,
  `std` float unsigned DEFAULT NULL,
  `pathway` smallint(6) unsigned DEFAULT NULL,
  `allpaths` smallint(6) unsigned DEFAULT NULL,
  `binDecReprSomaDe1s` tinyint(3) unsigned DEFAULT NULL,
  `lgiDist` int(11) DEFAULT NULL,
  `arrecadacao` decimal(13,2) unsigned DEFAULT NULL,
  `ganhadoresSena` tinyint(3) unsigned DEFAULT NULL,
  `rateioSena` decimal(13,2) unsigned DEFAULT NULL,
  `ganhadoresQuina` smallint(5) unsigned DEFAULT NULL,
  `rateioQuina` decimal(10,2) unsigned DEFAULT NULL,
  `ganhadoresQuadra` mediumint(8) unsigned DEFAULT NULL,
  `rateioQuadra` decimal(6,2) unsigned DEFAULT NULL,
  `foiAcumulado` tinyint(1) DEFAULT NULL,
  `acumulado` decimal(12,2) unsigned DEFAULT NULL,
  `premioEstimado` decimal(13,2) unsigned DEFAULT NULL,
  `premioAcumNatal` decimal(13,2) unsigned DEFAULT NULL,
  PRIMARY KEY (`nDoConc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;'''

lfCreateForMySql = '''
CREATE TABLE IF NOT EXISTS `lf` (
  `nDoConc` smallint(6) unsigned NOT NULL,
  `jogoCharOrig` char(30) COLLATE utf8_unicode_ci DEFAULT NULL,
  `date` date DEFAULT NULL,
  `iguaisComOAnterior` tinyint(3) unsigned DEFAULT NULL,
  `coincsComOs3Anteriores` tinyint(3) unsigned DEFAULT NULL,
  `maxDeIguais` tinyint(3) unsigned DEFAULT NULL,
  `maxDeIguaisDistAo1o` smallint(5) unsigned DEFAULT NULL,
  `maxDeIguaisOcorrencia` tinyint(3) unsigned DEFAULT NULL,
  `minDeIguais` tinyint(3) unsigned DEFAULT NULL,
  `minDeIguaisDistAo1o` mediumint(8) unsigned DEFAULT NULL,
  `minDeIguaisOcorrencia` smallint(5) unsigned DEFAULT NULL,
  `iguaisMediaComPassado` float DEFAULT NULL,
  `rem2pattern` char(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `parParImparImpar` char(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `rem3pattern` char(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `rem5pattern` char(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `rem6pattern` char(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `colpattern` char(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `til4pattern` char(4) COLLATE utf8_unicode_ci DEFAULT NULL,
  `til5pattern` char(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `til6pattern` char(6) COLLATE utf8_unicode_ci DEFAULT NULL,
  `til10pattern` char(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `consecEnc` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `soma1` smallint(5) unsigned DEFAULT NULL,
  `soma3` smallint(5) unsigned DEFAULT NULL,
  `soma7` smallint(6) unsigned DEFAULT NULL,
  `soma15` mediumint(8) unsigned DEFAULT NULL,
  `std` float DEFAULT NULL,
  `pathway` smallint(6) unsigned DEFAULT NULL,
  `allpaths` smallint(6) unsigned DEFAULT NULL,
  `binDecReprSomaDe1s` tinyint(3) unsigned DEFAULT NULL,
  `lgiDist` int(11) DEFAULT NULL,
  `arrecadacao` decimal(13,2) unsigned DEFAULT NULL,
  `ganhadores15N` tinyint(3) unsigned DEFAULT NULL,
  `ganhadores14N` smallint(5) unsigned DEFAULT NULL,
  `ganhadores13N` smallint(5) unsigned DEFAULT NULL,
  `ganhadores12N` mediumint(8) unsigned DEFAULT NULL,
  `ganhadores11N` mediumint(8) unsigned DEFAULT NULL,
  `rateio15` decimal(12,2) unsigned DEFAULT NULL,
  `rateio14` decimal(9,2) unsigned DEFAULT NULL,
  `premioAcum15` decimal(12,2) unsigned DEFAULT NULL,
  `premioEstimado` decimal(12,2) unsigned DEFAULT NULL,
  PRIMARY KEY (`nDoConc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;'''

lfCreateForSqlite = '''
CREATE TABLE IF NOT EXISTS `lf` (
  `nDoConc` smallint(6) NOT NULL,
  `jogoCharOrig` char(30) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `iguaisComOAnterior` tinyint(3) DEFAULT NULL,
  `coincsComOs3Anteriores` tinyint(3) DEFAULT NULL,
  `maxDeIguais` tinyint(3) DEFAULT NULL,
  `maxDeIguaisDistAo1o` smallint(5) DEFAULT NULL,
  `maxDeIguaisOcorrencia` tinyint(3) DEFAULT NULL,
  `minDeIguais` tinyint(3) DEFAULT NULL,
  `minDeIguaisDistAo1o` mediumint(8) DEFAULT NULL,
  `minDeIguaisOcorrencia` smallint(5) DEFAULT NULL,
  `iguaisMediaComPassado` float DEFAULT NULL,
  `rem2pattern` char(15) DEFAULT NULL,
  `parParImparImpar` char(15) DEFAULT NULL,
  `rem3pattern` char(15) DEFAULT NULL,
  `rem5pattern` char(15) DEFAULT NULL,
  `rem6pattern` char(15) DEFAULT NULL,
  `colpattern` char(15) DEFAULT NULL,
  `til4pattern` char(4) DEFAULT NULL,
  `til5pattern` char(5) DEFAULT NULL,
  `til6pattern` char(6) DEFAULT NULL,
  `til10pattern` char(10) DEFAULT NULL,
  `consecEnc` varchar(11) DEFAULT NULL,
  `soma1` smallint(5) DEFAULT NULL,
  `soma3` smallint(5) DEFAULT NULL,
  `soma7` smallint(6) DEFAULT NULL,
  `soma15` mediumint(8) DEFAULT NULL,
  `std` float DEFAULT NULL,
  `pathway` smallint(6) DEFAULT NULL,
  `allpaths` smallint(6) DEFAULT NULL,
  `binDecReprSomaDe1s` tinyint(3) DEFAULT NULL,
  `lgiDist` int(11) DEFAULT NULL,
  `arrecadacao` decimal(13,2) DEFAULT NULL,
  `ganhadores15N` tinyint(3) DEFAULT NULL,
  `ganhadores14N` smallint(5) DEFAULT NULL,
  `ganhadores13N` smallint(5) DEFAULT NULL,
  `ganhadores12N` mediumint(8) DEFAULT NULL,
  `ganhadores11N` mediumint(8) DEFAULT NULL,
  `rateio15` decimal(12,2) DEFAULT NULL,
  `rateio14` decimal(9,2) DEFAULT NULL,
  `premioAcum15` decimal(12,2) DEFAULT NULL,
  `premioEstimado` decimal(12,2) DEFAULT NULL,
  PRIMARY KEY (`nDoConc`)) ;'''

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


def createTablesWithConn(conn, whichDB):
  varNameEnding = ''
  if whichDB == fSql.MYSQL:
    varNameEnding = 'CreateForMySql'
  elif whichDB == fSql.SQLITE:
    varNameEnding = 'CreateForSqlite'
  cursor = conn.cursor()
  for tableName in ['lf', 'ms']:
    sqlComm = 'DROP TABLE IF EXISTS `%s`;' %(tableName)
    print sqlComm
    cursor.execute(sqlComm)
    print 'Creating sqlite table for', tableName,
    varName = tableName + varNameEnding
    print 'varName', varName
    sqlComm = eval(varName)
    #print sqlComm
    cursor.execute(sqlComm)
  conn.commit()
  print 'createTablesWithConn(conn, whichDB) ==>> committed'

def recreate():
  print 'recreate() sql tables'
  for whichDB in fSql.DBCONSTANTS:
    #if whichDB == 2:
      #continue
    print 'recreate() sql tables for db=', whichDB
    dbObj = fSql.getDBObj(whichDB)
    if not dbObj:
      continue
    if dbObj.whichDB <> whichDB:
      # this may happen because getDBObj() returns a Sqlite DB object if a MySQL is not available (either MySQLdb module is not available or some other cause like server is offline)
      continue
    dbObj.openConnection()
    conn = dbObj.conn
    createTablesWithConn(conn, whichDB)
    conn.close()
    del dbObj
  for jogoTipo in ['lf','ms']:
    hu.doHistoricoUpdater(jogoTipo)
    Stat.processDBStats(jogoTipo)


if __name__ == '__main__':
  if len(sys.argv) > 1:
    arg = sys.argv[1]
    if arg == '-recreate':
      recreate()
  pass
