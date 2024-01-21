#!/usr/bin/env python3
"""

"""
import Sena
import combinador
a=1

jogosPool = Sena.JogosPool()
n_of_last_jogo_param=Sena.getNOfLastJogo()


def passa_quant_of_jogos_with_max(max_repeat_in_the_run, quant_of_jogos_with_this_max):
  if max_repeat_in_the_run == 3:
    if quant_of_jogos_with_this_max > 17:
      return False
  elif max_repeat_in_the_run == 4:
    if quant_of_jogos_with_this_max > 3:
      return False
  return True


def analyze_par_impar_et_al():
  file_path = '../Dados/fileVariacaoParImpar.txt'
  file_in = open(file_path)
  line = file_in.readline()
  rem5_dict, rem3_dict, par_par_impar_impar_dict = {}, {}, {}
  while line:
    if line[0]=='#':
      line = file_in.readline()
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
          rem5_dict[remainders5]+=1
        except KeyError:
          rem5_dict[remainders5]=1
        remainders3 = pp[-2]
        try:
          rem3_dict[remainders3]+=1
        except KeyError:
          rem3_dict[remainders3]=1
        par_par_impar_impar = pp[-3]
        str_n_of_pares =  pp[-4]
        par_par_impar_impar = str_n_of_pares + par_par_impar_impar
        try:
          par_par_impar_impar_dict[par_par_impar_impar]+=1
        except KeyError:
          par_par_impar_impar_dict[par_par_impar_impar]=1
    line=file_in.readline()


def verify_file(rem5_dict):
  filename_out = '../Dados/analyzeVarParImpar.txt'
  n_of_lines = 0
  print('Going to write file',  filename_out)
  file_out = open(filename_out, 'w')
  rem5_list = rem5_dict.keys()
  rem5_list.sort()
  total = 0
  line = 'Remainders of 5 (rem5_dict):'
  n_of_lines += 1; file_out.write(line + '\n')
  for remainder_patt in rem5_list:
    quant = rem5_dict[remainder_patt]
    total += quant
    line = '%s q=%d' %(remainder_patt, quant)
    n_of_lines += 1; file_out.write(line + '\n')
  line = 'quantOfPatterns = %d, total = %d, n_of_lines = %d' %(len(rem5_list), total, n_of_lines)
  n_of_lines += 1; file_out.write(line + '\n')
  rem3_list = rem3_dict.keys()
  rem3_list.sort(); total = 0
  line = 'Remainders of 3 (rem3_dict):'
  n_of_lines += 1; file_out.write(line + '\n')
  for remainder_patt in rem3_list:
    quant = rem3_dict[remainder_patt]
    total += quant
    line = '%s q=%d' %(remainder_patt, quant)
    n_of_lines += 1; file_out.write(line + '\n')
  line = 'quantOfPatterns = %d, total = %d, n_of_lines = %d' %(len(rem3_list), total, n_of_lines)
  n_of_lines += 1; file_out.write(line + '\n')
  par_par_impar_impar_list = par_par_impar_impar_dict.keys()
  par_par_impar_impar_list.sort(); total = 0
  line = 'par_par_impar_impar_dict:'
  n_of_lines += 1; file_out.write(line + '\n')
  for pPIIPattern in par_par_impar_impar_list:
    quant = par_par_impar_impar_dict[pPIIPattern]
    total += quant
    line = '%s q=%d' %(pPIIPattern, quant)
    n_of_lines += 1; file_out.write(line + '\n')
  line = 'quantOfPatterns = %d, total = %d, n_of_lines = %d' %(len(par_par_impar_impar_list), total, n_of_lines)
  n_of_lines += 1; file_out.write(line + '\n')
  line = '# OK, that is all for now folks.'
  n_of_lines += 1; file_out.write(line + '\n')
  file_out.close()
  print(n_of_lines, 'lines recorded.')


def gen_depth_of_dezenas1():
  """
  This method organizes the following info:
  dezn quant sixtil últ.dist.ocorrida dist.média dist.mín dist.máx
  últ.dist.ocorrida means the number of concursos passed between two appearances of the same dezena
  The method accounts for all occurrences of each dezena, and then it calculates the mín, máx and média of these "distances".
  """
  n_of_occurs_dict, max_dist_between_occurs_dict, min_dist_between_occurs_dict = {}, {}, {}
  ult_dist_between_occurs_dict, pos_of_occur_dict, dists_of_occur_dict = {}, {}, {}
  max_do_max = 0
  min_do_max = 1000
  for d in range(1, 61):
    n_of_occurs_dict[d]=0
    max_dist_between_occurs_dict[d] = 0
    min_dist_between_occurs_dict[d] = 1000
    ult_dist_between_occurs_dict[d] = 0
    pos_of_occur_dict[d] = 0
    dists_of_occur_dict[d] = []
  # traverse all concursos
  for n_of_jogo in range(1, Sena.getNOfLastJogo() + 1):
    jogo = Sena.jogosPool.getJogo(n_of_jogo)
    dezenas = jogo.getDezenas()
    for d in dezenas:
      n_of_occurs_dict[d] += 1
      if pos_of_occur_dict[d] > 0:
        ult_dist_between_occurs_dict[d] = n_of_jogo - pos_of_occur_dict[d]
        dists_of_occur_dict[d].append(ult_dist_between_occurs_dict[d])
      pos_of_occur_dict[d] = n_of_jogo
      if ult_dist_between_occurs_dict[d] > 0:
        if ult_dist_between_occurs_dict[d] > max_dist_between_occurs_dict[d]:
          max_dist_between_occurs_dict[d] = ult_dist_between_occurs_dict[d]
        if ult_dist_between_occurs_dict[d] < min_dist_between_occurs_dict[d]:
          min_dist_between_occurs_dict[d] = ult_dist_between_occurs_dict[d]

