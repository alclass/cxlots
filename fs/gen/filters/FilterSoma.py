#!/usr/bin/env python
#-*-coding:utf8-*-

justAllocateSomeMemoryBeforeImporting = 1
import Sena

jogosPool = Sena.JogosPool()
nOfLastJogoParam=Sena.getNOfLastJogo()

def passaQuantOfJogosWithMax(maxRepeatInTheRun, quantOfJogosWithThisMax):
  if maxRepeatInTheRun == 3:
    if quantOfJogosWithThisMax > 17:
      return False
  elif maxRepeatInTheRun == 4:
    if quantOfJogosWithThisMax > 3:
      return False
  return True

def analyzeParImparEtAl():
  filePath = '../Dados/fileVariacaoParImpar.txt'
  fileIn = open(filePath)
  line = fileIn.readline()
  rem5Dict = {}; rem3Dict = {}; parParImparImparDict = {}
  while line:
    if line[0]=='#':
      line = fileIn.readline()
      continue
    if line[-1] == '\n':
      line = line[:-1]
    pp = line.split('::')
    if len(pp) >= 2:
      wanted = pp[-1]
      pp = wanted.split(' ')
      if len(pp) >= 4:
        remainders5 = pp[-1]
        try:
          rem5Dict[remainders5]+=1
        except KeyError:
          rem5Dict[remainders5]=1
        remainders3 = pp[-2]
        try:
          rem3Dict[remainders3]+=1
        except KeyError:
          rem3Dict[remainders3]=1
        parParImparImpar = pp[-3]
        strNOfPares =  pp[-4]
        parParImparImpar = strNOfPares + parParImparImpar
        try:
          parParImparImparDict[parParImparImpar]+=1
        except KeyError:
          parParImparImparDict[parParImparImpar]=1
    line=fileIn.readline()

  filenameOut = '../Dados/analyzeVarParImpar.txt'; nOfLines = 0
  print 'Going to write file',  filenameOut 
  fileOut = open(filenameOut, 'w')
  rem5List = rem5Dict.keys()
  rem5List.sort(); total = 0
  line = 'Remainders of 5 (rem5Dict):'
  nOfLines += 1; fileOut.write(line + '\n')
  for remainderPatt in rem5List:
    quant = rem5Dict[remainderPatt]
    total += quant
    line = '%s q=%d' %(remainderPatt, quant)
    nOfLines += 1; fileOut.write(line + '\n')
  line = 'quantOfPatterns = %d, total = %d, nOfLines = %d' %(len(rem5List), total, nOfLines)
  nOfLines += 1; fileOut.write(line + '\n')
  rem3List = rem3Dict.keys()
  rem3List.sort(); total = 0
  line = 'Remainders of 3 (rem3Dict):'
  nOfLines += 1; fileOut.write(line + '\n')
  for remainderPatt in rem3List:
    quant = rem3Dict[remainderPatt]
    total += quant
    line = '%s q=%d' %(remainderPatt, quant)
    nOfLines += 1; fileOut.write(line + '\n')
  line = 'quantOfPatterns = %d, total = %d, nOfLines = %d' %(len(rem3List), total, nOfLines)
  nOfLines += 1; fileOut.write(line + '\n')
  parParImparImparList = parParImparImparDict.keys()
  parParImparImparList.sort(); total = 0
  line = 'parParImparImparDict:'
  nOfLines += 1; fileOut.write(line + '\n')
  for pPIIPattern in parParImparImparList:
    quant = parParImparImparDict[pPIIPattern]
    total += quant
    line = '%s q=%d' %(pPIIPattern, quant)
    nOfLines += 1; fileOut.write(line + '\n')
  line = 'quantOfPatterns = %d, total = %d, nOfLines = %d' %(len(parParImparImparList), total, nOfLines)
  nOfLines += 1; fileOut.write(line + '\n')
  line = '# OK, that is all for now folks.'
  nOfLines += 1; fileOut.write(line + '\n')
  fileOut.close()
  print nOfLines, 'lines recorded.'  
  
