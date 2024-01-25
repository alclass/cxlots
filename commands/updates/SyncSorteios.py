#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime, os, sys

a=1
import CLClasses
import funcs
import funcsForSql as fSql
import funcsForDates as fDates
import HistoricoUpdater as huc


class SyncSorteios(CLClasses.Base):

  def __init__(self, standard2LetterName):
    CLClasses.Base.__init__(self, standard2LetterName)
    self.initWeekDays()
    self.printMsg    = False
    self.nOfInserted = 0
    self.htmlFilename         = self.getFilename('htm')
    self.lastdownloadfilename = '.%s-lastdownload.txt' %(self.sqlTable)
    self.shellDlScript        = self.sqlTable + 'downloadzip.sh'

  def initWeekDays(self):
    # ['wed','sat'] is [2, 5]
    self.weekDays =  [2, 5]   # for 'LM' and 'MS'
    if self.standard2LetterName == 'LF':
      # ['mon','thu'] is [0, 3]
      self.weekDays = [0, 3]

  def getFileDate(self):
    intDate = os.stat(self.htmlFilename)[6]
    return intDate

  def execDlScript(self):
    now = datetime.datetime.now()
    if os.path.isfile(self.lastdownloadfilename):
      line = open(self.lastdownloadfilename).read()
      # 2009-09-26 17:19:17.383316
      lastDownloadDate = fDates.get_date_from_string(line)
      dif = now - lastDownloadDate
      seconds = dif.seconds
      threeHours = 3 * 60 * 60
      if seconds < threeHours:
        if self.printMsg:
          print self.name + ' was downloaded less than 3 hours ago. *'
          print '* Please, wait at least 3 hours for a new download try.'
        return
    # retVal = 1
    retVal = os.system('sh ' + self.shellDlScript)
    if self.printMsg:
      print 'execDlScript() retVal', retVal
    if retVal == 0:
      fld = open(self.lastdownloadfilename,'w')
      line = '%s' %(str(now))
      fld.write(line)
      fld.close()
      hu = huc.HistoricoUpdater(self.standard2LetterName)
      hu.updateHistorico()
      self.nOfInserted = hu.nOfInserted
      if self.printMsg:
        print 'hu.nOfInserted', hu.nOfInserted

  def getLastSqlDate(self):
    sql = "select max(`date`) from `%s`;" %(self.sqlTable)
    conn = fSql.getConnection()
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = []
    for row in cursor:
      rows.append(row)
    date = None
    if len(rows) == 1:
      # date comes as datetime.date
      date = rows[0][0]
    # print 'getLastSqlDate(self) :: date =', date
    return date

  def getLastSorteioDate(self):
    '''
    ...
    '''
    today = datetime.date.today()
    weekday = today.weekday()
    dif1 = fDates.get_weekday_dif(weekday, self.weekDays[0])
    dif2 = fDates.get_weekday_dif(weekday, self.weekDays[1])
    # print 'dif1', dif1, 'dif2', dif2
    # horaDoSorteio = 21*60*60
    dif = None
    if dif1 < dif2: # they are never equal
      dif = dif1
      if dif1 == 0:
        dif = dif2
    else: # ie, dif2 < dif1: 
      dif = dif2
      if dif2 == 0:
        # back to dif1
        dif = dif1
    difToLastSorteio = datetime.timedelta(dif)
    lastSorteio = today - difToLastSorteio
    return lastSorteio

  def getNextSorteioDate(self):
    '''
    next sorteio is either today or related to the closest backward weekday to today's date
    '''
    nextSorteio = datetime.date.today()
    weekday     = nextSorteio.weekday()
    if weekday == self.weekDays[0] or weekday == self.weekDays[1]:
      return nextSorteio
      '''
      # Deprecated (ie, because Sorteio is late at night, nextSorteio may be today in applicable
      while weekday <> self.weekDays[1]:
        nextSorteio = nextSorteio + datetime.timedelta(1)
        weekday     = nextSorteio.weekday()
      return nextSorteio
    elif weekday == self.weekDays[1]:
      while weekday <> self.weekDays[0]:
        nextSorteio = nextSorteio + datetime.timedelta(1)
        weekday     = nextSorteio.weekday()
      return nextSorteio
      '''
    else:
      while weekday <> self.weekDays[0] and weekday <> self.weekDays[1]:
        nextSorteio = nextSorteio + datetime.timedelta(1)
        weekday     = nextSorteio.weekday()
      return nextSorteio
    return None

  def sync(self):
    osToken = sys.version
    if self.printMsg:
      print "Sync'ing", self.standard2LetterName
    if osToken.find('windows') > -1:
      print "It's Windows, I'm probably under a firewall, can't download."
      return
    lastSorteioDate = self.getLastSorteioDate()
    lastSqlDate = self.getLastSqlDate()
    # it should be never "greater than" (>)
    if lastSqlDate == lastSorteioDate:
      if self.printMsg:
        print 'No need to sync, lastSqlDate (%s) == lastSorteioDate (%s)' %(lastSqlDate, lastSorteioDate)
        date = self.getNextSorteioDate()
        print 'Next sorteio will be', date,
        if date == datetime.date.today():
          print 'ie, today, tonight'
        else:
          print
      return
    # okay, lastSqlDate no longer needed
    today = datetime.date.today()
    deltaDays = today - lastSorteioDate
    difDays = deltaDays.days
    if difDays >= 1:
      if self.printMsg:
        print 'difDays =', difDays, 'should download new set.'
      self.execDlScript()
      return
    if self.printMsg:
      print 'difDays =', difDays, 'should NOT YET download new set.'

  def __str__(self):
    outStr = '%s date = %s' %(self.htmlFilename, self.fileDate())
    return outStr


