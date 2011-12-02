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
        frequencyOfAllDezenas[dezena-1] += 1
      snapShotForCurrentPosition = copy.copy(frequencyOfAllDezenas)
      self.accumulatedFrequencyUpToConcurso.append(snapShotForCurrentPosition) 
  
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

  def getAllDezenasInAscendingOrderOfFrequency(self, nDoConcurso=None):
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

class TilMaker():

  def __init__(self, tilNumber=None, nDoConcurso=None):
    if tilNumber == None or tilNumber not in [5,6,10,12,15]:
      tilNumber = 5
    self.tilNumber = tilNumber
    totalDeConcursos = len(sl.getListAllConcursosObjs())      
    if nDoConcurso == None:
      nDoConcurso = totalDeConcursos
    elif nDoConcurso < 1 or nDoConcurso > totalDeConcursos:
      indexErrorMsg = 'passed in nDoConcurso=%d and range acceptable is 1 to %d' %(nDoConcurso, totalDeConcursos)
      raise IndexError, indexErrorMsg 
    self.nDoConcurso = nDoConcurso
    self.listWithFrequencyFrontiers = None
    self.tilSets = None
    self.freqAtEachConcurso = FrequenciesThruConcursos() 

  def calculateTilOfNUpToConcursoI(self):
    frequenciesAtConcursoN = self.freqAtEachConcurso.getFrequenciesOfAllDezenasByNDoConcurso(self.nDoConcurso)
    minN = min(frequenciesAtConcursoN)
    maxN = max(frequenciesAtConcursoN)
    amplitude = maxN - minN + 1
    incrementSize =  amplitude / self.tilNumber
    # nTotalDeDezenas = self.freqAtEachConcurso.getNTotalDeDezenas() 
    remainder = amplitude % self.tilNumber
    #remainder =  (maxN - minN) % tilNumber
    self.listWithFrequencyFrontiers = [incrementSize] * self.tilNumber
    for i in range(incrementSize):
      if remainder > 0:
        self.listWithFrequencyFrontiers[i] += 1
        remainder -= 1
    # logically list is in ascending order
    if sum(self.listWithFrequencyFrontiers) != amplitude:
      valueErrorMsg = 'sum(listWithFrequencyFrontiers)=%d != amplitude=%d :: The two should be equal' %(sum(self.listWithFrequencyFrontiers), amplitude)
      raise ValueError, valueErrorMsg
    '''
    if sum(self.listWithFrequencyFrontiers) != nTotalDeDezenas:
      valueErrorMsg = 'sum(listWithFrequencyFrontiers)=%d != nTotalDeDezenas=%d :: The two should be equal' %(sum(self.listWithFrequencyFrontiers), nTotalDeDezenas)
      valueErrorMsg += '\n self.listWithFrequencyFrontiers = %s' %(str(self.listWithFrequencyFrontiers))
      valueErrorMsg += '\n tilN = %d  nTotalDeDezenas %d' %(self.tilNumber, nTotalDeDezenas)
      valueErrorMsg += '\n self.nDoConcurso = %d  min %d max %d' %(self.nDoConcurso, minN, maxN)
      raise ValueError, valueErrorMsg
    ''' 
    return self.listWithFrequencyFrontiers

  def getTilSets(self):
    self.separateTilSets()
    self.checkTilSetsBorders()
    return self.tilSets
  
  def separateTilSets(self):
    if self.listWithFrequencyFrontiers == None:
      self.calculateTilOfNUpToConcursoI()
    dezenas = self.freqAtEachConcurso.getAllDezenasInAscendingOrderOfFrequency()
    print 'dezenas', dezenas 
    self.tilSets = [[]] * len(self.listWithFrequencyFrontiers); ini = 0
    for i in range(len(self.listWithFrequencyFrontiers)):
      frontier = self.listWithFrequencyFrontiers[i]
      fim = ini + frontier
      print 'i fim = ini + frontier', i, fim , ini , frontier
      if fim > len(dezenas):
        valueErrorMsg = 'An inconsistency happened, index fim (=%d) is greater than len(dezenas) = %d ' %(fim, len(dezenas)) 
        raise ValueError, valueErrorMsg
      self.tilSets[i] = dezenas[ ini : fim]
      print i, 'tilSets[i]', self.tilSets[i]
      ini = fim
  
  def checkTilSetsBorders(self):
    '''
    This method compares he last element of one tilSet
      with the first element of the next tilSet and if equal, 
      bring the next tilSet element to the previous set and recurse to look for more
    '''
    if self.tilSets == None:
      self.separateTilSets()
    for i in range(len(self.tilSets)-1):
      passingTilSet = self.tilSets[i]
      nextTilSet = self.tilSets[i+1]
      try:
        while passingTilSet[-1] == nextTilSet[0]:
          passingTilSet.append(nextTilSet[0])
          del nextTilSet[0]
      except IndexError:
        pass

def sumUpTilPattern(pattern):
  soma=0
  for c in pattern:
    soma+=int(c)
  return soma

class TilElement():
  '''
  This class covers a Til Element
  A Til Element is instantiated with a pattern (eg '03021')
  From any pattern, length and sum can be derived.  Length is the pattern string size
    ( in the example above len('03021')=5 )
    and sum is the summing up of its digits (in the example above 0+3+0+2+1=6)
  
  It implements a method called getWorkSetsWithQuantities() which does the following:
    it gets the frequency-til-positioned dezenas and joins this set with the quantity expressed in the digit
    
    let's see this in the example above '03021'
    0, the first digit, means 0 dezenas in the first quintil
    3 means 3 dezenas in the second quintil which may have x dezenas altogether
    the pair (tuple) to form is this set of x dezenas, together with the quantity 3
    this tuple will be used elsewhere for combinations of this til(size=5, index=1) 3 by 3

    index 1 is because pattern[1]=3
    
    So this method is applied in a calling routine that produces these combinations
    
  '''
  def __init__(self, pattern):
    self.pattern = pattern
    self.setLengthAndSum()
  def setLengthAndSum(self):
    self.length  = len(self.pattern)
    self.sum = sumUpTilPattern(self.pattern)
  def getWorkSetsWithQuantities(self):
    workSetsWithQuantities = []
    tilObj = TilMaker(self.length)
    workSets = []
    for i in range(len(self.pattern)):
      quantity = int(self.pattern[i])
      if quantity > 0:
        dezenas = tilObj.getTilSets()[i]
        workSetWithQuantity = (dezenas, quantity)
        workSetsWithQuantities.append(workSetWithQuantity)
    return workSetsWithQuantities

def testTilElement():
  tilElement = TilElement('03021')
  workSetsWithQuantities = tilElement.getWorkSetsWithQuantities()
  print workSetsWithQuantities
  
if __name__ == '__main__':
  pass
  testTilElement()
  # process()
  #printFreqThru()

