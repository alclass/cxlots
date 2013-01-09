#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 29/12/2011

@author: friend
'''
a=1
import sqlLayer as sl
import frequencyMounting as fm
import statmetrics.funcsForFrequencies as fForFreqs

def lookUpDozenLastOccurDepth(dezena, nDoConcWhereDezenaIs):
  '''
  this method may be considered 'static'
  '''
  for nDoConc in range(nDoConcWhereDezenaIs - 1, 0, -1):
    concObj = sl.getConcursoObjByN(nDoConc)
    dezenas = concObj.getDezenas()
    if dezena in dezenas:
      depth = nDoConcWhereDezenaIs - nDoConc
      return depth  
  return None

def lookUpDozenLastOccurrenceNDoConc(dezena):
  '''
  this method may be considered 'static'
  it considers the last concurso and call lookUpDozenDepth(dezena, nDoConcWhereDezenaIs)
  
  However, one care is taken: if dezena happened in the last concurso. 0 (zero) should be returned
  '''
  concurso = sl.getConcursoObjByN() # this picks up the last concurso
  if concurso.isDezenaInConcurso(dezena):
    # if true, depth is 0, ie, dezena happened at the last concurso 
    return 0
  nTotalDeConcursos =  sl.getNTotalDeConcursos() # the same thing: = concurso['nDoConcurso']
  return lookUpDozenLastOccurDepth(dezena, nTotalDeConcursos)

def produceDozensDepthRow(dezena):
  '''
  each dezena has an array that corresponds to the number of concursos it last occurred from occurrence to occurrence 
  Ex. depthRow of dozen 15 = [3, 5, 1, ..., 12]
      This means, starting backwards, from its last occurrence, it occurred 3 concursos before the last, than 5 from the one before last and so on
  '''
  allDezenasDepthRow = []
  # nTotalDeConcursos =  sl.getNTotalDeConcursos()
  lastOccurrence = lookUpDozenLastOccurrenceNDoConc(dezena); currentDepth = 0  
  for nDoConc in range(lastOccurrence - 1, 0, -1):
    currentDepth += 1
    concurso = sl.getConcursoObjByN(nDoConc)
    dezenas = concurso.getDezenas()
    if dezena in dezenas:
      allDezenasDepthRow.append(currentDepth)
      currentDepth = 0
  return allDezenasDepthRow

class OccurrenceDepths:

  def __init__(self):
    self.allDezenasDepthRow = {}
    self.tilN = 6 # default 
    self.produceAllDepthsPerDozen()
    self.dozensLastOccurrenceForAllConcursos = None

  def setTilN(self, tilN):
    self.tilN = tilN 

  def produceAllDepthsPerDozen(self):
    for dezena in range(1, 61):
      self.allDezenasDepthRow[dezena] = produceDozensDepthRow(dezena)
  
  def displayDepthArraySizePerDozen(self):
    for dezena in range(1, 61):
      print 'dezena', dezena, 'DepthArraySize', len(self.allDezenasDepthRow[dezena]), self.allDezenasDepthRow[dezena]   

  def getDozensLastOccurrencePerConcurso(self, nDoConc=None):
    nTotalDeConcursos = sl.getNTotalDeConcursos()
    if nDoConc == None:
      nDoConc = nTotalDeConcursos
    if nDoConc < 1 or nDoConc > nTotalDeConcursos:
      return None
    concurso = sl.getConcursoObjByN(nDoConc)
    dezenas = concurso.getDezenas(); lastDepthPerDozenDict = {}
    for dezena in dezenas:
      lastDepthPerDozenDict[dezena] = lookUpDozenLastOccurDepth(dezena, nDoConc)
    return lastDepthPerDozenDict

  def generateDozensLastOccurrenceForAllConcursos(self):
    nTotalDeConcursos = sl.getNTotalDeConcursos()
    self.dozensLastOccurrenceForAllConcursos = []
    for nDoConc in range(1, nTotalDeConcursos+1):
      lastDepthPerDozenDict = self.getDozensLastOccurrencePerConcurso(nDoConc)
      self.dozensLastOccurrenceForAllConcursos.append(lastDepthPerDozenDict)

  def stats_lastDepthPerDozenForAllConcursos(self, printCallBack=None):
    if self.dozensLastOccurrenceForAllConcursos == None:
      self.generateDozensLastOccurrenceForAllConcursos()
    nTotalDeConcursos = sl.getNTotalDeConcursos()
    self.minDepth = 100; self.maxDepth = 0; depthHistogram = {}
    # sweep all concursos
    for nDoConc in range(1, nTotalDeConcursos+1):
      lastDepthPerDozenDict = self.dozensLastOccurrenceForAllConcursos[nDoConc - 1]
      tilIndices = self.processDezenasFor_stats_lastDepthPerDozenForAllConcursos(lastDepthPerDozenDict, depthHistogram)
      tilStats = fForFreqs.Stats1(tilIndices)
      #params = nDoConc, tilIndices, tilStats #.getHistogram()
      concurso = sl.getConcursoObjByN(nDoConc)
      print nDoConc, concurso.getDezenasPrintable(), tilStats #.getHistogram()tilIndices,
      
    print 'minDepth', self.minDepth, 'maxDepth', self.maxDepth
    '''
      if nDoConc > 1000:
        tilSetsObj = fForFreqs.TilSets(depthHistogram.values(), 6)
        tilSets = tilSetsObj.getTilSets()
        tilIndices = []
        for dezena in dezenas:
          tilIndex = tilSetsObj.findTilIndexForFreq(depthHistogram.keys(), lastDepthPerDozenDict[dezena])
          tilIndices.append(tilIndex)
        print '>>>', nDoConc, tilIndices, lastDepthPerDozenDict #,
        print depthHistogram
        print 'tilSets', tilSets 
        #sixtilIndices += findSixtilIndex(depth, depthHistogram)
      ''' 

  def processDezenasFor_stats_lastDepthPerDozenForAllConcursos(self, lastDepthPerDozenDict, depthHistogram):
    depth = None; dezenas = lastDepthPerDozenDict.keys() #; dezenas.sort()
    for dezena in dezenas:
      depth = lastDepthPerDozenDict[dezena]
      if depth == None:
        return None
      if depth < self.minDepth:
        self.minDepth = depth  
      if depth > self.maxDepth:
        self.maxDepth = depth
      if depth in depthHistogram.keys():
        depthHistogram[depth] += 1
      else:
        depthHistogram[depth] = 1
    # if program flow got to here, depth is not None, so depthHistogram must have some values, let's move on! 
    tilSetsObj = fForFreqs.TilSets(depthHistogram.values(), self.tilN) #tilSets = tilSetsObj.getTilSets()
    tilIndices = []
    for dezena in dezenas:
      tilIndex = tilSetsObj.findTilIndexForFreq(depthHistogram.keys(), lastDepthPerDozenDict[dezena])
      if tilIndex == None or tilIndex == -1:
        return None  
      tilIndices.append(tilIndex)
    return tilIndices 

  def print_lastDepthPerDozenForAllConcursos(self):
    if self.dozensLastOccurrenceForAllConcursos == None:
      self.generateDozensLastOccurrenceForAllConcursos()
    nTotalDeConcursos = sl.getNTotalDeConcursos()
    for nDoConc in range(1, nTotalDeConcursos+1):
      self.print_lastDepthPerDozen(nDoConc)

  def print_lastDepthPerDozen(self, nDoConc):
    lastDepthPerDozenDict = self.dozensLastOccurrenceForAllConcursos[nDoConc - 1]
    dezenas = lastDepthPerDozenDict.keys()
    dezenas.sort(); line = ''
    for dezena in dezenas:
      depth = lastDepthPerDozenDict[dezena]
      if depth == None:
        return
      else:
        line += '%02d:%02d ' %(dezena, depth)
    print nDoConc, line
    
  def print_allDezenasDepthRow(self):
    lastNDoConc = sl.getNTotalDeConcursos()
    print self.dozensLastOccurrenceForAllConcursos[lastNDoConc - 1]

  def compareOccurDepthWithFrequencies(self): 
    freqsObj = fm.FrequenciesThruConcursos()
    freqs = freqsObj.getLast()
    for dezena in range(1, 61):
      print dezena, self.allDezenasDepthRow[dezena], len(self.allDezenasDepthRow[dezena]), freqs[dezena-1]

def testDepth(concurso):
  dezenas = concurso.getDezenas(); depthsStr = '' 
  for dezena in dezenas:
    nDoConcWhereDezenaIs = concurso['nDoConcurso'] 
    depth = lookUpDozenLastOccurDepth(dezena, nDoConcWhereDezenaIs)
    depthsStr += ':' + str(depth).zfill(2)
  print nDoConcWhereDezenaIs, ' :', dezenas
  print 'depths', depthsStr

def testDepths():
  concursos = sl.getLastConcursosObjs(10)
  for concurso in concursos:
    testDepth(concurso)

def test_produceDozensDepthRow():
  occurenceDepths = OccurrenceDepths()
  #occurenceDepths.displayDepthArraySizePerDozen() 
  #occurenceDepths.displayAllDezenasDepthRow()
  #occurenceDepths.compareOccurDepthWithFrequencies()
  # occurenceDepths.getDozensLastOccurrencePerConcurso()
  #occurenceDepths.print_lastDepthPerDozenForAllConcursos()
  occurenceDepths.setTilN(12)
  occurenceDepths.stats_lastDepthPerDozenForAllConcursos()
  #occurenceDepths.displayDepthArraySizePerDozen()
  

if __name__ == '__main__':
  # testDepths()
  test_produceDozensDepthRow()
