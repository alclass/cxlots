#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import numpy
import random
import sys


JOGOSOBJ_STREAM = 1
FILE_STREAM     = 2
import analyzer
import CLClasses
from cardprint import pprint

class Filter(object):

  def __init__(self, stream, standard2LetterName=None):
    if type(stream) == CLClasses.Jogos:
      self.jogosObj = stream
      self.streamType = JOGOSOBJ_STREAM
      dateNow = datetime.date.today()
      # in the case stream is JogosObj, the s2LN passed in is ignored
      self.standard2LetterName = stream.standard2LetterName
      apostasFilename = '%s-%s-apostas.txt' %(dateNow, standard2LetterName)
    elif type(stream) == str:
      apostasFilename  = stream
      self.standard2LetterName = findStandard2LetterNameInFilename(apostasFilename)
      self.apostasFile = open(apostasFilename)
      self.streamType  = FILE_STREAM
      self.jogosObj = CLClasses.getJogosObj(self.standard2LetterName)
    else:
      errorMsg = 'Filter should receive either a JOGOSOBJ_STREAM or a FILE_STREAM stream=%s' %(stream)
      raise ValueError, errorMsg
    self.jogoObj = None
    self.c = 0
    self.controller = getController(self.jogosObj)
    self.initOutFile(apostasFilename)

  def initOutFile(self, apostasFilename):
    number = 1
    if apostasFilename.find('.') > -1:
      try:
        lastPart = apostasFilename.split('.')[-1]
        number = int(lastPart)
      except ValueError:
        pass
    nextApostasFilename = '%s.%d' %(apostasFilename, number)
    self.nextApostasFile = open(nextApostasFilename, 'w')

  def filterOut(self):
    self.c += 1
    if self.c % 10000 == 0:
      print self.c,
    tam = len(self.controller.filters)
    for i in range(tam):
      if self.controller.filters[i]:
        retVal = self.controller.filterOut(self.jogoObj, i)
        if retVal:
          outLine = self.jogoObj.pprint.numberListToStickedChar() # zfill=2
          outLine +=  '\n'
          self.nextApostasFile.write(outLine)
    
  def next(self):
    if self.streamType == FILE_STREAM:
      stickedLine = self.apostasFile.readline()
      if stickedLine:
        jObj = CLClasses.JogoObj(stickedLine)
        if jObj == None:
          return None
        self.jogoObj = jObj
      else:
        return None
    else:  #JOGOSOBJ_STREAM
      jObj = self.jogosObj.next()
      if jObj == None:
        return None
      self.jogoObj = jObj
    return self.filter()

  def runThru(self):
    r = self.next()
    while r:
      r = self.next()


def seeConsecutives():
  jogoTipo='ms'
  attr = 'consecEnc'
  cDict, cList = sa.getAttr(attr, jogoTipo)
  jogosObj = CLClasses.getJogosObj(jogoTipo)
  jogoObj = jogosObj.first(); i=0
  while jogoObj:
    nDoConc = jogosObj.getNDoConc()
    print nDoConc, jogoObj.pprintCommaless(), cList[i]
    jogoObj = jogosObj.next(); i+=1
  pprint.printDict(cDict)
  '''
1 0 644
2 1 390
3 2 44
4 12 33
5 13 1
6 123 2
  '''



def hasMoreThanNCoincs(jogo, jogoNext, nOfCoincs=11):
  coinc = 0
  for dezena in jogo:
    if dezena in jogoNext:
      coinc+=1
  if coinc > nOfCoincs:
    printJogo(jogoNext)
    print 'coinc', coinc
    return True
  return False

def filterOutNCoincs(jogos, nOfCoincs=11, ruleCod=None):
  if len(jogos)==0:
    return 0
  filteredOut = 0
  newJogos = [jogos[0]]
  for i in range(len(jogos)-1):
    jogo = jogos[i]
    jogoNext = jogos[i+1]
    if hasMoreThanNCoincs(jogo, jogoNext, nOfCoincs):
      filteredOut+=1
      continue
    newJogos.append(list(jogoNext))
  return newJogos #filteredOut

def filter11OutImpl2(binDecReprJogosDict):
  '''
  Enter dict
  Goes out list
  '''
  binDecReprJogos = binDecReprJogosDict.keys()
  print 'start sort binDecReprJogos', time.ctime()
  #binDecReprJogos.sort()
  print 'finish sort binDecReprJogos', time.ctime()
  nOfExcluded = 0; i=0
  for i in range(len(binDecReprJogos)-1):
    binDecReprJogoI = binDecReprJogos[i]
    if binDecReprJogosDict[binDecReprJogoI] == 0:
      continue
    jogoLineI = JogoLine(None,None,binDecReprJogoI)
    for j in range(i+1, len(binDecReprJogos)):
      binDecReprJogoJ = binDecReprJogos[j]
      if binDecReprJogosDict[binDecReprJogoJ] == 0:
        continue
      jogoLineJ = JogoLine(None,None,binDecReprJogoJ)
      r = has11OrMoreCoincs(jogoLineI.jogo, jogoLineJ.jogo)
      if r:
        binDecReprJogosDict[binDecReprJogoJ] = 0
        nOfExcluded+=1
        if nOfExcluded % 10000 == 0:
          print nOfExcluded,
      else:
        pass
        #print 1,
    if i % 10000 == 0:
      print i, time.ctime()
  print 'nOfExcluded', nOfExcluded
  outBinDecReprJogos = []
  for binDecReprJogo in binDecReprJogos:
    if binDecReprJogosDict[binDecReprJogo] == 1:
      outBinDecReprJogos.append(binDecReprJogo)
  #del binDecReprJogosDict
  newJogosBetSize = len(outBinDecReprJogos)
  print 'size of remaining', newJogosBetSize
  return outBinDecReprJogos

def generateRandomJogo():
  nOfDezenas = 15
  jogo = []
  while len(jogo) < nOfDezenas:
    dezena = random.randint(1,25)
    if dezena in jogo:
      continue
    jogo.append(dezena)
  jogo.sort()
  #print 'Random', jogo
  printJogo(jogo)
  return jogo

def generateRandomJogos(nOfJogosToGen=3):
  if nOfJogosToGen < 1:
    return []
  jogos = []
  for i in range(nOfJogosToGen):
    jogo = generateRandomJogo()
    jogos.append(jogo)
  return jogos

jogosInHistory = ra.getHistoryJogos()
def filterOutAgainstHistoryWithNCoincs(jogoToCheck, nOfCoincsIn=15):
  for jogoIndex in range(len(jogosInHistory)):
    jogo = jogosInHistory[jogoIndex]
    nOfCoincs=0
    for dezena in jogoToCheck:
      if dezena in jogo:
        nOfCoincs+=1
    if nOfCoincs >= nOfCoincsIn:
      return True, jogoIndex
  return False, -1

