#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob

tmpF = lambda x : int(x)
#import tableops

def compare(jogo1, jogo2):
  equals = 0
  for i in range(len(jogo1)):
    dezena = jogo1[i]
    if dezena == jogo2[i] and i==equals:
      equals += 1
      if equals == 15:
        return True
    else:
      #print False, 'equals', equals, 'i', i
      return False
  return False

def testCompare():
  jogoStr = '02 03 05 06 09 10 11 13 14 16 18 20 23 24 25'
  jogo1 = map(tmpF, jogoStr.split(' '))
  print 'j1', jogo1
  jogoStr = '02 03 05 06 09 10 11 13 14 16 18 20 23 24 25'
  jogo2 = map(tmpF, jogoStr.split(' '))
  print 'j2', jogo2
  print compare(jogo1, jogo2)

def compareAllFiles():
  dats = glob.glob('*.dat'); goNextWhileI = False
  dats.sort(); nOfEquals = 0
  for i in range(len(dats)-1):
    datI = dats[i]
    newDat = open(datI + '.2', 'w')
    print 'Sweeping datI', datI
    filI = open(datI)
    jogoLineI = filI.readline()
    while jogoLineI:
      if goNextWhileI:
        goNextWhileI = False
        jogoLineI = filI.readline()
        print 'goNextWhileI i'
      if jogoLineI.find('\n') > -1:
        jogoLineI = jogoLineI[:-1]
      jogoI = map(tmpF, jogoLineI.split(' '))
      if len(jogoI) <> 15:
        jogoLineI = filI.readline()
        continue
      for j in range(i+1, len(dats)):
        if goNextWhileI:
          print 'break j'
          break
        datJ = dats[j]
        print 'Checking datI', datI, 'Against datJ', datJ
        filJ = open(datJ)
        jogoLineJ = filJ.readline()
        while jogoLineJ:
          if jogoLineJ.find('\n') > -1:
            jogoLineJ = jogoLineJ[:-1]
          jogoJ = map(tmpF, jogoLineJ.split(' '))
          if len(jogoJ) <> 15:
            jogoLineJ = filJ.readline()
            continue
          r = compare(jogoI, jogoJ)
          if r:
            nOfEquals += 1
            print nOfEquals, 'Found EQUAL, breaking and continuing...'
            goNextWhileI = True
            break
          jogoLineJ = filJ.readline()
      newDat.write(jogoLineI + '\n')
      jogoLineI = filI.readline()

    print 'closing newDat', newDat
    newDat.close()

if __name__ == '__main__':
  compareAllFiles()
