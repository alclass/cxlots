#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, random, sys, time
sys.path.insert(0, '../../../fs/dbfs')
import Sena  # filters

charEmpty = '|_|'
charX = '|X|'
charBar = '='
charBarEmpty = ' '

def printX(jogo):
  text2D = ' '
  dezenas = jogo.getSorteadosEmOrdemAscendente()	
  for coluna in range(1,10+1):
    if coluna == 10:
      char = 'A'
    else:
      char = str(coluna)
    text2D += '|'+char+'|'
  #text2D += '\n'
  for linha in range(6):
    text2D += '\n%d' %(linha)
    for coluna in range(1,10+1):
      pos2D = linha*10 + coluna
      if pos2D in dezenas:
	text2D += charX
      else:
	text2D += charEmpty
  return text2D
		
def testPrintX(nOfBackwardJogos=7):
  if nOfBackwardJogos < 1:
    nOfBackwardJogos = 1
  lastJogo = Sena.getNOfLastJogo()
  for i in range(nOfBackwardJogos):
    jogo = Sena.jogosPool.getJogo(lastJogo - i)
    print jogo
    print printX(jogo)
		
def generateImageBarsWithDezenas(dezenas):
  text2D = ''
  for linha in range(6):
    text2D += '\n'
    for coluna in range(1,10+1):
      pos2D = linha*10 + coluna
      if pos2D in dezenas:
	text2D += charBar
      else:
	text2D += charBarEmpty
  return text2D

def generateImageBars(jogo):
  dezenas = jogo.getSorteadosEmOrdemAscendente()
  return generateImageBarsWithDezenas(dezenas)

def testGenerateImageBars(nOfBackwardJogos=3):
  if nOfBackwardJogos < 1:
    nOfBackwardJogos = 1
  lastJogo = Sena.getNOfLastJogo()
  for i in range(nOfBackwardJogos):
    jogo = Sena.jogosPool.getJogo(lastJogo - i)
    print jogo
    print generateImageBars(jogo)
		
import filters
def pickUpJogosInApostasFile(nDoConcurso):
  filePath = '../Apostas/apostas-%s.txt' %(str(nDoConcurso).zfill(4))
  print 'Picking up dezenas:', filePath
  jogosApostados = filters.convertApostasFileToJogoList(filePath)
  return jogosApostados

def passJogosToGenImageBars(nOfRefJogo=Sena.getNOfLastJogo()):
  nOfNextJogo = nOfRefJogo + 1 
  jogosApostados = pickUpJogosInApostasFile(nOfNextJogo)
  for jogoApostado in jogosApostados:
    print 'jogoApostado', jogoApostado
    print generateImageBars(jogoApostado)

def showStatsForCheckAcertosThruJogos(nOfAcertosDict):
  print '='*50
  print 'Stats with nOfAcertosDict:'
  print '='*50
  nOfAcertosList = nOfAcertosDict.keys()
  maiorAcerto = -1; menorAcerto = 1000; total = 0
  for nOfAcertos in nOfAcertosList:
    quant = nOfAcertosDict[nOfAcertos]
    quantStr = '%2dx' %(quant)
    print quantStr, nOfAcertos, 'acerto(s)'
    total += quant
    if nOfAcertos < menorAcerto:
      menorAcerto = nOfAcertos
    if nOfAcertos > maiorAcerto:
      maiorAcerto = nOfAcertos
  print 'Total de apostas:', total, ':: menor nº de acertos:', menorAcerto, ':: maior nº de acertos:', maiorAcerto

tmpF = lambda x: str(x).zfill(2)
def compareJogosForAcertos(dezenasApostadas, dezenasSorteadas, nOfAcertosDict, minNOfAcertosForPrint=4):
  nOfAcertos = 0; coincList = []
  for d in dezenasApostadas:
    if d in dezenasSorteadas:
      nOfAcertos += 1
      coincList.append(d)
  try:
    nOfAcertosDict[nOfAcertos] += 1
  except KeyError:
    nOfAcertosDict[nOfAcertos] = 1
  if nOfAcertos >= minNOfAcertosForPrint:
    dezenasApostadasList = map(tmpF, dezenasApostadas)
    dezenasApostadasStr  = ' '.join(dezenasApostadasList)
    print dezenasApostadasStr, '::', nOfAcertos, 'acertos:', coincList
  return nOfAcertosDict

