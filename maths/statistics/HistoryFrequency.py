#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

'''
# import copy #  numpy #, os
import sys

import __init__
__init__.setlocalpythonpath()

from models.Concursos.ConcursoExt import ConcursoExt
from maths.statistics.HistoryFrequencyDB import HistFreqDBSlider # HistFreqDB,
from maths.statistics.HistoryFrequencyDB import HistFreqUpdater

class HistFreq(object):
  '''
  A histfreq composes (ie, its attributes):
  --------------------
  + bottomconc = the lower concurso number in the range composing the frequency histogram
  + topconc = the upper concurso number in the range composing the frequency histogram
  + (private) dezenasfreqs = sorted list of each dezena's total occurrence (ie, its frequency) in the related range (bottomconc, topconc)  
  --------------------
  A histfreq does (ie, its methods):
  + mount_histfreq  
  '''
  def __init__(self): # concurso_range
    self.histfreqdbslider = HistFreqDBSlider()
    self.total_histfreqs  = self.histfreqdbslider.get_total_histfreqs()
    self.slider           = ConcursoExt()
    self.total_concursos  = self.slider.get_total_concursos()
    self.update_histfreq_if_needed()
    
  def reissueHistFreqUpdater(self):
    HistFreqUpdater()
    self.total_histfreqs  = self.histfreqdbslider.get_total_histfreqs()
        
  def update_histfreq_if_needed(self, secondTry=False):
    if self.total_histfreqs < self.total_concursos:
      self.reissueHistFreqUpdater()
      if not secondTry:
        return self.update_histfreq_if_needed(secondTry=True)
      else:
        error_msg = 'Failed to update histfreq array. It should have the same size (=%d) as "concursos (=%d)".' %(self.total_histfreqs, self.total_concursos)
        raise ValueError, error_msg

  def get_concurso_by_nDoConc(self, nDoConc):
    '''
    Just a "convenience" public method (not used internally by the class)
    '''
    return self.concursoSlider.get_concurso_by_nDoConc(nDoConc)

  def get_histfreq_at(self, nDoConc=None, secondTry=False):
    '''
    histfreq is a numpy array that contains frequencies of all dozens (ex., in Megasena it's a 60-number array)
    dozen 1 has its frequency at index 0, dozen 2, index 1, so on until dozen 60 at index 59
    '''
    if nDoConc == None:
      nDoConc = self.total_concursos # JogoSlider().get_total_jogos() # ie, number of last one
    elif nDoConc < 1 or nDoConc > self.total_concursos:
      error_msg = 'nº (=%d) do concurso fora da faixa válida (1, %d) ' %(nDoConc, self.total_concursos)
      raise ValueError, error_msg
    elif nDoConc > self.total_histfreqs:
      if secondTry:
        error_msg = 'There is a size different between total_jogo (=%d) and total_histfreqs (=%d) and nDoConc = %d. Program cannot continue until this is corrected.' %(self.total_jogos, self.total_histfreqs, nDoConc)
        raise ValueError, error_msg
      else:
        # this should be a very rare use case, ie, database has changed while this class is still instantiated and running :: try to update histfreqs so that total_histfreqs equals total_concursos
        self.reissueHistFreqUpdater()
        return self.get_concurso_by_nDoConc(nDoConc, secondTry=True)
    # it return as a numpy array object
    histfreq = self.histfreqdbslider.get_histfreq_at(nDoConc)
    if histfreq == None:
      error_msg = "histfreq for concurso %d was not found. It's missing in database." %nDoConc
      raise IndexError, error_msg
    return histfreq
    # index = nDoConc - 1
    # return self.allhistfreqs[index]

  def get_histfreq_tuplelike_at(self, nDoConc=None, secondTry=False):
    '''
    Same as get_histfreq_at(), the plus is that it zips range(1, 61) with histfreq
    '''
    total_dezenas = len(self.get_histfreq_at(nDoConc))
    dezenas = range(1, total_dezenas + 1)
    return zip(dezenas, self.get_histfreq_at(nDoConc))

  def get_freqstair_at(self, nDoConc=None):
    '''
    freqstair is an ordered array from minimum frequency (least occurred) to maximum frequency (most occurred) at nDoConc
    '''
    histstair = set ( self.get_histfreq_at(nDoConc) )
    histstair = list( histstair )
    histstair.sort()
    return histstair

  def get_freqstair_with_dozens_at(self, nDoConc=None):
    '''
    freqstair is an ordered array from minimum frequency (least occurred) to maximum frequency (most occurred) at nDoConc
    '''
    freqstair_with_dozens = []
    freqstair = self.get_freqstair_at(nDoConc)
    for freq in freqstair:
      subset_dezenas = []; offset = 0; histfreq = list( self.get_histfreq_at(nDoConc) ) 
      while 1:
        try:
          index = histfreq.index(freq)
          del histfreq[ : index + 1]
          dezena = offset + index + 1
          offset += index + 1
          subset_dezenas.append(dezena)
          # print 'dezena', dezena, 'freq', freq, freqstair
          # print histfreq, 'tam', len(histfreq) 
          if len(histfreq) == 0:
            break
        except ValueError:
          break
      freqstair_with_dozens.append( (freq, subset_dezenas) )
    return freqstair_with_dozens

  def get_histfreq_within_range(self, concurso_range=None):
    if concurso_range == None:
      return self.get_histfreq_at()
    bottomconc = concurso_range[0] 
    topconc    = concurso_range[1]
    if bottomconc == 1:
      return self.get_histfreq_at(topconc)
    return self.get_deltahistfreq(bottomconc, topconc)

  def get_deltahistfreq(self, bottomconc, topconc):
    if bottomconc == 1:
      return self.get_histfreq_at(topconc)
    bottomfreqhist = self.get_histfreq_at(bottomconc-1)
    topfreqhist    = self.get_histfreq_at(topconc)
    deltafreqhist  = topfreqhist - bottomfreqhist  # + self.numpy_ones
    # it return as a numpy array object 
    return deltafreqhist # no need to hardcopy this one, because it's computed here

  def get_histfreq_for_dezena_witin_range(self, dezena, concurso_range=None):
    histfreq = self.get_histfreq_within_range(concurso_range)
    if histfreq == None:
      return None
    if dezena < 1 or dezena > len(histfreq) + 1:
      error_msg = 'Dezena (=%d) fora da faixa válida (%d, %d)' %(dezena, 1, len(histfreq) + 1)
      raise ValueError, error_msg
    index = dezena - 1
    return histfreq[index]

  def __str__(self):
    return '<HistFreq self.total_histfreqs=%d>' %self.total_histfreqs
     
histfreqobj = HistFreq() # simulates Singleton
def get_histfreq(concurso_range=None):
  return histfreqobj.get_histfreq_within_range(concurso_range)


def adhoc_test():
  for nDoConc in [100, 300, 900, 1201, 1401]:
    numpy_histfreq = histfreqobj.get_histfreq_at(nDoConc)
    jogo = histfreqobj.get_concurso_by_nDoConc(nDoConc)
    print jogo, numpy_histfreq, numpy_histfreq.sum()
    numpy_histfreq = histfreqobj.get_histfreq_within_range((nDoConc-50, nDoConc)) 
    print 'histfreq "-50"', numpy_histfreq, 'histfreq sum', numpy_histfreq.sum()
    freqstairmsg = 'histfreqobj.get_freqstair_at(%d)' %(nDoConc)
    freqstair = histfreqobj.get_freqstair_at(nDoConc)
    freqstairwithdozens = histfreqobj.get_freqstair_with_dozens_at(nDoConc)
    tam = len(freqstair)
    print freqstairmsg, freqstair, tam
    for freqstairwithdozen in freqstairwithdozens:
      print freqstairwithdozen  
  
def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