'''
 >>> filtros:
1 n de pares
2 soma desce ou sobe (se um ou outro, sai)
3 desvio padrão entre x e y
4 variacaoLinCol (ocorrência de linhas e colunas, previously named variacaoD1D2)
5 variacaoNDeIguaisJogoAntENDeJogosParaIguaisQuant
6 histograma evolutivo
7 sixtils
 
 >>> filtros com padrões incluintes
7 Repeats
se 1 ou n números devem repetir, excluir jogo quando a(s) repeat(s) não ocorrer(em)
 (estendendo) impedir, em alguns casos, mais que 1 repeat
 (estendendo)  quais poderiam repetir?
8 Consecutivos
'''
#FILT-BEGIN*** DO NOT CHANGE THIS LINE, AN EXTERNAL METHOD WILL READ THIS FILE FROM HERE 


FILT_PARIMPAR = 10
FILT_PARIMPAR_EXCL_LIST = 11
FILT_PARIMPAR_DIVERGE_DEPTH_PATTERN = 12
FILT_PARPARIMPARIMPAR_PATTERN_NOT_OCCURRED = 13
FILT_PATTERNPI_HAS_MAX_OCCURS = 14

FILT_REMAINDER3_PATTERN_NOT_OCCURRED = 15
FILT_PATTERN3_HAS_MAX_OCCURS = 16

FILT_REMAINDER5_PATTERN_NOT_OCCURRED = 17
FILT_PATTERN5_HAS_MAX_OCCURS = 18
FILT_5_OCCURS_OF_ONE_REMAINDER5 = 19

FILT_SOMA_OU_STD = 20
FILT_SOMA_MENOR_Q_MIN = 211
FILT_SOMA_MAIOR_Q_MAX  = 212
FILT_SOMADESCE_MAIOR_Q_MAXDESCE = 213
FILT_SOMASOBE_MAIOR_Q_MAXSOBE = 214
FILT_SOMAREPETIU_MAIOR_Q_1 = 215
FILT_SOMADIF_C_LASTJOGO_MENOR_Q_MIN = 216
FILT_SOMADIF_C_LASTJOGO_MAIOR_Q_MAX = 217

FILT_APOSTASE_Q_SOMA_DEVE_SUBIR = 221
FILT_APOSTASE_Q_SOMA_DEVE_DESCER = 222
FILT_APOSTASE_SOMA_ACIMA_DO_DECIL_MIN = 223 
FILT_APOSTASE_SOMA_ACIMA_DO_DECIL_MAX = 224

FILT_STD_MENOR_Q_MIN  = 231
FILT_STD_MAIOR_Q_MAX = 232
FILT_STDDESCE_MAIOR_Q_MAXDESCE = 233
FILT_STDSOBE_MAIOR_Q_MAXSOBE = 234
FILT_STDREPETIU_MAIOR_Q_1 = 235
FILT_STDDIF_C_LASTJOGO_MENOR_Q_MIN = 236
FILT_STDDIF_C_LASTJOGO_MAIOR_Q_MAX = 237

FILT_SIXTILE_OK  = 30
FILT_SIXTILPATTERN_IN_FORBIDDEN_LIST = 31
FILT_SIXTILPATTERN_EQUALS_THAT_OF_LASTJOGO = 32 # for patterns with quant=1 or those that can't have this condition after looking up Controller
FILT_SIXTILPATTERN_EQUALS_ONE_BACKWARDS = 33
FILT_SIXTILPATTERN_NOT_YET_OCCURRED = 34
FILT_SIXTILPATTERN_OCCURS_MENOS_Q_MIN_SUCH = 35
FILT_SIXTILPATTERN_OCCURS_MAIS_Q_MAX_SUCH = 36

FILT_HISTG_EVOL  = 40
FILT_HISTG_EXCL_N_DEZS_MAIS_FREQ = 41
FILT_HISTG_EXCL_DEZN_N_MAIS_FREQ_COMBD_M_LASTJOGOS = 42
FILT_HISTG_EXCL_HAVER_X_N_DEZS_MAIS_FREQ_COMBD_M_LASTJOGOS = 43

FILT_REPEATS = 50
FILT_ULTRAPASSA_MAX_REPEATS_PER_JOGO_IN_N_JOGOS = 51
FILT_REPEAT_MENOR_Q_MIN_PER_JOGO_IN_N_JOGOS = 52
FILT_REPEAT_MAIOR_Q_MAX_ALLOWED_OCCURRED = 53
FILT_REPEAT_MENOR_Q_MIN_IMPOSED_OCCURRED = 54
FILT_ULTRAPASSA_QUANT_OF_JOGOS_WITH_MAX_REPEAT = 55
FILT_REPEAT_COM_DEZENA_DO_JOGOREF = 56

FILT_CONSECUTIVO = 60
FILT_CONSECUTIVO_EXTRAPOLA_AS_PATTERN = 61
FILT_CONSEC_COINCIDES_WITH_LASTJOGOS = 62
FILT_NOSE_MAIS_Q_MAX = 63
FILT_NESO_MAIS_Q_MAX = 64
FILT_N_OF_PRIMES_MAIS_Q_MAX = 65

FILT_LINHA = 70
FILT_LINHA_IGUAL_ULTIMO_JOGO = 71
#FILT_ALGUMALINHA_MAIOR_Q_MAX_ESTIMADO = 71
FILT_LINHAPATTERN_NEVER_OCCURRED = 72   # D1 pattern is sixtil-like, D2 is a tentil-like (not implemented yet)
FILT_LINHAPATTERN_IGUALA_MAX_OCCUR = 73
FILT_LINHA_N_NAO_PRESENTE_QUANDO_LIKELY = 74
FILT_LINHA_EXCLUIDA = 75
FILT_LINHA_FORA_DA_TENDENCIA_DE_BALANCA = 76   # balança é a média ponderada (ou prod. escalar) com [-3 -2 -1 +1 +2 +3]
FILT_LINHA_STD_FORA_DA_TENDENCIA = 77 # ex. muito esparso quando deveria estar mais centrado ou vice-versa
FILT_FLATNESS_LINCOL_FORA_DO_ESTIMADO = 79  # flatness fornece o grau de achatamento da "curva lincol"