def checkAcertosThruJogos(jogoSorteado, nDoConcursoSorteado, minNOfAcertosForPrint=4):
  dezenasSorteadas = jogoSorteado
  if type(jogoSorteado) != type([]):
    dezenasSorteadas = jogoSorteado.getSorteadosEmOrdemAscendente()
  jogosApostados = pickUpJogosInApostasFile(nDoConcursoSorteado)
  nOfAcertosDict = {}
  sorteadasList = map(tmpF, dezenasSorteadas)
  sorteadasStr  = ' '.join(sorteadasList)
  print 'Verificando coincidências com', sorteadasStr
  for jogoApostado in jogosApostados:
    dezenasApostadas = jogoApostado.getDezenas()
    nOfAcertosDict = compareJogosForAcertos(dezenasApostadas, dezenasSorteadas, nOfAcertosDict, minNOfAcertosForPrint)
  showStatsForCheckAcertosThruJogos(nOfAcertosDict)

def coincsOfApostasWithLastJogo():
  lastJogo = Sena.getLastJogo()
  nOfNextJogo = lastJogo.getSeqNum() + 1
  minNOfAcertosForPrint = 2
  checkAcertosThruJogos(lastJogo, nOfNextJogo, minNOfAcertosForPrint)

def aproveitaCartoesJaImpressosSemCoincComUltJogo():
  lastJogo = Sena.getLastJogo()
  lastDezenas = lastJogo.getSorteadosEmOrdemAscendente()
  nOfNextJogo = lastJogo.getSeqNum() + 1
  jogosApostados = pickUpJogosInApostasFile(nOfNextJogo)
  cartao = 1; c = 0; cartaoList = []
  for jogoApostado in jogosApostados:
    c += 1
    dezenas = jogoApostado.getDezenas(); coinc = 0; cartaoSujo = False
    for dezena in dezenas:
      if dezena in lastDezenas:
        coinc += 1
	cartaoSujo = True
	break
    if coinc == 0 and not cartaoSujo:
      cartaoList.append(dezenas)
      if len(cartaoList) == 3:
        print 'cartao', cartao, cartaoList
	cartaoList = []
    if c % 3 == 0:
      cartao += 1
      cartaoSujo = False
      cartaoList = []



def testAcertosThruJogos3(dezenasSorteadas, nDoConcursoSorteado, minNOfAcertosForPrint=1):
  jogoSorteado = Sena.Jogo(0)
  jogoSorteado.setDezenas(dezenasSorteadas)
  checkAcertosThruJogos(jogoSorteado, nDoConcursoSorteado, minNOfAcertosForPrint)

def testAcertosThruJogos2(dezenasSorteadas, nDoConcursoSorteado, nOfChain=2):
  '''
  This will compare with the larger files
  '''
  jogoSorteado = Sena.Jogo(0)
  jogoSorteado.setDezenas(dezenasSorteadas)
  filenameApostasIn = '../Apostas/CombinationsChain-level-%d-%d.txt' %(nOfChain, nDoConcursoSorteado)
  print 'testAcertosThruJogos2 against file:', filenameApostasIn
  fileApostasIn = open(filenameApostasIn)
  line = fileApostasIn.readline(); nOfAcertosDict = {}; c = 0
  while line:
    dezenasApostadas = transformLineToDezenasList(line)
    nOfAcertosDict = compareJogosForAcertos(dezenasApostadas, dezenasSorteadas, nOfAcertosDict)
    line = fileApostasIn.readline()
  showStatsForCheckAcertosThruJogos(nOfAcertosDict)

def testAcertosThruJogos1(dezenasSorteadas, nDoConcursoSorteado, nOfChain=1):
  testAcertosThruJogos2(dezenasSorteadas, nDoConcursoSorteado, nOfChain)

