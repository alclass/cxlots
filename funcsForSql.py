#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os # datetime, sys

MYSQL  = 1
SQLITE = 2
DBCONSTANTS = [MYSQL, SQLITE]
import funcsForSqlCreateTable as funcsForCT

def parametersDict(whichDB):
  paramsDict = {}
  if whichDB == MYSQL:
    # Connection Parameters for MySQL
    # =====================
    paramsDict['SERVER'] = 'localhost'
    paramsDict['USER'  ] = 'webuser'
    paramsDict['PW'    ] = 'webpass'
    paramsDict['DB'    ] = 'cxlots'
    # =====================
    return paramsDict
  if whichDB == SQLITE:
    paramsDict['DBFILE'] = 'dados/cxlots.sqlite'
    return paramsDict

IS_MYSQL_OPENABLE = True
IS_MYSQL_MODULE_AVAILABLE = True
try:
  import MySQLdb
except ImportError:
  IS_MYSQL_MODULE_AVAILABLE = False
  IS_MYSQL_OPENABLE = False

IS_SQLITE_OPENABLE = True
IS_SQLITE_MODULE_AVAILABLE = True
try:
  import sqlite3
except ImportError:
  IS_SQLITE_MODULE_AVAILABLE = False
  IS_SQLITE_OPENABLE = False

def getConnectionFor(whichDB):
  if whichDB == MYSQL and IS_MYSQL_OPENABLE:
    paramsDict = parametersDict(MYSQL)
    try:
      conn = MySQLdb.connect(paramsDict['SERVER'],paramsDict['USER'],paramsDict['PW'], paramsDict['DB'])
      return conn
    except MySQLdb.OperationalError:
      IS_SQLITE_OPENABLE = False
  if whichDB == SQLITE or not IS_SQLITE_OPENABLE:
    paramsDict = parametersDict(SQLITE)
    sqliteDBFile = paramsDict['DBFILE']
    # =======================================
    shouldCreateTablesInSqlite = False
    if not os.path.isfile(sqliteDBFile):
      shouldCreateTablesInSqlite = True
    else:
      if os.stat(sqliteDBFile)[6] == 0:  # file size
        shouldCreateTablesInSqlite = True
    conn = sqlite3.connect(sqliteDBFile)
    if shouldCreateTablesInSqlite:
      funcsForCT.createTablesInSqlite(conn, SQLITE)
    return conn
    # =======================================
  return None

def getConnection():
  '''
  getConnection
  getAvailableConnection
  gets the first available connection among a list of possible connections
  '''
  if IS_MYSQL_MODULE_AVAILABLE:
    return getConnectionFor(MYSQL)
  if IS_SQLITE_MODULE_AVAILABLE:
    return getConnectionFor(SQLITE)
  return None

if IS_MYSQL_OPENABLE:
  conn = getConnectionFor(MYSQL)
  if conn == None:
    IS_MYSQL_OPENABLE = False

if IS_SQLITE_OPENABLE:
  conn = getConnectionFor(SQLITE)
  if conn == None:
    IS_SQLITE_OPENABLE = False


