#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import datetime,
import copy, sys

#from Jogo import Jogo
from JogoSlider import JogoSlider
from TilPattern import JogoTilPattern 

import maths.frequencies.HistoryFrequency as hf
import maths.frequencies.TilSets as ts 

class JogoTil(object): #(Jogo):
  
  def __init__(self, jogo):
    #super(JogoTil, self).__init__()
    self.jogo = jogo
    self.jogotilpattern = None
    
  def find_jogotilpattern_like(self, jtilpattern):
    histfreq = hf.get_histfreq(jtilpattern.bottomconc, jtilpattern.topconc)
    print 'histfreq', histfreq 
    tilsets = ts.TilSets(histfreq, jtilpattern.slots)
    print 'histfreq', tilsets, tilsets.tilSets 
    dezenas = self.jogo.get_dezenas()
    tilPatternList = [0] * tilsets.tilN
    for dezena in dezenas:
      for i in range(len(tilsets.tilSets)):
        if dezena in tilsets.tilSets[i]:
          # print 'found', dezena, 'inside i=',i, tilSets[i]   
          tilPatternList[i] += 1
          break
    wpattern = ''.join(map(str, tilPatternList))
    print 'wpattern', wpattern 
    self.jogotilpattern = copy.copy(jtilpattern)
    self.jogotilpattern.set_wpattern(wpattern) 
    return self.jogotilpattern
  
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

def adhoc_test():
  jogo = JogoSlider().get_jogo_by_nDoConc(300)
  jogotil = JogoTil(jogo)
  jtilpattern = JogoTilPattern(5, 6, (100, 299))  
  print 'jtilpattern', jtilpattern
  print 'jogotil.find_jogotilpattern_like()', jogotil.find_jogotilpattern_like(jtilpattern), 'for', jogo
  jtilpattern = JogoTilPattern(5, 6, (71, 210))  
  print 'jtilpattern', jtilpattern
  print 'jogotil.find_jogotilpattern_like()', jogotil.find_jogotilpattern_like(jtilpattern), 'for', jogo
  # changing jogo
  jogo = JogoSlider().get_jogo_by_nDoConc(1200)
  print 'jogo 1200', jogo
  jogotil = JogoTil(jogo)
  # DEU ERRO COM # jtilpattern = JogoTilPattern(5, 6, (71, 210))  
  jtilpattern = JogoTilPattern(5, 6, (500, 600))  
  print 'jtilpattern', jtilpattern
  print 'jogotil.find_jogotilpattern_like()', jogotil.find_jogotilpattern_like(jtilpattern), 'for', jogo


def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