def verifyAcertosDasApostas(getLastJogoFromDB=False, minNOfAcertosForPrint=1):
  dezenasSorteadas = None
  if getLastJogoFromDB:
    jogo = Sena.getLastJogo()
    dezenasSorteadas = jogo.getSorteadosEmOrdemAscendente()
    nDoConcursoSorteado = jogo.getSeqNum()
  else:
    fileIn = open('../Dados/lastJogoParaVerificarAcertosDasApostas.txt')
    line = fileIn.readline()
    if line:
      dezenasList = line.split()[:6]
      dezenasSorteadas = map(int, dezenasList)
      nDoConcursoSorteado = Sena.getNOfLastJogo() + 1
  testAcertosThruJogos2(dezenasSorteadas, nDoConcursoSorteado)
  testAcertosThruJogos3(dezenasSorteadas, nDoConcursoSorteado, minNOfAcertosForPrint)

def verifyAcertosDasApostasWithLargerChain1(getLastJogoFromDB=False):
  dezenasSorteadas = None
  if getLastJogoFromDB:
    jogo = Sena.getLastJogo()
    dezenasSorteadas = jogo.getSorteadosEmOrdemAscendente()
    nDoConcursoSorteado = jogo.getSeqNum()
  else:
    fileIn = open('../Dados/lastJogoParaVerificarAcertosDasApostas.txt')
    line = fileIn.readline()
    if line:
      dezenasList = line.split()[:6]
      dezenasSorteadas = map(int, dezenasList)
      nDoConcursoSorteado = Sena.getNOfLastJogo() + 1
  testAcertosThruJogos1(dezenasSorteadas, nDoConcursoSorteado)


def sorteadasThruAllFilters(getLastJogoFromDB=False):
  # it needs to get it from verifyAcertosThruJogosWithLastJogo.txt anyway
  filenameIn = '../Dados/lastJogoParaVerificarAcertosDasApostas.txt'
  fileIn = open(filenameIn)
  line = fileIn.readline()
  if not line:
    msg = filenameIn + ' is missing, could not be opened.'
    raise IOError, msg
  dezenasList = line.split()[:6]
  dezenasSorteadas = map(int, dezenasList)
  nDoConcursoSorteado = Sena.getNOfLastJogo() + 1
  jogoSorteado = Sena.Jogo(nDoConcursoSorteado)
  jogoSorteado.setDezenas(dezenasSorteadas)
  print 'Verificando se jogo nº', nDoConcursoSorteado, dezenasSorteadas, 'passa pelos filtros:'
  respList = filters.passThruAllFilters(jogoSorteado)
  for msgCode in respList:
    print msgCode, filters.getMessageStrFromFilterReturnNumberCode(msgCode)

def updateSorteadasToHistDB():
  filenameIn = '../Dados/lastJogoParaVerificarAcertosDasApostas.txt'
  fileIn = open(filenameIn)
  line = 'any'; nOfLine=0
  while line:
    nOfLine += 1
    line = fileIn.readline()
    if not line:
      msg = filenameIn + ' is missing, could not be opened.'
      raise IOError, msg
    # it should be the second line !!!
    if nOfLine==2:
      break
  dezenasList = line.split()[:6]
  dezenasNaOrdemDoSorteio = map(int, dezenasList)
  #nDoConcursoSorteado = Sena.getNOfLastJogo() + 1
  #jogoSorteado = Sena.Jogo(nDoConcursoSorteado)
  #jogoSorteado.setDezenas(dezenasSorteadas)
  Sena.insertIntoDB(dezenasNaOrdemDoSorteio)

def transformLineToDezenasList(line):
  #if len(line)==0:
  #  return []
  if line[0]=='#':
    return None
  dezenas = None
  try:
    pp = line[:-1].split(' ')
    dezenas = map(int, pp[:6])
  except IndexError:  # IndexError in case len(pp) is < 6; ValueError in case some word is not really int
    pass
  except ValueError:
    pass
  return dezenas

