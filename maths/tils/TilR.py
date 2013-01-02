#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
TilR.py
'''
# import numpy, time, sys
import sys

import localpythonpath
from models.ConcursoHTML import ConcursoHTML
localpythonpath.setlocalpythonpath()

from models.Concurso import ConcursoBase
from TilPattern import TilDefiner
import maths.frequencies.HistoryFrequency as hf

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
  def __init__(self, n_slots = 5, concurso = None, inclusive=False, concurso_range = None):
    '''
    Parameter "inclusive" (attribute self.CONCURSO_PROPER_INCLUDED_IN_RANGE) does one important differenciation in the process
    
    This differenciation is the following
    1) when one wants to observe/analyze a drawn sorteio, the sorteio itself should not be not counted, ie, should not contribute to the frequencies
    2) when one wants to "bet" a coming (not happened) sorteio, the last concurso should contribute to the frequencies
    
    In other words, when analyzing, inclusive is False; when deriving for bets, inclusive is True 
    
    '''
    self.CONCURSO_PROPER_INCLUDED_IN_RANGE = inclusive
    self.set_concurso(concurso)
    self.set_concurso_range(concurso_range)
    self.set_n_slots(n_slots)
    self.calc_tilr()
    self.wpattern = None
    
  def get_tildefiner(self):
    '''
    tildefiner is obtain "on-the-fly"
    '''
    return TilDefiner(self.n_slots, self.concurso.N_DE_DEZENAS)

  def set_n_slots(self, n_slots):
    self.n_slots = n_slots
    remainder = self.concurso.N_DE_DEZENAS_NO_VOLANTE % self.n_slots
    if remainder != 0:
      error_msg = 'Not yet implemented to inexact divide quantiles.'
      raise ValueError, error_msg
    self.n_elems_per_slot = self.concurso.N_DE_DEZENAS_NO_VOLANTE / self.n_slots 

  def set_concurso(self, concurso):
    if concurso == None:
      self.concurso = ConcursoBase().get_last_concurso()
    else:
      self.concurso = concurso
    
  def set_concurso_range(self, concurso_range):
    if concurso_range == None:
      bottomconc = 1
      if self.CONCURSO_PROPER_INCLUDED_IN_RANGE:
        topconc = self.concurso.nDoConc
      else:
        topconc = self.concurso.nDoConc - 1
      self.concurso_range = (bottomconc, topconc)
    else:
      self.concurso_range = concurso_range
      
  def calc_tilr(self):
    histfreq = hf.histfreqobj.get_histfreq_within_range(self.concurso_range)
    all_dezenas = range(1, self.concurso.N_DE_DEZENAS_NO_VOLANTE + 1)
    self.dezenas_with_histfreq = zip(all_dezenas, histfreq)
    self.dezenas_with_histfreq_sorted_by_freqs = self.dezenas_with_histfreq[:] 
    self.dezenas_with_histfreq_sorted_by_freqs.sort(key = lambda x : x[1])
    dezenas_to_slots = zip(*self.dezenas_with_histfreq_sorted_by_freqs)[0]
    self.tilrsets = []
    index_ini = 0; index_fim = self.n_elems_per_slot 
    while index_ini < self.concurso.N_DE_DEZENAS_NO_VOLANTE - self.n_elems_per_slot + 1:
      tilrset = dezenas_to_slots[index_ini : index_fim] 
      self.tilrsets.append(tilrset)
      index_ini = index_fim; index_fim += self.n_elems_per_slot 

  def get_tilrwpattern_of_game(self, dezenas):
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
    tilrwpattern = ''.join(map(str, tilrpattern))
    return tilrwpattern
  
  def get_wpattern(self, reprocess=False):
    if self.wpattern != None and not reprocess:
      return self.wpattern
    self.wpattern = self.get_tilrwpattern_of_game(self.concurso.get_dezenas())
    return self.wpattern
  
def run_history():
  concurso = ConcursoBase(); wpatterndict = Dict2()
  for nDoConc in xrange(101, concurso.get_total_concursos()+1):
    concurso = concurso.get_concurso_by_nDoConc(nDoConc)
    tilrobj = TilR(n_slots=5, concurso=concurso)
    wpatt6 = tilrobj.get_wpattern()
    print concurso, wpatt6
    wpatterndict.add1_or_set1_to_key(wpatt6)
    '''if wpatterndict.has_key(wpatt6):
      wpatterndict[wpatt6] += 1
    else:
      wpatterndict[wpatt6] = 1'''
  for wpatt6 in wpatterndict:
    print wpatt6, wpatterndict[wpatt6]
  print len(wpatterndict)
      
def get_tilrwpattern_of_game(dezenas, n_slots=5, up_to_concurso=None):
  if up_to_concurso == None:
    up_to_concurso = ConcursoHTML.get_last_concurso()
  tilr_obj = TilR(n_slots, up_to_concurso) #, inclusive=False, concurso_range = None)
  return tilr_obj.get_tilrwpattern_of_game(dezenas)
      
def adhoc_test():
  '''
  tilrobj = TilR()
  print 'tilrsets', tilrobj.tilrsets
  print 'tilrpattern', tilrobj.get_wpattern()'''
  run_history()

def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
