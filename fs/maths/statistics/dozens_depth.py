#!/usr/bin/env python3
"""
fs/maths/statistics/dozens_depth.py

Created on 29/12/2011
Modified/Updated (to Python3) on 06/01/2023
"""
import sqlLayer as sl
import frequencyMounting as fm
import statmetrics.funcsForFrequencies as fForFreqs


def look_up_dozen_last_occur_depth(dezena, n_do_conc_where_dezena_is):
  """
  this method may be considered 'static'
  """
  for n_do_conc in range(n_do_conc_where_dezena_is - 1, 0, -1):
    conc_obj = sl.getConcursoObjByN(n_do_conc)
    dezenas = conc_obj.getDezenas()
    if dezena in dezenas:
      depth = n_do_conc_where_dezena_is - n_do_conc
      return depth  
  return None


def look_up_dozen_last_occurrence_n_do_conc(dezena):
  """
  this method may be considered 'static'
  it considers the last concurso and call lookUpDozenDepth(dezena, nDoConcWhereDezenaIs)
  
  However, one care is taken: if dezena happened in the last concurso. 0 (zero) should be returned
  """
  concurso = sl.getConcursoObjByN() # this picks up the last concurso
  if concurso.isDezenaInConcurso(dezena):
    # if true, depth is 0, ie, dezena happened at the last concurso 
    return 0
  n_total_de_concursos =  sl.getNTotalDeConcursos() # the same thing: = concurso['nDoConcurso']
  return look_up_dozen_last_occur_depth(dezena, n_total_de_concursos)


def produce_dozens_depth_row(dezena):
  """
  each dezena has an array that corresponds to the number of concursos
    it lastly occurred from occurrence to occurrence
  Example:
    depthRow of dozen 15 = [3, 5, 1, ..., 12]
      This means, starting backwards, from its last occurrence,
      it occurred 3 concursos before the last, than 5 from the one before last and so on
  """
  all_dezenas_depth_row = []
  # nTotalDeConcursos =  sl.getNTotalDeConcursos()
  last_occurrence = look_up_dozen_last_occurrence_n_do_conc(dezena)
  current_depth = 0
  for n_do_conc in range(last_occurrence - 1, 0, -1):
    current_depth += 1
    concurso = sl.getConcursoObjByN(n_do_conc)
    dezenas = concurso.getDezenas()
    if dezena in dezenas:
      all_dezenas_depth_row.append(current_depth)
      current_depth = 0
  return all_dezenas_depth_row


class OccurrenceDepths:

  DEFAULT_TILN = 6
  NUMBERSIZE = 60

  def __init__(self, til_n):
    self.all_dezenas_depth_row = {}
    self.til_n = self.DEFAULT_TILN
    self.produce_all_depths_per_dozen()
    self._all_depths = None
    self.dozens_last_occurrence_for_all_concursos = None

  def produce_all_depths_per_dozen(self):
    for dezena in range(1, self.NUMBERSIZE):
      self.all_dezenas_depth_row[dezena] = produce_dozens_depth_row(dezena)
  
  def displayDepthArraySizePerDozen(self):
    for dezena in range(1, 61):
      print 'dezena', dezena, 'DepthArraySize', len(self.all_dezenas_depth_row[dezena]), self.all_dezenas_depth_row[dezena]

  def getDozensLastOccurrencePerConcurso(self, nDoConc=None):
    nTotalDeConcursos = sl.getNTotalDeConcursos()
    if nDoConc == None:
      nDoConc = nTotalDeConcursos
    if nDoConc < 1 or nDoConc > nTotalDeConcursos:
      return None
    concurso = sl.getConcursoObjByN(nDoConc)
    dezenas = concurso.getDezenas(); lastDepthPerDozenDict = {}
    for dezena in dezenas:
      lastDepthPerDozenDict[dezena] = look_up_dozen_last_occur_depth(dezena, nDoConc)
    return lastDepthPerDozenDict

  def generateDozensLastOccurrenceForAllConcursos(self):
    nTotalDeConcursos = sl.getNTotalDeConcursos()
    self.dozens_last_occurrence_for_all_concursos = []
    for nDoConc in range(1, nTotalDeConcursos+1):
      lastDepthPerDozenDict = self.getDozensLastOccurrencePerConcurso(nDoConc)
      self.dozens_last_occurrence_for_all_concursos.append(lastDepthPerDozenDict)

  def stats_lastDepthPerDozenForAllConcursos(self, printCallBack=None):
    if self.dozens_last_occurrence_for_all_concursos == None:
      self.generateDozensLastOccurrenceForAllConcursos()
    nTotalDeConcursos = sl.getNTotalDeConcursos()
    self.minDepth = 100; self.maxDepth = 0; depthHistogram = {}
    # sweep all concursos
    for nDoConc in range(1, nTotalDeConcursos+1):
      lastDepthPerDozenDict = self.dozens_last_occurrence_for_all_concursos[nDoConc - 1]
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
    tilSetsObj = fForFreqs.TilSets(depthHistogram.values(), self.til_n) #tilSets = tilSetsObj.getTilSets()
    tilIndices = []
    for dezena in dezenas:
      tilIndex = tilSetsObj.findTilIndexForFreq(depthHistogram.keys(), lastDepthPerDozenDict[dezena])
      if tilIndex == None or tilIndex == -1:
        return None  
      tilIndices.append(tilIndex)
    return tilIndices 

  def print_lastDepthPerDozenForAllConcursos(self):
    if self.dozens_last_occurrence_for_all_concursos == None:
      self.generateDozensLastOccurrenceForAllConcursos()
    nTotalDeConcursos = sl.getNTotalDeConcursos()
    for nDoConc in range(1, nTotalDeConcursos+1):
      self.print_lastDepthPerDozen(nDoConc)

  def print_lastDepthPerDozen(self, nDoConc):
    lastDepthPerDozenDict = self.dozens_last_occurrence_for_all_concursos[nDoConc - 1]
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
    print self.dozens_last_occurrence_for_all_concursos[lastNDoConc - 1]

  def compareOccurDepthWithFrequencies(self): 
    freqsObj = fm.FrequenciesThruConcursos()
    freqs = freqsObj.getLast()
    for dezena in range(1, 61):
      print dezena, self.all_dezenas_depth_row[dezena], len(self.all_dezenas_depth_row[dezena]), freqs[dezena - 1]

def testDepth(concurso):
  dezenas = concurso.getDezenas(); depthsStr = '' 
  for dezena in dezenas:
    nDoConcWhereDezenaIs = concurso['nDoConcurso'] 
    depth = look_up_dozen_last_occur_depth(dezena, nDoConcWhereDezenaIs)
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
  occurenceDepths.set_til_n(12)
  occurenceDepths.stats_lastDepthPerDozenForAllConcursos()
  #occurenceDepths.displayDepthArraySizePerDozen()
  

if __name__ == '__main__':
  # testDepths()
  test_produceDozensDepthRow()
