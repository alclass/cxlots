#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
TilPattern.py
'''
import sys

import localpythonpath
localpythonpath.setlocalpythonpath()

class TilDefiner(object):
  '''
  This class only defines two attributes:
  + slots
  + soma
  
  Usage example:
    A Til5 (or a statistics quintil) for a 6-number set has 5 slots and "soma" 6
    
  TilDefiner is a base (or parent) class for TilPattern and TilPattern is parent for JogoTilPattern
  '''

  def __init__(self, slots=None, soma=None):
    if slots==None:
      slots = 5 # default
    if soma==None:
      soma = 6 # default
    self.slots = int(slots)
    self.soma  = int(soma)


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

  def __init__(self, slots=None, soma=None):
    super(TilPattern, self).__init__(slots, soma)
    self.wpattern = None
    #self.tilnumber = int(tilnumber)
    #self.freqsoma  = int(freqsoma)

  def set_wpattern(self, wpattern):
    self.wpattern = wpattern
    self.is_self_consistent()

  def is_self_consistent(self):
    if len(self.wpattern) != self.slots:
      error_msg = 'len(self.wpattern)=%d != self.tilnumber=%d' %(len(self.wpattern), self.slots)
      raise TypeError, error_msg 
    freqsoma_to_compare = 0
    for char in self.wpattern:
      freqsoma_to_compare += int(char)
    if self.soma != freqsoma_to_compare:
      error_msg = 'self.freqsoma=%d != freqsoma_to_compare=%d' %(self.soma, freqsoma_to_compare)
      raise TypeError, error_msg
    
  def __eq__(self, tilpattern):
    # DeMorgan to improve performance if case wpattern differs right away (believed to be most of the cases in filtering processing)
    if (self.wpattern != tilpattern.wpattern or  
          self.slots != tilpattern.slots or 
           self.soma != tilpattern.soma):
      return False
    return True
  
  def __str__(self):
    return "'<TilPattern(%d,%d,'%s')>" %(self.slots, self.soma, self.wpattern)

def adhoc_test():
  print 'adhoc_test()'
  tilpattern = TilPattern(5, 6)
  tilpattern.set_wpattern('02220')
  print 'tilpattern', tilpattern
  
def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
