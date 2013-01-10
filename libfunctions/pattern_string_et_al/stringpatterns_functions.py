#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
(...)
'''
import string, sys # datetime
letters52 = string.letters

import __init__
__init__.setlocalpythonpath()

from libfunctions import system_wide_lambdas as swlambda


def convert_intlist_to_spaced_zfillstr(dezenas_in, zfill_n=2, do_sort=False):
  '''
  This function converts a dozens list to a string
  Eg.:
  f([1,2,3,4,5,6]) ==>> '01 02 03 04 05 06'
  '''
  if do_sort:
    dezenas_in.sort()
  if zfill_n < 2:
    return dezenas_in
  if zfill_n==2:
    dezenas = map(swlambda.zfill2, dezenas_in)
  else:
    dezenas = map(swlambda.zfilln, dezenas_in, [zfill_n]*len(dezenas_in))
  dezenas = ' '.join(dezenas)
  return dezenas

def listToStr(listIn):
  outStr = ''
  for element in listIn:
    outStr += str(element) 
  return outStr 

def dezenasToPrintableStr(dezenas):
  dezenasStr = ''
  for dezena in dezenas:
    dezenasStr += str(dezena).zfill(2) + ' '
  dezenasStr = dezenasStr[:-1]
  return dezenasStr 

def clearLineEnding(line):
  if line.endswith('\n'):
    line = line.rstrip('\n')
  if line.endswith('\r'):
    line = line.rstrip('\r')
  return line

def reverseString(line):
  charList = strToCharList(line)
  charList.reverse()
  newLine = ''.join(charList)
  return newLine

def extractNumbersInANumberSpacedStrIntoANumberList(line):
  line = clearLineEnding(line)
  pp = line.split(' ')
  jogo = map(swlambda.toInt, pp)
  return jogo

def numberListToStrCommaless(lista, nForZfill=2):
  '''
  Pretty Print for a list
  Instead of coming out like [5,12,...]
  it will come out like 05 12 ...
  '''
  newList = []
  for elem in lista:
    newList.append(str(elem).zfill(nForZfill))
  s = str(newList)
  s = s.replace("'",'')
  s = s.replace(",",'')
  s = s[1:-1]
  return s

def numberListToStrNoPrettyPrint(jogo):
  '''
  Not Pretty Print for jogo list
  Instead of coming out like [5,12,...]
  it will come out like 5 12 ...
  The pretty-print version above, instead, will come out like 05 12 ...
  '''
  s = str(jogo)
  s = s.replace("'",'')
  s = s.replace(",",'')
  s = s[1:-1]
  return s

def numberListToStickedChar(jogo, nForZfill=2):
  '''
  Spaceless Pretty Print for jogo list
  Instead of coming out like [5,12,...]
  it will come out like 0512 ...
  '''
  s = numberListToStrCommaless(jogo, nForZfill)
  s = s.replace(" ",'')
  return s

def numberListToAWholeInt(jogo):
  '''
  Example for Lotofácil
  nLower = 10203040506070809101112131415
  nUpper = 111213141516171819202122232425
  '''
  s = numberListToStickedChar(jogo)
  if s[0] == '0':
    s = s[1:]
  #print 's', s
  wholeInt = int(s)
  return wholeInt

def printNumberList(lista, nOfZfill=2):
  for elem in lista:
    print str(elem).zfill(nOfZfill),
  print

def printList(lista):
  for elem in lista:
    print elem

def strToCharList(s):
  lista = []
  for x in s:
    lista.append(x)
  return lista

def printJogos(jogos):
  c=0
  for jogo in jogos:
    c+=1
    print c,
    printNumberList(jogo)

def printHistG(histG):
  if histG == None:
    return 
  numbers = histG.keys()
  numbers.sort()
  for number in numbers:
    print number, '=> quant:', histG[number]

def printDict(occurDict):
  if occurDict == None or len(occurDict) == 0:
    print "occurDict is None or empty."
    return
  occurences = occurDict.keys()
  occurences.sort() #;c=0
  for occurence in occurences:
    parcelStr = '%s:%s ' %(str(occurence), str(occurDict[occurence])) 
    print parcelStr,
  print
  minValue = min(occurDict.values())
  maxValue = max(occurDict.values())
  print 'min', minValue, ':: max', maxValue

def testAdHocPrintDict():
  dDict = {'a':33, 'b':17, 'c':21, 'd':-3}
  printDict(dDict)
# testAdHocPrintDict()  
  

'''
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
'''

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

'''
def updateCaller(methodToBeCalled):
  moduleName = sys.argv[0]
  moduleName
  if len(sys.argv) >= 3:
    arg = sys.argv[1]
    if arg == '-u':
      jogoTipo = sys.argv[2] # eg 'MS'
      argCaller = formArgCaller(methodToBeCalled)
      #sys.exit(0)
      argCaller(jogoTipo)
      return
  pprint.printUsage()
'''

def testCalcConsec():
  jogo = [1,2,4,5,30,31]
  #jogo = [1,4,30,35,40,47]
  patt = calcConsec(jogo)
  print jogo, patt


if __name__ == '__main__':
  pass
  #testCalcConsec()