def lookForEqualsInJogosFiles(filenameA, filenameB):
  fileA = open(filenameA)
  nOfLineA = 1
  print time.ctime().split(' ')[-2], 'nOfLineA', nOfLineA
  lineFileA = fileA.readline()
  nOfEquals = 0; equalsList = []
  while lineFileA:
    dezenasA = transformLineToDezenasList(lineFileA)
    if dezenasA == None:
      lineFileA = fileA.readline()
      continue
    #print 'Looking for equals of', dezenasA
    fileB = open(filenameB)
    lineFileB = fileB.readline()
    while lineFileB:
      dezenasB  = transformLineToDezenasList(lineFileB)
      if dezenasB == None:
        lineFileB = fileB.readline()
        continue
      if dezenasA == dezenasB:
        nOfEquals += 1
	equalsList.append(dezenasA)
	print 'Found equal for', dezenasA, ':: nOfEquals =', nOfEquals
      lineFileB = fileB.readline()
    fileB.close()
    nOfLineA += 1
    if nOfLineA % 50 == 0:
      print time.ctime().split(' ')[-2], 'nOfLineA', nOfLineA
    lineFileA = fileA.readline()
  fileA.close()
  print 'Finished at', time.ctime().split(' ')[-2], 'N. of equals is', nOfEquals

def verifyEqualsInJogosFiles():
  #filenameA = '../Apostas/CombinationsChain-level-2-982.txt'
  #filenameB = '../Apostas/CombinationsChain-level-2-983.txt'
  for i in range(975,982+1):
    filenameA = '../Apostas/apostas-0%d.txt' %(i)
    if not os.path.isfile(filenameA):
      continue
    for j in range(i+1,983+1):
      filenameB = '../Apostas/apostas-0%d.txt' %(j)
      if not os.path.isfile(filenameB):
        continue
      print 'LookForEqualsInJogosFiles', filenameA, filenameB
      print 'Long processing, please wait.'
      lookForEqualsInJogosFiles(filenameA, filenameB)

def almostManualJogo(freqOrderSets):
  if len(freqOrderSets) != 6:
    raise ValueError
  combs = []; d = [None] * 6
  for d[0] in freqOrderSets[0]:
    for d[1] in freqOrderSets[1]:
      for d[2] in freqOrderSets[2]:
        for d[3] in freqOrderSets[3]:
          for d[4] in freqOrderSets[4]:
	    for d[5] in freqOrderSets[5]:
              dezenas = d[:] # hard copy
	      dezenas.sort()
	      combs.append(dezenas)
  combs.sort(); c = 0
  nextConc = Sena.getNOfLastJogo() + 1
  apostasFilename = '../Apostas/apostasAlmostManual-%04d.txt' %(nextConc)
  print 'Begin writing', apostasFilename, 'with', len(combs), 'jogosfs.'
  apostasFile = open(apostasFilename, 'w')
  for dezenas in combs:
    c += 1
    jogo = Sena.Jogo(-c)
    jogo.setDezenas(dezenas)
    #print 'filter', jogo,
    respBool, code = filters.passThruFilters(jogo)
    if not respBool:
      pass
      #print respBool, filters.getMessageStrFromFilterReturnNumberCode(code)
    else:
      dezenasList = map(tmpF, dezenas)
      line = ' '.join(dezenasList)
      print line
      apostasFile.write(line + '\n')
  print 'Closing', apostasFilename, 'with', len(combs), 'jogosfs.'
  apostasFile.close()

import atualizaStatisticsEtAl
def freqOrderChosenForAlmostManualComb(freqOrderList=None):
  if freqOrderList == None:
    freqOrderList = [4,5,15,16,19,23]
  freqOrderSets = [None] * 6
  hg2Obj = atualizaStatisticsEtAl.DezenasHGSingleton()
  hg2Obj.setNDoJogo(Sena.getNOfLastJogo())
  freqOrderSets = map(hg2Obj.getDezenasWithOrderOfFreq, freqOrderList)
  freqOrderSetsList = []
  freqOrderSetsList.append(freqOrderSets)
  freqOrderList = [3,4,17,21,22,27]
  freqOrderSets = map(hg2Obj.getDezenasWithOrderOfFreq, freqOrderList)
  freqOrderSetsList.append(freqOrderSets)
  freqOrderList = [6,18,20,23,24,26]
  freqOrderSets = map(hg2Obj.getDezenasWithOrderOfFreq, freqOrderList)
  freqOrderSetsList.append(freqOrderSets)
  freqOrderSets = freqOrderSetsList[0]
  for freqSet in freqOrderSetsList[1:]:
    for j in range(6):
      freqOrderSets[j]+=freqSet[j]
  print almostManualJogo(freqOrderSets)
