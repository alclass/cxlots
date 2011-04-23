#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime, os, sys, time
import sqlite3

a=1
import CLClasses
import Filtre
import funcs
import funcsForBinDecRepr as binDec
#import funcsForSql as fSql
import lambdas
import LgiCombiner as lc
import Stat
import Til as tilc
from cardprint import pprint

STREAM_TXTFILE = 1
STREAM_BINFILE = 2
STREAM_LGICOMB = 3
STREAM_SQL     = 4
STREAMS = [STREAM_TXTFILE, STREAM_BINFILE, STREAM_LGICOMB, STREAM_SQL]


def getOutBinFilename(sigla, ultimoNDoConc):
  seq = 1; seqZfill2 = str(seq).zfill(2)
  filename = '%s-%d-apostas-%s.bin' %(sigla, ultimoNDoConc, seqZfill2)
  exists = os.path.isfile(filename)
  while exists:
    seq += 1; seqZfill2 = str(seq).zfill(2)
    filename = '%s-%d-apostas-%s.bin' %(sigla, ultimoNDoConc, seqZfill2)
    exists = os.path.isfile(filename)

def getInBinFilename(sigla, ultimoNDoConc):
  files = glob.glob('%s-%d-apostas*.bin')  %(sigla, ultimoNDoConc)
  numbers = []
  for fil in files:
    try:
      n = int(fil.split('-')[3])
      numbers.append(n)
    except IndexError:
      continue
    except ValueError:
      continue
  numbers.sort()
  ultimo = numbers[-1]
  seqZfill2 = ultimo.zfill(2)
  filename = '%s-%d-apostas-%s.bin' %(sigla, ultimoNDoConc, seqZfill2)
  return filename
  