FILT_COLUNA = 80
FILT_COLUNA_IGUAL_ULTIMO_JOGO = 81
#FILT_ALGUMACOLUNA_MAIOR_Q_MAX_ESTIMADO = 81
FILT_COLUNAPATTERN_NEVER_OCCURRED = 82  # not used for the time being
FILT_COLUNAPATTERN_IGUALA_MAX_OCCUR = 83
FILT_COLUNA_N_NAO_PRESENTE_QUANDO_LIKELY = 84
FILT_COLUNA_EXCLUIDA = 85
FILT_COLUNA_FORA_DA_TENDENCIA_DE_BALANCA = 86
FILT_COLUNA_STD_FUZZY_PATTORA_DA_TENDENCIA = 87
FILT_FUZZYNESS_LINCOL_FORA_DO_ESTIMADO = 89  # fuzzyness aqui é o Desvio Padrão em 2D

#FILT-END*** DO NOT CHANGE THIS LINE, AN EXTERNAL METHOD WILL READ THIS FILE UP TO HERE 

filterReturnCodesMsgDict = {}
def makeMessagesFromFilterReturnCode():
  global filterReturnCodesMsgDict
  text = open('filters.py').read()  # read itself, ie the py module file that this is
  pos = text.find('#FILT-BEGIN***')
  if pos < 0:
    return None
  posIni = pos
  pos = text.find('#FILT-END***')
  if pos < 0:
    return None
  posFim = pos
  if posFim <= posIni:
    return None
  #print 'makeMessagesFromFilterReturnCode() read filters.py    pos =', posIni, posFim
  trunk = text[posIni:posFim]
  lines = trunk.split('\n')
  for line in lines:
    posComment = line.find('#') 
    if posComment == 0:
      continue
    if posComment > 0:
      line = line[:posComment] 
    if line.find('=') > -1:
      pp = line.split('=')
      phrase = pp[-1]
      posHash = phrase.find('#')
      if posHash > -1:
        phrase = phrase[:posHash-1]
      msgNumber = int(phrase)
      msgName = pp[-2].lstrip().strip()
      filterReturnCodesMsgDict[msgNumber] = msgName

def initMessageStrFromFilterReturnNumberCode():
  if len(filterReturnCodesMsgDict) == 0:
    makeMessagesFromFilterReturnCode()
  if len(filterReturnCodesMsgDict) == 0:
    # oops, some problem happened
    msg = '# oops, some problem happened, makeMessagesFromFilterReturnCode() was not able to read the filter code messages'
    raise KeyError, msg
  return

def getMessageStrFromFilterReturnNumberCode(numberCode):
  initMessageStrFromFilterReturnNumberCode()
  if numberCode in filterReturnCodesMsgDict.keys():
    return filterReturnCodesMsgDict[numberCode]
  return None

def joinMessageStrWithFilterReturnNumberCodes(codes):
  out2TupleList = []
  for code in codes:
    msg = getMessageStrFromFilterReturnNumberCode(code)
    out2TupleList.append((code, msg))
  return out2TupleList

def printAllMessagesFromFilterReturnNumberCode():
  initMessageStrFromFilterReturnNumberCode()
  numberCodes = filterReturnCodesMsgDict.keys()
  numberCodes.sort()
  for numberCode in numberCodes:
    msg = filterReturnCodesMsgDict[numberCode]
    print numberCode, msg

#@1,filtro
def filtroParImpar(jogo):
  '''
  This is the filter for par/ímpar.

FILT_PARIMPAR = 10
FILT_PARIMPAR_EXCL_LIST = 11
FILT_PARIMPAR_DIVERGE_DEPTH_PATTERN = 12
FILT_PARPARIMPARIMPAR_PATTERN_NOT_OCCURRED = 13
FILT_PATTERNPI_HAS_MAX_OCCURS = 14

FILT_REMAINDER3_PATTERN_NOT_OCCURRED = 15
FILT_PATTERN3_HAS_MAX_OCCURS = 16

FILT_REMAINDER5_PATTERN_NOT_OCCURRED = 17
FILT_PATTERN5_HAS_MAX_OCCURS = 18
FILT_5_OCCURS_OF_ONE_REMAINDER5 = 19
  
  Not implemented yet: FILT_PARIMPAR_IN_PATT = 12; FILT_PARIMPAR_OUTSIDE_DIF_EXPECTED_RELAT_LASTJOGO = 13
  '''
  piObj = analyzer.parImparPatternObj()
  excludeList = [0,6]
  nDePares = jogo.getNDePares()
  if nDePares in excludeList:
    return False, FILT_PARIMPAR_EXCL_LIST
  rem3Dict = {0:0, 1:0, 2:0}
  dezenas = jogo.getDezenas()
  for d in dezenas:
    rem3 = d % 3
    rem3Dict[rem3]+=1
  rem3Str = '' 
  for i in range(3):
    rem3Str += str(rem3Dict[i])
  if rem3Str in piObj.sobrando3:
    return False, FILT_REMAINDER3_PATTERN_NOT_OCCURRED
  if piObj.equalsMaxP3Occurs(rem3Str):
    return False, FILT_PATTERN3_HAS_MAX_OCCURS  
  rem5Dict = {0:0, 1:0, 2:0, 3:0, 4:0}
  for d in dezenas:
    rem5 = d % 5
    rem5Dict[rem5]+=1
  rem5Str = ''
  for i in range(5):
    rem5Str += str(rem5Dict[i])
  if '5' in rem5Str:
    return False, FILT_5_OCCURS_OF_ONE_REMAINDER5
  if rem5Str in piObj.sobrando5:
    return False, FILT_REMAINDER5_PATTERN_NOT_OCCURRED
  if piObj.equalsMaxP5Occurs(rem5Str):
    return False, FILT_PATTERN5_HAS_MAX_OCCURS  

  nDeParPar = 0; nDeImparImpar = 0
  for d in dezenas:
    leftDigit = d / 10
    if d % 2 == 0:
      if leftDigit % 2 == 0:
        nDeParPar += 1   
    else:
      if leftDigit % 2 == 1:
        nDeImparImpar += 1   
  #print 'nDePares, nDeParPar, nDeImparImpar', nDePares, nDeParPar, nDeImparImpar
  pattPI = '%d%d%d' %(nDePares, nDeParPar, nDeImparImpar)
  if pattPI in piObj.sobrandoPI:
    return False, FILT_PARPARIMPARIMPAR_PATTERN_NOT_OCCURRED

  if piObj.equalsMaxP3Occurs(pattPI):
    return False, FILT_PATTERNPI_HAS_MAX_OCCURS  

  answer = piObj.lookUpDivergePattern(jogo)
  if not answer:
    return False, FILT_PARIMPAR_DIVERGE_DEPTH_PATTERN
  
  return True, FILT_PARIMPAR

