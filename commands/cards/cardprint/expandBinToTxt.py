#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Image, sys

a=1
sys.path.insert(0, '')
#sys.path.insert(0,'..')
import CLClasses
import funcsForCoincs as fCoincs
import Stream


# lf-468-apostas-01.bin
filename = 'Apostas/lf-468-apostas-01.bin'
sigla = 'lf'
jogosObj = CLClasses.getJogosObj(sigla)
streamIn = Stream.Stream(jogosObj)
streamIn.setStreamInFile(filename)
def checkThru(jogo):
  print 'checkThru(jogo):', jogo
  jogoComp = streamIn.first(); c=0
  while jogoComp:
    nOfCoincs = fCoincs.getNOfCoincidences
    c+=1
    if nOfCoincs > 11:
      print c, jogo, nOfCoincs
    jogo = streamIn.next()

def do():
  #fileNDoConc = 468
  compareToList = range(469, 471)
  for nDoConc in compareToList:
    jogo = jogosObj.getJogos()[nDoConc-1]
    checkThru(jogo)
    
#getInBinFilename(sigla, nDoConc)
  

if __name__ == '__main__':
  do()
  pass