def gen_depth_of_dezenas2():
  filename_out = '../Dados/analyzeVarDezenasDepth.txt'
  n_of_lines = 0
  print('Going to write file',  filename_out)
  file_out = open(filename_out, 'w')
  line = '# Stats for Dezenas Depth.'
  n_of_lines += 1; file_out.write(line + '\n')
  file_out.write(line + '\n')
  medias = []
  for d in range(1, 61):
    if max_dist_between_occurs_dict[d] > max_do_max:
      max_do_max = max_dist_between_occurs_dict[d]
    if max_dist_between_occurs_dict[d] < min_do_max:
      min_do_max = max_dist_between_occurs_dict[d]
    soma = 0
    for dist in dists_of_occur_dict[d]:
      soma += dist 
    mediaDistBetweenOccursDict[d] = soma / (0.0 + len(dists_of_occur_dict[d]))
    nOfOccurs = n_of_occurs_dict[d]
    ult = ult_dist_between_occurs_dict[d]
    pos = pos_of_occur_dict[d]
    #min = min_dist_between_occurs_dict[d]
    max = max_dist_between_occurs_dict[d]
    med = mediaDistBetweenOccursDict[d]
    medias.append(med)
    line = '%d %3d x%3d u=%2d m=%2d a=%g' %(d, pos, nOfOccurs, ult, max, med)
    n_of_lines += 1; file_out.write(line + '\n')
  medias_na = numpy.array(medias)
  media_da_media = medias_na.sum() / (0.0 + len(medias_na))
  dp_da_media = medias_na.std()
  min_da_media = medias_na.min()
  max_da_media = medias_na.max()
  line = ('media_da_media %g  dp_da_media %g \n min_da_media %g   max_da_media %g' %
         (media_da_media, dp_da_media, min_da_media, max_da_media))
  n_of_lines += 2
  file_out.write(line + '\n')
  line = 'min_do_max %d     max_do_max %d' %(min_do_max, max_do_max)
  n_of_lines += 1; file_out.write(line + '\n')
  line = '# OK, that is all for now folks (n_of_lines=%d).' %(n_of_lines)
  n_of_lines += 1; file_out.write(line + '\n')
  file_out.close()
  print(n_of_lines, 'lines recorded.')


def get_desvio_padrao_min_max(jogo, n_of_last_jogo=n_of_last_jogo_param):
  """
  returns (dpMin, dpMax)

  """
  # rule 1: looks at the immediate previous one
  difs = []
  for i in range(1,51):
    jogo_comp = jogosPool.getJogo(n_of_last_jogo - i)
    #print 'jogo_comp', jogo_comp
    dp, dif_comp = atSt.calcDesvioPadraoDas6(jogo, jogo_comp)
    #print 'dp, dif_comp', dp, dif_comp
    difs.append(dif_comp)
  difNA = numpy.array(difs)
  difMin = difNA.min() 
  difMax = difNA.max()
  dpMin = dp - difMin
  dpMax = dp + difMax
  #print 'dpMin, dpMax',  dpMin, dpMax
  return dpMin, dpMax


def is_to_exclude_some_par_impar(n_de_ref_backward_jogo=Sena.getNOfLastJogo()):
  """
  Data Stru. => list with excluded number of evens eg [0, 2, 6]

  """
  exclude_list = [0,6] # 0 nºs pares e 6 nºs pares
  jogo_comp = Sena.jogosPool.getJogo(n_de_ref_backward_jogo)
  n_de_pares = jogo_comp.getNDePares()
  #print 'nDeRefBackwardJogo', nDeRefBackwardJogo, jogo_comp, 'n_de_pares', n_de_pares
  if n_de_pares in [0,6]:
    return exclude_list
  if n_de_pares == 5:
    exclude_list.append(n_de_pares)
    return exclude_list
  if n_de_pares == 1:
    exclude_list.append(n_de_pares)
    return exclude_list
  acc = {}
  acc[2] = 0; acc[3] = 0; acc[4] = 0
  # logically, the if below is not needed, but code may change in the future (the way it is is for clearness) 
  if n_de_pares in [2,3,4]:
    acc[n_de_pares] += 1
  for i in range(1,4): # go backwards 4 jogosfs (3 here + 1 above)
    backwardJogo = Sena.jogosPool.getJogo(n_de_ref_backward_jogo - i)
    n_de_pares = backwardJogo.getNDePares()
    #print backwardJogo, 'n_de_pares', n_de_pares
    if n_de_pares < 2 or n_de_pares > 4:
      continue
    acc[n_de_pares] += 1
  for i in range(2,5):
    if acc[i] == 4:
      exclude_list.append(i)
      return exclude_list
  return exclude_list