'''
def freqOrderChosenForAlmostManualCombRange(freqOrderRanges=None):
  if freqOrderList == None:
    freqOrderList = [4,5,15,16,19,23]
  freqOrderSets = [None] * 6
  hg2Obj = atualizaStatisticsEtAl.DezenasHGSingleton()
  hg2Obj.setNDoJogo(Sena.getNOfLastJogo())
  for faixa in 
  freqOrderSets = map(hg2Obj.getDezenasWithOrderOfFreq, freqOrderList)
  freqOrderSetsList = []
  freqOrderSetsList.append(freqOrderSets)
  freqOrderList = [3,4,17,21,22,27]
  freqOrderSets = map(hg2Obj.getDezenasWithOrderOfFreq, freqOrderList)
  freqOrderSetsList.append(freqOrderSets)
  freqOrderList = [6,18,20,23,24,26]
  freqOrderSets = map(hg2Obj.getDezenasWithOrderOfFreq, freqOrderList)
  freqOrderSetsList.append(freqOrderSets)
  freqOrderSets = freqOrderSetsList[0]
  for freqSet in freqOrderSetsList[1:]:
    for j in range(6):
      freqOrderSets[j]+=freqSet[j]
  print almostManualJogo(freqOrderSets)
'''

def diminishApostasSizeTo2(newCount, apostasFilename):
  lines = open(apostasFilename).readlines(); apostas = []
  for line in lines:
    dezenas = transformLineToDezenasList(line)
    if dezenas != None:
      apostas.append(dezenas)
  nOfThoseToDelete = len(apostas) - newCount
  for i in range(nOfThoseToDelete, 0, -1):
    tam = len(apostas)
    indexToDelete = random.randint(1,tam) - 1
    print 'del apostas[indexToDelete]', apostas[indexToDelete], 'indexToDelete', indexToDelete
    del apostas[indexToDelete]
  newApostasFilename = '../Apostas/%s-with-%d-apostas.txt' %(apostasFilename, len(apostas))
  newApostasFile = open(newApostasFilename, 'w')
  c = 0
  for dezenas in apostas:
    c+=1;print c, dezenas
    tmpList = map(tmpF, dezenas)
    line = ' '.join(tmpList)
    newApostasFile.write(line + '\n')
  newApostasFile.close()

def diminishApostasSizeTo(newCount, apostasFilename=None):
  if apostasFilename == None:
    nextConc = Sena.getNOfLastJogo() + 1
    apostasFilename = '../Apostas/apostas-%04d.txt' %(nextConc)
  diminishApostasSizeTo2(newCount, apostasFilename)

def prepareDiminishApostasSizeTo():
  newCount = raw_input('Entre com a nova contagem (diminuída de apostas: ')
  newCount = int(newCount)
  diminishApostasSizeTo(newCount)

def percentualDeJogosComUmaDasSeguintesDezenas(dList):
  '''
  This method calculates the percentage any one dezena in a set
  occurs through Sena history
  (Based on the idea of 'dezenas de ouro' (too general to have any appeal!)
  '''
  nDeJogos = Sena.getNOfLastJogo(); count=0
  for nDoJogo in range(1, nDeJogos+1):
    jogo = Sena.jogosPool.getJogo(nDoJogo)
    dezenas = jogo.getDezenas()
    for d in dezenas:
      if d in dList:
        count+=1
	break
  print 'count/nDeJogos', count, '/', nDeJogos, '=', count/(0.0+nDeJogos)


def histogramOfApostasFile(apostasFilename=None):
  nextConc = Sena.getNOfLastJogo() + 1
  if apostasFilename == None:
    apostasFilename = '../Apostas/apostas-%04d.txt' %(nextConc)
  else:
    apostasFilename = '../Apostas/' + apostasFilename
  lines = open(apostasFilename).readlines(); dezenasHist = {}
  for line in lines:
    dezenas = transformLineToDezenasList(line)
    if dezenas == None:
      continue
    for dezena in dezenas:
      try:
        dezenasHist[dezena]+=1
      except KeyError:
        dezenasHist[dezena]=1
  dezenas = dezenasHist.keys()
  dezenas.sort(); total = 0
  for dezena in dezenas:
    quant = dezenasHist[dezena]
    print dezena, quant
    total += quant
  print 'n of dezenas =', len(dezenasHist), ' total =', total

