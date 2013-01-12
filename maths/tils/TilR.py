#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
TilR.py
'''
# import numpy, time, sys
import sys

import __init__
__init__.setlocalpythonpath()

from libfunctions.jogos import volante_functions
from models.Concursos.ConcursoExt import ConcursoExt
from models.Concursos.VolanteCharacteristics import VolanteCharacteristics
# from TilPattern import TilDefiner
from TilProducer import TilProducer
import maths.statistics.HistoryFrequency as hf


class Dict2(dict):
  def add1_or_set1_to_key(self, k):
    if self.has_key(k):
      self[k]+=1
    else:
      self[k]=1
      
      
          
class TilR(object):
  '''
  This class (TilR) slots 1/nth, where n is the number of slots, of dozens in their frequency ascending order.
  
  As an illustration, suppose total elements is 60. Then, quintils (TilR n_slots=5) will order all dozens in their frequency order into 5 sets (slots).
  
  The difference between TilR and Til is following:
  
  Til cuts sets limits by equal distance frequencies, so the frequency is the determing factor in slicing dozens into slots
  TilR cuts sets limits by equal (or so, depending on division remainders) number of dozens
  
  Eg. outlining this difference:
   1) in TilR(n_slots=5) each slots (metric set) has exactly 12 dozens
   2) in Til(n_slots=5) each slots (metric set) has a variable number of dozens, 
      and it's not surprising to observe an empty set (or a set with very few dozens) and another one with much more than 12 in it
  
  '''
  DEFAULT_N_SLOTS = 5
  
  def __init__(self, n_slots = None, history_nDoConc_range = None, volante_caract=None):
    '''
    Parameter "inclusive" (attribute self.CONCURSO_PROPER_INCLUDED_IN_RANGE) 
      does one important differenciation in the process
    
    This differentiation is the following
    1) when one wants to observe/analyze a drawn sorteio, the sorteio itself should not be not counted,
       ie, should not contribute to the frequencies
    2) when one wants to "bet" a coming (not happened) sorteio, 
       the last concurso should contribute to the frequencies
    
    In other words, when analyzing, inclusive is False; when deriving for bets, inclusive is True 
    
    '''
    self.set_volante_caract(volante_caract)
    self.set_n_slots(n_slots)
    self.set_history_nDoConc_range(history_nDoConc_range)

  def set_volante_caract(self, volante_caract):
    if volante_caract == None or type(volante_caract) != VolanteCharacteristics:
      self.volante_caract = VolanteCharacteristics()
      return
    self.volante_caract = volante_caract
    
  def set_n_slots(self, n_slots=None):
    if n_slots == None:
      self.n_slots = self.DEFAULT_N_SLOTS
      return
    try:
      if n_slots == self.n_slots:
        return
    except AttributeError:
      pass
    try:
      int(n_slots)
    except ValueError:
      self.n_slots = self.DEFAULT_N_SLOTS
      return
    if n_slots < 2:
      raise ValueError, 'n_slots (=%d) < 2' %n_slots
    self.n_slots = n_slots
    self.verify_n_slots_is_good()
    self.redo_place_dozens_in_the_slots()

  def verify_n_slots_is_good(self):
    remainder = self.volante_caract.n_dezenas_no_volante % self.n_slots
    if remainder != 0:
      error_msg = 'Not yet implemented to inexact division quantiles. Example: a 60-number game can have 5, 6, 10 as n_slots, but cannot have 7 or 8 for instance.'
      raise ValueError, error_msg
    self.n_elems_per_slot = self.volante_caract.n_dezenas_no_volante / self.n_slots

  def set_history_nDoConc_range(self, history_nDoConc_range=None):
    '''
    This method is private!!!  From the "outside", use set_concurso_and_range() 
    '''
    slider = ConcursoExt()
    HIST_RANGE_DEFAULT = (1, slider.get_n_last_concurso()) 
    self.history_nDoConc_range = volante_functions.return_int_range_or_default_or_raise_ValueError(history_nDoConc_range, HIST_RANGE_DEFAULT)
    self.redo_place_dozens_in_the_slots()

  def place_dozens_in_the_slots(self):
    # in the future, whether jogo is Megasena or other will have to be passed on to histfreqobj
    histfreq = hf.histfreqobj.get_histfreq_within_range(self.history_nDoConc_range)
    all_dezenas = range(1, self.volante_caract.n_dezenas_no_volante + 1)
    self.dezenas_with_histfreq = zip(all_dezenas, histfreq)
    self.dezenas_with_histfreq_sorted_by_freqs = self.dezenas_with_histfreq[:] 
    self.dezenas_with_histfreq_sorted_by_freqs.sort(key = lambda x : x[1])
    dezenas_to_slots = zip(*self.dezenas_with_histfreq_sorted_by_freqs)[0]
    self.tilrsets = []
    index_ini = 0; index_fim = self.n_elems_per_slot 
    while index_ini < self.volante_caract.n_dezenas_no_volante - self.n_elems_per_slot + 1:
      tilrset = dezenas_to_slots[index_ini : index_fim] 
      self.tilrsets.append(tilrset)
      index_ini = index_fim; index_fim += self.n_elems_per_slot

  def redo_place_dozens_in_the_slots(self):
    try:
      self.history_nDoConc_range
    except AttributeError:
      # not yet time to recompute, due to construction-time order of attribute setting
      return
    self.place_dozens_in_the_slots()

  def get_game_tilrpattern_as_list(self, dezenas):
    '''
    This method takes a tuple of dozens (a game) and calculates its TilR(n) pattern
    Example:
    game = 1,7,13,24,35,46
    Suppose TilR(n=5):
      freq(d1=1)=slot3 
      freq(d2=7)=slot3 
      freq(d3=13)=slot5
      freq(d4=24)=slot1
      freq(d5=35)=slot2
      freq(d6=46)=slot1
    Its TilR(5) pattern will be 21201 which means 2 dozens in slot 1, 1 dozen in slot 2 and so on
    ''' 
    tilrpattern = [0]*len(self.tilrsets)
    for dezena in dezenas:
      for i, tilr in enumerate(self.tilrsets):
        if dezena in tilr:
          tilrpattern[i]+=1
          break
    return tilrpattern
  
  def get_game_tilrpattern_as_list_and_str(self, dezenas):
    tilrpattern_as_list = self.get_game_tilrpattern_as_list(dezenas)
    tilrpattern_as_str = ''.join(map(str, tilrpattern_as_list))
    return tilrpattern_as_list, tilrpattern_as_str 

  def get_game_tilrpattern_as_str(self, dezenas):
    return self.get_game_tilrpattern_as_list_and_str(dezenas)[1]
   
  
class TilStats(TilProducer):
  
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
    
tilr_pool = {}; tilr_pool_keys_queue = []; TILR_POOL_SIZE = 20
def get_tilr_from_pool(n_slots = None, history_nDoConc_range = None, volante_caract=None):
  '''
  This function is an object reuse queue that aims to improve performance
    by avoiding the overhead of "heavily" many TilR object instantiations
  
  TilR needs three parameters to be constructed (a triple).
  This triple becomes a key to a dictionary (dict).
  
  '''
  tilr_pool_key = (n_slots, history_nDoConc_range, volante_caract)
  if tilr_pool.has_key(tilr_pool_key):
    return tilr_pool[tilr_pool_key] 
  tilr_pool_obj = TilR(n_slots, history_nDoConc_range, volante_caract)
  tilr_pool[tilr_pool_key] = tilr_pool_obj
  tilr_pool_keys_queue.append(tilr_pool_key)
  # in case some None has enter function as parameter
  nonnone_tilr_pool_key = (tilr_pool_obj.n_slots, tilr_pool_obj.history_nDoConc_range, tilr_pool_obj.volante_caract) 
  if not tilr_pool.has_key(nonnone_tilr_pool_key):
    tilr_pool[nonnone_tilr_pool_key] = tilr_pool_obj
    tilr_pool_keys_queue.append(nonnone_tilr_pool_key)
  if len(tilr_pool_keys_queue) > TILR_POOL_SIZE:
    # This is a FIFO Queue, ie, First-In First-Out
    tilr_pool_key = tilr_pool_keys_queue[0] 
    del tilr_pool[tilr_pool_key]
    del tilr_pool_keys_queue[0]
  if len(tilr_pool_keys_queue) > TILR_POOL_SIZE or len(tilr_pool) > TILR_POOL_SIZE:
    current_queue_size = len(tilr_pool_keys_queue)
    msg_dict = {'TILR_POOL_SIZE':TILR_POOL_SIZE, 'current_queue_size':current_queue_size}
    error_msg = 'TilR Pool Queue exceeded its maximum size of %(TILR_POOL_SIZE)d :: len(tilr_pool_keys_queue)=%(current_queue_size)d > %(TILR_POOL_SIZE)d' %msg_dict
    raise IndexError, error_msg
  return tilr_pool_obj
  
 
def run_history():
  slider = ConcursoExt()
  volante_caract = VolanteCharacteristics(n_dezenas_no_volante=60, n_dezenas_no_sorteio=6)
  tilrstats = TilStats(n_slots=5, soma=volante_caract.n_dezenas_no_sorteio)
  tilrobj   = TilR(n_slots=5, history_nDoConc_range = None, volante_caract=volante_caract)
  for nDoConc in xrange(101, slider.get_n_last_concurso()+1):
    concurso = slider.get_concurso_by_nDoConc(nDoConc)
    # reuse tilrobj!
    tilrobj.set_history_nDoConc_range(history_nDoConc_range = (1, nDoConc-1))
    pattern_as_list = tilrobj.get_game_tilrpattern_as_list(concurso.get_dezenas())
    tilrstats.add_pattern_as_list(pattern_as_list)
  tilrstats.print_summary()
  print 'len(tilrstats)', len(tilrstats) 
      
def get_tilrwpattern_of_game(dezenas, n_slots=5, up_to_concurso=None):
  slider = ConcursoExt()
  if up_to_concurso == None:
    up_to_concurso = slider.get_last_concurso()
  tilr_obj = TilR(n_slots, up_to_concurso) #, inclusive=False, concurso_range = None)
  return tilr_obj.get_tilrwpattern_of_game(dezenas)
      
def adhoc_test():
  '''
  tilrobj = TilR()
  print 'tilrsets', tilrobj.tilrsets
  print 'tilrpattern', tilrobj.get_wpattern()'''
  run_history()


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