class Stream(Filtre.Filtre):

  def __init__(self, eitherJogosObjOrS2):
    Filtre.Filtre.__init__(self, eitherJogosObjOrS2)
    self.tableSeq = 0
    totalDezn     = self.jogosObj.totalDeDezenasNoVolante - 1
    deznSorteadas = self.jogosObj.nDeDezenasSorteadas
    self.mockIc = lc.LgiCombiner(totalDezn, deznSorteadas)
    self.outBinFilename = None
    self.inBinFilename  = None

  def setStreamInLgiCombiner(self):
    '''
    This can only be a reader
    '''
    volanteMenosUm    = self.jogosObj.totalDeDezenasNoVolante - 1
    nDeDezenas        = self.jogosObj.nDeDezenasSorteadas
    self.inStream     = lc.LgiCombiner(volanteMenosUm, nDeDezenas)
    self.inStreamType = STREAM_LGICOMB
    
  def setStreamInTxtFile(self, filename):
    self.inStream     = open(filename)
    self.inStreamType = STREAM_TXTFILE

  def setStreamInBinFile(self, filename=None):
    if filename == None:
      if self.outBinFilename <> None:
        filename = self.outBinFilename
      else:
        sigla = self.jogosObj.sqlTable
        ultimoNDoConc = len(self.jogosObj.getJogos())
        filename = getInBinFilename()
    nOfBytesForPacker = self.jogosObj.getNOfBytesForPacker()
    self.inStream     = binDec.IntPacker(nOfBytesForPacker)
    inFile            = open(filename, 'rb')
    self.inBinFilename = filename
    self.inStream.setFileObj(inFile, True)
    self.inStreamType = STREAM_BINFILE

  def setStreamOutBinFile(self, filename=None):
    nOfBytesForPacker = self.jogosObj.getNOfBytesForPacker()
    self.outStream    = binDec.IntPacker(nOfBytesForPacker)
    if filename == None:
      sigla = self.jogosObj.sqlTable
      ultimoNDoConc = len(self.jogosObj.getJogos())
      filename = getOutBinFilename(sigla, ultimoNDoConc)
    self.outBinFilename = filename
    outFile             = open(filename, 'wb')
    self.outStream.setFileObj(outFile, False)
    self.outStreamType = STREAM_BINFILE

  def setStreamOutTxtFile(self, filename):
    self.outStream     = open(filename,'w')
    self.outStreamType = STREAM_TXTFILE

  def setStreamInSql(self, tableSeq=-1, sqliteFile=None):
    self.inTable, sqliteInFile = self.findTableAndFileNames(tableSeq, sqliteFile)
    self.inConn = sqlite3.connect(sqliteInFile)
    self.inCursor = self.inConn.cursor()
    sql = "select * from `%s`;" %(self.inTable)
    self.inCursor.execute(sql)
    self.inStreamType = STREAM_SQL

  def setStreamOutSql(self, tableSeq=-1, sqliteFile=None):
    self.outTable, sqliteOutFile = self.findTableAndFileNames(tableSeq, sqliteFile)
    self.outConn = sqlite3.connect(sqliteOutFile)
    # ==========================================
    print 'creating table', self.outTable
    createTableSql = '''create table if not exists `%s` (
      `lgi` int
    );
''' %(self.outTable)
    # ==========================================
    self.outCursor = self.outConn.cursor()
    self.outCursor.execute(createTableSql)
    self.outConn.commit()
    self.streamOut = STREAM_SQL

  def findTableAndFileNames(self, tableSeq, sqliteFile):
    if tableSeq == -1:
      self.tableSeq += 1
    nextConc = len(self.jogosObj.getJogos()) + 1
    table = '%s%dapostasPara%d' %(self.jogosObj.sqlTable, self.tableSeq, nextConc)
    if sqliteFile == None:
      sqliteFile = table
    return table, sqliteFile

  def returnJogoObjFromLgi(self, lgi):
    #print 'returnJogoObjFromLgi(self, lgi) lgi=', lgi
    if lgi == None:
      return None
    jogo = self.mockIc.moveTo(lgi)
    jogoObj = CLClasses.Jogo(jogo, self.jogosObj.standard2LetterName)
    return jogoObj

  def first(self):
    return self.next()
    '''
    if self.inStreamType == STREAM_FILE:
    if self.inStreamType == STREAM_LGICOMB:
      jogo = self.inStream.first()
      return jogo
    return self.returnJogoObjFromLgi(lgi)
    '''

  def next(self):
    if self.inStreamType == STREAM_TXTFILE:
      line = self.inStream.readline()
      line = pprint.clearLineEnding(line)
      lgi = int(line)
    elif self.inStreamType == STREAM_LGICOMB:
      jogo = self.inStream.next()
      return jogo
    else:
      lgi = self.inStream.next()
      #print ' next()', lgi
    jogoObj = self.returnJogoObjFromLgi(lgi)
    #jogo = jogoObj.jogo
    return jogoObj

  '''    if self.streamIn == STREAM_SQL:
      row = cursor.next()
      if row:
        lgi = row[0]
      return jogoObj # transformRow(row)
'''

  def write(self, jogoObj):
    if type(jogoObj) == list:
      jogoObj = CLClasses.Jogo(jogoObj, self.jogosObj.standard2LetterName)
      lgi = jogoObj.getLgi()
    elif type(jogoObj) in [int, long]:
      lgi = jogoObj
    else:
      lgi = jogoObj.getLgi()
    if self.outStreamType == STREAM_TXTFILE:
      line = '%d' %(lgi)
      self.outStream.write(line + '\n')
      return
    elif self.outStreamType == STREAM_SQL:
      sql = "insert into %(table)s (`lgi`) values ('%(lgi)d');" %{'table':self.outTable, 'lgi':lgi}
      self.outCursor.execute(sql)
    else:
      self.outStream.write(lgi)

  def close(self):
    if self.outStreamType == STREAM_SQL:
      self.outConn.commit()
      self.outConn.close()
      return
    self.outStream.close()

def createSqliteTest():
  sqliteDBFile = 'test.sqlite'
  apostasConn = sqlite3.connect(sqliteDBFile)
  sql = '''CREATE TABLE `lfapostas2` (
  lgi int
  );
  '''
  cursor = apostasConn.cursor()
  try:
    cursor.execute(sql)
    apostasConn.commit()
  except sqlite3.OperationalError:
    # table is already created, go on
    pass
  return apostasConn



def testStream():
  pass


if __name__ == '__main__':
  testStream()