def genDepthOfDezenas():
  '''
  This method organizes the following info:
  dezn quant sixtil últ.dist.ocorrida dist.média dist.mín dist.máx
  últ.dist.ocorrida means the number of concursos passed between two appearances of the same dezena
  The method accounts for all occurrences of each dezena, and then it calculates the mín, máx and média of these "distances".
  '''  

  nOfOccursDict={}; maxDistBetweenOccursDict={}; minDistBetweenOccursDict={}
  ultDistBetweenOccursDict={}; posOfOccurDict={}; distsOfOccurDict={}; mediaDistBetweenOccursDict={}
  maxDoMax = 0
  minDoMax = 1000
  for d in range(1,61):
    nOfOccursDict[d]=0
    maxDistBetweenOccursDict[d]=0
    minDistBetweenOccursDict[d]=1000
    ultDistBetweenOccursDict[d]=0
    posOfOccurDict[d] = 0
    distsOfOccurDict[d] = []
  # traverse all concursos
  for nOfJogo in range(1, Sena.getNOfLastJogo() + 1):
    jogo = Sena.jogosPool.getJogo(nOfJogo)
    dezenas = jogo.getDezenas()
    for d in dezenas:
      nOfOccursDict[d] += 1
      if posOfOccurDict[d] > 0:
        ultDistBetweenOccursDict[d] = nOfJogo - posOfOccurDict[d]
        distsOfOccurDict[d].append(ultDistBetweenOccursDict[d])
      posOfOccurDict[d] = nOfJogo
      if ultDistBetweenOccursDict[d] > 0:
        if ultDistBetweenOccursDict[d] > maxDistBetweenOccursDict[d]:
          maxDistBetweenOccursDict[d] = ultDistBetweenOccursDict[d]
        if ultDistBetweenOccursDict[d] < minDistBetweenOccursDict[d]:
          minDistBetweenOccursDict[d] = ultDistBetweenOccursDict[d]

  filenameOut = '../Dados/analyzeVarDezenasDepth.txt'; nOfLines = 0
  print 'Going to write file',  filenameOut 
  fileOut = open(filenameOut, 'w')
  line = '# Stats for Dezenas Depth.'
  nOfLines += 1; fileOut.write(line + '\n')
  fileOut.write(line + '\n')
  medias = []
  for d in range(1,61):
    if maxDistBetweenOccursDict[d] > maxDoMax:
      maxDoMax = maxDistBetweenOccursDict[d]  
    if maxDistBetweenOccursDict[d] < minDoMax:
      minDoMax = maxDistBetweenOccursDict[d]  
    soma = 0
    for dist in distsOfOccurDict[d]:
      soma += dist 
    mediaDistBetweenOccursDict[d] = soma / (0.0 + len(distsOfOccurDict[d]))
    nOfOccurs = nOfOccursDict[d]
    ult = ultDistBetweenOccursDict[d]
    pos = posOfOccurDict[d]
    #min = minDistBetweenOccursDict[d]
    max = maxDistBetweenOccursDict[d]
    med = mediaDistBetweenOccursDict[d]
    medias.append(med)
    line = '%d %3d x%3d u=%2d m=%2d a=%g' %(d, pos, nOfOccurs, ult, max, med)
    nOfLines += 1; fileOut.write(line + '\n')
  mediasNA = numpy.array(medias)
  mediaDaMedia = mediasNA.sum() / (0.0 + len(mediasNA))
  dpDaMedia = mediasNA.std()
  minDaMedia = mediasNA.min()
  maxDaMedia = mediasNA.max()
  line = 'mediaDaMedia %g  dpDaMedia %g \n minDaMedia %g   maxDaMedia %g' %(mediaDaMedia, dpDaMedia, minDaMedia, maxDaMedia)
  nOfLines += 2; fileOut.write(line + '\n')
  line = 'minDoMax %d     maxDoMax %d' %(minDoMax, maxDoMax)
  nOfLines += 1; fileOut.write(line + '\n')
  line = '# OK, that is all for now folks (nOfLines=%d).' %(nOfLines)
  nOfLines += 1; fileOut.write(line + '\n')
  fileOut.close()
  print nOfLines, 'lines recorded.'  

