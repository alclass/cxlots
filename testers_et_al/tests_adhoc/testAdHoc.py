#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 20/11/2011

@author: friend
'''
#import os # datetime, sys

a=1
import frequencyMounting as fm
import sqlLayer as sl

def testAdHoc():
  # freqAtEachConcurso = fm.statsStore['freqAtEachConcurso']
  freqAtEachConcurso = fm.FrequenciesThruConcursos()
  dikt = fm.calculateTilOfNUpToConcursoI(5, freqAtEachConcurso)
  print dikt  

def testAdHoc2():
  listWithFrequencyFrontiers = fm.calculateTilOfNUpToConcursoI() 
  print 'listWithFrequencyFrontiers', listWithFrequencyFrontiers
  freqAtEachConcurso = fm.FrequenciesThruConcursos()
  frequencies = freqAtEachConcurso.frequenciesOfAllDezenasAtConcursoI()  
  print 'frequencies', frequencies
  concursos = sl.getListAllConcursosObjs()
  nDoConcurso = len(concursos)
  print 'nDoConcurso', nDoConcurso, freqAtEachConcurso[nDoConcurso]
  
def testAdHoc3():
  freqAtEachConcurso = fm.FrequenciesThruConcursos()
  allFrequenciesOfAllConcursos = freqAtEachConcurso.getAllFrequenciesOfAllConcursos(); n=0; soma = 0
  for each in allFrequenciesOfAllConcursos:
    n += 1
    somaAnterior = soma
    soma = sum(each)
    print n, # soma, each
    if n>1:
      if soma == somaAnterior + 6:
        print 'OKAY soma == somaAnterior + 6 (=%d, = %d)' %(soma, somaAnterior)
      else:
        msg = 'NOT OKAY soma (=%d) != somaAnterior + 6 (=%d)' %(soma, somaAnterior)
        print msg
        raise ValueError, msg 

def testAdHoc4():
  tilObj = fm.TilMaker()
  tilSets = tilObj.getTilSets()
  print 'tilObj.getTilSets()', tilSets
  concurso = sl.getConcursoObjByN()
  print 'concurso', concurso
  print 'concurso.getTilN()', concurso.getTilN(), concurso.getDezenas()

def testAdHoc5():
  freqAtEachConcurso = fm.FrequenciesThruConcursos()
  print 'freqAtEachConcurso.getAllDezenasInAscendingOrderOfFrequency()', freqAtEachConcurso.getAllDezenasInAscendingOrderOfFrequency()

def testAdHoc6():
  tilPatterns = []
  for nDoConcurso in range(1000, 1334):
    concurso = sl.getConcursoObjByN(nDoConcurso)
    tilPattern = concurso.getTilN()
    tilPatterns.append(tilPattern)
    print concurso.getDezenas(), tilPattern
  print tilPatterns  

if __name__ == '__main__':
  testAdHoc6()
  #testAdHoc()
