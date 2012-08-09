#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import datetime,
import sys

import localpythonpath
localpythonpath.setlocalpythonpath()

from models.JogoSlider import JogoSlider
from TilPattern import TilPattern

import maths.frequencies.HistoryFrequency as hf
import TilSets as ts 

class JogoTil(TilPattern): #(Jogo):
  '''
  This class inherits from TilPattern adding a tuple attribute, ie, concurso_range (composed of (bottomconc, topconc)) 
  '''

  def __init__(self, jogo, slots=None, soma=None, concurso_range=None):
    super(JogoTil, self).__init__(slots, soma)
    self.jogo = jogo
    self.histfreq = None
    self.set_concurso_range(concurso_range)
    
  def set_slots_soma_and_concurso_range(self, slots, soma, concurso_range):
    self.slots = int(slots)
    self.soma  = int(soma)
    self.set_concurso_range(concurso_range)

  def set_concurso_range(self, concurso_range = None):
    '''
    The default is assumed as (bottomconc = 1, topconc = LAST)
    '''
    if concurso_range == None:
      bottomconc = 1
      topconc = JogoSlider().get_total_jogos()
      self.concurso_range = (bottomconc, topconc)
    elif type(concurso_range) == type((1,2)):
      self.concurso_range = concurso_range
    else:
      error_msg = 'concurso_range != None and type(concurso_range) == type((1,2)) :: False; str concurso_range = %s' %str(concurso_range)
      raise ValueError, error_msg
          
  def set_histfreq(self):
    if self.concurso_range != None and type(self.concurso_range) == type((1,2)):
      self.histfreq = hf.get_histfreq(self.concurso_range)
    else:
      error_msg = 'cannot set histfreq for not having concurso_range; str concurso_range = %s' %str(self.concurso_range)
      raise ValueError, error_msg

  def set_jogotil_wpattern(self):
    if self.histfreq == None:
      self.set_histfreq()
    tilsetobj = ts.TilSets(self.histfreq, self.slots)
    dezenas = self.jogo.get_dezenas()
    tilpatternlist = [0] * tilsetobj.tilN # tilN is the same as slots
    for dezena in dezenas:
      for i in range(len(tilsetobj.tilSets)):
        if dezena in tilsetobj.tilSets[i]:
          # print 'found', dezena, 'inside i=',i, tilSets[i]   
          tilpatternlist[i] += 1
          break
    wpattern = ''.join(map(str, tilpatternlist))
    self.set_wpattern(wpattern)
    # self.tilpatternlist = tilpatternlist 
  
  def is_same_tilpattern(self, tilpattern):
    if self.jogotilpattern == tilpattern:
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
    output_text = str(self.jogo)
    output_text += ' range' + str(self.concurso_range)
    return output_text

'''
def freqs_per_tilslot(tilpatterndict, n_slots):
  freqs_per_slot = [] * n_slots
  slotdict = {}
  for wpattern in tilpatterndict.keys():
    for digit, position in wpattern.enumerate:
      digitsdict[]
      if digitsdict.has_key(digit):
        tilpatterndict[jogotil.wpattern] += 1
      else:
        tilpatterndict[jogotil.wpattern] = 1
      print wpattern, tilpatterndict[wpattern]
'''  

def adhoc_test():
  tilpatterndict = {}
  n_lastjogo = JogoSlider().get_total_jogos()
  for nDoConc in range(201, n_lastjogo + 1):
    jogo = JogoSlider().get_jogo_by_nDoConc(nDoConc)
    jogotil = JogoTil(jogo, 5, 6, (nDoConc-200, nDoConc-1))
    jogotil.set_jogotil_wpattern()
    if tilpatterndict.has_key(jogotil.wpattern):
      tilpatterndict[jogotil.wpattern] += 1
    else:
      tilpatterndict[jogotil.wpattern] = 1
    print nDoConc, jogotil.wpattern
  for wpattern in tilpatterndict.keys():
    print wpattern, tilpatterndict[wpattern]

  '''
  jogo = JogoSlider().get_jogo_by_nDoConc(1200)
  jogotil = JogoTil(jogo, 6, 6, (800, 1199))
  jogotil.set_jogotil_wpattern()
  print 'jogotil.wpattern', jogotil.wpattern, 'for', jogotil
  '''
  
def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