#@2,filtro
def filtroSomaEtAl(jogo, nDoJogoToCompare=Sena.getNOfLastJogo()):
  '''
  This is the filter for either "Soma" ou "Desvio Padrão".

FILT_SOMA_OU_STD = 20
FILT_SOMA_MENOR_Q_MIN = 211
FILT_SOMA_MAIOR_Q_MAX  = 212
FILT_SOMADESCE_MAIOR_Q_MAXDESCE = 213
FILT_SOMASOBE_MAIOR_Q_MAXSOBE = 214
FILT_SOMAREPETIU_MAIOR_Q_1 = 215
FILT_SOMADIF_C_LASTJOGO_MENOR_Q_MIN = 216
FILT_SOMADIF_C_LASTJOGO_MAIOR_Q_MAX = 217

FILT_APOSTASE_Q_SOMA_DEVE_SUBIR = 221
FILT_APOSTASE_Q_SOMA_DEVE_DESCER = 222
FILT_APOSTASE_SOMA_ACIMA_DO_DECIL_MIN = 223 
FILT_APOSTASE_SOMA_ACIMA_DO_DECIL_MAX = 224

FILT_STD_MENOR_Q_MIN  = 231
FILT_STD_MAIOR_Q_MAX = 232
FILT_STDDESCE_MAIOR_Q_MAXDESCE = 233
FILT_STDSOBE_MAIOR_Q_MAXSOBE = 234
FILT_STDREPETIU_MAIOR_Q_1 = 235
FILT_STDDIF_C_LASTJOGO_MENOR_Q_MIN = 236
FILT_STDDIF_C_LASTJOGO_MAIOR_Q_MAX = 237
  
  '''
  soma = jogo.soma()
    
  # filter Soma Min
  contr = analyzer.Controller()
  somaStats = contr.getSomaStats()
  if soma < somaStats.min:
    return False, FILT_SOMA_MENOR_Q_MIN
    
  # filter Soma Max
  if soma > somaStats.max:
    return False, FILT_SOMA_MAIOR_Q_MAX

  # filter Soma Dif
  backwardJogo = Sena.jogosPool.getJogo(nDoJogoToCompare)
  somaBackward = backwardJogo.soma()
  somaDif = soma - somaBackward
  if somaDif < somaStats.difMin:
    return False, FILT_SOMADIF_C_LASTJOGO_MENOR_Q_MIN
  if somaDif > somaStats.difMax:
    return False, FILT_SOMADIF_C_LASTJOGO_MAIOR_Q_MAX

  dezPorCentoMinMax = (somaStats.max - somaStats.min) / 10
  if somaBackward < somaStats.min + dezPorCentoMinMax:
    if soma <  somaStats.min + dezPorCentoMinMax:
      return False, FILT_APOSTASE_SOMA_ACIMA_DO_DECIL_MIN
    elif soma < somaBackward:
      return False, FILT_APOSTASE_Q_SOMA_DEVE_SUBIR

  if somaBackward > somaStats.max - dezPorCentoMinMax:
    if soma >  somaStats.max - dezPorCentoMinMax:
      return False, FILT_APOSTASE_SOMA_ACIMA_DO_DECIL_MAX
    elif soma > somaBackward:
      return False, FILT_APOSTASE_Q_SOMA_DEVE_DESCER
 

  # filter Soma Sobe e Desce Absoluta
  # look up if it's climbing or descending
  currentMaxDesce = somaStats.maxDesce
  currentMaxDSobe = somaStats.maxSobe
  goBackwardsNJogos = max(currentMaxDesce, currentMaxDSobe) * 2
  somaAcima = soma; subindo = None; descendo=None; quantoSubiu = 0; quantoDesceu = 0; somaRepetiu = 0; c = 0
  for i in range(nDoJogoToCompare, nDoJogoToCompare - goBackwardsNJogos, -1): # go backwards 3 jogos
    backwardJogo = Sena.jogosPool.getJogo(i)
    somaBackward = backwardJogo.soma()
    c += 1
    if somaAcima > somaBackward:
      if c==1:
        subindo = True; descendo = False
        quantoSubiu = 1
      else:
        if subindo:
          quantoSubiu += 1
        else:
          # ok, we already know how it has gone down
          break
    elif somaAcima < somaBackward:
      if c==1:
        subindo = False; descendo = True
        quantoDesceu += 1
      else:
        if descendo:
          quantoDesceu += 1
        else:
          # ok, we already know how it has gone either up
          break
    else:  # equal sums
      if c==1:
        subindo = False; descendo = False
        somaRepetiu = 1
      else:
        if not subindo and not descendo:
          somaRepetiu += 1
        else:
          # ok break loop for it already knows how many it has gone up or down
          break
    somaAcima = somaBackward

  #print 'sobeDesce', sobeDesce
  if quantoDesceu > currentMaxDesce:
    return False, FILT_SOMADESCE_MAIOR_Q_MAXDESCE
  if quantoSubiu > currentMaxDSobe:
    return False, FILT_SOMASOBE_MAIOR_Q_MAXSOBE
  if somaRepetiu > 1:
    return False, FILT_SOMAREPETIU_MAIOR_Q_1

  # =========================================
  # Now the STD part
  # =========================================

  # filter Soma Sobe e Desce Dif
  stdStats = contr.getStdStats()
  dp = jogo.std()
  if dp < stdStats.min:
    return False, FILT_STD_MENOR_Q_MIN
  if dp > stdStats.max:
    return False, FILT_STD_MAIOR_Q_MAX
  
  backwardJogo = Sena.jogosPool.getJogo(nDoJogoToCompare)
  dpAnt = backwardJogo.std()
  dpDif = dp - dpAnt
  if dpDif < stdStats.difMin:
    return False, FILT_STDDIF_C_LASTJOGO_MENOR_Q_MIN
  if dpDif > stdStats.difMax:
    return False, FILT_STDDIF_C_LASTJOGO_MAIOR_Q_MAX

  # filter Std Sobe e Desce Absoluta
  # look up if it's climbing or descending
  currentMaxDesce = stdStats.maxDesce
  currentMaxDSobe = stdStats.maxSobe
  goBackwardsNJogos = max(currentMaxDesce, currentMaxDSobe) * 2
  dpAcima = dp; subindo = None; descendo=None; quantoSubiu = 0; quantoDesceu = 0; dpRepetiu = 0; c = 0
  for i in range(nDoJogoToCompare, nDoJogoToCompare - goBackwardsNJogos, -1):
    backwardJogo = Sena.jogosPool.getJogo(i)
    dpBackward = backwardJogo.std()
    c += 1
    if dpAcima > dpBackward:
      if c==1:
        subindo = True; descendo = False
        quantoSubiu = 1
      else:
        if subindo:
          quantoSubiu += 1
        else:
          # ok, we already know how it has gone up
          break
    elif dpAcima < somaBackward:
      if c==1:
        subindo = False; descendo = True
        quantoDesceu += 1
      else:
        if descendo:
          quantoDesceu += 1
        else:
          # ok, we already know how it has gone down
          break
    else:  # equal sums
      if c==1:
        subindo = False; descendo = False
        dpRepetiu = 1
      else:
        if not subindo and not descendo:
          dpRepetiu += 1
        else:
          # ok break loop for it already knows how many it has gone up or down
          break
    dpAcima = dpBackward
  
  #print 'sobeDesce', sobeDesce
  if quantoDesceu > currentMaxDesce:
    return False, FILT_STDDESCE_MAIOR_Q_MAXDESCE
  if quantoSubiu > currentMaxDSobe:
    return False, FILT_STDSOBE_MAIOR_Q_MAXSOBE
  if dpRepetiu > 1:
    return False, FILT_STDREPETIU_MAIOR_Q_1
    
  return True, FILT_SOMA_OU_STD

