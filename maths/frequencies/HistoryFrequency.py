#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

'''
# import copy #  numpy #, os
import sys

import localpythonpath
localpythonpath.setlocalpythonpath()

from models.JogoSlider import JogoSlider
from maths.frequencies.HistoryFrequencyDB import HistFreqDBSlider # HistFreqDB,
from maths.frequencies.HistoryFrequencyDB import HistFreqUpdater

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
    self.total_histfreqs = self.histfreqdbslider.get_total_histfreqs()
    self.jogoSlider  = JogoSlider()
    self.total_jogos = self.jogoSlider.get_total_jogos()
    self.update_histfreq_if_needed()
    
  def update_histfreq_if_needed(self, secondTry=False):
    if self.total_histfreqs < self.total_jogos:
      self.histfreqdbslider.update_histfreqdb()
      if not secondTry:
        return self.update_histfreq_if_needed(secondTry=True)
      else:
        error_msg = 'Failed to update histfreq array. It should have the same size (=%d) as "concursos (=%d)".' %(self.total_histfreqs, self.total_jogos)
        raise ValueError, error_msg

  def get_jogo_by_nDoConc(self, nDoConc):
    '''
    Just a "convenience" public method (not used internally by the class)
    '''
    return self.jogoSlider.get_jogo_by_nDoConc(nDoConc)

  def get_histfreq_at(self, nDoConc=None, secondTry=False):
    if nDoConc == None:
      nDoConc = self.total_jogos # JogoSlider().get_total_jogos() # ie, number of last one
    elif nDoConc < 1 or nDoConc > self.total_jogos:
      error_msg = 'nº (=%d) do concurso fora da faixa válida (1, %d) ' %(nDoConc, self.total_jogos)
      raise ValueError, error_msg
    elif nDoConc > self.total_histfreqs:
      if secondTry:
        error_msg = 'There is a size different between total_jogo (=%d) and total_histfreqs (=%d) and nDoConc = %d. Program cannot continue until this is corrected.' %(self.total_jogos, self.total_histfreqs, nDoConc)
        raise ValueError, error_msg
      else:
        # try to update histfreqs so that total_histfreqs equals total_jogos
        HistFreqUpdater()
        return self.get_jogo_by_nDoConc(nDoConc, secondTry=True)
    # it return as a numpy array object
    histfreq = self.histfreqdbslider.get_histfreq_at(nDoConc)
    if histfreq == None:
      error_msg = "histfreq for concurso %d was not found. It's missing in database." %nDoConc
      raise IndexError, error_msg
    return histfreq
    # index = nDoConc - 1
    # return self.allhistfreqs[index]

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
  for nDoConc in [100, 300, 900, 1201]:
    numpy_histfreq = histfreqobj.get_histfreq_at(nDoConc)
    jogo = histfreqobj.get_jogo_by_nDoConc(nDoConc)
    print jogo, numpy_histfreq, numpy_histfreq.sum()
    numpy_histfreq = histfreqobj.get_histfreq_within_range((nDoConc-50, nDoConc)) 
    print 'faixa', numpy_histfreq, numpy_histfreq.sum()
  
def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