def getDesvioPadraoMinMax(jogo, nOfLastJogo=nOfLastJogoParam):
  '''
  returns (dpMin, dpMax)
  '''
  # rule 1: looks at the immediate previous one
  difs = []
  for i in range(1,51):
    jogoComp = jogosPool.getJogo(nOfLastJogo - i)
    #print 'jogoComp', jogoComp
    dp, difComp = atSt.calcDesvioPadraoDas6(jogo, jogoComp)
    #print 'dp, difComp', dp, difComp
    difs.append(difComp)
  difNA = numpy.array(difs)
  difMin = difNA.min() 
  difMax = difNA.max()
  dpMin = dp - difMin
  dpMax = dp + difMax
  #print 'dpMin, dpMax',  dpMin, dpMax
  return dpMin, dpMax

def isToExcludeSomeParImpar(nDeRefBackwardJogo=Sena.getNOfLastJogo()):
  '''
  Data Stru. => list with excluded number of evens eg [0, 2, 6]
  '''
  excludeList = [0,6] # 0 nºs pares e 6 nºs pares
  jogoComp = Sena.jogosPool.getJogo(nDeRefBackwardJogo)
  nDePares = jogoComp.getNDePares()
  #print 'nDeRefBackwardJogo', nDeRefBackwardJogo, jogoComp, 'nDePares', nDePares 
  if nDePares in [0,6]:
    return excludeList 
  if nDePares == 5:
    excludeList.append(nDePares)
    return excludeList 
  if nDePares == 1:
    excludeList.append(nDePares)
    return excludeList
  acc = {}
  acc[2] = 0; acc[3] = 0; acc[4] = 0
  # logically, the if below is not needed, but code may change in the future (the way it is is for clearness) 
  if nDePares in [2,3,4]:
    acc[nDePares] += 1
  for i in range(1,4): # go backwards 4 jogosfs (3 here + 1 above)
    backwardJogo = Sena.jogosPool.getJogo(nDeRefBackwardJogo-i)
    nDePares = backwardJogo.getNDePares()
    #print backwardJogo, 'nDePares', nDePares 
    if nDePares < 2 or nDePares > 4:
      continue
    acc[nDePares] += 1
  for i in range(2,5):
    if acc[i] == 4:
      excludeList.append(i) 
      return excludeList
  return excludeList

def getNDeParesMinMax(nOfLastJogo=nOfLastJogoParam):
  '''
  returns (ndpMin, ndpMax)
  '''
  paresComp = [];     ndpMin = 0;     ndpMax = 6
  for i in range(1,20):
    jogoComp = jogosPool.getJogo(nOfLastJogo - i)
    paresComp.append(jogoComp.getNDePares())
    
  if 0 in paresComp: # least frequent, come first in if
    ndpMin = 1
  elif 1 in paresComp:
    ndpMin = 2
  if 6 in paresComp: # least frequent, come first in if
    ndpMax = 5
  elif 5 in paresComp:
    ndpMax = 4
 # print 'ndpMin, ndpMax',  ndpMin, ndpMax
  return ndpMin, ndpMax

def organizeSixtils(dezenaHistG):
  '''
    Note:  There were Quartils in previous development, now they are Sixtils
  '''
  # fine, let's organize the Sixtils
  dezenas = dezenaHistG.keys()
  dezenas.sort(); dezenasQuant = []
  for dezena in dezenas:
    dezenasQuant.append(dezenaHistG[dezena])
  dezenasQuantNA = numpy.array(dezenasQuant)
  dezenasQuantNA.sort()
  sup = dezenasQuantNA.max() #dezenasQuantNA[59]
  inf = dezenasQuantNA.min() #dezenasQuantNA[0]
  dist = sup - inf; desloca = 0
  while dist % 6 != 0:
    dist -= 1
    desloca += 1
  sexto = dist / 6; points = []; points.append(inf-1); pos = inf + desloca; sixtils = []; sixtils.append([])
  #for i in range(1,7):
  # CORRECT HERE
  posSextos = map(pos + sexto, range(1,7))
  points.append(pos)
  sixtils.append([]*6)
  #print 'len(dezenasQuantNA)', len(dezenasQuantNA)
  #print 'len(points)', len(points) 
  for dezena in range(1, 61):
    quant = dezenaHistG[dezena]
    for j in range(1,7):  # quartis[0] is not used!
      if quant > points[j-1] and quant <= points[j]:
        sixtils[j].append(dezena)
  return sixtils

dezenaHistG = {}; jaFeitoSixtil = 1
for dezena in range(1, 61):
  dezenaHistG[dezena] = 0