#@3,filtro
def filtroSixtils(jogo): #, nDoJogoToCompare=Sena.getNOfLastJogo()):
  '''
  Sixtils Q1 Q2 Q3 Q4 Q5 Q6
  pelo menos uma dezena no Q1
  pelo menos uma dezena no Q4
  no máx. três dezenas no Q2 ou Q3 (sobraria uma no Q3 ou Q2, respectiva//

  somaSdObj = analyseSomaSobeOuDesce()
  print somaSdObj 
  soma = jogo.soma()
  
FILT_SIXTILE_OK  = 30
FILT_SIXTILPATTERN_IN_FORBIDDEN_LIST = 31
FILT_SIXTILPATTERN_EQUALS_THAT_OF_LASTJOGO = 32
FILT_SIXTILPATTERN_EQUALS_ONE_BACKWARDS = 33
FILT_SIXTILPATTERN_NOT_YET_OCCURRED = 34
FILT_SIXTILPATTERN_OCCURS_MENOS_Q_MIN_SUCH = 35
FILT_SIXTILPATTERN_OCCURS_MAIS_Q_MAX_SUCH = 36
  
  '''
  sixtilContrObj    = sixtileFunctions.SixtileController()
  thisSixtilPattern = jogo.getSixtilStr()
  occurred          = sixtilContrObj.hasPatternOccurred(thisSixtilPattern)
  if not occurred:
    return False, FILT_SIXTILPATTERN_NOT_YET_OCCURRED
  
  # getPatternsNotOccurred
  if thisSixtilPattern in sixtilContrObj.getForbiddenPatterns():
    return False, FILT_SIXTILPATTERN_IN_FORBIDDEN_LIST

  lastJogo = Sena.jogosPool.getLastJogo()
  patternOfLastJogo = lastJogo.getSixtilPatternLookingUpTable()
  if thisSixtilPattern == patternOfLastJogo:
    return False, FILT_SIXTILPATTERN_EQUALS_THAT_OF_LASTJOGO
  
  nDoLastJogo = Sena.getNOfLastJogo()
  nOfBackwardJogos = sixtilContrObj.getNOfBackwardJogosForCompare()
  #print 'nOfBackwardJogos', nOfBackwardJogos
  for i in range(1, nOfBackwardJogos+1):
    jogoComp = Sena.jogosPool.getJogo(nDoLastJogo - i)
    patternOfJogoComp = jogoComp.getSixtilPatternLookingUpTable()
    if thisSixtilPattern == patternOfJogoComp:
      #print 'jogoComp', jogoComp, patternOfJogoComp, 'thisSixtilPattern', thisSixtilPattern
      return False, FILT_SIXTILPATTERN_EQUALS_ONE_BACKWARDS    
  
  #deactivated = '''
  #if not sixtilContrObj.isPatternAboveMinImposed(thisSixtilPattern):
  #  return False, FILT_SIXTILPATTERN_OCCURS_MENOS_Q_MIN_SUCH          # '''
  
  if not sixtilContrObj.isPatternBelowMaxImposed(thisSixtilPattern):
    return False, FILT_SIXTILPATTERN_OCCURS_MAIS_Q_MAX_SUCH
  
  return True, FILT_SIXTILE_OK


#@4,filtro
def filtroHistogramaEvolutivo(jogo, nDoJogoToCompare=Sena.getNOfLastJogo()):
  '''
  This heuristic is relatively degradable ie as more jogos are added to history
  more likely it will be for a 5-repeat jogo to happen (but how long will it change substantially?)

  FILT_HISTG_EVOL  = 40
  FILT_HISTG_EXCL_N_DEZS_MAIS_FREQ = 41
  FILT_HISTG_EXCL_DEZN_N_MAIS_FREQ_COMBD_M_LASTJOGOS = 42
  FILT_HISTG_EXCL_HAVER_X_N_DEZS_MAIS_FREQ_COMBD_M_LASTJOGOS = 43
  '''
  pass

