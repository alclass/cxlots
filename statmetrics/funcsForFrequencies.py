#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 05/12/2011

@author: friend
'''
import scipy.stats

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
    self.tilSets = None
    self.frequencies = frequencies[:] 
    self.tilN = tilN
    self.minFreq = min(self.frequencies)
    self.maxFreq = max(self.frequencies)
    self.generateTilSets()

  def generateTilSets(self):
    '''
    This is the only public, externally callable, method of this class
    It invokes a 3-method tool-chain and then returns self.tilSets
    (Checkings will be implemented via unittests and other adhoc tests) 
    '''
    self.getDeltaFrequencyListAtConcurso()
    if self.listWithDeltaFrequencies == None:
      return None
    self.transformDeltaFrequenciesIntoFrequencyBorders()
    self.putDezenasInsideTilSets()

  def getTilSets(self, regenerate=False):
    if self.tilSets == None or regenerate:
      self.generateTilSets()
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
      self.listWithDeltaFrequencies = None
      return
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
    
  def findTilIndexForFreq(self, unorderedKeys, keyValue):
    if self.tilSets == None:
      return None
    unorderedKeys.sort()
    counterindex = unorderedKeys.index(keyValue) + 1
    for tilIndex in range(len(self.tilSets)):
      tilSet = self.tilSets[tilIndex]
      if counterindex in tilSet:
        return tilIndex
    return -1     


  
def getTilSets(frequencies, tilN):
  '''
  This method is a sort of "handler" to produce the til-sets via calling the same name instance method getTilSets()
  '''
  tilSetsObj = TilSets(frequencies, tilN)
  return tilSetsObj.getTilSets()



class Stats1:

  def __init__(self, numbers):
    '''
    Stats available: min, max, sum, histogram
    All of them are calculated "lazily", ie, as asked / on demand, then they are stored
    '''
    self.numbers   = numbers; self.nOfElements = None
    self.min       = None;    self.max         = None
    self.sum       = None;    self.avg         = None
    self.variance  = None;    self.std         = None
    self.median    = None;    self.mode        = None
    self.skew      = None;    self.kurtosis    = None
    self.histogram = None

  def describe(self):
    '''
    Left as a reference
    redesigned not to be used, due to the computation delay, plus storage, when only one of the descriptive metrics were asked
    
    self.quintuple     = scipy.stats.describe(self.numbers)
    self.nOfElements   = self.quintuple[0]
    self.min, self.max = self.quintuple[1]
    self.avg      = self.quintuple[2]
    self.variance = self.quintuple[3]
    self.skew     = self.quintuple[4]
    self.kurtosis = self.quintuple[4]
    '''
    pass

  def getMin(self):
    if self.min == None:
      self.min = min(self.numbers)
      #self.describe()
    return self.min

  def getMax(self):
    if self.max == None:
      self.max = max(self.numbers)
      #self.describe()
    return self.max

  def getSum(self):
    if self.sum == None:
      self.sum = sum(self.numbers)
      #self.describe()
    return self.sum

  def size(self):
    if self.nOfElements == None:
      self.nOfElements = len(self.numbers)
      #self.describe()
    return self.nOfElements

  def getAvg(self):
    if self.avg == None:
      self.avg = (self.getSum() + 0.0) / self.size()
    return self.avg

  def getMedian(self):
    if self.median == None:
      self.median = scipy.stats.cmedian(self.numbers)
    return self.median

  def getMode(self):
    if self.mode == None:
      self.mode = scipy.stats.mode(self.numbers)[0][0]
    return self.mode

  def getVariance(self):
    if self.variance == None:
      self.variance = scipy.stats.tvar(self.numbers)
    return self.variance

  def getStd(self):
    return self.getVariance() ** (1.0/2)

  def getSkew(self):
    if self.skew == None:
      self.skew = scipy.stats.skew(self.numbers)
    return self.skew

  def getKurtosis(self):
    if self.kurtosis == None:
      self.kurtosis = scipy.stats.kurtosis(self.numbers)
    return self.kurtosis
  
  def getHistogram(self):
    if self.histogram == None:
      self.generateHistogram()
    return self.histogram
  
  def generateHistogram(self):
    self.histogram = {}
    # this checking for number == None is to be improved on the Constructor level
    if self.numbers == None:
      return None
    for number in self.numbers:
      if number in self.histogram.keys():
        self.histogram[number]+=1
      else:
        self.histogram[number]=1

  def __str__(self):
    numbers = self.numbers
    if numbers == None:
      return '<empty>'
    si = self.size()
    mn = self.getMin()
    mx = self.getMax()
    sm = self.getSum()
    vr = self.getVariance()
    # st = self.getStd()
    av = self.getAvg()
    st = self.getStd()
    md = self.getMedian()
    mo = self.getMode()
    sk = self.getSkew()
    ku = self.getKurtosis()
    hi = str(self.getHistogram())
    outStr = '''dataArray = %(numbers)s \t siz=%(si)d
    min=%(mn)d \t max=%(mx)d
    sum=%(sm)d \t var=%(vr)d
    avg=%(av)f \t std=%(st)f
    med=%(md)f \t mod=%(mo)d
    ske=%(sk)f \t kur=%(ku)f
    his=%(hi)s
    ''' %{'numbers':numbers, 'si':si,'mn':mn,'mx':mx,'sm':sm,'vr':vr,'av':av,'st':st,'md':md,'mo':mo,'sk':sk,'ku':ku,'hi':hi}
    return outStr

# test Stats1 class
a=range(1,21)
stats1= Stats1(a)
print stats1

def test_tilObjs():
  freqs = range(1,14)
  tilSetsObj = TilSets(freqs, 14)
  tilSets = tilSetsObj.getTilSets()
  print 'tilSets', tilSets   #print 'listWithFrequencyBordersTuple', self.listWithFrequencyBordersTuple, 'min max', self.minFreq, self.maxFreq
#test_tilObjs()

def test_tilObjs2():
  hist = {1: 785, 2: 735, 3: 643, 4: 631, 5: 566, 6: 460, 7: 458, 8: 371, 9: 332, 10: 297, 11: 275, 12: 238, 13: 217, 14: 222, 15: 186, 16: 155, 17: 152, 18: 116, 19: 114, 20: 118, 21: 93, 22: 85, 23: 70, 24: 79, 25: 70, 26: 60, 27: 56, 28: 43, 29: 43, 30: 34, 31: 32, 32: 28, 33: 25, 34: 14, 35: 17, 36: 25, 37: 15, 38: 15, 39: 11, 40: 21, 41: 13, 42: 7, 43: 11, 44: 13, 45: 11, 46: 3, 47: 5, 48: 6, 49: 2, 50: 6, 51: 5, 52: 6, 53: 5, 54: 5, 55: 3, 56: 3, 58: 1, 59: 3, 60: 3, 61: 2, 62: 4, 63: 1, 65: 1, 68: 2, 70: 1, 73: 1, 76: 1, 78: 1, 83: 1, 89: 1}
  # keys will be thrown away (lost), because algorithm keeps only the sequencial position
  freqs = hist.values()
  tilSetsObj = TilSets(freqs, 6)
  tilSets = tilSetsObj.getTilSets()
  print 'tilSets', tilSets   #print 'listWithFrequencyBordersTuple', self.listWithFrequencyBordersTuple, 'min max', self.minFreq, self.maxFreq
#test_tilObjs2()

if __name__ == '__main__':
  pass
