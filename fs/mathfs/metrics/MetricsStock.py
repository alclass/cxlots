#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
  This module contains 'business' classes: Jogos and Til
'''

import localpythonpath
localpythonpath.setlocalpythonpath()

import funcsForMetrics as ffMetrics

somaNList = [1, 3, 7, 15]

def iguaisComOAnterior(jogo):
  '''
  jogo must implement get_dezenas()
  '''
  jogo_anterior = jogo.get_previous()
  if jogo_anterior == None:
    return 0
  return ffMetrics.getNOfCoincidences(jogo_anterior, jogo)
  
def coincsComNAnteriores(jogo, nDeAnteriores):
  '''
  jogo must implement get_dezenas()
  coincsComNAnteriores() call nDeAnteriores times iguaisComOAnterior 
  '''
  nDeCoincsComAnteriores = 0
  for backward_i in range(nDeAnteriores):
    nDeCoincsComAnteriores += iguaisComOAnterior(jogo)
    jogo = jogo.get_previous()
    if jogo == None:
      break
  return nDeCoincsComAnteriores 

def coincsComOs3Anteriores(jogo):
  return coincsComNAnteriores(jogo, 3)

def maxDeIguais(jogo):
  maxDeIguais = 0
  distAo1o = -1
  for nDoConc_to_compare in range(jogo.n_conc - 1, 0, -1):
    jogo_to_compare = jogo.get_jogo_by_nDoConc(nDoConc_to_compare)
    nDeCoincsComAnteriores = ffMetrics.getNOfCoincidences(jogo, jogo_to_compare)
    if nDeCoincsComAnteriores > maxDeIguais:
      maxDeIguais = nDeCoincsComAnteriores
      distAo1o = jogo.n_conc - nDoConc_to_compare
      maxDeIguaisOcorrencia = 1      
    elif nDeCoincsComAnteriores == maxDeIguais:
      maxDeIguaisOcorrencia += 1      
  return maxDeIguais, distAo1o, maxDeIguaisOcorrencia  

    
  #  self.iguaisMediaComPassado = totalForMedia / (i + 0.0)

  #print nDoConc, 'self.iguaisComOAnterior', self.iguaisComOAnterior

  '''
  standard2LN = self.jogosObj.standard2LetterName
  # Note: only LF has minDeIguais and related fields
  if i > 0 and standard2LN == 'LF':
    UP_LIMIT_FOR_minDeIguais = 255
    self.minDeIguais = UP_LIMIT_FOR_minDeIguais
    for j in range(i):
      nOfBackConc = i-1-j + 1
      iguais = fCoincs.getNOfCoincidences(jogo, jogosfs[i-1-j])
      if iguais < self.minDeIguais:
        self.minDeIguais = iguais
        self.minDeIguaisDistAo1o = nDoConc - nOfBackConc
        self.minDeIguaisOcorrencia = 1
      elif iguais == self.minDeIguais and self.minDeIguaisOcorrencia > 0:
        self.minDeIguaisOcorrencia += 1
    #print 'self.minDeIguais', self.minDeIguais
  '''

  self.rem2pattern = ''
  self.parParImparImpar = ''
  self.rem3pattern = ''
  self.rem5pattern = ''
  self.rem6pattern = ''
  self.colpattern = ''
  for dezena in jogo:
    d = dezena % 2
    self.rem2pattern += str(d)
    dzn   = dezena / 10
    rDzn  = dzn % 2
    rUnit = d
    strDigit = '3'
    if rDzn==0:
      if rUnit==0:
        strDigit = '0'
      else:
        strDigit = '1'
    else: # ie, rDzn==1:
      if rUnit==0:
        strDigit = '2'
    self.parParImparImpar += strDigit
    d = dezena % 3
    self.rem3pattern += str(d)
    d = dezena % 5
    self.rem5pattern += str(d)
    d = dezena % 6
    self.rem6pattern += str(d)
    d = colFnct(dezena)
    self.colpattern += str(d)

  partialJogos = CLClasses.PartialJogos(self.jogosObj.standard2LetterName)
  partialJogos.setAteConcurso(nDoConc)
    
  til4obj = tilc.Til(partialJogos, 4)
  self.til4pattern = til4obj.generateLgiForJogoVsTilFaixas(jogo)
  # get later-on til4ocorrencia

  til5obj = tilc.Til(partialJogos, 5)
  self.til5pattern = til5obj.generateLgiForJogoVsTilFaixas(jogo)
  # get later-on til5ocorrencia

  til6obj = tilc.Til(partialJogos, 6)
  self.til6pattern = til6obj.generateLgiForJogoVsTilFaixas(jogo)
  # get later-on til6ocorrencia

  til10obj = tilc.Til(partialJogos, 10)
  self.til10pattern =  til10obj.generateLgiForJogoVsTilFaixas(jogo)
  # get later-on til10ocorrencia
  
      '''
    # consecutivos

    Eg.
    28 29 30 39 40 55
    This jogo has consec1=3 (ie, [28->29, 29->30, 39->40])
    This jogo has consec2=1 (ie, [28->29->30])
    This jogo has consec3=0 and all above (consec4 and consec5) are 0 too

    In the old implementation, there were:
    consecutivo1 ==> now, consec[0]
    consecutivo2 ==> now, consec[1]
    and so on

    The current implementation is also general, in the sense that it serves MS, LF and anyone, based on "self.jogosObj.nDeDezenasSorteadas"
    So consec[i] :: i from 0 to nDeDezenas - 1
    '''

      currentJogoObj = CLClasses.ShapeAreaCircleCalculator(jogo, self.jogosObj.standard2LetterName)
      jogoMenorAMaior = currentJogoObj.jogo
      self.consecEnc = funcs.calc_consec(jogoMenorAMaior)

      partialJogosList = partialJogos.getJogos()
      for n in somaNList: # defined here in Stat.py [1, 3, 7, 15]  (may change there)
        if nDoConc < n:
          exec('self.soma%d = None' %(n))
        else:
          soma = calcSomaN(jogo, partialJogosList, n) # calcSomaN defined here in Stat.py
          exec('self.soma%d = soma' %(n))
        somaN = eval('self.soma%d' %(n))
        if somaN == None:
          somaN = -1
        outLine = '%d soma%d=%d' %(nDoConc, n, somaN)
        self.logFile.write(outLine + '\n')

      na = numpy.array(jogo)
      self.std = na.std()
      del na

      self.binDecReprSomaDe1s = 0
      binDecRepr = currentJogoObj.getBinDecRepr()
      while binDecRepr > 0:
        digit = binDecRepr & 1
        self.binDecReprSomaDe1s += digit
        binDecRepr = binDecRepr >> 1

      # lgiDist
      self.lgiDist = 0
      if i > 0:
        lgi = currentJogoObj.get_lgi()
        jogoObjAnt = CLClasses.ShapeAreaCircleCalculator(jogos[i - 1], self.jogosObj.standard2LetterName)
        lgiAnt = jogoObjAnt.get_lgi()
        self.lgiDist = lgi - lgiAnt

      # the current implementation needs jogo sorted crescently
      takeSquareRoot = True
      self.pathway  = self.radii.calculatePathway(currentJogoObj.jogo, takeSquareRoot)
      # make it integer "taking 2 decimal places"
      self.pathway  = int(self.pathway  * 100)
      self.allpaths = self.radii.calculateIntercrossed(currentJogoObj.jogo, takeSquareRoot)
      self.allpaths = int(self.allpaths * 100)

      #gauss = None
      #euclideandist = None
      #correlation = None
      #metricaZ = None

      '''
      self.origDrawnOrderQuad = 0; self.origDrawCresceDesce = 0
      jogoInOrder = self.jogosObj.getJogoInOrder(nDoConc)
      if not jogoInOrder:
        continue
      for j in range(len(jogo)):
        dezena = jogo[j]
        origIndex = jogoInOrder.index(dezena)
        dist = origIndex - j
        if dist > 0:
          self.origDrawCresceDesce += 1
        if dist < 0:
          self.origDrawCresceDesce -= 1
        self.origDrawnOrderQuad += dist ** 2
      self.origDrawnPattern = produceOrigDrawnPattern(jogoInOrder)
      '''

        
      self.updateDB(nDoConc)
      # END of FOR-loop (each nOfConc)
    #self.writeTo(jogo, nOfConc)
    # instantiate object from the DoubleDBs class (to update both MySql and Sqlite)
    dDB = fSql.DoubleDBs(self.jogosObj.sqlTable)
    # DIU means Delete, Insert or Update, next line sets it
    #print 'self.deltaUpdateSqls', self.deltaUpdateSqls
    dDB.setDeltaDIUSqlsForDBs(self.deltaUpdateSqls)
    dDB.executeSqls()
    
  def moveNDoConcForStatUpdate(self):
    sql = '''SELECT `nDoConc` from `%s`
  where `iguaisComOAnterior` is NULL 
  and `nDoConc` > 1 
  order by `nDoConc`;
  '''  %(self.jogosObj.sqlTable)
    #print sql
    conn = fSql.getConnection()
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = []
    for row in cursor:
      rows.append(row)
    if len(rows) > 0:
      VARRE_DO_JOGO = rows[0][0]
      #print 'VARRE_DO_JOGO ', VARRE_DO_JOGO 
      self.setVarreDe(VARRE_DO_JOGO)
      return True
    return False

  def updateDB(self, nDoConc):
    sql = "UPDATE `%(sqlTable)s` SET" %{'sqlTable':self.jogosObj.sqlTable}
    attrs = {}
    for attrKey in self.attrKeys:
      attrs[attrKey] = eval('self.' + attrKey)
      if attrs[attrKey] <> None: # ie, it's not None / NULL
        sql += " `%(attr)s`='%(valuesStr)s'," %{'attr':attrKey,'valuesStr':attrs[attrKey]}
    if sql[-1] == ',':
      sql = sql[:-1]
    sql += " WHERE `nDoConc`='%d';" %(nDoConc)
    #print 'sql', sql
    self.logFile.write(sql + '\n')
    self.deltaUpdateSqls.append(sql)
    #retVal = fSql.doDBsUpdate(sql)

    '''
    if retVal == 1:
      print 'self.nOfUpdated', self.nOfUpdated
      self.nOfUpdated += retVal # ie = += 1
      self.retVal = retVal
      if self.logIt:
        line = '%d sql: %d' %(nDoConc, sql)
        self.logFile.write(line + '\n')
    if self.logIt:
      line = '%d retVal=%d' %(nDoConc, retVal)
      self.logFile.write(line  + '\n')
    '''

  def writeTo(self, jogo, nOfConc):

    aprint = '''  
  nOfConc = %(nOfConc)d   %(jogo)s
  iguaisComOAnterior = %(iguaisComOAnterior)d
  coincsComOs3Anteriores =  %(coincsComOs3Anteriores)d
  maxDeIguais =  %(maxDeIguais)d
  maxDeIguaisDistAo1o =  %(maxDeIguaisDistAo1o)d
  maxDeIguaisOcorrencia =  %(maxDeIguaisOcorrencia)d
  minDeIguais =  %(minDeIguais)d
  minDeIguaisDistAo1o =  %(minDeIguaisDistAo1o)d
  minDeIguaisOcorrencia =  %(minDeIguaisOcorrencia)d
  iguaisMediaComPassado =  %(iguaisMediaComPassado)f
  rem2pattern =  %(rem2pattern)s
  rem3pattern =  %(rem3pattern)s
  rem5pattern =  %(rem5pattern)s
  til5pattern =  %(til5pattern)s
  til6pattern =  %(til6pattern)s
  til10pattern =  %(til10pattern)s
  soma = %(soma)d
  std = %(std)f
  binDecReprSomaDe1s = %(binDecReprSomaDe1s)d
    ''' %{'nOfConc':nOfConc,'jogo':jogo,'iguaisComOAnterior':iguaisComOAnterior,'coincsComOs3Anteriores':coincsComOs3Anteriores,'maxDeIguais':maxDeIguais,'maxDeIguaisDistAo1o':maxDeIguaisDistAo1o,'maxDeIguaisOcorrencia':maxDeIguaisOcorrencia,'minDeIguais':minDeIguais,'minDeIguaisDistAo1o':minDeIguaisDistAo1o,'minDeIguaisOcorrencia':minDeIguaisOcorrencia,'iguaisMediaComPassado':iguaisMediaComPassado,'rem2pattern':rem2pattern,'rem3pattern':rem3pattern,'rem5pattern':rem5pattern,'til5pattern':til5pattern,'til6pattern':til6pattern,'til6pattern':til6pattern,'til10pattern':til10pattern,'soma':soma,'std':std,'binDecReprSomaDe1s':binDecReprSomaDe1s}
    self.outFile.write(aprint)

  def __str__(self):
    outStr = 'Stat for ' + str(self.jogosObj)
    return outStr

def calcSomaN(jogo, jogos, n):
  if n not in somaNList:
    return 0
  soma = sum(jogo)
  for i in range(1, n):
    soma += sum(jogos[-i])
  return soma

def produceOrigDrawnPattern(jogoInOrder, standard2LetterName):
  '''
  if jogoInOrder == None:
    return None
  '''
  dznDict = {}; unitDict = {}
  for pos in range(len(jogoInOrder)):
    dezena = jogoInOrder[pos]
    dznDigit  = dezena  / 10
    if standard2LetterName == 'MS' and dezena == 60:
      dznDigit = 0
    try:
      dznDict[dznDigit] += str(pos)
    except KeyError:
      dznDict[dznDigit] = str(pos)
    unitDigit = dezena % 10
    try:
      unitDict[unitDigit] += str(pos)
    except KeyError:
      unitDict[unitDigit] = str(pos)

  # unpack dict into a str
  drawnPattern = 'd'
  dznsKeys = dznDict.keys()
  dznsKeys.sort()
  for dzn in dznsKeys:
    quants = dznDict[dzn]
    #quant  = len(quants)
    strQuants = lambdas.strChr(quants)
    #strSeq = str(dzn) + str(quant) + ''.join(strQuants)
    strSeq = str(dzn) + ''.join(strQuants)
    drawnPattern += strSeq + 'd'
  drawnPattern =  drawnPattern[:-1] + 'u'
  unitKeys = unitDict.keys()
  unitKeys.sort()
  for unit in unitKeys:
    quants = unitDict[unit]
    strQuants = lambdas.strChr(quants)
    strSeq = str(unit) + ''.join(strQuants)
    drawnPattern += strSeq + 'u'
  drawnPattern =  drawnPattern[:-1]
  quantD = len(dznDict)
  quantU = len(unitDict)
  drawnPattern = '%d%d:' %(quantD, quantU) + drawnPattern
  return drawnPattern


def processDBStats(standard2):
  print 'Instantiating', standard2
  print '-'*40
  jogosObj = CLClasses.getJogosObj(standard2)
  statObj = Stat(jogosObj)
  print 'statObj.moveNDoConcForStatUpdate()', statObj.moveNDoConcForStatUpdate()
  #statObj.setVarreDe(1)
  print 'statObj.nOfUpdated', statObj.nOfUpdated
  print 'statObj.VARRE_DO_JOGO', statObj.VARRE_DO_JOGO
  statObj.updateAll = True
  statObj.logIt = True
  statObj.gatherStats()
  print 'statObj.updateAll', statObj.updateAll
  print 'statObj.nOfUpdated', statObj.nOfUpdated

def testProduceOrigDrawnPattern():
  jogosObj = CLClasses.getJogosObj('ms')
  pattKeys = {}
  for i in range(jogosObj.getNDoUltimoConcurso()):
    nDoConc = i+1
    jogoInOrder = jogosObj.getJogoInOrder(nDoConc)
    if not jogoInOrder:
      print '*** not jogoInOrder', nDoConc
      continue
    patt = produceOrigDrawnPattern(jogoInOrder, jogosObj.standard2LetterName)
    try:
      pattKeys[patt] += 1
    except KeyError:
      pattKeys[patt] = 1
    print nDoConc, pprint.jogoListToStr(jogoInOrder), patt, pattKeys[patt]


if __name__ == '__main__':
  funcs.updateCaller('processDBStats') # methodToBeCalled = 'processDBStats'