class DB(object):

  def __init__(self, whichDB=MYSQL):
    self.logFile = open('logs/DBClass.log','w')
    self.whichDB = whichDB
    self.dbEngine = None
    if whichDB == SQLITE:
      #print 'Instantiating SQLITE dbObj'
      self.dbEngine = 'SQLITE'
    elif whichDB == MYSQL:
      #print 'Instantiating MYSQL dbObj'
      self.dbEngine = 'MYSQL'
    self.conn = None

  def verifyConnection(self, alreadyPassedHere=False):
    if self.conn == None:
      if alreadyPassedHere:
        errorMsg = 'Could not open DB or server is offline'
        raise ValueError, errorMsg
      self.openConnection()
      return self.verifyConnection(True)

    status = str(self.conn)
    if status.find('closed') > -1:
      if alreadyPassedHere:
        errorMsg = 'Could not open DB or server is offline'
        raise ValueError, errorMsg
      self.openConnection()
      return self.verifyConnection(True)

  def openConnection(self):
    self.conn = getConnectionFor(self.whichDB)
    self.verifyConnection()

  def executeAndCommit(self, sql):
    self.verifyConnection()
    cursor = self.conn.cursor()
    retVal = cursor.execute(sql)
    print 'executeAndCommit(self, sql) retVal =', retVal,
    if retVal:
      print 'retVal True-like >> self.conn.commit()'
      self.conn.commit()
    cursor.close()
    return retVal

  def executeSqlsAndCommitAtTheEnd(self, sqls):
    retValAll = False; c=0
    self.verifyConnection()
    cursor = self.conn.cursor()
    line = 'executeSqlsAndCommitAtTheEnd sqls size = %d' %(len(sqls))
    line += '\n sqls = %s' %(sqls)
    self.logFile.write(line + '\n')
    for sql in sqls:
      c+=1
      #print c, 'sql', sql
      retVal = cursor.execute(sql)
      if retVal:
        retValAll = True # if only one sql is executed, conn should be commited so that the D/I/U actions will take place
      #print 'executeAndCommit(self, sql) retVal =', retVal
    # either
    if retValAll:
      #print 'retVal = 1 >> self.conn.commit()'
      self.conn.commit()
      cursor.close()
    return retValAll

  def doSelect(self, sql):
    self.verifyConnection()
    cursor = self.conn.cursor()
    cursor.execute(sql)
    rows = []
    for row in cursor:
      rows.append(row)
    return list(rows)

  def closeConnection(self):
    self.conn.close()

  '''
  def __destroy__(self):
    print '*** destroy'
    self.closeConnection()
    object.__del__()
  '''

  def exists(self, sql):
    self.verifyConnection()
    cursor = self.conn.cursor()
    cursor.execute(sql)
    rows = cursor._rows
    if len(rows) > 0:
      return True
    return False

  def __str__(self):
    self.verifyConnection()
    outStr = '%s %s' %(self.dbEngine, self.conn)
    return outStr


'''
    
  if MYSQL_AVAILABLE:
    sql += ' ENGINE = InnoDB;'
  conn = getConnection()
  cursor = conn.cursor()
  retVal = cursor.execute(sql)
  print 'retVal', retVal 

  def getJogoInOrder(self, nDoConc):
    sqlTable = self.standard2LetterName.lower()
    sql = "select `jogoCharOrig` from `%s` where `nDoConc` = '%d';" %(sqlTable, nDoConc)
    conn = sf.getConnection()
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor._rows
    if len(rows) <> 1:
      return None
    jogoOrigChar = rows[0][0]; jogoInOrder = []
    i1=0; i2=2
    for i in range(6):
      jogoInOrder.append(int(jogoOrigChar[i1:i2]))
      i1+=2; i2+=2
    return jogoInOrder
  '''

def getDBObj(whichDB=-1):
  if whichDB==-1:
    if IS_MYSQL_OPENABLE:
      return DB(MYSQL)
    elif IS_SQLITE_OPENABLE:
      return DB(SQLITE)
  if whichDB == MYSQL and IS_MYSQL_OPENABLE:
    return DB(MYSQL)
  if whichDB == SQLITE and IS_SQLITE_OPENABLE:
    return DB(SQLITE)
  return None

class DoubleDBs(object):

  def __init__(self, sqlTable):
    self.logFile = open('logs/DoubleDBs.log','w')
    self.sqlTable = sqlTable
    self.dbObj = {}
    for db in DBCONSTANTS:
      dbObj = getDBObj(db)
      if dbObj:
        self.dbObj[db] = dbObj
        line = 'set db for db=%d' %(db)
        self.logFile.write(line + '\n')
    if len(self.dbObj) == 0:
      errorMsg = 'No DB available.'
      raise NameError, errorMsg
    #self.initDBs()

    line = 'after initDBs() dbObj dict size = %d' %(len(self.dbObj))
    self.logFile.write(line + '\n')
    line = 'IS_SQLITE_OPENABLE = %d IS_MYSQL_OPENABLE=%d' %(IS_SQLITE_OPENABLE, IS_MYSQL_OPENABLE)
    self.logFile.write(line + '\n')

    self.deltaDIUSqls = {} # DIU means Delete, Insert or Update
    self.retVal = {}

  def setDeltaDIUSqlsForDBs(self, sqls):
    for db in DBCONSTANTS:
      self.deltaDIUSqls[db] = sqls

  def initDBs(self):
    for db in DBCONSTANTS:
      dbObj = getDBObj(db)
      if dbObj:
        self.dbObj[db] = dbObj
        line = 'set db for db=%d' %(db)
        self.logFile.write(line + '\n')
    if len(self.dbObj) == 0:
      errorMsg = 'No DB available.'
      raise NameError, errorMsg

  def executeSqls(self):
    nOfDIUs = 0
    for db in self.dbObj.keys():
      dbObj = self.dbObj[db]
      try:
        sqls = self.deltaDIUSqls[db]
      except KeyError:
        continue
      self.retVal[db] = dbObj.executeSqlsAndCommitAtTheEnd(sqls)
    return nOfDIUs

  def closeDBs(self):
    for db in DBCONSTANTS:
      dbObj = self.dbObj[db]
      if dbObj:
        dbObj.close()


