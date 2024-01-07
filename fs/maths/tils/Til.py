#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Til.py
This module implements TWO public classes (in general, we have one class per module)
These 2 classes are:

+ TilF
+ TilR

Most of the explanation for TilF and TilR are found in TilBase class's documentation.
TilBase implements equal parts for the two.
'''
# import numpy, time, sys
import copy, sys

import __init__
__init__.setlocalpythonpath()

from fs.jogos import volante_functions
from fs.strfs.str_patterns import trans_intlist_to_descendant_stair_strlist
from models.Concursos.concurso_extended import ConcursoExt
from models.Concursos.VolanteCharacteristics import VolanteCharacteristics
import maths.statistics.HistoryFrequency as hf
from TilStats import TilStats
from TilFSets import TilFSets

class TilInterface(object):
  '''
  This class "simulates" an Interface in the "Object-Oriented" sense
  It more or less is a sketch of methods to be implemented in the class TilBase
  See TilBase for more info. 
  '''
  
  def set_volante_caract(self):
    pass

  def set_n_slots(self):
    pass
  
  def place_dozens_in_the_slots(self):
    pass


class TilBase(TilInterface):
  '''
  This class shapes a protocol-like method definition
    to be used for the TWO classes:
    + TilF  
     and
    + TilR
  
  TilBase contains functionality for the extending classes: TilF and TilR.  
  TilF and TilR are classes that are capable of calculating a "til element".
  
  A Til Element is a pattern, generally expressed as a string or a list, 
    that indicates where the components of an array or set position themselves in frequency slots.
    
  An example of a Til Element pattern (to be further explained below) is '03210'.
    
  The difference between a TilF object and a TilR object is << semantic >> in their frequency information.
  
  For example:
  
  1) A TilF(n_slot=5, n_items=6) = '03210' means:

  + 3 items occurred in the second frequency range, 
  + 2 items occurred in the third frequency range,
  + 1 item  occurred in the fourth frequency range
  
  The first and last frequency ranges had no occurrence of items.
  
  2) A TilR(n_slot=5, n_items=6) = '03210' means the same as above, 
     the difference is how the frequency slots are constructed.
     
  How frequency slots are constructed in each of the two Tils (TilF and TilR)
  
  1) In TilF:
     Each slot is defined by the frequency amounts themselves. So from the least frequency to the highest, 
       the slots are divided taking into account so that the frequencies themselves
       are equally distanced among the slots.
     
     Example:
       If MinFreq is 11 and MaxFreq is 50 and there are 4 frequency slots: slot ranges will be:
        [11,20],[21,30],[31,40],[41,50]
  
  2) In TilR:
     Items enter the slots equally, independently on its frequencies.

     Example:
       If number of items is 60 and there are 5 frequency slots:
        each slot will contain 12 items (notice: 12*5=60),
        items entering the slots in the order of least occurring to the most occurring
     
  A comparing example with TilF and TilR:
    If a game has, against a certain games background, the following tils:

  +  TilF(n_slot=5, n_items=6)(game x1) = '03210'
  +  TilR(n_slot=5, n_items=6)(game x1) = '21111'
  
  Each til will be interpreted according to the explanation given above.  In a nut shell:

  1) the TilF distribution takes into account ranges based on frequency
  2) the TilR distribution takes into account the fact that each slot
     has equal (or almost equal if division has remainder) amount of items
      

  In other words, the difference between TilR and Til is following:
  
  Til cuts set limits by equal distance frequencies, so that frequency is the determing factor
    in slicing dozens into slots
  TilR cuts set limits by equal (or so, depending on division remainders) number of dozens
  
  Eg. outlining this difference:
   1) in TilF(n_slots=5) each slots (metric set) has a variable number of dozens,
      and it's not surprising to observe an empty set (or a set with very few dozens)
      and another one with much more than 12 in it
   2) in TilR(n_slots=5) each slots (metric set) has exactly 12 dozens
      (if total is 60 elements, of course)
  '''
 
  DEFAULT_N_SLOTS = 5
  
  def __init__(self, n_slots = None, history_ini_fin_range = None, volante_caract=None):
    '''
    Constructor of class TilBase()

    Parameter "inclusive" (attribute self.CONCURSO_PROPER_INCLUDED_IN_RANGE)
      does one important differentiation in the process
    
    This differentiation is the following
    1) when one wants to observe/analyze a drawn sorteio, the sorteio itself should not be not counted,
       ie, should not contribute to the frequencies
    2) when one wants to "bet" a coming (not happened) sorteio, 
       the last concurso should contribute to the frequencies
    
    In other words, when analyzing, inclusive is False; when deriving for bets, inclusive is True 
    
    '''
    self.set_volante_caract(volante_caract)
    self.set_n_slots(n_slots)
    self.set_history_ini_fin_range(history_ini_fin_range)

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
    self.redo_place_items_in_the_slots()

  def verify_n_slots_is_good(self):
    remainder = self.volante_caract.n_dezenas_no_volante % self.n_slots
    if remainder != 0:
      error_msg = 'Not yet implemented to inexact division quantiles. Example: a 60-number game can have 5, 6, 10 as n_slots, but cannot have 7 or 8 for instance.'
      raise ValueError, error_msg
    self.n_elems_per_slot = self.volante_caract.n_dezenas_no_volante / self.n_slots

  def set_history_ini_fin_range(self, history_ini_fin_range=None):
    '''
    This method is private!!!  From the "outside", use set_concurso_and_range() 
    '''
    slider = ConcursoExt()
    HIST_RANGE_DEFAULT = (1, slider.get_n_last_concurso()) 
    self.history_ini_fin_range = volante_functions.return_int_range_or_default_or_raise_ValueError(history_ini_fin_range, HIST_RANGE_DEFAULT)
    self.redo_place_items_in_the_slots()

  def get_items_in_slot_n(self, n):
    if self.tilsets == None or len(self.tilsets) == 0:
      return []
    try:
      int(n)
    except ValueError:
      return []
    last_index = len(self.tilsets) - 1
    if n < 0 or n > last_index:
      return []
    return copy.copy(self.tilsets[n])

  def redo_place_items_in_the_slots(self):
    try:
      self.history_ini_fin_range
    except AttributeError:
      # not yet time to recompute, due to construction-time order of attribute setting
      return
    self.place_items_in_the_slots()

  def get_items_tilpattern_as_list(self, items):
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
    tilpattern = [0]*len(self.tilsets)
    for item in items:
      for i, tilset in enumerate(self.tilsets):
        if item in tilset:
          tilpattern[i]+=1
          break
    return tilpattern
  
  def get_items_tilpattern_as_list_and_str(self, items):
    tilpattern_as_list = self.get_items_tilpattern_as_list(items)
    tilpattern_as_str = ''.join(map(str, tilpattern_as_list))
    return tilpattern_as_list, tilpattern_as_str 

  def get_items_tilpattern_as_str(self, items):
    return self.get_items_tilpattern_as_list_and_str(items)[1]
   
  def get_items_tilpattern_as_desc_stair(self, items):
    '''
    Examples:
      1) suppose wpattern is '01212'
      Its descendent stair is '2211' (information is lost here)
      2) suppose wpattern is '01302'
      Its descendent stair is '321' (information is lost here)
    '''
    tilpattern_as_list = self.get_game_tilrpattern_as_list(items)
    return trans_intlist_to_descendant_stair_strlist(tilpattern_as_list)

class TilF(TilBase):
  '''
  This class (TilF) slots 1/nth, where n is the number of slots, of dozens
    in an equal-frequency distribution,
    ie, items fall into slots according to their frequencies
  
  As an illustration, suppose total elements is 60. Then, quintils (TilR n_slots=5)
    will order all items (dozens) in their frequency orders into 5 sets (slots).
    
  Suppose item is (1,2,3,4,5,6) and their frequencies are (f1,f2,f3,f4,f5,f6)
  Suppose universe set is range(1, 61) (or set {1, 60} Naturals) and
  Suppose that occurrences minimum is 10 and maximum is 100
  Suppose that the slots (let's say we have 5 slots) are ranged with the following min-max tuples:
  slot0 = (10,25)
  slot1 = (26,47)
  slot2 = (48,67)
  slot3 = (68,96)
  slot4 = (97,100)
  Suppose lastly that:
  (f1=100, f2=11, f3=55, f4=34, f5=71, f6=71)
  Now we can "place" items into their slots:
    1 with f1=100 goes to slot4 = (97,100), because 100 belongs to (97,100) 
    2 with f2=11  goes to slot0 = (10,25),  because  11 belongs to (10,25) 
      And so on up to 6
  The tilset indices in order are 402133 and the til pattern is 11121
    ie 1 of 0, 1 of 1, 1 of 2, 2 of 3 and 1 of 4
  '''
  def place_items_in_the_slots(self):
    # in the future, whether jogo is Megasena or other, info-argument will have to be passed on to histfreqobj
    histfreq     = hf.histfreqobj.get_histfreq_within_range(self.history_ini_fin_range)
    # all_dezenas  = range(1, self.volante_caract.n_dezenas_no_volante + 1)
    tilSetsObj   = TilFSets(histfreq, self.n_slots)
    # though the name is tilrset, here, in fact, it's tilset with the "r"
    self.tilsets = tilSetsObj.getTilSets()


class TilR(TilBase):
  '''
  This class (TilR) slots 1/nth, where n is the number of slots, of dozens in
    their frequency ascending order.
  
  As an illustration, suppose total elements is 60. Then, quintils (TilR n_slots=5)
    will order all dozens in their frequency order into 5 sets (slots).
  '''
  def place_items_in_the_slots(self):
    '''
    This method is polymorphic (ie, it's different in between TilF and (this) TilR
    '''
    histfreq = hf.histfreqobj.get_histfreq_within_range(self.history_ini_fin_range)
    all_dezenas = range(1, self.volante_caract.n_dezenas_no_volante + 1)
    dezenas_with_histfreq_sorted_by_freqs = zip(all_dezenas, histfreq)
    dezenas_with_histfreq_sorted_by_freqs.sort(key = lambda x : x[1])
    dezenas_to_slots = zip(*dezenas_with_histfreq_sorted_by_freqs)[0]
    self.tilsets = []

    # self.n_elems_per_slot is calculated previously in the process chain
    index_ini = 0; index_fim = self.n_elems_per_slot 
    while index_ini < self.volante_caract.n_dezenas_no_volante - self.n_elems_per_slot + 1:
      tilset = dezenas_to_slots[index_ini : index_fim] 
      self.tilsets.append(tilset)
      index_ini = index_fim; index_fim += self.n_elems_per_slot 

  def getBorderTupleOfTilSets(self, retry=False):
    if self.tilsetobj == None:
      if retry:
        error_msg = 'Error in getBorderTupleOfTilSets() :: self.tilsetobj continued to be None after a retry. It is either a program error or database is empty.'
        raise ValueError, error_msg
      else:
        self.flow_concurso_concursorange_histfreq_wpattern()
        return self.getBorderTupleOfTilSets(self, retry=True)
    return self.tilsetobj.getBorderTupleOfTilSets()

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
  while len(tilr_pool_keys_queue) > TILR_POOL_SIZE or len(tilr_pool) > TILR_POOL_SIZE:
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
  tilfstats = TilStats(n_slots=5, soma=volante_caract.n_dezenas_no_sorteio)
  tilrstats = TilStats(n_slots=5, soma=volante_caract.n_dezenas_no_sorteio)
  tilfobj   = TilF(n_slots=5, history_ini_fin_range = None, volante_caract=volante_caract)
  tilrobj   = TilR(n_slots=5, history_ini_fin_range = None, volante_caract=volante_caract)
  for nDoConc in xrange(101, slider.get_n_last_concurso()+1):
    concurso = slider.get_concurso_by_nDoConc(nDoConc)
    # reuse tilrobj!
    tilfobj.set_history_ini_fin_range(history_ini_fin_range = (1, nDoConc-1))
    tilrobj.set_history_ini_fin_range(history_ini_fin_range = (1, nDoConc-1))
    f_pattern_as_list, f_wpattern = tilfobj.get_items_tilpattern_as_list_and_str(concurso.get_dezenas())
    r_pattern_as_list, r_wpattern = tilrobj.get_items_tilpattern_as_list_and_str(concurso.get_dezenas())
    tilfstats.add_pattern_as_list(f_pattern_as_list)
    tilrstats.add_pattern_as_list(r_pattern_as_list)
    print 'f', f_wpattern, 'r', r_wpattern, concurso.get_dezenas_str(), nDoConc 
  tilfstats.print_summary()
  print 'len(tilfstats)', len(tilfstats) 
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