def generateSixtilsIterative(ateJogoN):
  global dezenaHistG, jaFeitoSixtil
  if jaFeitoSixtil == ateJogoN:
    return dezenaHistG 
  for jogoN in range(jaFeitoSixtil, ateJogoN+1):
    jogo = jogosPool.getJogo(jogoN)
    dezenas = jogo.getDezenas()
    for dezena in dezenas:
      dezenaHistG[dezena] += 1
  jaFeitoSixtil = ateJogoN
  sixtils = organizeSixtils(dezenaHistG)
  #print ' [in analyzer] sixtils', sixtils
  return sixtils 

sixtilsGenerated = False; sixtils = []
def generateSixtils():
  global sixtilsGenerated, sixtils
  if sixtilsGenerated:
    return sixtils
  dezenaHistG = atSt.obtemHistGDas60()
  sixtils = organizeSixtils(dezenaHistG)
  if type(sixtils[0]) == type([]):
    sixtilsGenerated = True
  return sixtils 

def getSomaDesceOuSobe(jogo, nOfLastJogo=nOfLastJogoParam):
  '''
  returns True if sobe (boolean)
  '''
  difs = []
  soma = jogo.soma()
  for i in range(1,4):
    jogoComp = jogosPool.getJogo(nOfLastJogo - i)
    somaComp = jogoComp.soma()
    difs.append(soma - somaComp)
    soma = somaComp
  contDesce = 0; contSobe = 0 
  for dif in difs:
    if dif == -1:
      contDesce += 1
    if dif == 1:
      contSobe += 1
  if contSobe == 3:
    return True
  if contDesce == 3:
    return False
  return None

def getLinColDataStru():
  '''
  returns d1d2DataStru
    relative to filtro LINHAS x COLUNAS

  Data Structure
  Inner histogram eg 0:1 1:1 2:1 4:1 5:2    1:1 4:1 6:2 7:1 8:1
  
  The d1d2DataStru:
  * dezena abaixo e o dígito da esquerda
  (dezena-0, repetMin, repetMax)   
  (dezena-1, repetMin, repetMax)
  ...
  (dezena-5, repetMin, repetMax)

  * unidade abaixo é o dígito da direita
  unidade-0,
  unidade-1, repetMin, repetMax)
  ...
  (unidade-9, repetMin, repetMax)

  '''
  pass
  return None

def getNDeIguaisJogoAnt():
  '''
  returns iguaisAntStru
  '''
  pass

def getHistogramaEvolutivoStru():
  '''
  returns histEvolStru
  '''
  pass

histGStd = {}
for i in range(2,31):
  histGStd[i]=0

def analyze1Std():
  fileDesvioPadraoDas6 = open('../Dados/fileDesvioPadraoDas6.txt', 'r')
  stdArray = []; c=0 #; dpAnt = 0
  line = 'start'
  while line:
    line = fileDesvioPadraoDas6.readline()
    c+=1
    pp = line.split('\t')
    if len(pp) > 0 and len(pp[-1].split('.'))== 2:
      #print c,
      std = float(pp[-1])
      stdInt = int(std)
      histGStd[stdInt]+=1
      stdArray.append(std)
      #stdAntArray.append(stdAnt)
      #dpAnt = std

  #print
  print 'Processing statistics, please wait.'
  stdNA = numpy.array(stdArray)
  min = stdNA.min()
  max = stdNA.max()
  sum = stdNA.sum()
  avg = sum / len(stdNA)
  std = stdNA.std()
  
  print '''  %d   min = %g \t max = %g \t sum = %g \t avg = %g \t std = %g
'''  %(c, min, max, sum, avg, std)
  histIndices = histGStd.keys()
  histIndices.sort()
  print '=========='
  print 'std :: quant'
  print '=========='
  total = 0
  for i in histIndices:
    quant = histGStd[i]
    total += quant
    print '%2d ::  %3d' %(i, quant) 
  print 'total', total