#@5,filtro
def filtroDezenasQueRepetemEmLastJogos(jogo, nDoJogoToCompare=Sena.getNOfLastJogo()):
  '''
  This heuristic is relatively degradable ie as more jogos are added to history
  more likely it will be for a 5-repeat jogo to happen (but how long will it change substantially?)
  
FILT_REPEATS = 50
FILT_ULTRAPASSA_MAX_REPEATS_PER_JOGO_IN_N_JOGOS = 51
FILT_REPEAT_MENOR_Q_MIN_PER_JOGO_IN_N_JOGOS = 52
FILT_REPEAT_MAIOR_Q_MAX_ALLOWED_OCCURRED = 53
FILT_REPEAT_MENOR_Q_MIN_IMPOSED_OCCURRED = 54
FILT_ULTRAPASSA_QUANT_OF_JOGOS_WITH_MAX_REPEAT = 55
FILT_REPEAT_COM_DEZENA_DO_JOGOREF = 56

  
  *Previous name of this method/function: filtroNDeIguaisJogoAntENDeJogosParaIguaisQuant()

  1 repeat   1 jogos ago
  1 repeat   2 jogos ago
  (...)
  1 repeat   5 jogos ago
  2 repeats   1 jogos ago
  2 repeats   2 jogos ago
  (...)
  3 repeats   10 jogos ago

  mecânica:
  1) positiveConditions:
     1.1) deve ter r 1-repeat em j jogos-ago (eg. 5 1-repeat entre os 7 últimos jogos.)
     1.2) deve ter r 2-repeat em j jogos-ago (eg. 3 2-repeat entre os 8 últimos jogos.)
  2) negativeCondition:
     2.1) não dever ter mais que r n-repeat em j jogos-ago (eg. não haver 3 3-repeat entre os 5 últimos jogos.)
     2.2) não dever ter n-repeat maior que x (eg. não haver 3-repeat através de todo o histórico.)
  '''
  repeatContr = analyzer.RepeatController()
  dezenasNA = jogo.getDezenasNA()

  jogoRef = Sena.jogosPool.getJogo(nDoJogoToCompare)
  dezenasRef = jogoRef.getDezenas()
  for j in range(6):
    if dezenasNA[j] in dezenasRef:
      return False, FILT_REPEAT_COM_DEZENA_DO_JOGOREF

  #nOfRepeatsWithLastJogo = analyzer.contr.nOfRepeatsWithLastJogo # NOT IMPLEMENTED DUE to the way the comb set is formed
  #maxRepeat, backwardsN = repeatContr.tupleMaxQuantOfRepeatsNJogosAgo  # eg 1, 10
  maxRepeat, backwardsN = 1, 2
  for i in range(backwardsN):
    nDoRetroJogo = nDoJogoToCompare - 1 - i
    retroJogo = Sena.jogosPool.getJogo(nDoRetroJogo)
    retroDezenasNA = retroJogo.getDezenasNA()
    nOfRepeatsHere = 0
    for j in range(6):
      if dezenasNA[j] in retroDezenasNA:
        nOfRepeatsHere += 1
    if nOfRepeatsHere > maxRepeat:
      return False, FILT_ULTRAPASSA_MAX_REPEATS_PER_JOGO_IN_N_JOGOS
  minRepeat, backwardsN = repeatContr.tupleMinQuantOfRepeatsNJogosAgo  # eg 2, 25
  minReached = False
  for i in range(backwardsN):
    nDoRetroJogo = nDoJogoToCompare - i
    retroJogo = Sena.jogosPool.getJogo(nDoRetroJogo)
    retroDezenasNA = retroJogo.getDezenasNA()
    nOfRepeatsHere = 0
    for j in range(6):
      if dezenasNA[j] in retroDezenasNA:
        nOfRepeatsHere += 1
    if nOfRepeatsHere >= minRepeat:
      # that's ok, passed the min
      minReached = True
      break
  if not minReached: 
    return False, FILT_REPEAT_MENOR_Q_MIN_PER_JOGO_IN_N_JOGOS

  maxAllowedRepeat = repeatContr.maxAllowedRepeat   # eg 4
  minImposedRepeat = repeatContr.minImposedRepeat   # eg 3 

  maxRepeatInTheRun = 0; quantOfJogosWithThisMax = 0
  for nDoRetroJogo in range(1, nDoJogoToCompare+1):
    retroJogo = Sena.jogosPool.getJogo(nDoRetroJogo)
    retroDezenasNA = retroJogo.getDezenasNA()
    nOfRepeats = 0
    for i in range(6):
      if dezenasNA[i] in retroDezenasNA:
        nOfRepeats += 1
        if nOfRepeats > maxAllowedRepeat:
          return False, FILT_REPEAT_MAIOR_Q_MAX_ALLOWED_OCCURRED
    if nOfRepeats > maxRepeatInTheRun:
      maxRepeatInTheRun = nOfRepeats
      quantOfJogosWithThisMax = 1
    elif nOfRepeats == maxRepeatInTheRun:
      quantOfJogosWithThisMax += 1

  if maxRepeatInTheRun < minImposedRepeat:
      return False, FILT_REPEAT_MENOR_Q_MIN_IMPOSED_OCCURRED
  resp = repeatContr.passaQuantOfJogosWithMax(maxRepeatInTheRun, quantOfJogosWithThisMax)
  #print 'maxRepeatInTheRun, quantOfJogosWithThisMax', maxRepeatInTheRun, quantOfJogosWithThisMax, 'resp', resp 
  if not resp:
    return False, FILT_ULTRAPASSA_QUANT_OF_JOGOS_WITH_MAX_REPEAT


  return True, FILT_REPEATS

#@6,filtro
def filtroConsecutivos(jogo, nDoJogoRef=Sena.getNOfLastJogo()):
  '''
FILT_CONSECUTIVO = 60
FILT_CONSECUTIVO_EXTRAPOLA_AS_PATTERN = 61
FILT_CONSEC_COINCIDES_WITH_LASTJOGOS = 62
FILT_NOSE_MAIS_Q_MAX = 63
FILT_NESO_MAIS_Q_MAX = 64
FILT_N_OF_PRIMES_MAIS_Q_MAX = 65
  '''
  consec, patternStr = jogo.getConsecutiveArrayAndPattern()
  #print 'jogo', jogo, 'patternStr', patternStr
  # hardwired for the time being, to change in the future
  forbiddenPatterns = ['30000','31000','32100','42100','43210','54321'] 
  if patternStr in forbiddenPatterns:
    return False, FILT_CONSECUTIVO_EXTRAPOLA_AS_PATTERN

  # hardwired for the time being, to change in the future
  if patternStr == '00000':
    goBackwardN = 5
  elif patternStr == '10000':
    goBackwardN = 3
  else:
    goBackwardN = 1

  coincide = 0 
  for i in range(goBackwardN):
    backwardJogoN = nDoJogoRef - i
    jogoComp = Sena.jogosPool.getJogo(backwardJogoN)
    notUsed, patternComp = jogoComp.getConsecutiveArrayAndPattern()
    if patternStr == patternComp:
      coincide += 1
    else:
      break
  if coincide == goBackwardN:
    return False, FILT_CONSEC_COINCIDES_WITH_LASTJOGOS

  # NOSE diagonal depth/size
  maxAllowedNOSE = 2
  jogoRef = Sena.jogosPool.getJogo(nDoJogoRef)
  noseRef =  jogoRef.getNOSEDepth()
  if noseRef > 1:
    maxAllowedNOSE = 1
  if maxAllowedNOSE == 1:
    if nDoJogoRef - 1 > 0:
      jogoRef = Sena.getJogo(nDoJogoRef - 1)
      noseRef =  jogoRef.getNOSEDepth()
      if noseRef > 0:
        maxAllowedNOSE = 0
  noseDepth = jogo.getNOSEDepth()
  if noseDepth > maxAllowedNOSE:
    return False, FILT_NOSE_MAIS_Q_MAX
  
  # Primes
  maxAllowedNOfPrimes = 4
  jogoRef = Sena.jogosPool.getJogo(nDoJogoRef)
  nOfPrimesRef =  jogoRef.getNOfPrimes()
  if nOfPrimesRef >= 4:
    maxAllowedNOfPrimes = 3
  if maxAllowedNOfPrimes == 3:
    if nDoJogoRef - 1 > 0:
      jogoRef = Sena.getJogo(nDoJogoRef - 1)
      nOfPrimesRef =  jogoRef.getNOSEDepth()
      if nOfPrimesRef == 3:
        maxAllowedNOfPrimes = 2
  nOfPrimes = jogo.getNOfPrimes()
  if nOfPrimes > maxAllowedNOfPrimes:
    return False, FILT_N_OF_PRIMES_MAIS_Q_MAX

  return True, FILT_CONSECUTIVO