def convertPyListToJogoStr(filenameIn='../Apostas/aproveita-de-986-para-988.old.txt'):
  '''
Obs: this routine should be refactored/improved to a full regexp version.
     Error catching should also be included.

Text example:
cartao 6 [[1, 15, 16, 30, 43, 48], [1, 15, 18, 23, 55, 57], [1, 17, 19, 37, 43, 60]]
cartao 8 [[1, 21, 23, 36, 42, 43], [1, 22, 24, 39, 48, 50], [1, 28, 36, 37, 48, 49]]
(...)
  '''
  lines    = open(filenameIn).readlines()
  pattStr  = '(\d+)*' # [\d+.*]{6}\]  \d+[,]   \[\d+,\b*\]
  patt     = re.compile(pattStr)
  dezenasList = []
  for line in lines:
    if line[-1]=='\n':
      line = line[:-1]
    pos = line.find('[')
    if pos < 0:
      continue
    line = line[pos:]
    print line
    iterFound= patt.finditer(line)
    dezenas = []
    for matchObj in iterFound:
      number = matchObj.group(1)
      if number != None:
        if len(dezenas) == 6:
          dezenasList.append(dezenas[:])
          dezenas = []
        dezenas.append(number)

  #do the last 'append'
    if len(dezenas) == 6:
      dezenasList.append(dezenas[:])
    #else:  # taken out for generality purposes
      #raise 'could not append the last jogo in the row.'
  
  # printing the way it should be
  c = 0
  for dezenas in dezenasList:
    dezenasStr = map(tmpF, dezenas)
    dezenasStrList = ' '.join(dezenasStr)
    #c += 1
    print dezenasStrList


def compareTheTwoApostasFiles(filenameA, filenameB):
  print filenameA, filenameB
  fileA = open(filenameA)
  nOfLineA = 1
  print time.ctime().split(' ')[-2], 'nOfLineA', nOfLineA
  lineFileA = fileA.readline()
  while lineFileA:
    dezenasA = vpf.transformLineToDezenasList(lineFileA)
    if dezenasA == None:
      lineFileA = fileA.readline()
      continue
    #print 'Looking for equals of', dezenasA
    fileB = open(filenameB)
    lineFileB = fileB.readline(); maxCoincPerThisJogo = 0
    while lineFileB:
      dezenasB  = vpf.transformLineToDezenasList(lineFileB)
      #print lineFileB
      if dezenasB == None:
        lineFileB = fileB.readline()
        continue
      nOfEquals = 0; equalsList = []
      for dezenaA in dezenasA:
        if dezenaA in dezenasB:
          nOfEquals += 1; equalsList.append(dezenaA)
      if nOfEquals > maxCoincPerThisJogo:
        maxCoincPerThisJogo = nOfEquals
      print dezenasA, dezenasB
      print 'nOfEquals', nOfEquals, 'equalsList', equalsList
      lineFileB = fileB.readline()
    fileB.close()
    nOfLineA += 1
    if nOfLineA % 50 == 0:
      print time.ctime().split(' ')[-2], 'nOfLineA', nOfLineA
    print dezenasA, 'maxCoincPerThisJogo', maxCoincPerThisJogo
    lineFileA = fileA.readline()
  fileA.close()
  print 'Finished at', time.ctime().split(' ')[-2], 'N. of equals is', nOfEquals

def getNOfApostasAndPrice(nOfNextConc=Sena.getNOfLastJogo()+1, pricePer=1.75):
  filename    = '../Apostas/apostas-%04d.txt' %(nOfNextConc)
  apostasFile = open(filename)
  apostasLine = apostasFile.readline(); maxCoincPerThisJogo = 0; nOfApostas = 0
  while apostasLine:
    dezenas  = vpf.transformLineToDezenasList(apostasLine)
    if dezenas != None:
      nOfApostas += 1
    apostasLine = apostasFile.readline()
  totalPrice = nOfApostas * pricePer
  return nOfApostas, totalPrice

def compareTheTwoApostasFilesIni():
  filenameA = '../Apostas/apostas-0988.txt'
  filenameB = '../Apostas/aproveita-de-986-para-988.txt'
  compareTheTwoApostasFiles(filenameA, filenameB)



