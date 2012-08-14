#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import datetime,
import sys

import localpythonpath
localpythonpath.setlocalpythonpath()

from models.Concurso import ConcursoBase
from TilPattern import TilPattern

import maths.frequencies.HistoryFrequency as hf
import TilSets as ts 

class ConcursoTil(TilPattern): #(Jogo):
  '''
  This class inherits from TilPattern adding a tuple attribute, ie, concurso_range (composed of (bottomconc, topconc)) 
  '''

  def __init__(self, concurso=None, n_slots=None, soma=None, concurso_range=None):
    super(ConcursoTil, self).__init__(n_slots, soma)
    # wpattern is None as inherited from parent class TilPattern
    self.concurso = concurso
    self.concurso_range = None
    self.histfreq = None
    self.flow_concurso_concursorange_histfreq_wpattern()

  def reset_n_slots(self, n_slots):
    '''
    resetting n_slots only requires triggering calc_concursotil_wpattern(), does not require running flow_concurso_concursorange_histfreq_wpattern() 
    '''
    if self.n_slots == n_slots:
      return
    self.n_slots = n_slots
    self.calc_concursotil_wpattern()

  def reset_concurso(self, concurso):
    '''
    resetting concurso requires triggering flow_concurso_concursorange_histfreq_wpattern()
    '''
    self.concurso = concurso
    self.flow_concurso_concursorange_histfreq_wpattern()
    
  def reset_concurso_range(self, concurso_range):
    '''
    resetting concurso_range requires triggering flow_concurso_concursorange_histfreq_wpattern()
    '''
    self.concurso_range = concurso_range
    self.flow_concurso_concursorange_histfreq_wpattern()

  def flow_concurso_concursorange_histfreq_wpattern(self):
    '''
    This method is the one that should also be called if any state (ie, attribute) changes.
    The logic flow is the following:
    
    1) set concurso_range if available, if not, consider all history as range
    2) after setting concurso_range, set histfreq, which is based on concurso_range
    3) after setting histfreq, wpattern can be calculated
    '''
    self.process_concurso()
    self.process_concurso_range()
    self.fetch_histfreq()
    self.calc_concursotil_wpattern()
    
  def process_concurso(self):
    if self.concurso == None:
      self.concurso = ConcursoBase.get_last_concurso()

  # should be private to class, triggered by flow_concursorange_histfreq_wpattern()
  def process_concurso_range(self):
    '''
    The default is assumed as (bottomconc = 1, topconc = LAST)
    '''
    if self.concurso.get_total_concursos() == 0:
      error_msg = 'Database has no concursos yet. Processing must be halted.'
      raise IndexError, error_msg
    previous_concurso = self.concurso.get_previous()
    previous_topconc = previous_concurso.nDoConc 
    if self.concurso_range == None:
      bottomconc = 1
      self.concurso_range = (bottomconc, previous_topconc)
    elif type(self.concurso_range) == type((1,2)):
      # check that topconc must not be equal or greater than concurso.nDoConc, ie, it does not look to the future at this point!
      topconc_to_check = self.concurso_range[1]
      if topconc_to_check > previous_topconc:
        # replace the bogus one to the consistent "previous_topconc" 
        self.concurso_range = (self.concurso_range[0], previous_topconc)
    else:
      error_msg = 'Inconsistency in concurso_range, it is != None and type(concurso_range) != type((1,2)) :: str concurso_range = %s' %str(self.concurso_range)
      raise ValueError, error_msg
    if self.concurso_range[0] >= self.concurso_range[1]:
      # bottomconc must be corrected to consistency :: notice that range will be very small
      self.concurso_range = (self.concurso_range[1]-1, self.concurso_range[1])

  # should be private to class, triggered by flow_concursorange_histfreq_wpattern()
  def fetch_histfreq(self):
    self.histfreq = hf.get_histfreq(self.concurso_range)

  def get_histfreq_obj(self):
    return hf.histfreqobj

  def get_dezenas_and_their_frequencies_for_concurso(self):
    dezenas = self.concurso.get_dezenas()
    freqs = []
    for dezena in dezenas:
      index = dezena - 1
      freq = self.histfreq[index]
      freqs.append(freq)
    return zip(dezenas, freqs)

  def get_dezenas_their_frequencies_and_til_for_concurso(self):
    tilsetobj = ts.TilSets(self.histfreq, self.n_slots)
    zipped = self.get_dezenas_and_their_frequencies_for_concurso()
    dezenas, freqs = zip(*zipped)
    tils = []
    for dezena in dezenas:
      for i in range(len(tilsetobj.tilSets)):
        if dezena in tilsetobj.tilSets[i]:
          tils.append(i)
          break
    return zip(dezenas, freqs, tils)

  # should be private to class, triggered by flow_concursorange_histfreq_wpattern()
  def calc_concursotil_wpattern(self):
    tilsetobj = ts.TilSets(self.histfreq, self.n_slots)
    dezenas = self.concurso.get_dezenas()
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

from TilPatternsProducer import TilProducer
def adhoc_test():
  tilpatterndict = {}
  concurso = ConcursoBase() 
  n_lastjogo = concurso.get_n_last_concurso()
  for nDoConc in range(101, n_lastjogo + 1):
    concurso = concurso.get_concurso_by_nDoConc(nDoConc)
    concursotil = ConcursoTil(concurso, 5, 6) #, (nDoConc-200, nDoConc-1))
    concursotil.set_concursotil_wpattern()
    if tilpatterndict.has_key(concursotil.wpattern):
      tilpatterndict[concursotil.wpattern] += 1
    else:
      tilpatterndict[concursotil.wpattern] = 1
    #print nDoConc, concursotil.wpattern
  for wpattern in tilpatterndict.keys():
    print wpattern, tilpatterndict[wpattern]
  tilproducer = TilProducer(concursotil.n_slots, concursotil.soma)
  print 'tilproducer.alltilwpatterns', tilproducer.alltilwpatterns
  print 'tilpatterndict.keys()', tilpatterndict.keys()
  total_not_happen = 0
  for wpattern in tilproducer.alltilwpatterns:
    if wpattern not in tilpatterndict.keys():
      total_not_happen += 1
      print total_not_happen, wpattern, 'did not happen.'
  
def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
