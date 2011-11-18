#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 13/11/2011

@author: friend
'''
import copy
#import sqlite3, sys
a=1
import sqlLayer as sl
#import converterForDateAndCurrency as conv
#import FieldsAndTypes as fat
#import HTMLGrabber as hb

class Stats():
  def __init__(self):
    self.statsDict = {}
  def __setitem__(self, statsname, statsobj):
    self.statsDict[statsname] = statsobj 
  def __getitem__(self, statsname):
    return self.statsDict[statsname]
  def __len__(self):
    return len(self.statsDict)

#statsStore = Stats()
statsStore = {}

class FreqDictThruConcursos():
  def __init__(self):
    self.freqDictAtEachConcurso = {}
    self.maxNDoConcurso = 0
  def __setitem__(self, nDoConcurso, freqDict):
    self.freqDictAtEachConcurso[nDoConcurso] = freqDict
    if nDoConcurso > self.maxNDoConcurso:
      self.maxNDoConcurso = nDoConcurso 
  def __getitem__(self, nDoConcurso):
    return self.freqDictAtEachConcurso[nDoConcurso]
  def __len__(self):
    return len(self.freqDictAtEachConcurso)
  def getLast(self):
    return self.freqDictAtEachConcurso[self.maxNDoConcurso]
  def getByNDoConcurso(self, nDoConcurso):
    if nDoConcurso in self.freqDictAtEachConcurso.keys():
      return self.freqDictAtEachConcurso[nDoConcurso]
    else:
      return None
    
#freqAtEachConcurso = FreqDictThruConcursos()


def initializeFreqDict(nDeDezenas=60):
  freqDict = {}
  for dezena in range(1, nDeDezenas+1):
    freqDict[dezena] = 0
  return freqDict

def mountDezenasFrequencies(ate_concurso_n=None):
  global freqAtEachConcurso
  concursos = sl.sqlSelect()
  if ate_concurso_n != None:
    if ate_concurso_n > 0 and ate_concurso_n < len(concursos):
      concursos = concursos[ : ate_concurso_n]
  freqDict = initializeFreqDict()
  freqAtEachConcurso = FreqDictThruConcursos()
  for concurso in concursos:
    for dezena in concurso.getDezenas():
      freqDict[dezena] += 1
    nDoConcurso = concurso['nDoConcurso']
    freqAtEachConcurso[nDoConcurso]=copy.copy(freqDict)
    #print nDoConcurso, 'freqAtEachConcurso[nDoConcurso]', freqAtEachConcurso[nDoConcurso] 
  #return freqAtEachConcurso
  statsStore['freqAtEachConcurso'] = freqAtEachConcurso

def process():
  mountDezenasFrequencies()
  freqAtEachConcurso = statsStore['freqAtEachConcurso']
  freqDict = freqAtEachConcurso.getLast()  
  print 'lastFreqDict', freqDict
  freqDict = freqAtEachConcurso.getByNDoConcurso(100)  
  print '100th freqDict', freqDict

def printFreqThru():
  print 'printFreqThru():', 'len(freqAtEachConcurso)', len(freqAtEachConcurso)
  for nDoConcurso in range(1, len(freqAtEachConcurso)+1):
    print nDoConcurso, freqAtEachConcurso[nDoConcurso]

import unittest
class Test(unittest.TestCase):
  def test_initializeFreqDict(self):
    dictCompare = {}
    for i in range(61): dictCompare[i]=0
    self.assertEqual(initializeFreqDict(60), dictCompare)
    dictCompare['blah']='blah'
    self.assertFalse(initializeFreqDict(3), dictCompare)
  def mountDezenasFrequencies(self):
    concursos = sl.sqlSelect()
    concurso1 = concursos[0]
    dictForConc1 = {}
    for dezena in concurso1:
      dictForConc1[dezena] = 1
    self.assertEqual(mountDezenasFrequencies(ate_concurso_n=1), dictForConc1)
    # self.assertEqual(type(mountDezenasFrequencies()), dict)
    self.assertEqual(mountDezenasFrequencies(ate_concurso_n=0), mountDezenasFrequencies())
    

if __name__ == '__main__':
  process()
  #printFreqThru()

