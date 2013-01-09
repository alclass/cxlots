#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
TilPattern.py
'''
import sys
from decimal import Decimal, getcontext

import __init__
__init__.setlocalpythonpath()

from models.Concursos.ConcursoExt import ConcursoExt
import maths.statistics.HistoryFrequency as hf
from TilSets import TilSets


class TilFreqSlotSeparator(object):

  def __init__(self, n_slots = 5, nDoConc=None):
    '''
    or tilNumber not in [5,6,10,12,15,20]:
    '''
    self.n_slots      = n_slots
    self.tilsetobj    = None
    self.tilhistogram = None
    self.set_nDoConc(nDoConc)
    self.fetch_histfreq()

  def set_nDoConc(self, nDoConc):
    slider = ConcursoExt()
    n_last_concurso = slider.get_n_last_concurso() # len(sl.getListAllConcursosObjs())      
    if nDoConc == None:
      nDoConc = n_last_concurso
    elif nDoConc < 1 or nDoConc > n_last_concurso:
      indexErrorMsg = 'passed in nDoConcurso=%d and range acceptable is 1 to %d' %(nDoConc, n_last_concurso)
      raise IndexError, indexErrorMsg 
    self.nDoConc = nDoConc

  def fetch_histfreq(self):
    '''
    histfreq is a numpy array that contains the frequencies of all dozens in concurso
    '''
    self.frequenciesAtConcursoN = hf.histfreqobj.get_histfreq_at(self.nDoConc)
    self.freqmin = min(self.frequenciesAtConcursoN)
    self.freqmax = max(self.frequenciesAtConcursoN)
  
  def setTilSets(self):
    self.tilsetobj = TilSets(self.frequenciesAtConcursoN, self.n_slots)
  
  def getTilSets(self):
    if self.tilsetobj == None:
      self.setTilSets()
    return self.tilsetobj.getTilSets()

  def get_quantities_of_dozens_per_tilslot(self):
    return [len(tilset) for tilset in self.getTilSets()]  
  
  def calc_tilhistogram(self):
    '''
    tilhistogram contains the percentual quantities of each slot in the til.
    Ex. 
    Suppose a jogotil(5,6) happens to be 02310.
    Suppose further that the 5 quintils are unbalanced, so that til 02211,
      focusing on the right-most one, does not make sense for there is no dozen at til 4 (the last one), 
      in other words, the last til-digit must always be 0 anyway.
      
    Thus the tilhistogram is a way to "sense" a bit this discrepancy in the frequencies. 
     
    '''
    self.tilhistogram = []
    n_elems = sum( self.get_quantities_of_dozens_per_tilslot() )  # this sum must equal N_DE_DEZENAS_NO_VOLANTE
    getcontext().prec = 5 # a percent like [1]nn.nn% 
    for tilset in self.getTilSets():
      fraction = Decimal( len(tilset) ) / Decimal(n_elems)
      percent = 100 * fraction 
      self.tilhistogram.append(percent)

  def show_tilhistogram_table(self):
    tilhistogram = self.get_tilhistogram()
    outline = 'Til \t Percent\n  Slot \t % \n '
    outline += '==================\n'
    for i, decobj in enumerate(tilhistogram):
      tilset = self.getTilSets()[i]
      outline += '%d \t %s \t %s size=%d\n' %(i, str(decobj), tilset, len(tilset))
    return outline

  def get_tilhistogram(self, reprocess=False):
    if self.tilhistogram != None and not reprocess:
      return self.tilhistogram
    self.calc_tilhistogram()
    return self.tilhistogram 

  def show_slot_elements(self):
    tilsets = self.getTilSets()
    for tilset in tilsets:
      print tilset

class TilSlotsMigration(object):

  def __init__(self):
    pass
    #array = []
    
  def sweep(self):
    for nDoConc in range(101, 1400):
      pass
      

def adhoc_test():
  tilfreqslotter = TilFreqSlotSeparator(5)
  tilfreqslotter.show_slot_elements()
  print tilfreqslotter.show_tilhistogram_table()      
  print '='*40
  tilfreqslotter = TilFreqSlotSeparator(6)
  tilfreqslotter.show_slot_elements()
  print tilfreqslotter.show_tilhistogram_table()      
  print '='*40
  tilfreqslotter = TilFreqSlotSeparator(10)
  tilfreqslotter.show_slot_elements()
  print tilfreqslotter.show_tilhistogram_table()      
  print '='*40
  tilfreqslotter = TilFreqSlotSeparator(12)
  tilfreqslotter.show_slot_elements()
  print tilfreqslotter.show_tilhistogram_table()      
  print '='*40
  tilfreqslotter = TilFreqSlotSeparator(32)
  tilfreqslotter.show_slot_elements()
  print tilfreqslotter.show_tilhistogram_table()      
  
def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
