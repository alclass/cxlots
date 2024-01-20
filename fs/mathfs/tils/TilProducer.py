#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
TilPattern.py
'''
import sys

import __init__
__init__.setlocalpythonpath()

import fs.jogosfs.til_functions as ffTil
from TilPattern import TilDefiner
from TilPattern import TilPattern


class TilProducer(TilDefiner):

  def __init__(self, n_slots=None, soma=None):
    super(TilProducer, self).__init__(n_slots, soma)
    self.partition_index = None
    self.alltilwpatterns = get_only_instance_of_tilallpatternsSingleton().get_alltilwpatterns_from_buffer(self)
    self.set_total_combinations()

  def get_alltilpatterns_as_intlists(self):
    patterns_as_intlist = []
    for wpattern in self.alltilwpatterns:
      pattern_intlist = map(int, [c for c in wpattern] )
      patterns_as_intlist.append(pattern_intlist)
    return patterns_as_intlist 

  def set_total_combinations(self):
    self.total_combinations = len(self.alltilwpatterns)
    # calc_n_integer_partitions(self.n_slots, self.soma) 

  def __len__(self):
    return self.total_combinations
      
  def get_tilwpattern_at_current_partition_index(self):
    if self.partition_index < 0 or self.partition_index > self.total_combinations - 1:
      return None
    wpattern = self.alltilwpatterns[self.partition_index]
    return wpattern 

  def get_tilpattern_at_current_partition_index(self):
    wpattern = self.get_tilwpattern_at_current_partition_index()
    if wpattern == None:
      return None 
    tilpattern = TilPattern(self.n_slots, self.soma)
    tilpattern.set_wpattern(wpattern)
    return tilpattern 
    #fetch_integer_partition(self.n_slots, self.soma, self.partition_index)
  
  def park_partition_index_at_start(self):
    self.partition_index = 0
    
  def park_partition_index_at_end(self):
    self.partition_index = self.total_combinations - 1 

  def common_next(self):
    if self.partition_index == None:
      self.park_partition_index_at_start()
    else:
      self.partition_index += 1

  def next(self):
    self.common_next()
    return self.get_tilpattern_at_current_partition_index()

  def wnext(self):
    self.common_next()
    return self.get_tilwpattern_at_current_partition_index()

#  def __next__(self):
#    return self.next()

  def common_previous(self):
    if self.partition_index == None:
      self.park_partition_index_at_end()
    else:
      self.partition_index -= 1

  def previous(self):
    self.common_previous()
    return self.get_tilpattern_at_current_partition_index()

  def wprevious(self):
    self.common_previous()
    return self.get_tilwpattern_at_current_partition_index()

  def first(self):
    self.park_partition_index_at_start()
    return self.get_tilpattern_at_current_partition_index()
    
  def wfirst(self):
    self.park_partition_index_at_start()
    return self.get_tilwpattern_at_current_partition_index()

  def last(self):
    self.park_partition_index_at_end()
    return self.get_tilpattern_at_current_partition_index()

  def wlast(self):
    self.park_partition_index_at_end()
    return self.get_tilwpattern_at_current_partition_index()

  def at(self, partition_index):
    self.partition_index = partition_index 
    return self.get_tilpattern_at_current_partition_index()

  def wat(self, partition_index):
    self.partition_index = partition_index 
    return self.get_tilwpattern_at_current_partition_index()

  def __str__(self):
    return '<Til(%d,%d) %d tils>' %(self.n_slots, self.soma, self.total_combinations)
    

class TilAllPatternsBuffer(object):
  '''
  This class only exists for buffering Til wpatterns. Ex. Til(5,6) has 210 wpatterns.
  Class TilProducer holds a reference to these objects so that many TilProducer objects don't use too much memory.
  '''
  
  def __init__(self):
    self.tilbuffer = {}
    
  def add_alltilpatterns_to_buffer(self, tildefiner, alltilpatterns):
    self.tilbuffer[(tildefiner.n_slots, tildefiner.soma)] = alltilpatterns
    
  def get_alltilwpatterns_from_buffer(self, tildefiner):
    definertuple = (tildefiner.n_slots, tildefiner.soma)
    if self.tilbuffer.has_key(definertuple):
      return self.tilbuffer[definertuple]
    alltilpatterns = ffTil.getTilPatternsFor(tildefiner.n_slots, tildefiner.soma)
    self.add_alltilpatterns_to_buffer(tildefiner, alltilpatterns)
    return alltilpatterns

tilallpatternsSingleton = None
def get_only_instance_of_tilallpatternsSingleton():
  '''
  This function simulates a singleton hand-out for a unique instantiated TilAllPatternsBuffer object
  '''
  global tilallpatternsSingleton
  if tilallpatternsSingleton == None:
    tilallpatternsSingleton = TilAllPatternsBuffer()
  return tilallpatternsSingleton 


def adhoc_test():
  print 'list_dist_xysum_metric_thry_ms_history()'
  tilproducer = TilProducer(12, 6); c=0
  while 1:
    tilpattern = tilproducer.wnext()
    if tilpattern == None:
      break 
    c+=1
    print c, 'tilpattern', tilpattern, tilproducer.partition_index 
  print 'print first', tilproducer.wfirst()
  print 'print last', tilproducer.wlast()
  print 'print at 100', tilproducer.wat(100)
  print 'print size', tilproducer.total_combinations

def adhoc_test2():
  print 'list_dist_xysum_metric_thry_ms_history()'
  tilproducer = TilProducer(5, 6); c=0
  while 1:
    tilpattern = tilproducer.next()
    if tilpattern == None:
      break 
    c+=1
    print c, 'tilpattern', tilpattern, tilproducer.partition_index 
  print 'print first', tilproducer.first()
  print 'print last', tilproducer.last()
  print 'print at 100', tilproducer.at(100)
    
  
def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
