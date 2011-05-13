#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

a=1
sys.path.insert(0,'..')
import lambdas

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
  jogo = map(lambdas.toInt, pp)
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
  s = str(s)
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

def intToJogoList(n, baseObj):
  intFromLowest = baseObj.getIntFromLowestJogo()
  return intToNumberList(n, intFromLowest)

def intToNumberList(n, intFromLowest):
  nOrig = n + intFromLowest
  s = str(nOrig)
  if len(s) % 2 == 1:
    s = '0' + s
  dezenasStrList = []
  for i in range(baseObj.nDeDezenasSorteadas):
    indexLower = 2*i
    indexUpper = indexLower + 2
    dezenaStr  = s[indexLower:indexUpper]
    dezenasStrList.append(dezenaStr)
  dezenasStr = jogoStrListToStr(dezenasStrList)
  return dezenasStr

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
  if not occurDict or len(occurDict) == 0:
    return
  occurences = occurDict.keys()
  occurences.sort();c=0
  min = occurDict[occurences[0]]
  max = occurDict[occurences[0]]
  for occurence in occurences:
    c+=1
    value = occurDict[occurence]
    print c, occurence, value
    if value < min:
      min = value
    if value > max:
      max = value
  print 'min', min
  print 'max', max

def printJogoWithTils(histG, jogo, atIndex, tilIn=5, nOfDezenas=15):
  totalOfDraws = atIndex * nOfDezenas
  tils = generateTils(histG, tilIn)
  for dezena in jogo:
    quant = histG[dezena]
    for til in tils:
      if quant < til:
        dezenaTil = til
        break
    print 'dezena', dezena, 'quant', quant, 'til', til

def printUsage():
  moduleName = sys.argv[0]
  print '''Usage:
  %(moduleName)s -u <jogotipo>
Example:
  %(moduleName)s -u LF
''' %{'moduleName':moduleName}

def testJogoToInt():
  nUpper = 111213141516171819202122232425
  nMax = nUpper - nLower
  print 'nMax', hex(nMax)
  gain = nUpper - nMax
  print 'gain', gain
  n2to75 = 2**75
  print 'n2to75', n2to75


if __name__ == '__main__':
  pass