def testDataFileClass():
  wdays = weekDaysDict.keys()
  wdays.sort()
  for i in range(len(wdays)):
    for j in range(i+1, len(wdays)):
      wdi= wdays[i]; wdj = wdays[j]
      dif = fDates.get_weekday_dif(wdi, wdj)
      print wdi, wdj, dif

def testDateFromString():
  s = str(datetime.datetime.now())
  print 's', s
  d = fDates.get_date_from_string(s)
  print 'd', d
  df = DataFile('MS')
  print df.getLastSorteioDate()
  df.tryToUpdate()

shellTemplate = '''if [ -f %(zipFilename)s ]; then
  echo Deleting file %(zipFilename)s
  rm %(zipFilename)s
fi
if [ -d %(dirName)s ]; then
  echo Deleting dir %(dirName)s
  rm -rf %(dirName)s
fi
echo Downloading %(zipFilename)s
wget http://www1.caixa.gov.br/loterias/_arquivos/loterias/%(zipFilename)s
echo Expanding %(zipFilename)s
unzip D_lotfac.zip -d %(dirName)s
echo Moving %(htmlFile)s
mv ./%(dirName)s/%(htmlFile)s ./dados/%(htmlFileLower)s
# clean-up
if [ -f %(zipFilename)s ]; then
  echo Deleting file %(zipFilename)s
  rm %(zipFilename)s
fi
if [ -d %(dirName)s ]; then
  echo Deleting dir %(dirName)s
  rm -rf %(dirName)s
fi'''

dirNamesDict = {'lf':'D_lotfac','lm':'D_lotman','ms':'D_mega'}
def createShellExecFiles():
  for standard2LetterName in CLClasses.standardNames:
    base = CLClasses.Base(standard2LetterName)
    jogoTipo = base.sqlTable # 'lf'
    shellFilename = '%sdownloadzip.sh' %(jogoTipo)
    if os.path.isfile(shellFilename):
      print shellFilename, 'already exists, not recreating it now, continuing.'
      continue
    dirName = dirNamesDict[jogoTipo]
    zipFilename = '%s.zip' %(dirName)
    htmlFile = base.getFilename('htm')
    htmlFileLower = htmlFile.lower()
    shellContext = shellTemplate %{ \
        'dirName'      : dirName, \
        'htmlFile'     : htmlFile,\
        'htmlFileLower': htmlFileLower,\
        'zipFilename'  : zipFilename \
      }
    outFile = open(shellFilename, 'w')
    outFile.write(shellContext)
    outFile.close()

def sync(jogoTipo):
  '''
Usage:
  syncSorteio.py -u <tipoJogo>
Example:
  syncSorteio.py -u ms
Where:
  -u is a parameter which means sync/update
  ms means megasena to be sync'ed
  '''
  ss = SyncSorteios(jogoTipo)
  # ss.printMsg = True
  ss.sync()

def tellNextSorteios():
  jogoTipos = CLClasses.standardNames
  for jogoTipo in jogoTipos:
    ss = SyncSorteios(jogoTipo)
    print jogoTipo, ss.getNextSorteioDate(), ss.getLastSorteioDate()

if __name__ == '__main__':
  funcs.updateCaller('sync') # methodToBeCalled = 'sync'
  '''
  testDataFileClass()
  testDateFromString()
  createShellExecFiles()
  tellNextSorteio()
  '''