#@7,filtro
def filtroVarLinhaColuna(jogo, nDoJogoRef=Sena.getNOfLastJogo()):
  '''
  filtroVariacaoD1D2 ou filtro LINHAS x COLUNAS
  Data Structure
  eg  0:1 1:1 2:1 4:1 5:2    1:1 4:1 6:2 7:1 8:1
  * dezena abaixo é o dígito da esquerda
  (dezena-0, repetMin, repetMax)   
  (dezena-0, repetMin, repetMax)
  ...
  (dezena-5, repetMin, repetMax)

  * unidade abaixo é o dígito da direita
  unidade-0,
  unidade-1, repetMin, repetMax)
  ...
  (unidade-9, repetMin, repetMax)
  
  
FILT_LINHA = 70
FILT_LINHA_IGUAL_ULTIMO_JOGO = 71
#FILT_ALGUMALINHA_MAIOR_Q_MAX_ESTIMADO = 71
FILT_LINHAPATTERN_NEVER_OCCURRED = 72   # D1 pattern is sixtil-like, D2 is a tentil-like (not implemented yet)
FILT_LINHAPATTERN_IGUALA_MAX_OCCUR = 73
FILT_LINHA_N_NAO_PRESENTE_QUANDO_LIKELY = 74
FILT_LINHA_EXCLUIDA = 75
FILT_LINHA_FORA_DA_TENDENCIA_DE_BALANCA = 76   # balança é a média ponderada (ou prod. escalar) com [-3 -2 -1 +1 +2 +3]
FILT_LINHA_STD_FORA_DA_TENDENCIA = 77 # ex. muito esparso quando deveria estar mais centrado ou vice-versa
FILT_FLATNESS_LINCOL_FORA_DO_ESTIMADO = 79  # flatness fornece o grau de achatamento da "curva lincol"

FILT_COLUNA = 80
FILT_COLUNA_IGUAL_ULTIMO_JOGO = 81
#FILT_ALGUMACOLUNA_MAIOR_Q_MAX_ESTIMADO = 81
FILT_COLUNAPATTERN_NEVER_OCCURRED = 82  # not used for the time being
FILT_COLUNAPATTERN_IGUALA_MAX_OCCUR = 83
FILT_COLUNA_N_NAO_PRESENTE_QUANDO_LIKELY = 84
FILT_COLUNA_EXCLUIDA = 85
FILT_COLUNA_FORA_DA_TENDENCIA_DE_BALANCA = 86
FILT_COLUNA_STD_FUZZY_PATTORA_DA_TENDENCIA = 87
FILT_FUZZYNESS_LINCOL_FORA_DO_ESTIMADO = 89  # fuzzyness aqui é o Desvio Padrão em 2D
  '''
  patternLinha, patternColuna = jogo.getTuple2LinCol()
  contr = analyzer.Controller()

  linColPatternObj = contr.getLinColPatternObj()
  #print 'linColPatternObj', linColPatternObj

  patternsLinhaNeverOccurred = linColPatternObj.getPatternsLinhaNeverOccurred() # eg ['600000', '510000', '420000']
  if patternLinha in patternsLinhaNeverOccurred:
    return False, FILT_LINHAPATTERN_NEVER_OCCURRED

  patternsLinhaFoundDict = linColPatternObj.getPatternsLinhaFoundDict()
  try:
    if patternsLinhaFoundDict[patternLinha] == linColPatternObj.getMaxPatternLinhaRepeat(): # two less the max
      return False, FILT_LINHAPATTERN_IGUALA_MAX_OCCUR
  except KeyError:
    pass
  
  patternsColunaFoundDict = linColPatternObj.getPatternsColunaFoundDict()
  try:
    if patternsColunaFoundDict[patternColuna] == linColPatternObj.getMaxPatternColunaRepeat(): # two less the max
      return False, FILT_COLUNAPATTERN_IGUALA_MAX_OCCUR
  except KeyError:
    pass
  
  jogoRef = Sena.jogosPool.getJogo(nDoJogoRef)
  if patternLinha == jogoRef.getLinhaPattern():
    return False, FILT_LINHA_IGUAL_ULTIMO_JOGO
  if patternColuna == jogoRef.getColunaPattern():
    return False, FILT_COLUNA_IGUAL_ULTIMO_JOGO
  
  return True, FILT_LINHA

todosOsFiltros = [filtroParImpar,filtroSomaEtAl,filtroSixtils,filtroDezenasQueRepetemEmLastJogos,filtroConsecutivos,filtroVarLinhaColuna]
def passThruFilters(jogo):
  '''
  filtroParImpar(jogo)
  filtroSomaEtAl(jogo)
  filtroSixtils(jogo)
  #filtroHistogramaEvolutivo
  filtroDezenasQueRepetemEmLastJogos(jogo)
  filtroConsecutivos(jogo)
  filtroVarLinhaColuna(jogo)
  '''
  tuple2 = True, FILT_LINHA  # just an initial value, though the last filter is indeed FILT_LINHA
  for filtro in todosOsFiltros:
    tuple2 = filtro(jogo)
    #print jogo, tuple2
    hasPassed = tuple2[0]
    if not hasPassed:
      return tuple2
  return tuple2 

def passThruAllFilters(jogo):
  '''
  filtroParImpar(jogo)
  filtroSomaEtAl(jogo)
  filtroSixtils(jogo)       # or filtroHistograma1()
  #filtroHistograma2(jogo)  # previously "HistogramaEvolutivo()
  filtroDezenasQueRepetemEmLastJogos(jogo)
  filtroConsecutivos(jogo)
  filtroVarLinhaColuna(jogo)
  '''
  responsesList = []
  for filtro in todosOsFiltros:
    tuple2 = filtro(jogo)
    #print jogo, tuple2
    responsesList.append(tuple2[1])
  if len(responsesList) == 0:
    responsesList.append(True)
  return responsesList

def convertApostasFileToJogoList(filePath):
  lines = open(filePath).readlines() # eg from ./Apostas/
  jogoList = []; c = 0
  for line in lines:
    pp = line.split(' ')
    if len(pp) < 6:
      continue
    dezenas = []
    for d in pp[:6]: # exactly 6
      try:
        dezenas.append(int(d))
      except ValueError:
        continue
    if len(dezenas) == 6:
      c += 1
      jogo = Sena.Jogo(-c)
      jogo.setDezenas(dezenas)
      jogoList.append(jogo)
  return jogoList

def testApostasFilePassThruAllFilters(filePath):
  jogoList = convertApostasFileToJogoList(filePath)
  for jogo in jogoList:
    responsesList = filters.passThruAllFilters(jogo)
    for resp in responsesList:
      print resp, filters.getMessageStrFromFilterReturnNumberCode(resp)