class DoubleDBsDeltaInserts(DoubleDBs):

  def __init__(self, sqlTable, jogosRegBase):
    DoubleDBs.__init__(self, sqlTable)
    self.ultimoNDoConc = {}
    self.discoverUltimos()
    self.jogosRegBase = jogosRegBase
    self.jogosReg3DD = {} # this will a 3-D dict, one dim. for db, one for nDoConc, one for jogoReg
    self.retVal = {}
    self.cutJogosReg()
    self.makeInsertDeltaSql()

  def initDBs(self):
    for db in DBCONSTANTS:
      dbObj = getDBObj(db)
      if dbObj:
        self.dbObj[db] = dbObj
    if len(self.dbObj) == 0:
      errorMsg = 'No DB available.'
      raise NameError, errorMsg

  def obtainSqlUltimoNDoConc(self, dbObj):
    self.ultimoNDoConc[dbObj.whichDB] = 0
    sql = "SELECT max(`nDoConc`) FROM `%s`;" %(self.sqlTable)
    rows = dbObj.doSelect(sql)
    ultimoNDoConc = 0
    if rows and len(rows) == 1:
      cell = rows[0][0]
      if cell and type(cell) == int:
        ultimoNDoConc = int(cell)

      self.ultimoNDoConc[dbObj.whichDB] = ultimoNDoConc

  def discoverUltimos(self):
    for db in self.dbObj.keys():
      dbObj = self.dbObj[db]
      self.obtainSqlUltimoNDoConc(dbObj)

  def cutJogosReg(self):
    for db in self.dbObj.keys():
      jogosReg = dict(self.jogosRegBase)
      line = 'for db=%d ultimoNDoConc %d' %(db, self.ultimoNDoConc[db])
      self.logFile.write(line + '\n')
      for nDoConc in range(1, self.ultimoNDoConc[db]+1):
        del jogosReg[nDoConc]
      self.jogosReg3DD[db] = dict(jogosReg)
      line = 'for db=%d size of jogosReg is %d' %(db, len(self.jogosReg3DD[db]))
      self.logFile.write(line + '\n')
      line = 'jogosReg = %s' %(self.jogosReg3DD[db])
      self.logFile.write(line + '\n')

  def makeInsertDeltaSql(self):
    for db in self.dbObj.keys():
      jogosReg = self.jogosReg3DD[db]
      nDoConcs = jogosReg.keys()
      if len(nDoConcs) == 0:
        self.deltaDIUSqls[db] = []
        continue
      sql1 = "INSERT INTO `%(sqlTable)s` (" %{'sqlTable':self.sqlTable}
      # it needs one jogoReg so that fields may be available
      jogoReg = jogosReg[nDoConcs[0]] # this is guaranteed, for if len(nDoConcs) is 0, a continue would avoid running this part
      fields = jogoReg.keys()
      for field in fields:
        sql1 += "`%s`," %(field)
      sql1 = sql1[:-1] + ') VALUES ('
      sqls = []
      for nDoConc in nDoConcs:
        jogoReg = jogosReg[nDoConc]
        jogoReg['nDoConc'] = nDoConc
        sql2 = ''
        for field in fields:
          value = jogoReg[field]
          sql2 += "'%s'," %(value)
        sql2 = sql2[:-1] + ');'
        sql = sql1 + sql2
        print sql
        sqls.append(sql)
      self.deltaDIUSqls[db] = list(sqls)

  def getNOfInserts(self):
    nOfInserts = 0
    for db in self.dbObj.keys():
      try:
        nOfInsert = self.retVal[db]
        nOfInserts += nOfInsert
      except KeyError:
        pass
    return nOfInserts


