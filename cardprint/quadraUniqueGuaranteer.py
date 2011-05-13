#!/usr/bin/env python
#--*--encoding:utf8--*--
import re, sys
import volantePrintingFunctions as vpf
import extractPatternHistogram2 as eph
import combinadics

def guaranteeOneQuadPerVolant(apostaFilename):
  apostaFile = open(apostaFilename)
  line = apostaFile.readline(); allDezenas = []; nOfLines = 0
  print 'Reading lines:',
  while line:
    dezenas = vpf.transformLineToDezenasList(line)
    if dezenas == None:
      line = apostaFile.readline()
      continue
    nOfLines += 1
    allDezenas.append(dezenas)
    line = apostaFile.readline()
  print nOfLines

  iList = []; dictQuadClash = {}; allQuadrasDict = {}
  for i in range(len(allDezenas)):
    dictQuadClash[i] = {}
    quadrasI = eph.getQuadrasFromDezenasList(allDezenas[i])
    for quadra in quadrasI:
      # lgi is LexicoGraphical Index 
      # lgi = combinadics.findIndexFromCombination(quadra, 4)
      quadraStrList = map(eph.tmpF, quadra)
      quadraStr = ' '.join(quadraStrList)
      if quadraStr in allQuadrasDict.keys():
        print 'quadraStr', quadraStr, 'REPEATED at jogo', i
      allQuadrasDict[quadraStr]=1

  for i in range(len(allDezenas)-1):
    dezenasI = allDezenas[i]
    quadrasI = eph.getQuadrasFromDezenasList(dezenasI)
    print 'Dezenas', dezenasI
    print 'Quadras', quadrasI
    for j in range(i+1,len(allDezenas)):
      dezenasJ = allDezenas[j]
      quadrasJ = eph.getQuadrasFromDezenasList(dezenasJ)
      for quadraJ in quadrasJ:
        if quadraJ in quadrasI:
          dictQuadI = dictQuadClash[i]
          if j in dictQuadI.keys():
            quant = dictQuadI[j]
            dictQuadI[j] = quant + 1
          else:
            dictQuadI[j]=1
          dictQuadJ = dictQuadClash[j]
          if i in dictQuadJ.keys():
            quant = dictQuadJ[i]
            dictQuadJ[i] = quant + 1
          else:
            dictQuadJ[i]=1

  for i in range(len(allDezenas)):
    dictQuadI = dictQuadClash[i]
    print i+1, '=', dictQuadI

  # all quadras
  allQuadras = allQuadrasDict.keys()
  allQuadras.sort()
  for quadraStr in allQuadras:
    print quadraStr
  print 'total allQuadras', len(allQuadras)
  print 'total allDezenas', len(allDezenas)
  print '15 quadras por dezenas = ', 15 * len(allDezenas)
  


if __name__ == '__main__':
  pass

  print 'hi'
  #sys.exit(0)
  apostaFilename = '../Apostas/apostas-test.txt'
  guaranteeOneQuadPerVolant(apostaFilename)
