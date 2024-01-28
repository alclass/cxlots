#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
  This module contains 'business' classes: Base, Jogo, Jogos and PartialJogos
'''
import sys
sys.path.insert(0, '..')
standardNames = ['LF','LM','MS']

# import syncSorteios as sync  CAN NOT happen here, because it instantiates Base
#   (and Base is not yet ready, because it's below),
#   so it is imported down below close to where it is needed, in getJogosObj(s2LN)


class Base(object):

  def __init__(self, standard2LetterName):
    # a module method, before here, checks for standardName consistency
    standard2LetterName = standard2LetterName.upper()
    if standard2LetterName not in standardNames:
      raise ValueError, 'Jogo must be either ' + str(standardNames)
    self.standard2LetterName = standard2LetterName
    self.sqlTable = self.standard2LetterName.lower()
    self.nDeCombs = None
    self.genericLgiComb = None
    self.initIt()

  def initIt(self):
    self.primeiraDezenaNoVolante = 1 # the only exception is LM which has 0 as first dezena
    # the next attribute is private, it should be obtain via a get-method
    self.nDeDezenasAMarcar = -1 # marker for the exception in LM which alows 50 dezenas to be chosen
    if self.standard2LetterName == 'LF': # for lotofácil
      self.name = 'Lotofácil'
      self.htmlJogosDataFilename = 'dados/d_lotfac.htm'
      self.nDeDezenasSorteadas     = 15
      self.totalDeDezenasNoVolante = 25
      self.nOfCols                 = 5
      self.nOfLins                 = 5
      self.greatestSum = sum(range(26-15, 26))
      self.leastSum = sum(range(1, 16))
      self.rateio13 = 12.5 # R$ 12.50 in October 2009
      self.rateio12 = 5.0
      self.rateio11 = 2.5
    elif self.standard2LetterName == 'LM': # for lotomania
      self.name = 'Lotomania'
      self.htmlJogosDataFilename = 'dados/d_lotman.htm'
      self.primeiraDezenaNoVolante = 0
      self.nDeDezenasAMarcar       = 50
      self.nDeDezenasSorteadas     = 20
      self.totalDeDezenasNoVolante = 100
      self.nOfCols                 = 10
      self.nOfLins                 = 10
      self.greatestSum = sum(range(101-50, 101))
      self.leastSum = sum(range(1, 51))
    elif self.standard2LetterName == 'MS': # for megasena
      self.name = 'Megasena'
      self.htmlJogosDataFilename = 'dados/d_mega.htm'
      self.nDeDezenasSorteadas     = 6
      self.totalDeDezenasNoVolante = 60
      self.nOfCols                 = 10
      self.nOfLins                 = 6
      self.greatestSum = sum(range(61-6, 61))
      self.leastSum = sum(range(1, 7))
      self.genericLgiComb = None
    self.intFromLowestJogo = None

  def getGenericLgiComb(self):
    if self.genericLgiComb == None:
      self.genericLgiComb = lc.LgiCombiner(self.totalDeDezenasNoVolante, self.nDeDezenasSorteadas)
    return self.genericLgiComb

  def getNOfBytesForPacker(self):
    nOfCombs = self.getNDeCombs()
    return binDec.get_n_of_bytes_for_packer(nOfCombs)

  def getNOfBits(self):
    return binDec.minNOfBits(self.totalDeDezenasNoVolante)

  def getMaiorDezenaNoVolante(self):
    if self.primeiraDezenaNoVolante == 0:
      return self.totalDeDezenasNoVolante - 1
    return self.totalDeDezenasNoVolante

  def getNDeDezenasAMarcar(self):
    if self.nDeDezenasAMarcar == -1:
      return self.nDeDezenasSorteadas
    return self.nDeDezenasAMarcar

  def getIntFromLowestJogo(self):
    '''
    Example for MS:
    1,2,3,4,5,6 will transform into:
    10203040506
    11,12,13,14,15,16 will transform into:
    111213141516
    And so on

    Important to notice:
    Convention was set to nDeDezenasSorteadas instead of getNDeDezenasAMarcar()

    This will be a problem only for lotomania
    In due time, one scheme will be needed for encoding jogosfs to generate
    Notice that lgi_b1idx's and binDecRepr's will 'suffer' of the same problem

    '''
    if self.intFromLowestJogo:
      return self.intFromLowestJogo
    de  = self.primeiraDezenaNoVolante
    ate = de + self.nDeDezenasSorteadas - 1
    dezenas = range(de, ate + 1)
    s = self.jogoListToStr(dezenas)
    if s[0] == '0':
      s = s[1:]
    self.intFromLowestJogo = int(s)
    return self.intFromLowestJogo

  def getFilename(self, ext):
    ext = ext.lower()
    filename = None
    if ext == 'html' or ext == 'htm':
      filename = self.htmlJogosDataFilename
    '''
    # txt and pickle.obj were discontinued

    elif ext == 'txt':
      filename = self.sqlTable + '-jogosfs-sorteados.txt'
    elif ext == 'obj':
      filename = self.sqlTable + '-jogosfs-sorteados.pickle.obj'
    '''
    return filename

  def updateHistoricoDosJogosSorteados(self):
    print 'updateHistoricoDosJogosSorteados(self)'
    huc.HistoricoUpdater(self)

  def getNDeCombs(self):
    if self.nDeCombs <> None:
      return self.nDeCombs
    if self.standard2LetterName == 'LM':
      # plug "business rule" in the future, ie, call a method to calculate probabilities such as those of lotomania
      self.nDeCombs = 11372635
      return self.nDeCombs
    self.nDeCombs = ic.iCmb(self.totalDeDezenasNoVolante, self.nDeDezenasSorteadas)
    return self.nDeCombs

  def __str__(self):
    outStr = '%s %s: %d a sortear, %d a escolher entre %d e %d (n. de combs.=%d)' \
    %( \
      self.standard2LetterName, \
      self.name, \
      self.nDeDezenasSorteadas, \
      self.getNDeDezenasAMarcar(), \
      self.primeiraDezenaNoVolante, \
      self.getMaiorDezenaNoVolante(), \
      self.getNDeCombs() \
    )
    return outStr

import funcsForBinDecRepr as binDec
import funcsForSql        as fSql
import HistoricoUpdater   as huc
import IndicesCombiner    as ic
import lambdas
import LgiCombiner        as lc 
import sqlAccessors       as sa
#import Stat   # must be import after Base
import Til                as tilc
from cardprint import pprint


class Jogo(Base):
  '''
  Class Jogo extends class Base
  An instance is obtained by either a jogo-list or a binDecRepr plus the standard2LetterName (for the parent-class)
  When binDecRepr is given, jogo-list is unpacked from it
  The jogo-list is validated against the following parent-class attributes:
    nDeDezenasSorteadas (list length must equal it)
    primeiraDezenaNoVolante (dezenas must not be lesser than it)
    maiorDezenaNoVolante/getMaiorDezenaNoVolante()  (dezenas must not be greater than it)

  Data transformation and encodings:
  jogo can be transformed into:
  1) a binDecRepr
  2) a lgi_b1idx
  3) an int from list minus intFromLowestJogo

  However, one issue remains to be decided
  This is the lotomania difference of the nDeDezenasSorteadas from nDeDezenasAMarcar
  ie, how to encode a jogo?  The aposta or the sorteio?

  '''

  def __init__(self, jogo, standard2LetterName):
    Base.__init__(self, standard2LetterName)
    self.lgi = None
    self.tilPatternDict = {}
    typ = type(jogo)
    if typ == list:
      self.validateJogo(jogo)
      self.setBinDecRepr()
    elif typ == int or typ == long:
      binDecRepr = jogo
      self.setJogoFromBinDecRepr(binDecRepr)
    elif typ == str:
      self.verifyJogoStr(jogo)
    else:
      errorMsg = 'Invalid jogo paramenter (=%s), it must be either a list or an int' %(str(jogo))
      raise ValueError, errorMsg

  def verifyJogoStr(self, jogoStr):
    '''
    jogo str is a stickerCharJogo string
    Eg.
    010203040506
    '''
    shouldBeSize = self.nDeDezenasSorteadas * 2
    if len(jogoStr) <> shouldBeSize:
      errorMsg = 'jogo %s should be a string of size %d' %(jogoStr, shouldBeSize)
      raise ValueError, errorMsg
    jogo = []
    for i in range(self.nDeDezenasSorteadas):
      de  = 2 * i
      ate = de + 2
      dezena = int(jogoStr[de:ate])
      jogo.append(dezena)
    self.validateJogo(jogo)

  def validateJogo(self, jogo):
    tam = len(jogo)
    if tam <> self.nDeDezenasSorteadas:
      errorMsg = 'len(jogo)=%d <> self.nDeDezenasSorteadas=%d s2Letter=%s' %(tam, self.nDeDezenasSorteadas, self.standard2LetterName)
      raise IndexError, errorMsg
    maiorDezenaNoVolante = self.getMaiorDezenaNoVolante()
    for dezena in jogo:
      if dezena < self.primeiraDezenaNoVolante:
        errorMsg = 'dezena=%d < self.primeiraDezenaNoVolante=%d jogo=%s' %(dezena, self.primeiraDezenaNoVolante, str(jogo))
        raise ValueError, errorMsg
      if dezena > maiorDezenaNoVolante:
        errorMsg = 'dezena=%d > maiorDezenaNoVolante=%d jogo=%s' %(dezena, maiorDezenaNoVolante, str(jogo))
        raise ValueError, errorMsg

    self.jogoAsEntered = list(jogo)
    self.jogo = list(jogo)
    self.jogo.sort()

  def setBinDecRepr(self):
    binDecRepr = binDec.packJogoToBinaryDecRepr(self.jogo, self.getNOfBits())
    # test in here
    jogo = binDec.unpackJogoFromBinaryDecRepr(binDecRepr, self.nDeDezenasSorteadas, self.getNOfBits())
    if jogo <> self.jogo:
      errorMsg = 'Inconsistency of jogo %s with self.jogo %s and its binDecRepr %d' %(str(jogo), str(self.jogo), binDecRepr)
      raise ValueError, errorMsg
    self.binDecRepr = binDecRepr

  def getBinDecRepr(self):
    if self.binDecRepr:
      return self.binDecRepr
    self.setBinDecRepr()
    if not self.binDecRepr:
      errorMsg = 'Could not get binDecRepr from self.jogo %s' %(str(self.jogo))
      raise ValueError, errorMsg
    return self.binDecRepr

  def jogoToAWholeInt(self):
    '''
    Example for Lotofácil
    nLower = 10203040506070809101112131415
    nUpper = 111213141516171819202122232425
    '''
    jogo = self.getJogo()
    wholeInt = pprint.number_list_to_a_whole_int(jogo)
    nInt = wholeInt - self.getIntFromLowestJogo()
    return nInt

  def setLgi(self):
    maiorAMenor = list(self.jogo)
    maiorAMenor.sort()
    maiorAMenor.reverse()
    maiorAMenor = map(lambdas.minus_one, maiorAMenor)
    #print 'maiorAMenor', maiorAMenor
    lgiObj = lc.LgiCombiner(self.getNDeCombs()-1,-1,maiorAMenor)
    lgi = lgiObj.get_lgi()
    #print 'lgi_b1idx', lgi_b1idx
    # test in here
    '''
    jogo = getJogoFromLgi(lgi_b1idx)
    if jogo <> self.jogo:
      errorMsg = 'Inconsistency of jogo %s with self.jogo %s and its lgi_b1idx %d' %(str(jogo), str(self.jogo), lgi_b1idx)
      raise ValueError, errorMsg
    '''
    self.lgi = lgi

  def getLgi(self):
    if self.lgi:
      return self.lgi
    self.setLgi()
    if not self.lgi:
      errorMsg = 'Could not get lgi_b1idx (the LexoGraphic Index) from self.jogo %s' %(str(self.jogo))
      raise ValueError, errorMsg
    return self.lgi

  def getTilPattern(self, tilN):
    if tilN in self.tilPatternDict.keys():
      return self.tilPatternDict[tilN]
    partialJogos = PartialJogos(self.standard2LetterName)
    partialJogos.addJogo(self.jogo)
    tilObj = tilc.Til(partialJogos, tilN)
    tilPattern = tilObj.generateLgiForJogoVsTilFaixas(self.jogo)
    self.tilPatternDict[tilN] = tilPattern
    return tilPattern



  def setJogoFromBinDecRepr(self, binDecRepr):
    jogo = takeOut11.unpackJogoFromBinaryDecRepr(binDecRepr, self.nDeDezenasSorteadas, self.nOfBits)
    self.validateJogo(jogo)
    # if an exception was not raised, okay, binDecRepr will also become an attribute
    self.binDecRepr = binDecRepr

  def updateHistoricoDosJogosSorteados(self):
    '''
    This is the only parent-class to be overridden so that a Jogo instance doesn't really call the code in the parent-class
    '''
    return

  def pprintCommaless(self):
    return pprint.number_list_to_str_commaless(self.jogo) # default zfill is 2

  def __str__(self):
    outStr = '%s %s' %(self.standard2LetterName, str(self.jogo))
    return outStr

unpickleCount = 0

def getBaseObj(standardName):
  '''
  The Base object is not buffered as the JogosObj object is
  So objects may be recreated (reinstantiated) at will
  '''
  if standardName not in standardNames:
    return None
  obj = Base(standardName)
  return obj

# now ok, Stat is need for Jogos
import Stat

class Jogos(Base):
  '''
  Class Jogos extends class Base
  An instance is obtained by a module method, imitating, so to say,
  a singleton
  That way, an instance is buffered in a module global dictionary called:
    getJogosObj(standard2LetterName, reinstantiate=False)
  '''

  def __init__(self, standard2LetterName):
    global instantiatedCount
    Base.__init__(self, standard2LetterName)
    self.jogos = []
    self.i = 0  # this is the nDoConc minus 1 pointer
    self.getJogosFromDB()
    self.histG = Stat.makeHistogram(self.jogos)
    self.initializeHistGOfHistG()

  def getJogosFromDB(self):
    jDict, jogosCharOrig = sa.getAttr('jogoCharOrig', self.sqlTable)
    # if inconsistent, an error will be raised
    fSql.checkConsistencyOfJogosCharOrigAgainstNDoConcs(self.sqlTable, jogosCharOrig)
    for jogoCharOrig in jogosCharOrig:
      jogo = []
      for i in range(self.nDeDezenasSorteadas):
        de  = i  * 2
        ate = de + 2
        dezenaStr = jogoCharOrig[de:ate]
        jogo.append(int(dezenaStr))
      self.jogos.append(jogo)
      
  '''
  def unpickelHistoricoDosJogosSorteados(self):
    filename = self.getFilename('obj')
    nOfBits = takeOut11.minNOfBits(self.totalDeDezenasNoVolante)
    self.jogosfs = du.unpickleJogosDataFile(filename, self.nDeDezenasSorteadas, nOfBits)

  def getTable(self):
    return self.table

  def getHeaderFields(self):
    return self.table[0]
  '''

  def getJogos(self):
    return self.jogos

  def size(self):
    return len(self.jogos)

  def getJogoObjI(self):
    jogoObj = Jogo(self.jogos[self.i], self.standard2LetterName)
    return jogoObj

  def getNDoConc(self):
    return self.i + 1

  def moveTo(self, nDoConc, returnJO=True):
    '''
    JO means JogoObj
    '''
    i = nDoConc - 1
    if i < 0:
      # necessary to work with while
      return None
    tam = len(self.jogos)
    if i >= tam:
      # necessary to work with while
      return None
    # i is inside the range (0 , tam - 1)
    self.i = i
    if returnJO:
      return self.getJogoObjI()
    return self.jogos[self.i]

  def first(self, returnJO=True):
    nDoConc = 1
    return self.moveTo(nDoConc)

  def last(self, returnJO=True):
    nDoConc = len(self.jogos)
    return self.moveTo(nDoConc, returnJO)

  def next(self, returnJO=True):
    nDoConc = self.i + 1 + 1
    return self.moveTo(nDoConc, returnJO)
    
  def previous(self, returnJO=True):
    nDoConc = self.i - 1 + 1
    return self.moveTo(nDoConc, returnJO)

  def getNDoUltimoConcurso(self):
    return len(self.jogos)

  def getJogosAteConcurso(self, ateNumero=-1):
    if self.jogos == None:
      return None
    if ateNumero < -1:
    # well, this should never happen, raise an exception
      raise IndexError, 'ateNumero is less than -1, this means an error exists in the system. Program cannot continue.'
    if ateNumero == -1 or ateNumero > len(self.jogos):
      # if ateNumero is not given, default to all jogosfs
      # if ateNumero is greater than total, do the same, default to all jogosfs
      return self.jogos
    return self.jogos[:ateNumero]

  def getHistG(self):
    return self.histG

  def getHistGOfHistG(self):
    return self.histGOfHistG

  def initializeHistGOfHistG(self):
    '''
    The Histogram tells the quantity each dezena appeared
     The Histogram of Histogram tells the quantity of equal quantities
    '''
    self.histGOfHistG = {} # originally: occurDict
    occurences = self.histG.values()
    for occurrence in occurences:
      try:
        self.histGOfHistG[occurrence]+=1
      except KeyError:
        self.histGOfHistG[occurrence]=1

  def getSubtableAteConcursoNumero(self, ateNumero=-1):
    '''
    This method will be deprecated because table data will, in the future,
    come from a sql table
    '''
    # table has one row more than jogosfs
    if ateNumero == -1 or ateNumero > len(self.table) + 1:
      return self.table
    return self.table[:ateNumero+1]

  jogosLgisTilFaixaDict = {}

  def postInitLgiForJogosVsTilFaixas(self, til=5):
    '''
    The prefix 'post' in the method's name is due to
    the fact that __init__() does not initialize it right away

    In the jargon, it's a lazy initialization
    '''
    tilObj = tilc.Til(til); lgis = []
    for jogo in self.jogos:
      lgi = tilObj.generateLgiForJogoVsTilFaixas(jogo)
      #print 'lgi_b1idx', lgi_b1idx,
      lgis.append(lgi)
    #print
    self.jogosLgisTilFaixaDict[til] = lgis
      
  def getJogosLgisForATilFaixa(self, til=5):
    #print 'til', til
    if til in self.jogosLgisTilFaixaDict.keys():
      return self.jogosLgisTilFaixaDict[til]
    self.postInitLgiForJogosVsTilFaixas(til)
    lgis = self.jogosLgisTilFaixaDict[til]
    if not lgis:
      raise ValueError, 'problem: jogosLgisTilFaixaDict[til] was not computed'
    return lgis

  def getJogoLgisForATilFaixa(self, concurso, til=5):
    lgis = self.getJogosLgisForATilFaixa(til)
    lgi = lgis[concurso-1]
    return lgi

  def getHistGJogosLgisForATilFaixa(self, til=5):
    lgis = self.getJogosLgisForATilFaixa(til)
    # histGJogosLgisForATilFaixa is not kept in the class object, as jogosLgisTilFaixaDict is
    histGJogosLgisForATilFaixa = {}
    for lgi in lgis:
      try:
        histGJogosLgisForATilFaixa[lgi]+=1
      except KeyError:
        histGJogosLgisForATilFaixa[lgi]=1
    return histGJogosLgisForATilFaixa

  def getAttrException(self, attr):
    # only LF has those below
    if self.standard2LetterName == 'LF' and attr.startswith('rateio'):
      if attr == 'rateio13':
        return self.rateio13 # R$ 12.50 in October 2009
      if attr == 'rateio12':
        return self.rateio12 # R$ 5.00 in October 2009
      if attr == 'rateio11':
        return self.rateio11 # R$ 2.50 in October 2009
    return None

  def getAttrFor(self, attr, nDoConc=-1):
    # first, see it's attr is an exception (ie, not in db)
    value = self.getAttrException(attr)
    if value <> None:
      return value
    tam = self.size()
    if nDoConc < 0: # == -1 (default) included!
      nDoConc = self.i + 1
    elif nDoConc > tam: 
      nDoConc = tam
    value = sa.getAttrFor(attr, self.sqlTable, nDoConc)
    return value


import SyncSorteios as sync
jogosObjDict = {}
def getJogosObj(standard2LetterName, reinstantiate=False):
  '''
  This method is a substitution for the Singleton 
  that was not implemented directly in the class Jogos
  In Python, it seems to be easier to device a Singleton as a module method
  '''
  global jogosObjDict
  if not reinstantiate:
    if standard2LetterName in jogosObjDict.keys():
      return jogosObjDict[standard2LetterName]
  print '  [INSTANTIATING] jogosObj', standard2LetterName
  obj = Jogos(standard2LetterName)
  if not obj:
    errorMsg =  'could not instantiate jogosObj with standard2LetterName = %s' %(standard2LetterName)
    raise ValueError, errorMsg
  jogosObjDict[standard2LetterName] = obj
  dataSync = sync.SyncSorteios(standard2LetterName)
  print "  [SYNC'ING] nOfInserted", 
  dataSync.sync()
  print dataSync.nOfInserted
  return jogosObjDict[standard2LetterName]


class PartialJogos(Base):
  '''
  Class PartialJogos
  Here it happens a mix of
    inheritance (from Base) and a
    composition with JogosObj

  In Java, what we would do is just a "cast" ie,
    partialJogos = (PartialJogos) jogosObj

  As our knowledge of Python grows, we'll refactor this class into
    a somewhat better design (for the time being, this is "awkward"/awful

  *** This class to be IMPROVED!!!

  '''
  def __init__(self, standard2LetterName):
    Base.__init__(self, standard2LetterName)
    self.jogosObj = getJogosObj(standard2LetterName)
    self.ateConcurso = -1

  def setAteConcurso(self, ateConcurso=-1):
    self.ateConcurso = ateConcurso
    self.workJogos   = self.jogosObj.getJogosAteConcurso(ateConcurso)
    self.histG       = Stat.makeHistogram(self.workJogos)
    self.ateConcurso = len(self.workJogos)

  def size(self):
    return len(self.workJogos)

  def addJogo(self, jogo):
    if self.ateConcurso == -1:
      self.setAteConcurso()
    self.workJogos.append(jogo)
    self.histG       = Stat.makeHistogram(self.workJogos)
    self.ateConcurso += 1

  def getJogos(self):
    if self.ateConcurso == -1:
      self.setAteConcurso()
    return self.workJogos

  def getHistG(self):
    if self.ateConcurso == -1:
      self.setAteConcurso()
    return self.histG

  '''
  def continueTheSequenceBy(table, newTable, amount=1):
    lastJogoN = len(newTable)-1
    for i in range(lastJogoN, lastJogoN + amount):
      newTable.append(table[i])
    return newTable

  def continueJogosSequenceBy(self, amount=1):
    newAteConcurso = self.ateConcurso + amount
    lastHistoryConcurso = self.jogosObj.getLastConcurso()
    if newAteConcurso > lastHistoryConcurso:
      self.ateConcurso = lastHistoryConcurso
      self.workJogos = self.jogosObj.getJogos()
      self.histG =  self.jogosObj.getHistG()
      return self.workJogos
    for i in range(self.ateConcurso + 1, newAteConcurso + 1):
      jogo = self.jogosfs[i]
      self.workJogos.append(jogo)
      self.histG =  incrementalHistogram(self.histG, jogo)
    return self.workJogos
  '''

class JogoLine(object):

  def __init__(self, line=None, jogo=None, binDecReprJogo=None):
    self.jogo = None
    self.line = None
    if line:
      self.line = line
      self.jogo = pprint.convertLineToJogo(line)
    elif jogo:
      self.jogo = jogo
    elif binDecReprJogo:
      self.setJogoFromBinDecRepr(binDecReprJogo)
    # by now, jogo should already have been initialized
      if not self.checkJogo():
        self = None

  def checkJogo(self):
    if not self.jogo:
      #raise ValueError, 'Jogo not initialized'
      return False
    if len(self.jogo) == 0:
      #raise IndexError, 'Jogo has no dezenas'
      return False
    for dezena in self.jogo:
      # lotomania has 100 dezenas, that's the largest
      if dezena < 1 or dezena > 100:
        #raise ValueError, 'dezena < 1 or dezena > 100'
        return False
    return True

  def getBinDecRepr(self, nOfBits):
    return packJogoToBinaryDecRepr(self.jogo, nOfBits)

  def setJogoFromBinDecRepr(self, binDecRepr):
    # nDeDezenasSorteadas, nOfBits
    self.jogo = unpackJogoFromBinaryDecRepr(binDecRepr)

  def getJogo(self):
    return self.jogo

  def getLine(self):
    return pprint.jogoListToStr(self.jogo)

  def getLineOrig(self):
    return self.line



def incrementalHistogram(histG, jogo):
  for dezena in jogo:
    try:
      histG[dezena]+=1
    except KeyError:
      histG[dezena]=1
  return histG

def updateBase(standard2LetterName):
  base = getBaseObj(standard2LetterName)
  print 'base.updateHistoricoDosJogosSorteados(%s)' %(standard2LetterName)
  base.updateHistoricoDosJogosSorteados()


def updateIt():
  arg = sys.argv[1]
  if arg == '-u':
    arg = sys.argv[2]
    std2letter = arg.upper()
    if std2letter in ['LF', 'LM', 'MS']:
      updateBase(std2letter)

def testGetJogosObj():
  jo = getJogosObj('ms')
  print 'jo', jo
  jo = getJogosObj('lf')
  print 'jo', jo


if __name__ == '__main__':
  '''
  Argument -u means 'update'
  '''
  if len(sys.argv) > 1:
    updateIt()
  testGetJogosObj()
