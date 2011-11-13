#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime, string, sys

letters52 = string.letters
import CLClasses
from cardprint import pprint


def getClassName(selfRef):
  rep = repr(selfRef)
  piece = rep.split(' ')[0]
  if piece.find('__main__.') > -1:
    className = piece[len(main):]
  else:
    dotPos = piece.find('.')  # Eg '<Stat.Stat object at 0xb7fc156c>' ==>> 'Stat'
    className = piece[dotPos+1:]
  return className


def mountLogFile(selfRef, jogosObj):
  className    = getClassName(selfRef)
  now = datetime.date.today()
  sigla = jogosObj.sqlTable
  ultimoNDoConc = len(jogosObj.getJogos())
  logFilename = 'logs/%s-%s-%d--%s.log' %(sigla, className, ultimoNDoConc, now)
  logFile = open(logFilename,'w')
  return logFile


def returnJogosObj(eitherJogosObjOrS2):
  jogosObj = None
  if type(eitherJogosObjOrS2) == str:
    standard2LetterName = eitherJogosObjOrS2
    jogosObj = CLClasses.getJogosObj(standard2LetterName)
  elif type(eitherJogosObjOrS2) == CLClasses.Jogos:
    jogosObj = eitherJogosObjOrS2
  else:
    errorMsg = 'eitherJogosObjOrS2 should be eitherJogosObjOrS2 but it is = %s' %(eitherJogosObjOrS2)
    raise ValueError, errorMsg
  return jogosObj


def calcConsecPattern(jogo, standard2LN):
  if standard2LN == 'MS':
    calcConsecPatternMS(jogo)
  elif standard2LN == 'LF':
    calcConsecPatternMS(jogo)


def convertConsecsToChars(consecs):
  consecStr = ''
  for consec in consecs:
    if consec == 0:
      break
    if consec > 61:
      errorMsg = 'max value for consec is 61 :: it was = %d' %(consec)
      raise ValueError, errorMsg
    if consec < 10:
      consecStr += str(consec)
    else:
      dif = consec - 10
      consecStr += letters52[dif]
  return consecStr
        
def calcConsec(jogo):
  nDeDezenas        = len(jogo)
  nDeDezenasMenosUm = nDeDezenas - 1
  consecs = [0] * nDeDezenasMenosUm

  for i in range(nDeDezenas-1, 0, -1):
    for j in range(i-1, -1, -1):
      inc = i - j
      if jogo[i] == jogo[j] + inc:
        consecs[inc-1] += 1
      else:
        break

  '''
  # code below is not working

  for i in range(0, nDeDezenasMenosUm):
    for j in range(i+1, nDeDezenas):
      inc = j - i
      if jogo[i] == jogo[j] + inc:
        consecs[inc-1] += 1
      else:
        break
  '''

  if consecs[0] == 0:
    return 0

  consecPattern = convertConsecsToChars(consecs)

  '''  consecPattern = 0; i = 0
  for consec in consecs:
    if consec == 0:
      break
    consecPattern += consec * 10 ** i
    i += 1
  '''
  return consecPattern


def noPointAndCommaToPoint(value):
  if value == None or type(value) <> str:
    return value
  if value.find('.') > -1:
    value = value.replace('.','') # ie, 1.000,00 should become 1000,00
  if value.find(',') > -1:
    value = value.replace(',','.') # ie, 1000,00 should become 1000.00
  return value

def formArgCaller(methodToBeCalled):
  moduleName = sys.argv[0]
  moduleName = moduleName.lstrip('./')
  moduleName = moduleName.rstrip('.py')
  argCaller  = moduleName + '.' + methodToBeCalled
  #print 'argCaller', argCaller
  try:
    argCaller  = eval(argCaller)
  except NameError:
    #print 'importing moduleName'
    exec('import ' + moduleName)
    argCaller  = eval(argCaller)
  #print 'argCaller', argCaller
  return argCaller

def updateCaller(methodToBeCalled):
  moduleName = sys.argv[0]
  if len(sys.argv) >= 3:
    arg = sys.argv[1]
    if arg == '-u':
      jogoTipo = sys.argv[2] # eg 'MS'
      argCaller = formArgCaller(methodToBeCalled)
      #sys.exit(0)
      argCaller(jogoTipo)
      return
  pprint.printUsage()

def divisorDeConjuntosEmMeios(n, nOfDivs):
  if n <= nOfDivs:
    return None, None, None
  for a in range(0, n):
    resto = (n - 2 * a ) % (nOfDivs - 1)
    if resto == 0:
      d = (n - 2 * a ) / (nOfDivs - 1)
      if d == 0:
        if n % 2 == 0:
          aIni, d, aFim = findIntsAandD(n-1, nOfDivs)
          if d <> 0:
            return aIni, d, aIni+1  # asymmetric
        return None, None, None
      aIni = a
      return aIni, d, aIni # symmetric
  return None, None, None


def testCalcConsec():
  jogo = [1,2,4,5,30,31]
  #jogo = [1,4,30,35,40,47]
  patt = calcConsec(jogo)
  print jogo, patt


if __name__ == '__main__':
  pass
  #testCalcConsec()