def doDBsUpdate(sql, DBs=DBCONSTANTS):
  atLeastOneDBHasBeenUpdatedOrInserted = False
  for db in DBs:
    dbObj = getDBObj(db)
    retVal = dbObj.executeAndCommit(sql)
    if retVal == 1:
      atLeastOneDBHasBeenUpdatedOrInserted = True
  if atLeastOneDBHasBeenUpdatedOrInserted:
    return 1
  return 0

def doDBUpdate(sql):
  if IS_MYSQL_OPENABLE:
    dbObj = getDBObj(MYSQL)
    retVal = dbObj.executeAndCommit(sql)
    return retVal
  if IS_SQLITE_OPENABLE:
    dbObj = getDBObj(SQLITE)
    retVal = dbObj.executeAndCommit(sql)
    return retVal
  return 0

def doDBsInsertsCheckingPrimaryKey(sqlInsert, table, pmField, pmValue):
  DBs = []
  for db in DBCONSTANTS:
    dbObj = getDBObj(db)
    sql = "SELECT `%(pmField)s` FROM `%(table)s` WHERE  `%(pmField)s`='%(pmValue)s';" %{'table':table,'pmField':pmField,'pmValue':pmValue}
    exists = dbObj.exists(sql)
    if not exists:
      DBs.append(db)
  return doDBsUpdate(sqlInsert, DBs)

def doDBsSelect(sql):
  rowsDBDict = {}
  for db in DBCONSTANTS:
    dbObj = getDBObj(db)
    rows = dbObj.doSelect(sql)
    rowsDBDict[db] = rows
  return rowsDBDict

def doDBSelect(sql):
  if IS_MYSQL_OPENABLE:
    dbObj = getDBObj(MYSQL)
    return dbObj.doSelect(sql)
  if IS_SQLITE_OPENABLE:
    dbObj = getDBObj(SQLITE)
    return dbObj.doSelect(sql)
  return None
    

def checkConsistencyOfJogosCharOrigAgainstNDoConcs(sqlTable, jogosCharOrig):
  '''
  Two inconsistent states are seached for here:
  1) a gap along nDoConcs
  2) a jogoCharOrig out of order
  '''

  sql = '''SELECT `nDoConc`, `jogoCharOrig` FROM `%s`
       order by `nDoConc`;''' %(sqlTable)

  supposedSeq = 0
  dbObj = getDBObj() # MYSQL is first option, SQLITE is second
  rows = dbObj.doSelect(sql)
  for cols in rows:
    nDoConc      = cols[0]
    jogoCharOrig = cols[1]
    if nDoConc <>  supposedSeq + 1:
      errorMsg = 'nDoConc (=%d) <>  supposedSeq + 1  (=%d)' %(nDoConc, supposedSeq)
      raise ValueError, errorMsg
    if jogosCharOrig[supposedSeq] <> jogoCharOrig:
      errorMsg = 'jogosCharOrig[supposedSeq=%d]=%s <>  jogoCharOrig=%s' %(jogosCharOrig[supposedSeq], jogoCharOrig)
      raise ValueError, errorMsg
    supposedSeq += 1
  print 'OK checkConsistencyOfJogosCharOrigAgainstNDoConcs'
  print ' SUMMARY: supposedSeq =', supposedSeq


def testDB():
  co = getDBObj(MYSQL)
  print 'co', co
  conn = co.conn
  print 'co.conn', conn
  co.closeConnection() # conn.close() 
  print 'co.conn', conn
  del co
  print 'co.conn', conn
  #print 'co', co
  c2 = getConnection()
  print 'c2', c2
  c3 = getConnectionFor(SQLITE)
  print 'c3', c3

if __name__ == '__main__':
  pass
  testDB()
  print 'IS_SQLITE_OPENABLE', IS_SQLITE_OPENABLE
  print 'IS_MYSQL_OPENABLE', IS_MYSQL_OPENABLE