def passThruAllFiltersReturningAlsoMsgs(jogo):
  responsesList = passThruAllFilters(jogo)
  print jogo, 'responsesList', responsesList
  out2TupleList = joinMessageStrWithFilterReturnNumberCodes(responsesList)
  for out2Tuple in out2TupleList:
    print out2Tuple[0], out2Tuple[1]



def checkIfAllDezenasAreDifferent(dezenas):
  # check if all of the 6 are different, if not, cast an exception
  nDeDezenas = len(dezenas)
  for i in range(nDeDezenas - 1):
    for j in range(i+1, nDeDezenas):
      if dezenas[i] == dezenas[j]:
        errorMsg = 'A dezena na posição %d está repetida com a da posição %d. Obs.: as 6 dezenas têm que ser diferentes. As dezenas foram %s. Por favor, recheque os dados.' %(i+1, j+1, str(dezenas))
      raise ValueError, errorMsg

arrayIni = [-1,-1,-1,-1,-1,-1]
class Filter2(object):
  def __init__(self, seqNum):
    pass
  def getNDePares(self):
    '''
    This method gives out the number of even values in the 6-tuple
    '''
    if len(self.dezenas) != 6 or None in self.dezenas:
      return None
    paresN = 0
    for dezena in self.dezenas:
      if dezena % 2 == 0:
        paresN += 1 
    return paresN  
  def getDezenasStrCom2DigitosCada(self):
    outStr = ''
    for d in self.dezenas:
      outStr += str(d).zfill(2) + ' '
    return outStr[:-1] 
  def getDezenasStrCom2DigitosCadaAscente(self):
    outStr = ''
    for d in self.getSorteadosEmOrdemAscendente():
      outStr += str(d).zfill(2) + ' '
    return outStr[:-1]

  def getConsecutiveArrayAndPattern(self):
    '''
  getConsecutive Array (consec) and Pattern Str (eg 00000 10000 21000 ... 54321)
  Input: d (6-D dezena list)
  Returns tuple (consec, patternStr)
    '''  
    d = self.getSorteadosEmOrdemAscendente()
    consec = [0]*6  # index 0 not used
    for i in range(6):
      if i > 0:
        if d[i]-1 == d[i-1]:
          consec[1]+=1
          if i > 1:
            if d[i]-2 == d[i-2]:
              consec[2]+=1
              if i > 2:
                if d[i]-3 == d[i-3]:
                  consec[3]+=1
                  if i > 3:
                    if d[i]-4 == d[i-4]:
                      consec[4]+=1
                      if i > 4:
                        if d[i]-5 == d[i-5]:
                          consec[5]+=1
    patternList = map(str, consec)
    patternStr  = ''.join(patternList[1:])  # take care with the starting index here, for index 0 is not used here
    return consec, patternStr

  def getSixtilPatternLookingUpTable(self):
    import sixtileFunctions
    return sixtileFunctions.getSixtilPatternFromHistory(self.seqNum)

  linhaPattern = None; colunaPattern = None 
  def getTuple2LinCol(self):
    if self.linhaPattern == None or self.colunaPattern == None: 
      import atualizaStatisticsEtAl
      self.linhaPattern, self.colunaPattern = atualizaStatisticsEtAl.geraStrPatternLinCol(self)
    if self.linhaPattern == None or self.colunaPattern == None:
      raise ' in class Jogo [getLinhaPattern()] :: self.linhaPattern continues = None or self.colunaPattern continues = None.'
    return self.linhaPattern, self.colunaPattern

  def getLinhaPattern(self):
    return self.getTuple2LinCol()[0]
     
  def getColunaPattern(self):
    return self.getTuple2LinCol()[1]
  
  def getSixtilStr(self):
    '''
    IMPORTANT NOTE: DO NOT CALL THIS METHOD FOR HISTORY JOGOS, instead CALL previous method which looks up a history table.
                    The sixtil string this method returns is a dynamic, on-the-fly one, only suitable for the filtering 'bet' jogos.
    '''                     
    if self.sixtilStr == None:
      import sixtileFunctions
      self.sixtilStr = sixtileFunctions.getSixtilPatternOfGeneralizedJogo(self)
      if self.sixtilStr == None or self.sixtilStr == '':
        raise 'self.sixtilStr is still either None or empty. Some problem has happened. Eg. Histogram file is missing or can not be read.'
    return self.sixtilStr
  
  def getHg2Pattern(self, nDoJogoRef=getNOfLastJogo()):
    import atualizaStatisticsEtAl   
    hg2Obj = atualizaStatisticsEtAl.DezenasHGSingleton()
    hg2Obj.setNDoJogo(nDoJogoRef)
    hg2Pattern = hg2Obj.getHg2PatternForJogo(self)
    return hg2Pattern

  def findIndexFromCombination(self):
    import combinadics
    return combinadics.findIndexFromCombination(self.getDezenas())

  def getNOfPrimes(self):
    nOfPrimes = 0
    for dezena in self.getDezenas():
      if dezena in PRIMES_TILL_60:
        nOfPrimes += 1
    return nOfPrimes

  def getNOSEDepth(self):
    dezenas = self.getSorteadosEmOrdemAscendente()
    maxDepthInJogo = 0; index = 0; depth = 0
    while index < 5:
      import analyzer
      depth, index = analyzer.getDepthForNoseDiag(dezenas, index, depth)
      if depth > maxDepthInJogo:
        maxDepthInJogo = depth
      index += 1; depth = 0
    return maxDepthInJogo

  def getJogoAnt(self):
    anterior = self.seqNum - 1
    if anterior < 1:
      return None
    jogoAnt = jogosPool.getJogo(anterior)
    return jogoAnt
  def previousJogo(self):
    return self.getJogoAnt()
  def nextJogo(self):
    nOfLastJogo = getNOfLastJogo()
    if self.seqNum == nOfLastJogo:
      return None
    jogoPos = jogosPool.getJogo(self.seqNum + 1) 
    return jogoPos
  def __str__(self):
    outStr = str(self.seqNum) + ' ' + self.getDezenasStrCom2DigitosCadaAscente()
    return outStr

'''
def testBackwardJogo():
  nlj = getNOfLastJogo()
  for i in range(5):
    backJogo = jogosPool.getJogo(nlj - i)
    #print backJogo
  for i in range(5):
    backJogo = jogosPool.getJogo(nlj - i)
    #print backJogo

if __name__ == '__main__':
  jogo = Sena.Jogo(-1)
  # dezenas = [46,20,04,43,47,10] # 984
  import sys
  dezenas = map(int, sys.argv[1:7])
  jogo.setDezenas(dezenas)
  passThruAllFiltersReturningAlsoMsgs(jogo)
'''


if __name__ == '__main__':
  seeConsecutives()