def getSdStats(difArray):
  # first dif is zero, ie, it's not either going up or down
  sdArray = []; sdArray.append(0)
  for dif in difArray[1:]:
    sobeDesce = 0
    if dif > 0:
      sobeDesce = 1
    elif dif < 0:
      sobeDesce = -1
    sdArray.append(sobeDesce)

  desceSobeNA = numpy.array(sdArray)
  sdAnt = 0; contSobe = 0; contDesce = 0; maxDesce = -10; maxSobe = -10
  for desceSobe in desceSobeNA:
    if desceSobe == sdAnt:
      if desceSobe > 0:
        contSobe += 1
      elif desceSobe < 0:
        contDesce += 1
    else:
      if desceSobe > 0:
        if contDesce > maxDesce:
          maxDesce = contDesce
        contSobe = 1
      elif desceSobe < 0:
        if contSobe > maxSobe:
          maxSobe = contSobe
        contDesce = 1
    sdAnt = desceSobe 

  sdAvg = desceSobeNA.sum() /  (0.0 + len(desceSobeNA))
  sdStd = desceSobeNA.std()

  return maxDesce, maxSobe, sdAvg, sdStd

def fillInStats(self, arrayIn, difArray, is64=False):
  if is64:
    na     = numpy.array(arrayIn, long)
  else:
    na     = numpy.array(arrayIn)  # it's gonna be 32bits (max is ~ 4.3*10**9 or (2**32-1))
  self.min = na.min()
  self.max = na.max()
  self.avg = na.sum() / (0.0 + len(na))
  self.std = na.std()
  maxDesce, maxSobe, sdAvg, sdStd = getSdStats(difArray)
  self.maxDesce = maxDesce
  self.maxSobe  = maxSobe
  self.sdAvg    = sdAvg
  self.sdStd    = sdStd
  difNA       = numpy.array(difArray)
  self.difMin = difNA.min()
  self.difMax = difNA.max()
  self.difAvg = difNA.sum() / (0.0 + len(na))
  self.difStd = difNA.std()
  return self

class ClassSomaEtAlStats():
  def __init__(self, arrayIn, difArray, is64=False):
    fillInStats(self, arrayIn, difArray, is64)

def getNumbersWithSplitSpace(ppStr):
  pp = ppStr.split(' ')
  numbers = []
  for part in pp:
    if part == '':
      continue
    try:
      number = float(part)
      numbers.append(number)
    except ValueError:
      continue
  return numbers

def gatherSomaEtAlStats(upToXNOfJogo=None):
  '''
  gatherSomaEtAlStats(upToXNOfJogo=None)
  '''
  # print 'SHOULD ENTER HERE (gatherSomaStats()) ONLY ONCE, via the SomaObj class singleton.'
  # jogo          :: soma somaDif :: std stdDif :: lexGrIndex  lgiCubicDif
  # 6 07 13 19 22 40 47 :: 148   58 ::  14.27 -1.14 :: 09949449 17.82
  somaArray = []; somaDifArray = []
  stdArray  = []; stdDifArray  = []
  lgiArray  = []; lgiDifArray  = []

  fileVarSoma = open('../Dados/fileVarSomaEtAl.txt', 'r')
  line = fileVarSoma.readline()
  while line:
    pp = line.split('::')
    if len(pp) != 4:
      continue
    if upToXNOfJogo != None:
      jogoStr = pp[0]
      nDoJogoHere = int(jogoStr.split(' ')[0])
      # do untill asked ie until upToXNOfJogo
      if nDoJogoHere > upToXNOfJogo:
        break
    # Appending to somaArray and somaDifArray
    numbers = getNumbersWithSplitSpace(pp[1])
    soma    = int(numbers[0])
    somaArray.append(soma)
    somaDif = int(numbers[1])
    somaDifArray.append(somaDif)
    # Appending to stdArray and stdDifArray
    numbers = getNumbersWithSplitSpace(pp[2])
    std     = numbers[0]
    stdArray.append(std)
    stdDif  = numbers[1]
    stdDifArray.append(stdDif)
    # Appending to lgiArray and lgiDifArray
    numbers = getNumbersWithSplitSpace(pp[3])
    lgi     = int(numbers[0])
    lgiArray.append(lgi)
    lgiDif  = numbers[1]
    lgiDifArray.append(lgiDif)
    # reading a new line and looping on
    line = fileVarSoma.readline()

  # ==========================
  # gathering Std Stats
  # ==========================
  somaStats = ClassSomaEtAlStats(somaArray, somaDifArray)
  stdStats  = ClassSomaEtAlStats(stdArray,  stdDifArray)
  #print 'size lgiArray lgiDifArray', len(lgiArray), len(lgiDifArray)
  is64 = True
  lgiStats  = ClassSomaEtAlStats(lgiArray,  lgiDifArray, is64)

  return somaStats, stdStats, lgiStats

