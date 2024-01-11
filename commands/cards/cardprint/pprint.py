#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

a=1
import lambdas
sys.path.insert(0, '../../../fs/dbfs')
import statmetrics.funcsForStringPatternsEtAl as ffStr

  
def printUsage():
  moduleName = sys.argv[0]
  print '''Usage:
  %(moduleName)s -u <jogotipo>
Example:
  %(moduleName)s -u LF
''' %{'moduleName':moduleName}

def testJogoToInt():
  '''
  yet to test
  '''
  nUpper = 111213141516171819202122232425
  nLower = 0
  nMax = nUpper - nLower
  print 'nMax', hex(nMax)
  gain = nUpper - nMax
  print 'gain', gain
  n2to75 = 2**75
  print 'n2to75', n2to75


if __name__ == '__main__':
  pass

'''

# this functions below is to be placed elsewhere to avoid circular importing

def intToJogoList(n, baseObj):
  intFromLowest = baseObj.getIntFromLowestJogo()
  return intToNumberList(n, intFromLowest)


def intToNumberList(n, intFromLowest, baseObj):
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
  dezenasStr = ffStr.jogoStrListToStr(dezenasStrList)
  return dezenasStr

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
'''
