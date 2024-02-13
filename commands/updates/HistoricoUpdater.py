#!/usr/bin/env python3
"""
This module altogether (HistoricoUpdater.py) is outdated. New code has replaced it.
  (As this comment is written, sqlLayer.py does the new code.)

"""
import datetime, sys
import CLClasses
import funcsForDates as fDates
import funcsForSql as fSql
import proprieties as props
from   cardprint import pprint


class HistoricoUpdater(object):

  def __init__(self, jogosBaseObj):
    '''
    self.jogosReg is a dict of dicts (a 2-D dict)
    one dim. to keep nDoConc, the other to keep jogoReg
    jogoReg also keeps nDoConc as an attribute

    Because of that, self.jogosReg might be reimplemented as a list of dict, but the way DoubleDBs had been implemented, it needs to look up nDoConc from the first dimension, ie, the dict's key

    Whatever the case, a refactoring may occur to make self.jogosReg a list of dicts, instead of a dict of dicts
    '''
    self.jogosReg = {}
    self.nOfInserted = 0
    if type(jogosBaseObj) == str:
      jogosBaseObj = CLClasses.Base(jogosBaseObj)
    self.initClassVariables(jogosBaseObj)
    self.initLogFile()

  def initClassVariables(self, jogosBaseObj):
    self.primeiraDezenaNoVolante = jogosBaseObj.primeiraDezenaNoVolante
    self.maiorDezenaNoVolante    = jogosBaseObj.getMaiorDezenaNoVolante()
    self.totalDeDezenasNoVolante = jogosBaseObj.totalDeDezenasNoVolante
    self.nDeDezenasSorteadas     = jogosBaseObj.nDeDezenasSorteadas
    self.htmlDataFilename    = jogosBaseObj.getFilename('htm')
    self.standard2LetterName = jogosBaseObj.standard2LetterName
    self.sqlTable            = self.standard2LetterName.lower()
    self.dbFields = DbFields(self.standard2LetterName)
    
  def initLogFile(self):
    today = datetime.date.today()
    logFilename = 'logs/HistoricoUpdater-%s-%s.log' %(self.sqlTable, today)
    self.logFile = open(logFilename, 'w')

  def goForCol(self, line):
    '''
    This method is outdated. The new version does a BeautifulSoup scraping to get History table's cells
    '''
    jogo = []; nDoConc = None; date = None; jogoReg = {}
    for i in range(self.dbFields.size()):
      pos = line.find('<td')
      if pos > -1:
        line = line[pos+4:]
        pos = line.find('</td')
        if pos > -1:
          trunk = line[:pos]
          if i == 0:
            try:
              nDoConc = int(trunk)
              jogoReg['nDoConc'] = nDoConc
            except ValueError:
              continue
          elif i == 1:
            try:
              #print 'date', trunk,
              date = fDates.transform_bar_ddmmyyyy_date_into_datetime(trunk)
              #print 'date', date
              jogoReg['date'] = date
            except ValueError:
              continue
            except TypeError, error:
              print 'TypeError trunk', trunk
              print TypeError
              sys.exit(0)
          elif i >= 2 and i <= 1 + self.nDeDezenasSorteadas:
            #print 'header', headerFields[i]
            try:
              dezena = int(trunk)
            except ValueError:
              continue
            if i==0:
              dezenaStr = str(dezena).zfill(3)
            else:
              if dezena < self.primeiraDezenaNoVolante or dezena > self.maiorDezenaNoVolante:
                errorLine = 'dezena=%d < %d or dezena > %d' %(dezena, self.primeiraDezenaNoVolante, self.maiorDezenaNoVolante)
                raise ValueError, errorLine
              dezenaStr = str(dezena).zfill(2)
              jogo.append(dezena)
            #print dezenaStr,
          elif i > 1 + self.nDeDezenasSorteadas and i < self.dbFields.size():
            fieldName = self.dbFields.field(i)
            # the below happens for some non-db fields, eg. rateio11, 12 and 13
            if len(fieldName) == 0:
              continue
            jogoReg[fieldName] = trunk
            # correct if boolean field 'foiAcumulado' was hit
            if fieldName.startswith('foiAcumulado'):
              if trunk.lower().startswith('sim'):
                jogoReg[fieldName] = 1
              else:
                jogoReg[fieldName] = 0
    # sortDezenas was discontinued
    #if self.sortDezenas:
      #jogo.sort()

    # consistency of nOfDezenas will be checked in the unpicking process
    if self.nDeDezenasSorteadas == len(jogo):
      jogoCharOrig = pprint.number_list_to_sticked_char(jogo)
      jogoReg['jogoCharOrig'] = jogoCharOrig
      if nDoConc >= 1:
        self.jogosReg[nDoConc] = dict(jogoReg)
        line = 'jogoReg: %s' %(jogoReg)
        self.logFile.write(line + '\n')

  def goForRow(self):
    pos = self.text.find('<tr')
    while pos > -1:
      self.text = self.text[pos+3:]
      pos = self.text.find('</tr')
      if pos > -1:
        line = self.text[:pos]
        #print 'line', line
        self.goForCol(line)
      pos = self.text.find('<tr')

  def goForTableTag(self):
    pos = self.text.find('<table')
    if pos > -1:
      self.text = self.text[pos+1:]
      self.goForRow()
  
  def readHtml(self, sortDezenas=False):
    '''
    The purpose of this method is to fill up self.jogosReg, 
      which is a dict of dicts (a 2-D dict)
    This dict works thus:
      jogosReg[nDoConc] = jogoReg
        jogoReg has the field-value pairs
    '''
    self.sortDezenas = sortDezenas
    self.text = open(self.htmlDataFilename).read()
    self.goForTableTag()

  def getJogos(self):
    jogos = []
    nDoConcList = self.jogosReg.keys()
    for nDoConc in nDoConcList:
      jogoReg = self.jogosReg[nDoConc]
      jogo = jogoReg['jogo']
      #jogo.sort()
      jogos.append(jogo)
    return jogos


  def correctDotAndCommaInDecimals(self):
    nDoConcs = self.jogosReg.keys()
    for nDoConc in nDoConcs:
      jogoReg = self.jogosReg[nDoConc]
      attrs = jogoReg.keys()
      for attr in attrs:
        value = jogoReg[attr]
        if type(value) <> str:
          continue
        if value.find('.') > -1:
          value = value.replace('.','') # strip off all dots
        if value.find(',') > -1:
          value = value.replace(',','.') # transform all commas to dots
        jogoReg[attr] = value


  def updateHistorico(self):
    self.readHtml()
    self.correctDotAndCommaInDecimals()
    doubleDBs = fSql.DoubleDBsDeltaInserts(self.sqlTable, self.jogosReg)
    doubleDBs.executeSqls()
    #self.nOfInserted = doubleDBs.getNOfInserts()
    self.nOfInserted = 0
    line = 'self.nOfInserted=%d' %(self.nOfInserted)
    print line
    self.logFile.write(line + '\n')


