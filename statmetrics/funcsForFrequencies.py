#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 05/12/2011

@author: friend
'''

class TilSets():
  '''
  This class has only one public method (though public/private is not enforced in Python)
  And this is getTilSets()
  
  getTilSets() is realized thru a 3-method tool-chain. (They should be considered "private" to the class.) They are:
    self.getDeltaFrequencyListAtConcurso()
    self.transformDeltaFrequenciesIntoFrequencyBorders()
    self.putDezenasInsideTilSets()

  This tool-chain does the following:
  1st) gets a list/array containing the frequency delta for each "til" eg (12,12,12,11,11) means 12 units in frequency for the 3 first elements and 11 units in frequency for the last two
  2nd) takes the frequency delta array and transform it into a tuple-array with the min-max border for each "til" eg (110,121) (122,133) (134,145) (146, 156) (157,167)
  3nd) puts the element in "frequencies" inside the til-sets according to where it gets in
  '''
  def __init__(self, frequencies, tilN):
    '''
    Two parameters suffice:  frequencies, tilN
    '''
    self.frequencies = frequencies 
    self.tilN = tilN
    self.minFreq = min(self.frequencies)
    self.maxFreq = max(self.frequencies)

  def getTilSets(self):
    '''
    This is the only public, externally callable, method of this class
    It invokes a 3-method tool-chain and then returns self.tilSets
    (Checkings will be implemented via unittests and other adhoc tests) 
    '''
    self.getDeltaFrequencyListAtConcurso()
    self.transformDeltaFrequenciesIntoFrequencyBorders()
    self.putDezenasInsideTilSets()
    return self.tilSets

  def getDeltaFrequencyListAtConcurso(self):
    '''
    Eg. min=10 max=20
    tilN = 5
    amplitude = 20 - 10 + 1 = 11
    increment = amplitude / tilN = 11 / 5 = 2
    remainder = amplitude % self.tilNumber = 11 % 2 = 1
    listWithFrequencyFrontiers = 2+1=3 2 2 2 2
    sum(listWithFrequencyFrontiers) = sum(3 2 2 2 2)=11=amplitude
    frontiers = [10,12] [13,14] [15,16] [17,18] [19,20]
    
    '''
    #print 'frequenciesAtConcursoN', self.frequencies, 'len(frequencies)', len(self.frequencies)
    amplitude = self.maxFreq - self.minFreq + 1
    deltaFrequency =  amplitude / self.tilN
    if deltaFrequency == 0:
      # cannot continue, data is not enough
      return None 
    remainder = amplitude % self.tilN
    #remainder =  (maxN - minN) % tilNumber
    self.listWithDeltaFrequencies = [deltaFrequency] * self.tilN
    for i in range(len(self.listWithDeltaFrequencies)):
      if remainder > 0:
        self.listWithDeltaFrequencies[i] += 1
        remainder -= 1
    # logically list is in ascending order
    if sum(self.listWithDeltaFrequencies) != amplitude:
      valueErrorMsg = 'sum(listWithDeltaFrequencies)=%d != amplitude=%d :: The two should be equal' %(sum(self.listWithDeltaFrequencies), amplitude)
      raise ValueError, valueErrorMsg
    #print 'minN, maxN, amplitude, listWithDeltaFrequencies', self.minFreq, self.maxFreq, amplitude, self.listWithDeltaFrequencies
  
  def transformDeltaFrequenciesIntoFrequencyBorders(self):
    self.listWithFrequencyBordersTuple = [()]*len(self.listWithDeltaFrequencies)
    ini = self.minFreq; i=0
    for deltaFrequency in self.listWithDeltaFrequencies:
      minFreqTil = ini
      maxFreqTil = minFreqTil + deltaFrequency - 1 
      borderTuple = (minFreqTil, maxFreqTil)
      self.listWithFrequencyBordersTuple[i] = borderTuple
      i+=1
      ini = maxFreqTil + 1
    if maxFreqTil != self.maxFreq:
      errorMsg = 'maxFreqTil=%d != maxFreq=%d  The two should be equal' %(maxFreqTil, self.maxFreq)
      raise ValueError, errorMsg
    
  def putDezenasInsideTilSets(self):
    '''
    Reimplement the list tilSet to a working dict that is transformed back to the tilSet list
    '''
    self.tilSets = [[]] * self.tilN
    #print 'self.tilSets', self.tilSets
    nOfDezenasProcessed = 0; currentDezena = 1
    #print 'listWithFrequencyBordersTuple', self.listWithFrequencyBordersTuple, 'min max', self.minFreq, self.maxFreq
    for frequency in self.frequencies:
      for i in range(len(self.listWithFrequencyBordersTuple)):
        borderTuple = self.listWithFrequencyBordersTuple[i]
        minTil = borderTuple[0]  
        maxTil = borderTuple[1]
        if minTil <= frequency and frequency <= maxTil:
          # 1st hard copy to avoid referencing and mixing up sets
          tilSet = self.tilSets[i][:] 
          tilSet.append(currentDezena)
          # 2nd hard copy to avoid referencing and mixing up sets
          self.tilSets[i] = tilSet[:]
          # 3rd delete list object to avoid another referencing and mixing up sets 
          del tilSet
          #print 'entering dezena', currentDezena, 'minTil, frequency, maxTil', minTil, frequency, maxTil, 'tilN is', i, self.tilSets[i]  
          nOfDezenasProcessed += 1
          break
      currentDezena += 1
    # print 'nOfDezenasProcessed', nOfDezenasProcessed, self.tilSets
  
  def checkIfAllDezenasAreTaken(self):
    '''
    this method will be relocated to the unittests
    ''' 
    nDeDezenasTotais = len(self.frequencies)
    nDeElementos = 0
    for tilSet in self.tilSets:
      nDeElementos += len(tilSet)
    if nDeDezenasTotais != nDeElementos:
      errorMsg = 'checkIfAllDezenasAreTaken(self) failed ie some dezena is not inside tilSets :: nDeDezenasTotais=%d - nDeElementos=%d = %d' %(nDeDezenasTotais, nDeElementos, nDeDezenasTotais - nDeElementos)
      raise ValueError, errorMsg
    
  
def getTilSets(frequencies, tilN):
  '''
  This method is a sort of "handler" to produce the til-sets via calling the same name instance method getTilSets()
  '''
  tilSetsObj = TilSets(frequencies, tilN)
  return tilSetsObj.getTilSets()


if __name__ == '__main__':
  pass
    