import combinador
def testDezenasDeOuro():
  '''
  This method calls randomSet and then calls 
  percentualDeJogosComUmaDasSeguintesDezenas(dList)
  (Based on the idea of 'dezenas de ouro' (too general to have any appeal!)
  '''
  dListOrig = [5,7,13,14,16,25,28,29,37,38,43,44,53,54,60]
  #dList = [1,4,6,12,17,24,28,29,37,38,43,44,53,54,60]
  dList = combinador.randomSet(15); coinc = 0
  for d in dList:
    if d in dListOrig:
      coinc += 1
  print 'dList', dList, 'len', len(dList)
  print 'coinc', coinc
  percentualDeJogosComUmaDasSeguintesDezenas(dList)

VERIFY_ACERTOS_DAS_APOSTAS  = 1
SORTEADAS_THRU_ALL_FILTERS = 2
COINCS_OF_APOSTAS_WITH_LAST_JOGO = 3
APROVEITA_CARTOES_JA_IMPRESSOS   = 4
VERIFY_EQUALS_IN_JOGOSFILES = 5
FREQ_ORDER_ALMOST_MANUAL    = 6
UPDATE_HIST_DB              = 7
CHECK_WITH_LARGER_CHAIN_1   = 8
DIMINISH_APOSTAS_SIZE_TO    = 9
HISTOGRAM_APOSTAS_FILE      = 10
def main():
  print '''Opções:
1 VERIFY_ACERTOS_DAS_APOSTAS
2 SORTEADAS_THRU_ALL_FILTERS
3 COINCS_OF_APOSTAS_WITH_LAST_JOGO
4 APROVEITA_CARTOES_JA_IMPRESSOS
5 VERIFY_EQUALS_IN_JOGOSFILES
6 FREQ_ORDER_ALMOST_MANUAL
7 UPDATE_HIST_DB
8 CHECK_WITH_LARGER_CHAIN_1
9 DIMINISH_APOSTAS_SIZE_TO
10 HISTOGRAM_APOSTAS_FILE
P/ SAIR qualquer outra tecla
'''
  choice = raw_input('Escolha a opção:')
  choice = int(choice)
  if choice == VERIFY_ACERTOS_DAS_APOSTAS:
    testWithLastJogo = False
    print 'Opção 1 VERIFY_ACERTOS_DAS_APOSTAS escolhida.'
    choice = raw_input('Para checar com lastJogoParaVerificarAcertosDasApostas.txt, escolha "S",\n para checar com o último jogo do sqlite, escolha "N" (Default="S") ')
    if choice in ['n','N']:
      testWithLastJogo = True
    imprimeAPartirDeNCoincidencias = 0
    choice = raw_input('Imprime apostas a partir de quantas coincidências? (0 a 6, default=0) ')
    try:
      choice = int(choice)
      if choice > 0 and choice <= 6:
        imprimeAPartirDeNCoincidencias = choice
    except ValueError:
      pass
    verifyAcertosDasApostas(testWithLastJogo, imprimeAPartirDeNCoincidencias)
  elif choice == SORTEADAS_THRU_ALL_FILTERS:
    sorteadasThruAllFilters()
  elif choice == COINCS_OF_APOSTAS_WITH_LAST_JOGO:
    coincsOfApostasWithLastJogo()
  elif choice == APROVEITA_CARTOES_JA_IMPRESSOS:
    aproveitaCartoesJaImpressosSemCoincComUltJogo()
  elif choice == VERIFY_EQUALS_IN_JOGOSFILES:
    verifyEqualsInJogosFiles()
  elif choice == FREQ_ORDER_ALMOST_MANUAL:
    freqOrderChosenForAlmostManualComb()
  elif choice == UPDATE_HIST_DB:
    updateSorteadasToHistDB()
  elif choice == CHECK_WITH_LARGER_CHAIN_1:
    verifyAcertosDasApostasWithLargerChain1(getLastJogoFromDB=False)
  elif choice == DIMINISH_APOSTAS_SIZE_TO:
    prepareDiminishApostasSizeTo()
  elif choice == HISTOGRAM_APOSTAS_FILE:
    histogramOfApostasFile()

if __name__ == '__main__':
  main()