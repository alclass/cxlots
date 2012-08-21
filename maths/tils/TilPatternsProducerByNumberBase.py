#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
TilPatternsProducerByNumberBase.py
'''
import sys

import localpythonpath
localpythonpath.setlocalpythonpath()
#import funcsForTil as ffTil
from TilPattern import TilDefiner
# from TilPattern import TilPattern
import maths.NumberSystem as NS
import maths.combinatorics.algorithmsForCombinatorics as afc

class TilProducerByNumberBase(NS.NumberSystem):
  '''
  This class inherits from NumberSystem (in package maths, homonime module NumberSystem.py)
  
  The parent class is capable of adding one.  Here, the polymorphic intent is to adding one continuously until sum(digits) is equal to "soma".
  
  The functionality in this class also exists in class TilProducer. The two do the same thing, but via different ways.
  
  TilProducer follows a 3-step algorithm, starting by find the Integer Partitions of "soma".
  There, these (integer) partitions are zero-stuffed and mirrored.
  Because of that, the number ascending ordering is not clear and this motivated the creation of this class.
  
  So this class generates the valid "wpatterns", having a sequence that has number ascending ordering.
  
  Eg.  

  tildefiner = TilDefiner(n_slots=5, soma=6)
  tpbns = TilProducerByNumberBase(tildefiner)
  wpattern = tpbns.next_partition(); c=0
  while wpattern:
    c+=1
    print '%d:%s ' %(c, wpattern) , 
    wpattern = tpbns.next_partition()

  Results in:
    
    1:00006  2:00015  3:00024  4:00033  5:00042  6:00051  7:00060  8:00105 (...) 
    (...) 
    (...) 207:50010  208:50100  209:51000  210:60000 
    
  
  '''

  def __init__(self, tildefiner):
    '''
    The former implementation of this class did not store patterns array,
      because of that, it was a lot slower and had a few bugs;
      storing patterns array, on another had, speeded up the whole process and eliminated mentioned bugs
      However, it takes a bit more memory depending on tildefiner "size"
    '''
    arraySize = tildefiner.n_slots
    base = tildefiner.soma + 1
    super(self.__class__, self).__init__(arraySize, base)
    self.tildefiner = tildefiner
    self.wpatterns_array = []
    self.store_wpatterns_array()
    self.restart_parcours() # same as ==>> self.parcours_index = 0

  def store_wpatterns_array(self):
    '''
    Programmers' notice: If constructor parameters changes (ie, tildefiner), this method should rerun
      In fact, tildefiner has no corresponding set method, so, the better approach,
        in case tildefiner needs to change, is to instantiate another object
    '''
    # save current state (to restore after totaling)
    self.total = 0; self.values = self.digits_zeroed()
    while self.next_partition():
      digits = self.values[:]
      wpattern = ''.join(map(str, digits))
      self.wpatterns_array.append(wpattern)

  def get_n_combinations(self, concursoBase):
    '''
    This method is applied to "wpattern" (in fact, array, its list transform) that is pointer to by the parcours_index, ie, the current wpattern
    
    Eg.
      Suppose current wpattern is '02211' (notice tildefiner is 5,6 in the example)
      Because TilR equally occupies the slots, there are, in the example of Megasena, 12 dozens per slot (5 slots total, 60 dozens altogether)
      So the n. of combinations will be:
      
      afc.combineNbyC(12,0) * afc.combineNbyC(12,2) * afc.combineNbyC(12,2) * afc.combineNbyC(12,1) * afc.combineNbyC(12,1) =
      = 1 * 66 * 66 * 12 * 12 = 
      = 627264 combinations
    '''
    remainder = concursoBase.N_DE_DEZENAS_NO_VOLANTE % self.tildefiner.n_slots
    if remainder != 0:
      # not yet implemented
      return None
    total_elems_per_slot = concursoBase.N_DE_DEZENAS_NO_VOLANTE / self.tildefiner.n_slots
    array = self.get_pattern()
    total_combinations = 1
    for n_elems_happening_in_slot in array:
      total_combinations *= afc.combineNbyC(total_elems_per_slot, n_elems_happening_in_slot)
    return total_combinations
    
    return len(self.wpatterns_array)
  
  def get_total(self):
    return len(self.wpatterns_array)

  def who_is_wfirst(self):
    return self.wpatterns_array[0]

  def who_is_first(self):
    '''
    Reimplemented from parent
    
    No need to reimplement:
      move_to_first() 
      get_first() 
    '''
    wpattern = self.who_is_wfirst()
    array = [int(c) for c in wpattern]
    return array 

  def who_is_wlast(self):
    return self.wpatterns_array[-1]

  def who_is_last(self):
    '''
    Reimplemented from parent
    
    No need to reimplement:
      move_to_last() 
      get_last() 
    '''
    wpattern = self.who_is_wlast()
    array = [int(c) for c in wpattern]
    return array 

  def index(self, p_wpattern):
    if type(p_wpattern) == str:
      wpattern = p_wpattern
    elif type(p_wpattern) in [list, tuple]:
      wpattern = ''.join(map(str, p_wpattern))
    try:
      i = self.wpatterns_array.index(wpattern)
      return i
    except ValueError:
      return None 

  def at(self, p_index):
    if 0 > p_index > len(self.patterns_array) - 1:
      return None
    return self.wpatterns_array[p_index]

  def move_to_wpattern(self, p_wpattern):
    i = self.index(p_wpattern)
    if i != None:
      self.parcours_index = i
      return
    error_msg = 'wpattern (=%s) does not exist to return its index in move_to_wpattern()' %p_wpattern
    raise IndexError, error_msg  

  def get_wpattern(self):
    '''
    get_wpattern = form_strdigits (implemented in parent class)
    It's the same with a more contextual name
    '''
    #return self.form_strdigits()
    return self.wpatterns_array[self.parcours_index]

  def get_pattern(self):
    wpattern = self.get_wpattern()
    array = [int(c) for c in wpattern]
    return array 

  def restart_parcours(self):
    self.parcours_index = -1

  def parcours_wnext(self):
    self.parcours_index += 1
    if self.parcours_index > len(self.wpatterns_array) - 1:
      return None
    return self.wpatterns_array[self.parcours_index]

  def parcours_next(self):
    wpattern = self.parcours_wnext()
    array = [int(c) for c in wpattern]
    return array 

  def parcours_wprevious(self):
    self.parcours_index -= 1
    if self.parcours_index in [-2, -1]:
      self.parcours_index = len(self.patterns_array) - 1
    if self.parcours_index > len(self.patterns_array) - 1:
      return None
    return self.wpatterns_array[self.parcours_index]

  def parcours_previous(self):
    wpattern = self.parcours_wprevious()
    array = [int(c) for c in wpattern]
    return array 

  def do_next_partition(self):
    '''
    This method does not return wpattern is just "position" self.values
    
    Notice also that do_next() is used originally (and in a "private" way) from the parent class
    ie, do_next() jump one at a time, where as do_next_partition() jumps to the next valid "partition" (eg. from '00006' to '00015')
    '''
    self.do_next()
    if self.values == None:
      return
    if sum(self.values) == self.tildefiner.soma:
      return
    # the while below was introduced to avoid recursive call here (it was raising RunTimeException - recursion too long 
    while sum(self.values) != self.tildefiner.soma:
      self.do_next()
      if self.values == None:
        return
    return

  def next_partition(self):
    self.do_next_partition()
    if self.values == None:
      return None
    return self.values
  
  def __str__(self):
    return '<TilByNBase(%d,%d) last=%s>' %(self.tildefiner.n_slots, self.tildefiner.soma, str(self.lastElem))
    

def adhoc_test():
  tildefiner = TilDefiner(5,6)
  tpbns = TilProducerByNumberBase(tildefiner)
  exec('from models.Concurso import ConcursoBase')
  concursoBase = eval('ConcursoBase()')
  print 'first / last', tpbns.get_first(), tpbns.get_last()
  total_combinations = 0; tpbns.restart_parcours()
  while tpbns.parcours_wnext():
    n_combinations = tpbns.get_n_combinations(concursoBase)
    print '>>>', tpbns.parcours_index, tpbns.get_wpattern(), n_combinations 
    total_combinations += n_combinations
  print 'total_combinations', total_combinations

def adhoc_test2():
  tildefiner = TilDefiner(6,6)
  tpbns = TilProducerByNumberBase(tildefiner)
  wpattern = tpbns.next_wpattern(); c=0
  print 'first / last', tpbns.get_first(), tpbns.get_last()
  print 'before while-loop', tpbns.get_wpattern()
  while wpattern != None:
    c+=1
    print '%d:%s ' %(c, wpattern) , 
    wpattern = tpbns.next_wpattern()
  print 'after while-loop', tpbns.get_wpattern()
  print 'total', tpbns.get_total() 
  tildefiner = TilDefiner(6,6)
  tpbns = TilProducerByNumberBase(tildefiner)
  print tpbns.get_total()
  print 'first / last', tpbns.at(0), tpbns.at(tpbns.get_total() - 1)
  print 'index of "000005"', tpbns.index('000005')
  print 'index of "000006"', tpbns.index('000006')
  print 'index of "000024"', tpbns.index('000024')
  print 'index of "600000"', tpbns.index('600000')
  print 'index of "650000"', tpbns.index('650000')
  

def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