def pickUpThoseNeverOccurred(patternsLinhaFoundDict):
  allFoundLinhaPatterns = patternsLinhaFoundDict.keys()
  allFoundLinhaPatterns.sort()
  allSixtilPatts = sf.arrangeSixtilPatternsSoma6()
  
  # make the difference set ie  C = A - B
  i=0
  while i < len(allSixtilPatts):
    sixtilPatt = allSixtilPatts[i]
    if sixtilPatt in allFoundLinhaPatterns:
      del allSixtilPatts[i]
    else:
      i+=1
  patternsLinhaNeverOccurred = list(allSixtilPatts)
  return patternsLinhaNeverOccurred

def getLinColPatternObj():
  fileVarLinCol = open('../Dados/fileVarLinhaColuna.txt', 'r')
  lines = fileVarLinCol.readlines()
  patternsLinhaFoundDict = {}
  patternsColunaFoundDict = {}
  for line in lines:
    pp = line.split('\t')
    if len(pp) > 1:
      linPatt = pp[-2]
      colPatt = pp[-1]
      linPatt = linPatt.replace(' ','')
      if len(colPatt) > 0 and colPatt[-1]=='\n':
          colPatt = colPatt[:-1]
      # LINHAS
      try:
        patternsLinhaFoundDict[linPatt] += 1
      except KeyError:
        patternsLinhaFoundDict[linPatt] = 1
      # COLUNAS
      try:
        patternsColunaFoundDict[colPatt] += 1
      except KeyError:
        patternsColunaFoundDict[colPatt] = 1
  
  #print patternsColunaFoundDict
  patternsLinhaNeverOccurred = pickUpThoseNeverOccurred(patternsLinhaFoundDict)
  
  return patternsLinhaFoundDict, patternsColunaFoundDict, patternsLinhaNeverOccurred # patternsColunaNeverOccurred does not exist as yet (would be too large in memory)

class parImparPatternObj(object):
  # singleton
  _instance = None
  def __new__(self, *args, **kargs):
    if self._instance is None: 
      self._instance = object.__new__(self, *args, **kargs)
      self._instance.initParImparPatternObj()
    return self._instance
  def initParImparPatternObj(self):
    tuple9 = verPatternsOfCombinationsOfRemainder5()
    # return sobrando5, foundP5, patterns5, sobrando3, foundP3, patterns3, sobrandoPI, foundPI, patternsPI
    self.sobrando5, self.foundP5, self.patterns5, self.sobrando3, self.foundP3, self.patterns3, self.sobrandoPI, self.foundPI, self.patternsPI = tuple9
  def lookUpDivergePattern(self, jogo):
    nDePares = jogo.getNDePares()
    if nDePares == 3:
      goBackwards = 4
    elif nDePares in [2, 4]:
      goBackwards = 2
    #elif nDePares in [1,5]:
    else:
      goBackwards = 1
    nDoLastJogo = Sena.getNOfLastJogo();  coincide = 0
    for i in range(goBackwards):
      nDoJogo = nDoLastJogo - i
      jogoN = Sena.jogosPool.getJogo(nDoJogo)
      if nDePares == jogoN.getNDePares():
        coincide += 1
    if coincide == goBackwards:
      return False
    return True

  maxPattern3Deja = False
  maxPatternP3 = ''; maxOccurOfPattern3 = 0
  def getMaxPattern3(self):
    if self.maxPattern3Deja:
      return self.maxPattern3, self.maxOccurOfPattern3
    for patt in self.foundP3:
      quant = self.patterns3[patt]
      if quant > self.maxOccurOfPattern3:
        self.maxOccurOfPattern3 = quant
        self.maxPattern3 = patt
    self.maxPattern3Deja = True
    return self.maxPattern3, self.maxOccurOfPattern3
  def equalsMaxP3Occurs(self, pattIn):
    tuple2 = self.getMaxPattern3()
    if tuple2[0] == pattIn:
      return True
    return False
  
  maxPattern5Deja = False
  maxPatternP5 = ''; maxOccurOfPattern5 = 0
  def getMaxPattern5(self):
    if self.maxPattern5Deja:
      return self.maxPattern5, self.maxOccurOfPattern5
    for patt in self.foundP5:
      quant = self.patterns5[patt]
      if quant > self.maxOccurOfPattern5:
        self.maxOccurOfPattern5 = quant
        self.maxPattern5 = patt
    self.maxPattern5Deja = True
    return self.maxPattern5, self.maxOccurOfPattern5
  def equalsMaxP5Occurs(self, pattIn):
    tuple2 = self.getMaxPattern5()
    if tuple2[0] == pattIn:
      return True
    return False

  maxPatternPIDeja = False
  maxPatternPI = ''; maxOccurOfPatternPI = 0
  def getMaxPatternPI(self):
    if self.maxPatternPIDeja:
      return self.maxPatternPI, self.maxOccurOfPatternPI
    for patt in self.foundPI:
      quant = self.patternsPI[patt]
      if quant > self.maxOccurOfPatternPI:
        self.maxOccurOfPatternPI = quant
        self.maxPatternPI = patt
    self.maxPatternPIDeja = True
    return self.maxPatternPI, self.maxOccurOfPatternPI
  def equalsMaxPIOccurs(self, pattIn):
    tuple2 = self.getMaxPatternPI()
    if tuple2[0] == pattIn:
      return True
    return False

  def __str__(self):
    outStr = ''
    outStr += 'sobrando5' + str(self.sobrando5) + '\n'
    outStr += 'sobrando3' + str(self.sobrando3) + '\n'
    outStr += 'sobrandoPI' + str(self.sobrandoPI) + '\n'
    return outStr

