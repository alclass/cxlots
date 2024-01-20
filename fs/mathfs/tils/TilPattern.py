#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
TilPattern.py
'''
import sys

import __init__
__init__.setlocalpythonpath()

import fs.jogosfs.til_functions as ffTil

class TilDefiner(object):
  '''
  This class only defines two attributes:
  + slots
  + soma
  
  Usage example:
    A Til5 (or a statistics quintil) for a 6-number set has 5 slots and "soma" 6
    
  TilDefiner is a base (or parent) class for TilPattern and TilPattern is parent for JogoTilPattern
  '''

  def __init__(self, n_slots=None, soma=None):
    if n_slots==None:
      n_slots = 5 # default
    if soma==None:
      soma = 6 # default
    self.n_slots = int(n_slots)
    self.soma  = int(soma)

  def __str__(self):
    return '<Til(%d,%d)>' %(self.n_slots, self.soma)


class TilProducer(TilDefiner):
  '''
  This class buffers all tilpatterns that its tildefiner object produces. This buffer is kept in the variable self.alltilpatterns
  
  Eg. Suppose tildefiner is TilDefiner(n_slots=4, soma=6), thus, all wpatterns (word-patterns) will be:
      '0006', '0015', '0024', ... , '6000'  :: altogether, there will be x patterns
    
    Notice that the order of these patterns differ depending on the originating algorithm.
      The one indicated above comes from the "Number Base"-like algorithm, which increases patterns as if they were numbers of base 7 (soma[=6] + 1)
      
  '''
  def __init__(self, n_slots=None, soma=None):
    super(TilProducer, self).__init__(n_slots, soma)
    self.partition_index = None
    self.alltilpatterns = get_tilallpatterns(self)

    self.set_total_combinations()
  def set_total_combinations(self):
    self.total_combinations = len(self.alltilpatterns)
    # calc_n_integer_partitions(self.n_slots, self.soma) 

  def fetch_integer_partition(self):
    if self.partition_index < 0 or self.partition_index > self.total_combinations - 1:
      return None
    return self.alltilpatterns[self.partition_index]
    #fetch_integer_partition(self.n_slots, self.soma, self.partition_index)
  
  def park_partition_index_at_start(self):
    self.partition_index = 0
    
  def park_partition_index_at_end(self):
    self.partition_index = self.total_combinations - 1 

  def next(self):
    if self.partition_index == None:
      self.park_partition_index_at_start()
    else:
      self.partition_index += 1
    return self.fetch_integer_partition()

  def previous(self):
    if self.partition_index == None:
      self.park_partition_index_at_end()
    else:
      self.partition_index -= 1
    return self.fetch_integer_partition()

  def first(self):
    self.park_partition_index_at_start()
    return self.fetch_integer_partition()
    
  def last(self):
    self.park_partition_index_at_end()
    return self.fetch_integer_partition()

  def __str__(self):
    return '<Til(%d,%d) %d tils>' %(self.n_slots, self.soma, self.total_combinations)
    
def fetch_integer_partition():
  pass    
      
def calc_n_integer_partitions():
  pass


  

class TilPattern(TilDefiner):
  '''

  This class inherits from TilDefiner adding the wpattern (standing for word-pattern) attribute

  This class also adds the following methods:
  1) a consistency check to be trigged when wpattern is set to the object
  2) __eq__() defining equality as the 3 attributes are equal,
    ie, self.slots, self.soma and self.wpattern should be equal to their counterparts in the second object,
    for the two to be equal
  3) the __str__() method
  
  Usage Examples: 

    Eg.  1
    
    Til(5, 6) means quintil where frequencies sum to 6
    
    Valid TilPattern objects for Til(5, 6)
    02220 01221 32010 60000 06000 05100 etc
    (ie, it must be have 5 digits and individually these digits sum to 6

    Eg.  2  (Not yet implemented, but it will be implemented as soon as possible)
    
    Til(12, 50)
    This TilPattern object uses more than the 10 numeric digits to represent a character place in the pattern
    It must be have 12 digits and individually these digits sum to 50
    However, it's possible that more than 9 elements may occupy one frequency place, so letters from A to Z,
      then lowercase a to z are used.
  '''

  def __init__(self, n_slots=None, soma=None):
    super(TilPattern, self).__init__(n_slots, soma)
    self.wpattern = None
    #self.tilnumber = int(tilnumber)
    #self.freqsoma  = int(freqsoma)

  def set_wpattern(self, wpattern):
    self.wpattern = wpattern
    self.is_self_consistent()

  def is_self_consistent(self):
    if len(self.wpattern) != self.n_slots:
      error_msg = 'len(self.wpattern)=%d != self.tilnumber=%d' %(len(self.wpattern), self.n_slots)
      raise TypeError, error_msg 
    freqsoma_to_compare = 0
    for char in self.wpattern:
      freqsoma_to_compare += int(char)
    if self.soma != freqsoma_to_compare:
      error_msg = 'self.freqsoma=%d != freqsoma_to_compare=%d' %(self.soma, freqsoma_to_compare)
      raise TypeError, error_msg
    
  def __eq__(self, tilpattern):
    # DeMorgan to improve performance if case wpattern differs right away (believed to be most of the cases in filtering processing)
    if tilpattern == None:
      return False
    if (self.wpattern != tilpattern.wpattern or  
          self.n_slots != tilpattern.n_slots or 
           self.soma != tilpattern.soma):
      return False
    return True
  
  def __str__(self):
    return "'<TilPattern(%d,%d,'%s')>" %(self.n_slots, self.soma, self.wpattern)

class TilAllPatternsBuffer(object):
  
  def __init__(self):
    self.tilbuffer = {}
    
  def add_alltilpatterns_to_buffer(self, tildefiner, alltilpatterns):
    self.tilbuffer[(tildefiner.n_slots, tildefiner.soma)] = alltilpatterns
    
  def get_alltilpatterns_from_buffer(self, tildefiner):
    definertuple = (tildefiner.n_slots, tildefiner.soma)
    if self.tilbuffer.has_key(definertuple):
      return self.tilbuffer[definertuple]
    alltilpatterns = ffTil.getTilPatternsFor(tildefiner.n_slots, tildefiner.soma)
    self.add_alltilpatterns_to_buffer(tildefiner, alltilpatterns)
    return alltilpatterns

tilallpatterns = None
def get_tilallpatterns(tildefiner):
  if tilallpatterns == None:
    tilallpatterns = TilAllPatternsBuffer()
  return tilallpatterns(tildefiner) 


def adhoc_test():
  print 'list_dist_xysum_metric_thry_ms_history()'
  tilpattern = TilPattern(5, 6)
  tilpattern.set_wpattern('02220')
  print 'tilpattern', tilpattern
  
def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
