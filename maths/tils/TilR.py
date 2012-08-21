#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
TilR.py
'''
# import numpy, time, sys
import sys

import localpythonpath
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
  
  def __init__(self, n_slots = 5, concurso = None, concurso_range = None):
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

  def get_wpattern(self, reprocess=False):
    if self.wpattern != None and not reprocess:
      return self.wpattern
    tilrpattern = [0]*len(self.tilrsets)
    for dezena in self.concurso.get_dezenas():
      for i, tilr in enumerate(self.tilrsets):
        if dezena in tilr:
          tilrpattern[i]+=1
          break
    self.wpattern = ''.join(map(str, tilrpattern))
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