class DbFields(object):

  def __init__(self, standard2LetterName):
    standard2LetterName = standard2LetterName.upper()
    if standard2LetterName not in ['LF','MS']:
      errorMsg = 'should be either %s' %(['LF','MS'])
    self.standard2LetterName = standard2LetterName
    self.sqlTable = standard2LetterName.lower()
    self.dbFieldNames = props.getDbFieldsFor(self.sqlTable)

  def size(self):
    return len(self.dbFieldNames)

  def field(self, i):
    tam = self.size()
    if i >= tam:
      i = tam - 1
    return self.dbFieldNames[i]

  def fields(self):
    return self.dbFieldNames


def writeJogosToFile(jogos, txtDataFilename):
  tam = len(jogos)
  fileOut = open(txtDataFilename,'a')
  nOfConcurso = 0
  for jogo in jogos:
    line = pprint.number_list_to_str_commaless(jogo)
    nOfConcurso += 1
    print 'Writing conc.', nOfConcurso, '==>>', line
    line += '\n'
    fileOut.write(line)
  fileOut.close()

def produceTxtDataFileFromHtml(jogos, txtDataFilename):
  print 'Going to write', len(jogos), 'jogosfs'
  writeJogosToFile(jogos, txtDataFilename)

def getJogosFromTxt(txtDataFilename):
  lines = open(txtDataFilename).readlines()
  jogos = []
  for line in lines:
    jogo = tableops.getJogoFromLine(line)
    jogos.append(jogo)
  return jogos

def pickleJogosFromTxt(txtDataFilename, pickleFilename, nOfBits):
  jogos = getJogosFromTxt(txtDataFilename)
  pickleFile = open(pickleFilename,'w')
  binDecReprJogos = []
  for jogo in jogos:
    jogoLine = takeOut11.JogoLine(None,jogo)
    binDecReprJogo = jogoLine.getBinDecRepr(nOfBits)
    binDecReprJogos.append(binDecReprJogo)
  print 'Dumping', pickleFilename, '--', len(jogos), 'jogosfs'
  pickle.dump(binDecReprJogos, pickleFile)

def unpickleJogosDataFile(pickleFilename, nDeDezenasSorteadas, nOfBits):
  binDecReprJogos = pickle.load(open(pickleFilename))
  jogos = []
  for binDecReprJogo in binDecReprJogos:
    jogo = takeOut11.unpack_jogo_from_binary_dec_repr(binDecReprJogo, nDeDezenasSorteadas, nOfBits)
    jogos.append(jogo)
  #print jogosfs
  print 'unpickled', len(jogos), 'jogosfs'
  return jogos  

pickleFilename = 'lf-jogosfs-sorteados-pickle.obj'
def pickleAndUnpickle(txtDataFilename, pickleFilename):
  pickleJogosFromTxt()
  jogos = unpickleJogosFromTxt()

def checkTxtWithPickle(): #(txtDataFilename, pickleFilename):
  txtDataFilename = 'ms-jogosfs-sorteados.txt'
  pickleFilename =  'ms-jogosfs-sorteados.pickle.obj'
  jogos1 = getJogosFromTxt(txtDataFilename)
  print 'getJogosFromTxt(...) len', len(jogos1)
  jogos2 = unpickleJogosDataFile(pickleFilename, 6, 6)
  print 'unpickleJogosDataFile(...) len', len(jogos2)
  print 'assert(jogos1 == jogos2)'
  #assert(jogos1 == jogos2)
  for i in range(len(jogos1)):
    print jogos1[i], jogos2[i]

def testHistoricoUpdater():
  jogoTipo = 'LF'
  # base = CLClasses.Base(jogoTipo)
  hu = HistoricoUpdater(jogoTipo)
  hu.updateHistorico()
  jogoTipo = 'MS'
  hu = HistoricoUpdater(jogoTipo)
  hu.updateHistorico()

def doHistoricoUpdater(jogoTipo):
  hu = HistoricoUpdater(jogoTipo)
  hu.updateHistorico()


if __name__ == '__main__':
  '''
  updateJogosSorteadosDataFile()
  checkTxtWithPickle()
  testHistoricoUpdater()
  '''
  funcs.updateCaller('doHistoricoUpdater')
