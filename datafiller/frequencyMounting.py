#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 13/11/2011

@author: friend
'''
import copy #import sqlite3, sys
a=1
import sqlLayer as sl
#import converterForDateAndCurrency as conv
#import FieldsAndTypes as fat
#import HTMLGrabber as hb

class FrequenciesThruConcursos():
  '''
  This class is supposed to be a singleton, but no enforcement for it is made
  As it's need somewhere, the calling point just instantiate one object
  As it's no longer necessary, the garbage collector will recover the memory it used
  
  The memory used here is an m by n array
  The inner array is an n-position array (eg. 60 for megasena) with the accumulated frequency of all the n dezenas
  The outer array has an inner array for each concurso
  
  '''
  def __init__(self, nDeDezenasNoVolante=60):
    self.accumulatedFrequencyUpToConcurso = []
    self.nDeDezenasNoVolante = nDeDezenasNoVolante 
    self.initializeaccumulatedFrequencyUpToConcurso()
    
  def initializeaccumulatedFrequencyUpToConcurso(self):
    concursos = sl.getListAllConcursosObjs()
    frequencyOfAllDezenas = [0] * self.nDeDezenasNoVolante
    for concurso in concursos:
      for dezena in concurso.getDezenas():
        dezenaAsIndexFrom0 = dezena-1
        frequencyOfAllDezenas[dezenaAsIndexFrom0] += 1
      hardCopyDezenasFrequenciesAtConcurso = frequencyOfAllDezenas[:]
      self.accumulatedFrequencyUpToConcurso.append(hardCopyDezenasFrequenciesAtConcurso) 
  
#  def append(self, frequencyOfEveryDezena):
#    self.accumulatedFrequencyUpToConcurso.append(frequencyOfEveryDezena)

  def getFrequenciesOfAllDezenasByNDoConcurso(self, nDoConcurso):
    if nDoConcurso < 1 or nDoConcurso > len(self.accumulatedFrequencyUpToConcurso):
      return None
    return self.accumulatedFrequencyUpToConcurso[nDoConcurso-1]

  def getAllFrequenciesOfAllConcursos(self):
    return self.accumulatedFrequencyUpToConcurso
    
  def __getitem__(self, nDoConcurso=0):
    return self.getFrequenciesOfAllDezenasByNDoConcurso(nDoConcurso)
  
  def __len__(self):
    return len(self.accumulatedFrequencyUpToConcurso)
  
  def sumUpTo(self, upToConcursoI):
    if upToConcursoI < 1:
      return 0
    if upToConcursoI > len(self.accumulatedFrequencyUpToConcurso):
      return None
    freqOfAllDezenasUpToConcursoI = self.accumulatedFrequencyUpToConcurso[upToConcursoI-1]
    sumOfFreqsOfAllDezenasUpToConcursoI = sum(freqOfAllDezenasUpToConcursoI)
    return sumOfFreqsOfAllDezenasUpToConcursoI
  
  def getLast(self):
    return self.accumulatedFrequencyUpToConcurso[-1]
  
  def getDezenaFreqAtConcursoN(self, dezena, nDoConcurso):
    concurso = sl.getConcursoObjByN(nDoConcurso)
    if concurso == None:
      return None
    dezenas = concurso.getDezenas()
    if dezena not in dezenas:
      return None
    return self.accumulatedFrequencyUpToConcurso[dezena-1]

  def getAllDezenas(self):
    '''
    Since implementation of this class changed from dict to list, allDezenas are a rule starting from 1 to len(list)+1
    '''
    return range(1, len(self.accumulatedFrequencyUpToConcurso) + 1)

  def getNTotalDeDezenas(self):
    return self.nDeDezenasNoVolante

  def returnFrequenciesAsADezenaFreqDict(self):
    freqDict = {}
    for i in range(len(self.accumulatedFrequencyUpToConcurso)):
      dezena = i + 1  # this is a logical rule (dezenas must start at 1 and be consecutive)
      frequency = self.accumulatedFrequencyUpToConcurso[i]
      freqDict[dezena] = frequency
    return freqDict 

  def getDezenasWithFrequencyF(self, frequencyIn, nDoConcurso):
    '''
    This method is somewhat inefficient, so it'll be change in the future
    This method is also meant to be private, though it's not enforced
    '''
    i = 0; dezenasOut = []
    for frequency in self.accumulatedFrequencyUpToConcurso[nDoConcurso-1]:
      if frequency == frequencyIn:
        # dezena is index i + 1, for indices are from 0 to 59 and dezenas from 1 to 60
        dezenasOut.append(i+1)
      i+=1
    return dezenasOut

  def getAllDezenasInAscendingOrderOfFrequencyForConcursoN(self, nDoConcurso=None):
    totalDeConcursos = len(sl.getListAllConcursosObjs())
    if nDoConcurso == None:
      nDoConcurso = len(sl.getListAllConcursosObjs())      
    elif nDoConcurso < 1 or nDoConcurso > totalDeConcursos:
      return None 
    toBeOrdered = copy.copy(self.accumulatedFrequencyUpToConcurso[nDoConcurso-1])
    toBeOrdered.sort(); i=0
    dezenasInAscendingOrderOfFrequency = []; frequencyAnterior = -1 # this guarantees the first only will not be equal when looking ahead to equal consecutives
    while i < len(toBeOrdered):
      frequency = toBeOrdered[i]
      # look ahead and jump posterior equals
      if frequency == frequencyAnterior:
        i+=1
        continue
      dezenasWithF = self.getDezenasWithFrequencyF(frequency, nDoConcurso)
      dezenasInAscendingOrderOfFrequency += dezenasWithF 
      frequencyAnterior = frequency
      i += 1 
    return dezenasInAscendingOrderOfFrequency    
    
'''
freqAtEachConcurso = FrequenciesThruConcursos()  
statsStore = {}
statsStore['freqAtEachConcurso'] = freqAtEachConcurso
'''
  
if __name__ == '__main__':
  pass

'''
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
'''
