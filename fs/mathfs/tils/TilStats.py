#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
TilR.py
'''
# import numpy, time, sys
import sys

import __init__
__init__.setlocalpythonpath()

from fs.util.pyobjects_ext import Dict2
from TilProducer import TilProducer

  
class TilStats(TilProducer):
  '''
  The purpose of this class (TilStats) is to perform statistics on an array of Til Patterns
  
  For the time being, the statistics are:
  1) histogram with occurrences
  2) the difference set (though this is not properly a statistic)
  
  Examples:
  1) About the histogram:
     02211 may have happened 21 times, so a Python-dict (say, pydict) will have pydict['02211']=21
  
  2) About the difference set
     In spite of TilR's (5, 6), there are 210 combinations of them.  Some of them have never occurred.
     More particularly, a pattern such as 06000 or 00501 has never occurred,
     so they will come up in the difference set.
  '''
  
  def __init__(self, n_slots=None, soma=None):
    super(TilStats, self).__init__(n_slots, soma)
    self.wpatterndict = Dict2()
    self.wpatterns = []
 
  def add_pattern_as_str(self, pattern_str):
    self.wpatterndict.add1_or_set1_to_key(pattern_str)
    self.wpatterns = self.wpatterndict.keys()

  def add_pattern_as_list(self, pattern_list):
    pattern_str = ''.join(map(str, pattern_list))
    self.add_pattern_as_str(pattern_str)

  def get_wpatterns(self):
    return self.wpatterns # to gain performance instead of issuing dict.keys() (below)
    # return self.wpatterndict.keys()
  
  def print_difference(self):
    self.alltilwpatterns
    added_wpatterns = self.wpatterndict.keys() 
    for wpattern in self.alltilwpatterns:
      if wpattern not in added_wpatterns:
        print 'Not occurred', wpattern   

  def print_summary(self):
    wpatterns_and_quants = self.wpatterndict.items()
    wpatterns_and_quants.sort(key = lambda x : x[1])
    for wpattern_and_quant in wpatterns_and_quants:
      wpattern = wpattern_and_quant[0]
      quant    = wpattern_and_quant[1]
      print wpattern, ':', quant, 'times'
    print 'pattern total', len(wpatterns_and_quants)
    self.print_difference()
    self.print_python_list_for_all_patterns_with_less_than_n_occurrences(4)

  def print_python_list_for_all_patterns_with_less_than_n_occurrences(self, n_occurrences):
    outlist = []
    print 'self.alltilwpatterns', self.alltilwpatterns
    for wpattern in self.alltilwpatterns:
      if self.wpatterndict.has_key(wpattern):
        quant = self.wpatterndict[wpattern]
        if quant >= n_occurrences:
          continue
    # ie, either not wpattern is not in self.wpatterndict or its quant < n_occurrences
      outlist.append(wpattern)
    # now write a Python list source code
    print 'outlist', outlist
    outstr = "tilrwpatterns_to_filter_out = ["
    for wpattern in outlist:
      sourcecode ="'%s'," %wpattern 
      outstr += sourcecode
    outstr += "] # len/size = %d" %(len(outlist))
    # return outstr
    print outstr
    
  # (inherited) get_n_all_tilrpatterns(self) or __len__(self):
  # (inherited) def get_alltilpatterns_as_intlists(self):
    
      
class TilStatsWithDozens(object):
  '''
  This class is a beginning idea, nothing has been "accomplished" yet
  Its methods come from the now extinct TilConcurso class, 
    so it's to be thought out later on, okay?
  '''


  def get_freq_of_dozen(self, dezena):
      index = dezena - 1
      freq = self.histfreq[index]
      return freq

  def get_dezenas_and_their_frequencies_for_concurso(self):
    dezenas = self.concurso.get_dezenas()
    freqs = []
    for dezena in dezenas:
      freq = self.get_freq_of_dozen(dezena)
      freqs.append(freq)
    return zip(dezenas, freqs)

  def get_dezenas_their_frequencies_and_til_for_concurso(self):
    # tilsetobj = ts.TilSets(self.histfreq, self.n_slots)
    zipped = self.get_dezenas_and_their_frequencies_for_concurso()
    # unzip dezenas and freqs
    dezenas, freqs = zip(*zipped)
    tils = []
    for dezena in dezenas:
      for i in range(len(self.tilsetobj.tilSets)):
        if dezena in self.tilsetobj.tilSets[i]:
          tils.append(i)
          break
    return zip(dezenas, freqs, tils)
    
  # should be private to class, triggered by flow_concursorange_histfreq_wpattern()
  def calc_concursotil_wpattern(self):
    self.tilsetobj = ts.TilSets(self.histfreq, self.n_slots)
    dezenas = self.concurso.get_dezenas()
    tilpatternlist = [0] * self.tilsetobj.til_n # tilN is the same as slots
    for dezena in dezenas:
      for i, tilset in enumerate(self.tilsetobj.tilSets):
        if dezena in tilset:
          # print 'found', dezena, 'inside i=',i, tilSets[i]   
          tilpatternlist[i] += 1
          break
    wpattern = ''.join(map(str, tilpatternlist))
    self.set_wpattern(wpattern)
    # self.tilpatternlist = tilpatternlist 
  
  def get_percentual_freqs_per_til(self):
    percentual_freqs_per_til = []
    for tilset in self.tilsetobj.tilSets:
      tilset_total_freq = 0
      for dezena in tilset:
        freq = self.get_freq_of_dozen(dezena)
        tilset_total_freq += freq
      # percentual_per_til = 100 * tilset_total_freq / self.histfreq_sum # this version is supposedly quicker in computation time 
      percentual_per_til = int( round ( 100.0 * tilset_total_freq / self.histfreq_sum , 0) ) 
      percentual_freqs_per_til.append(percentual_per_til)
    return percentual_freqs_per_til

  def get_tilpattern_interlaced_with_n_dozens_per_til(self):
    n_dozens_per_til = []
    for tilset in self.tilsetobj.tilSets:
      n_dozens_per_til.append(len(tilset))
    tilpatternlist = [c for c in self.wpattern]      
    return zip(tilpatternlist, n_dozens_per_til, self.get_percentual_freqs_per_til())

  def is_same_tilpattern(self, tilpattern):
    if self.concursotilpattern == tilpattern:
      return True
    return False 

  def does_pass_tilqueue(self, tilqueue):
    '''
    Jogo passes (filters in) tilqueue if at least one tilpattern in the queue coincides with the one this jogo has
    '''
    # can this method be optimized?
    for tilpattern in tilqueue:
      if self.is_same_tilpattern(tilpattern):
        return True
    return False

  def __str__(self):
    output_text = str(self.concurso)
    output_text += ' range' + str(self.concurso_range)
    return output_text


      
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
