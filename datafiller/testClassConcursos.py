#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import datetime, sys
'''
Created on 18/11/2011

@author: friend
'''


a=1
import ClassConcursoEtc as conc
def t1():
  concurso = conc.Concurso()
  for i in range(1,7):
    fieldname = 'dezena%d' %i
    concurso[fieldname]=i
  print 'concurso', concurso
  print 'concurso.getDezenas()', concurso.getDezenas()

import frequencyMounting as fm

def t2():
  freqAtEachConcurso = fm.statsStore['freqAtEachConcurso'] 
  til = freqAtEachConcurso.getNTilForDezenasAt(5, 100)
  til = freqAtEachConcurso.getNTilForDezenasAt(7, 100)
  til = freqAtEachConcurso.getNTilForDezenasAt(5, 700)
  til = freqAtEachConcurso.getNTilForDezenasAt(7, 700)
  
  print 'til', til
  

#print 'running t2'  
#t2()

def t3():
  tilNumber=4
  freqDict = {1:5, 2:3, 3:2, 4:1}
  til = fm.calculateTilOfNForHistogram(tilNumber, freqDict)
  print 'in t3() til = ', til

print 'running t3'  
t3()