import combinador
def verPatternsOfCombinationsOfRemainder5():
  filePath = open('../Dados/fileVariacaoParImpar.txt', 'r')
  patterns5 = {}
  patterns3 = {}
  patternsPI = {}
  lines = filePath.readlines()
  for line in lines:
    if line[0]=='#':
      continue
    if line[-1]=='\n':
      line = line[:-1]
    pp = line.split(' ')
    if len(pp) < 4:
      continue
    patt5  = pp[-1]
    patt3  = pp[-2]
    pattPI = pp[-3]
    try:
      patterns5[patt5] += 1 
    except KeyError:
      patterns5[patt5] = 1 
    try:
      patterns3[patt3] += 1 
    except KeyError:
      patterns3[patt3] = 1 
    try:
      patternsPI[pattPI] += 1 
    except KeyError:
      patternsPI[pattPI] = 1 
  
  foundP5  = patterns5.keys()
  foundP5.sort()
  foundP3  = patterns3.keys()
  foundP3.sort()
  foundPI  = patternsPI.keys()
  foundPI.sort()
  allP5  = combinador.combinationsOfRemainder5()
  allP3  = combinador.combinationsOfRemainder3()
  allPPI = combinador.combinationsOfParParImparImpar()
  sobrando5, sobrando3, sobrandoPI = [], [], []
  for pattern in allP5:
    if pattern not in foundP5:
      sobrando5.append(pattern) 
  for pattern in allP3:
    if pattern not in foundP3:
      sobrando3.append(pattern) 
  for pattern in allPPI:
    if pattern not in foundPI:
      sobrandoPI.append(pattern)
  #print 'sobrando5', sobrando5
  #print 'foundP5', foundP5
  #print 'sobrando3', sobrando3
  #print 'foundP3', foundP3
  #print 'sobrandoPI', sobrandoPI
  #print 'foundPI', foundPI
  return sobrando5, foundP5, patterns5, sobrando3, foundP3, patterns3, sobrandoPI, foundPI, patternsPI

def nextDezenaForNoseDiag(dezena):
  if dezena > 50:
    return None
  if dezena % 10 == 0:
    return dezena + 1
  dezena  += 11
  return dezena

def getDepthForNoseDiag(dezenas, index, depth):
  if index == 5:
    return depth, index
  next = nextDezenaForNoseDiag(dezenas[index])
  if next == None:
    return depth, 5  # ie, Nose diagonals do not continue at the end for dezenas > 51
  if next == dezenas[index+1]:
    return getDepthForNoseDiag(dezenas, index+1, depth+1)
  return depth, index

