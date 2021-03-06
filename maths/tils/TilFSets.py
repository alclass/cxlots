#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 05/12/2011

@author: friend
'''
#import scipy.stats
import sys

class TilFSets(object):
  '''
  This class has only one public method (though public/private is not enforced in Python)
  And this is getTilSets()
  
  getTilSets() is realized thru a 3-method tool-chain. (They should be considered "private" to the class.) They are:
    self.getDeltaFrequencyListAtConcurso()
    self.transformDeltaFrequenciesIntoFrequencyBorders()
    self.putDezenasInsideTilSets()

  This tool-chain does the following:
  1st) gets a list/array containing the frequency delta for each "til" eg (12,12,12,11,11)
       means 12 units in frequency for the 3 first elements and 11 units in frequency
       for the last two
  2nd) takes the frequency delta array and transform it into a tuple-array with
       the min-max border for each "til"
       Ex. slot 1 = (110,121); slot 2 = (122,133); slot 3 = (134,145); slot 4 = (146, 156); slot 5 = (157,167)
  3nd) puts the element in "frequencies" inside the til-sets according to where it gets in
       Ex. if the game (1,2,3,4,5,6) has the following frequencies per dozen:
       f(1) = 115; f(2)=160; f(3)=122; f(4)=121; f(5)=156; f(6)=145
       Tils would be:
       f(1) = 115 which is within slot 1 = (110,121)
       f(2) = 160 which is within slot 5 = (157,167)
       f(3) = 122 which is within slot 2 = (122,133)
       f(4) = 121 which is within slot 1 = (110,121)
       f(5) = 156 which is within slot 4 = (146,156)
       f(6) = 145 which is within slot 3 = (134,145)
       The order of Tils, then, is 152143 and the quantity per slot (Til itself) is 21111.
       So, for the hipothetical game (1,2,3,4,5,6) its Til(5,6) is 21111.
  
  '''
  def __init__(self, frequencies, tilN):
    '''
    Two parameters suffice:  frequencies, tilN
    '''
    self.tilSets = None
    self.frequencies = frequencies[:] 
    self.tilN = tilN # same as n_slots
    self.minFreq = min(self.frequencies)
    self.maxFreq = max(self.frequencies)
    self.listWithDeltaFrequencies = None # None here means, not yet "initialized"
    self.listWithFrequencyBordersTuple = None # same as above, ie not yet "initialized"
    self.generateTilSets() # this is the process flow itself !

  def generateTilSets(self):
    '''
    This is the only public, externally callable, method of this class
    It invokes a 3-method tool-chain and then returns self.tilSets
    (Checkings will be implemented via unittests and other adhoc tests) 
    '''
    self.calcDeltaFrequencyListAtConcurso()
    if self.listWithDeltaFrequencies == []:
      return
    self.transformDeltaFrequenciesIntoFrequencyBorders()
    self.putDezenasInsideTilSets()

  def getTilSets(self, regenerate=False):
    if self.tilSets == None or regenerate:
      self.generateTilSets()
    return self.tilSets

  def calcDeltaFrequencyListAtConcurso(self):
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
      self.listWithDeltaFrequencies = []
      return
    remainder = amplitude % self.tilN
    #remainder =  (maxN - minN) % tilNumber
    self.listWithDeltaFrequencies = [deltaFrequency] * self.tilN
    for i in range(len(self.listWithDeltaFrequencies)):
      if remainder > 0:
        self.listWithDeltaFrequencies[i] += 1
        remainder -= 1
      else:
        break
    # logically list is in ascending order
    # check/test the following equality
    if sum(self.listWithDeltaFrequencies) != amplitude:
      valueErrorMsg = 'sum(listWithDeltaFrequencies)=%d != amplitude=%d :: The two should be equal' %(sum(self.listWithDeltaFrequencies), amplitude)
      raise ValueError, valueErrorMsg
    #print 'minN, maxN, amplitude, listWithDeltaFrequencies', self.minFreq, self.maxFreq, amplitude, self.listWithDeltaFrequencies

  def getDeltaFrequencyListAtConcurso(self):
    if self.listWithDeltaFrequencies == None:
      self.calcDeltaFrequencyListAtConcurso()
    return self.listWithDeltaFrequencies
  
  def transformDeltaFrequenciesIntoFrequencyBorders(self):
    self.listWithFrequencyBordersTuple = [()]*len(self.listWithDeltaFrequencies)
    range_min = self.minFreq
    for i, deltaFrequency in enumerate(self.listWithDeltaFrequencies):
      minFreqTil = range_min
      maxFreqTil = minFreqTil + deltaFrequency - 1 
      borderTuple = (minFreqTil, maxFreqTil)
      self.listWithFrequencyBordersTuple[i] = borderTuple
      range_min = maxFreqTil + 1
    if maxFreqTil != self.maxFreq:
      errorMsg = 'maxFreqTil=%d != maxFreq=%d  The two should be equal' %(maxFreqTil, self.maxFreq)
      raise ValueError, errorMsg
    
  def putDezenasInsideTilSets(self):
    '''
    Reimplement the list tilSet to a working dict that is transformed back to the tilSet list
    '''
    self.tilSets = [[]] * self.tilN
    #print 'self.tilSets', self.tilSets
    for index, frequency in enumerate(self.frequencies):
      dezena = index + 1
      for i, borderTuple in enumerate(self.listWithFrequencyBordersTuple):
        minTil = borderTuple[0]  
        maxTil = borderTuple[1]
        if minTil <= frequency and frequency <= maxTil:
          # 1st hard copy to avoid referencing and mixing up sets
          tilSet = self.tilSets[i][:] 
          tilSet.append(dezena)
          # 2nd hard copy to avoid referencing and mixing up sets
          self.tilSets[i] = tilSet[:]
          # 3rd delete list object to avoid another referencing and mixing up sets 
          del tilSet
          #print 'entering dezena', currentDezena, 'minTil, frequency, maxTil', minTil, frequency, maxTil, 'tilN is', i, self.tilSets[i]
          # break for next dezena (the one here has already been placed!)  
          break
    self.checkTestIfAllDozensHaveBeenAllocatedInsideTilSets()

  def checkTestIfAllDozensHaveBeenAllocatedInsideTilSets(self):
    '''
    checkTestIfAllDozensHaveBeenAllocatedInsideTilSets() (this check belongs to the Class's process flow, at the end)
    # check/test the following, ie, all dozens must have been allocated inside some til-slot
    ''' 
    if len(self.frequencies) != sum(map(len, self.tilSets)):
      errorMsg = 'checkTestIfAllDozensHaveBeenAllocatedInsideTilSets() :: len(self.frequencies)=%d != map(sum, self.tilSets)=%d :: The two should be equal' %(len(self.frequencies), map(sum, self.tilSets))
      raise ValueError, errorMsg
    
  def getBorderTupleOfTilSets(self, retry=False):
    if self.listWithFrequencyBordersTuple == None:
      if retry:
        errorMsg = 'Internal error: self.listWithFrequencyBordersTuple could not somehow be initialized (it continues None after retry). It is either a program error or database is empty.'
        raise ValueError, errorMsg
      else:
        self.generateTilSets()  # this method re-does this Class's process flow
        return self.getBorderTupleOfTilSets(retry=True)
    return self.listWithFrequencyBordersTuple
    
  def findTilIndexForFreq(self, freq):
    for i, bordersTuple in enumerate(self.listWithFrequencyBordersTuple):
      til_freq_min = bordersTuple[0]
      til_freq_max = bordersTuple[0]
      if til_freq_min <= freq <= til_freq_max:
        return i
    return None # None here meaning "not found"  

def getTilSets(frequencies, tilN):
  '''
  This method is a sort of "handler" to produce the til-sets via calling the same name instance method getTilSets()
  '''
  tilSetsObj = TilFSets(frequencies, tilN)
  return tilSetsObj.getTilSets()

def test_tilObjs():
  freqs = range(1,15)
  tilSetsObj = TilFSets(freqs, 14)
  tilSets = tilSetsObj.getTilSets()
  print 'tilSets', tilSets   #print 'listWithFrequencyBordersTuple', self.listWithFrequencyBordersTuple, 'min max', self.minFreq, self.maxFreq
#test_tilObjs()

def test_tilObjs2():
  hist = {1: 785, 2: 735, 3: 643, 4: 631, 5: 566, 6: 460, 7: 458, 8: 371, 9: 332, 10: 297, 11: 275, 12: 238, 13: 217, 14: 222, 15: 186, 16: 155, 17: 152, 18: 116, 19: 114, 20: 118, 21: 93, 22: 85, 23: 70, 24: 79, 25: 70, 26: 60, 27: 56, 28: 43, 29: 43, 30: 34, 31: 32, 32: 28, 33: 25, 34: 14, 35: 17, 36: 25, 37: 15, 38: 15, 39: 11, 40: 21, 41: 13, 42: 7, 43: 11, 44: 13, 45: 11, 46: 3, 47: 5, 48: 6, 49: 2, 50: 6, 51: 5, 52: 6, 53: 5, 54: 5, 55: 3, 56: 3, 58: 1, 59: 3, 60: 3, 61: 2, 62: 4, 63: 1, 65: 1, 68: 2, 70: 1, 73: 1, 76: 1, 78: 1, 83: 1, 89: 1}
  # keys will be thrown away (lost), because algorithm keeps only the sequencial position
  freqs = hist.values()
  tilSetsObj = TilFSets(freqs, 6)
  tilSets = tilSetsObj.getTilSets()
  print 'tilSets', tilSets   #print 'listWithFrequencyBordersTuple', self.listWithFrequencyBordersTuple, 'min max', self.minFreq, self.maxFreq
#test_tilObjs2()

def adhoc_test():
  '''
  '''
  pass

import unittest
class MyTest(unittest.TestCase):

  def test_1(self):
    pass
 

def look_up_cli_params_for_tests_or_processing():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()
    elif arg.startswith('-u'):
      # unittest complains if argument is available, so remove it from sys.argv
      del sys.argv[1]
      unittest.main()
    elif arg.startswith('-p'):
      pass
      # process()

if __name__ == '__main__':
  look_up_cli_params_for_tests_or_processing()