def get_n_de_pares_min_max(n_of_last_jogo=n_of_last_jogo_param):
  """
  returns (ndp_min, ndp_max)

  """
  paresComp = [];     ndp_min = 0;     ndp_max = 6
  for i in range(1,20):
    jogoComp = jogosPool.getJogo(n_of_last_jogo - i)
    paresComp.append(jogoComp.getNDePares())
    
  if 0 in paresComp: # least frequent, come first in if
    ndp_min = 1
  elif 1 in paresComp:
    ndp_min = 2
  if 6 in paresComp: # least frequent, come first in if
    ndp_max = 5
  elif 5 in paresComp:
    ndp_max = 4
 # print 'ndp_min, ndp_max',  ndp_min, ndp_max
  return ndp_min, ndp_max


def organize_sixtils(dezena_hist_g):
  """
    Note:  There were Quartils in previous development, now they are Sixtils
  """
  # fine, let's organize the Sixtils
  dezenas = dezena_hist_g.keys()
  dezenas.sort()
  dezenasQuant = []
  for dezena in dezenas:
    dezenasQuant.append(dezena_hist_g[dezena])
  dezenas_quant_na = numpy.array(dezenasQuant)
  dezenas_quant_na.sort()
  sup = dezenas_quant_na.max() #dezenas_quant_na[59]
  inf = dezenas_quant_na.min() #dezenas_quant_na[0]
  dist = sup - inf
  desloca = 0
  while dist % 6 != 0:
    dist -= 1
    desloca += 1
  sexto = dist / 6
  points = []
  points.append(inf-1)
  pos = inf + desloca
  sixtils = []
  sixtils.append([])
  #for i in range(1,7):
  # CORRECT HERE
  posSextos = map(pos + sexto, range(1,7))
  points.append(pos)
  sixtils.append([]*6)
  #print 'len(dezenas_quant_na)', len(dezenas_quant_na)
  #print 'len(points)', len(points) 
  for dezena in range(1, 61):
    quant = dezena_hist_g[dezena]
    for j in range(1,7):  # quartis[0] is not used!
      if quant > points[j-1] and quant <= points[j]:
        sixtils[j].append(dezena)
  return sixtils



def generate_sixtils_iterative(ateJogoN):
  global dezenaHistG, jaFeitoSixtil
  if jaFeitoSixtil == ateJogoN:
    return dezenaHistG 
  for jogoN in range(jaFeitoSixtil, ateJogoN+1):
    jogo = jogosPool.getJogo(jogoN)
    dezenas = jogo.getDezenas()
    for dezena in dezenas:
      dezenaHistG[dezena] += 1
  jaFeitoSixtil = ateJogoN
  sixtils = organize_sixtils(dezenaHistG)
  #print ' [in analyzer] sixtils', sixtils
  return sixtils 

sixtilsGenerated = False; sixtils = []

def generateSixtils():
  global sixtilsGenerated, sixtils
  if sixtilsGenerated:
    return sixtils
  dezena_hist_g = atSt.obtemHistGDas60()
  sixtils = organize_sixtils(dezena_hist_g)
  if type(sixtils[0]) == type([]):
    sixtilsGenerated = True
  return sixtils 


def get_soma_desce_ou_sobe(jogo, n_of_last_jogo=n_of_last_jogo_param):
  '''
  returns True if sobe (boolean)
  '''
  difs = []
  soma = jogo.soma()
  for i in range(1,4):
    jogoComp = jogosPool.getJogo(n_of_last_jogo - i)
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

def get_lin_col_data_stru():
  """
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

  """
  pass
  return None

def get_n_de_iguais_jogo_ant():
  """
  returns iguaisAntStru
  """
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
    # rethink below for j is not used
    for j in xrange(2,7):
      if d%10==0:
        d += 1
      else:
        d += 11
      if d > 60:
        d-=10
      nose[i-1].append(d)
  aaa='''
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
  maxNOfPrimesInHistory = 0; primesDict = {} # ; maxNOfPrimesInHistoryNDoJogo = None;
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
    sixtils = generate_sixtils_iterative(nDoJogo - 1)
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

def analyseJogoInOrderPatterns():
  lines = open('dznUnitPatt.txt').readlines()
  for line in lines:
    patt = ''
    pp = line.split(' ')
    try:
        int(pp[0])
        patt = pp[7]
    except IndexError:
      continue
    except ValueError:
      continue
  print patt
  
if __name__ == '__main__':
  pass
  analyseJogoInOrderPatterns()
  # testAnalyzer()