def initNoseDiagonals():
  '''
  NOSE means NOroeste -> SudEste
  '''
  # init'ing NOSE diagonals
  oneToTen = xrange(1,11); nose = [None]*10
  for i in oneToTen:
    nose[i-1] = [i]
    print i, 'nose', nose[i-1]
  for i in oneToTen:
    d = i
    for j in xrange(2,7):
      if d%10==0:
        d += 1
      else:
        d += 11
      if d > 60:
        d-=10
      nose[i-1].append(d)
  '''
  # printing nose 2D matrix
  for i in oneToTen:
    for j in xrange(1,7):
      d = nose[i-1][j-1]
      print '%2d ' %(d),
    print
  '''
  return nose

def searchingJogosNOSE():
  '''
  NOSE means NOroeste -> SudEste
  Until now (conc. 986 / 2008-07-13) no NOSE diagonal has been found
  '''	
  nose2D = initNoseDiagonals(); oneToSix = xrange(1,7)
  nDoLastJogo = Sena.getNOfLastJogo()
  maxDepthInHistory = 0; maxDepthInHistoryNDoJogo = None; depthDict = {}
  for nDoJogo in xrange(1,nDoLastJogo+1):
    jogo = Sena.jogosPool.getJogo(nDoJogo)
    maxDepthInJogo = jogo.getNOSEDepth()
    try:
      depthDict[maxDepthInJogo] += 1
    except KeyError:
      depthDict[maxDepthInJogo] = 1
    if maxDepthInJogo > 0:
      print  jogo, 'maxDepthInJogo', maxDepthInJogo
    if maxDepthInJogo > maxDepthInHistory:
      maxDepthInHistory = maxDepthInJogo
      maxDepthInHistoryNDoJogo = nDoJogo
    dezenas = jogo.getDezenas()
    dezenas.sort()
    for i in oneToSix:
      if dezenas[0]==i:
        #print 'in jogo', nDoJogo, dezenas
	if dezenas == nose2D[i-1]:
          print 'Found NOSE', i, 'with jogo', jogo
  print 'first maxDepthInHistory', maxDepthInHistory, 'in jogo', maxDepthInHistoryNDoJogo
  print 'depthDict', depthDict

def searchingPrimes():
  '''
  searchingPrimes
  '''	
  primes = Sena.PRIMES_TILL_60
  print 'primes', primes, 'len', len(primes)
  nDoLastJogo = Sena.getNOfLastJogo()
  maxNOfPrimesInHistory = 0; maxNOfPrimesInHistoryNDoJogo = None; primesDict = {}
  for nDoJogo in xrange(1,nDoLastJogo+1):
    jogo = Sena.jogosPool.getJogo(nDoJogo)
    nOfPrimes = jogo.getNOfPrimes()
    if nOfPrimes > maxNOfPrimesInHistory:
      maxNOfPrimesInHistory = nOfPrimes
    try:
      primesDict[nOfPrimes] += 1
    except KeyError:
      primesDict[nOfPrimes] = 1
    if nOfPrimes > 1:
      print  jogo, 'nOfPrimes', nOfPrimes
  print 'primesDict', primesDict

def analyzeLinhaColuna1():
  allFoundPatterns, patternsNeverOccurred = analyzeLinhaColuna()
  print allFoundPatterns, patternsNeverOccurred
  print 'trying tentils'
  #tentils = sf.arrangeTentilPatternsSoma6()
  print 'tentils'#, tentils

def testGenerateSixtils():
  sixtils = generateSixtils()
  nDoLastJogo = Sena.getNOfLastJogo()
  for nDoJogo in range(101, nDoLastJogo):
    jogo = jogosPool.getJogo(nDoJogo)
    print jogo,
    sixtils = generateSixtilsIterative(nDoJogo - 1) 
    dezenas = jogo.getDezenas(); acc = []
    for i in range(7):
      acc.append(0)
    for dezena in dezenas:
      for i in range(1,7):
        if dezena in sixtils[i]:
          acc[i]+=1
          #print 'dezena', dezena, 'no quartil', i
    for i in range(1, 7):
      print acc[i],
    print

if __name__ == '__main__':
  #piObj = parImparPatternObj()
  #print piObj
  #co=Controller()
  #lgi_b1idx=co.getLgiStats()
  #print 'lgi_b1idx.avg', lgi_b1idx.avg
  #searchingJogosNOSE()
  searchingPrimes()