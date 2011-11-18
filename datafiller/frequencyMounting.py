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
  def getDezenaFreqAtConcursoN(self, dezena, nDoConcurso):
    concurso = sl.concursos[nDoConcurso-1]
    dezenas = concurso.getDezenas()
    if dezena not in dezenas:
      return None
    freqDict = self.getByNDoConcurso(nDoConcurso)
    return freqDict[dezena]
  def getByNDoConcurso(self, nDoConcurso):
    if nDoConcurso in self.freqDictAtEachConcurso.keys():
      return self.freqDictAtEachConcurso[nDoConcurso]
    else:
      return None
  def getNTilForDezenasAt(self, tilN, nDoConcurso):
    concurso = sl.concursos[nDoConcurso-1]
    if concurso == None:
      return None
    listWithFrequencyFrontiers = calculateTilOfNForHistogram(tilN, self.freqDictAtEachConcurso[nDoConcurso])
    tilDict = {}
    for dezena in concurso.getDezenas():
      dezenaWasSet = False
      for quant in listWithFrequencyFrontiers:
        dezenaFreq = self.getDezenaFreqAtConcursoN(dezena, nDoConcurso)
        if dezenaFreq < quant:
          tilDict[dezena]=listWithFrequencyFrontiers.index(quant)+1
          dezenaWasSet = True
          break
      if not dezenaWasSet:
        tilDict[dezena] = len(listWithFrequencyFrontiers)
    return tilDict
#freqAtEachConcurso = FreqDictThruConcursos()


def calculateTilOfNForHistogram(tilNumber, freqDict):
  minN = min(freqDict)
  maxN = max(freqDict)
  incrementSize = (maxN - minN) / tilNumber
  remainder =  (maxN - minN) % tilNumber
  listWithFrequencyFrontiers = [incrementSize]*tilNumber
  for i in range(incrementSize):
    if remainder > 0:
      listWithFrequencyFrontiers[i] += 1
      remainder -= 1
  # logically list is in ascending order
  return listWithFrequencyFrontiers

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
  def test_mountDezenasFrequencies(self):
    concursos = sl.sqlSelect()
    concurso1 = concursos[0]
    dictForConc1 = {}
    for dezena in concurso1:
      dictForConc1[dezena] = 1
    self.assertEqual(mountDezenasFrequencies(ate_concurso_n=1), dictForConc1)
    # self.assertEqual(type(mountDezenasFrequencies()), dict)
    self.assertEqual(mountDezenasFrequencies(ate_concurso_n=0), mountDezenasFrequencies())
  def test_calculateTilOfNForHistogram(self):
    pass

    
process()

if __name__ == '__main__':
  pass
  # process()
  #printFreqThru()

