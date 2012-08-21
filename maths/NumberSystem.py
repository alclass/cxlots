#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, sys
#import numpy
'''
algo
'''

def convert_positive_dec_int_to_base_recurse(n, base, strdigits=''):
  '''
  This is a recursive function that transform decimal, positive integers, into a number of a different base
  Its entrance point, for checking input values, is function convert_positive_dec_int_to_base(n, base=2) 
  Eg. 
  
  f = convert_positive_dec_int_to_base
  f(1024, 2) returns '10000000000' (which is 1024 written on base 2)
  f(210, 5) returns '1320' (which 210 written on base 5)
  f(210, 6) returns '550'
  f(0, 6) returns '0'
  f(1, 6) returns '1'
  f(6, 6) returns '10'
  f(7, 6) returns '11'
  '''
  divided = n / base 
  remainder = n % base
  strdigits = str(remainder) + strdigits
  #print 'n', n, 'base', base, 'divided', divided, 'remainder', remainder, 'strdigits', strdigits  
  if divided < base:
    # it's finished
    if divided != 0:
      strdigits = str(divided) + strdigits
    #strdigits = strdigits.lstrip('0')
    return strdigits 
  return convert_positive_dec_int_to_base_recurse(divided, base, strdigits)


def convert_positive_dec_int_to_base(n, base=2):
  '''
  This function is the entrance point for the recursive function:
    convert_positive_dec_int_to_base_recurse(n, base, strdigits='') 
  Its aim is to convert a positive integer base 10 to a number of a different base
  The __doc__ of the recursive called function contains examples.
  '''
  if n < 0:
    error_msg = 'Cannot convert negative integers/numbers. Number passed = %d' %n
    raise ValueError, error_msg
  return convert_positive_dec_int_to_base_recurse(n, base)

def test_convert_positive_dec_int_to_base(n, base, strdigits=''):
  f = convert_positive_dec_int_to_base
  returned = f(1024, 2) # returns '10000000000' (which is 1024 written on base 2)
  expected = '10000000000'
  assert returned == expected
  returned = f(210, 5) # returns '1320' (which 210 written on base 5)
  expected = '1320'
  assert returned == expected
  returned = f(210, 6) # returns '550'
  expected = '550'
  assert returned == expected
  returned = f(0, 6) # returns '0'
  expected = '0'
  assert returned == expected
  returned = f(1, 6) # returns '1'
  expected = '1'
  assert returned == expected
  returned = f(6, 6) # returns '10'
  expected = '10'
  assert returned == expected
  returned = f(7, 6) # returns '11'
  expected = '11'
  assert returned == expected

class Mixer:
  '''
  This call, though it's here, it's not doing anything yet
  '''
  def __init__(self, sumUpTo, expandUpTo):
    self.sumUpTo    = sumUpTo
    self.expandUpTo = expandUpTo
  def process(self):
    self.elems=[self.sumUpTo]
  def recur(self, at, runningSet=[]):
    if at==0:
      return
    runningSet.append(at)
    missing=self.sumUpTo-at
    if missing == 1:
      runningSet.append(1)
      #return elem

class NumberSystem(object):
  '''
  This call models a number system. It's useful for some needs of the system.
    Eg. a combination sequence such as 0001, ..., 1234, ... , 4321, ..., 4444 works a base-4 system set 
  '''
  def __init__(self, arraySize, base):
    self.arraySize = arraySize # same as n_slots
    self.base      = base # number base
    self.values    = self.digits_zeroed() # do not use move_to_first() here because child classes use an extra attribute that's not here (self.first)

  def get_total(self):
    return self.base ** self.arraySize 

  def digits_zeroed(self):
    return [0]*self.arraySize

  def who_is_first(self):
    '''
    This method is the one that will be implemented by child classes, move_to_first() and get_first() depend on this one
      and, these two, are not to reimplement on child classes
    '''
    return self.digits_zeroed()

  def move_to_first(self):
    self.values = self.who_is_first()

  def get_first(self):
    self.move_to_first()
    return self.values

  def who_is_last(self):
    return [self.base-1]*self.arraySize

  def move_to_last(self):
    self.values = self.who_is_last()

  def get_last(self):
    self.move_to_last()
    return self.values

  def form_strdigits(self):
    if self.values == None:
      return None
    strdigits = ''.join(map(str, self.values)) 
    return strdigits

  def add_one(self, pos=None):
    if pos == None:
      pos = len(self.values) - 1
    if pos == -1:
      self.values = None
      return
    self.values[pos] += 1
    # print 'AFTER self.values[pos] += 1', self.values
    if self.values[pos] > self.base - 1:
      self.values[pos] = 0
      return self.add_one(pos-1) # ie, vai um

  def subtract_one(self, pos=None):
    if pos == None:
      # jump to the right-most digit
      pos = len(self.values) - 1
    if pos == 0 and self.values[pos] == 0:
      # supposedly, it's already element "zero", ie [0]*arraySize
      # diminishing from zero, null the array
      self.values = None
      return
    if self.values[pos] == 0:
      self.values[pos] = self.base - 1
      return self.subtract_one(pos-1)
    self.values[pos] -= 1

  def do_next(self):
    if self.values != None:
      self.add_one()

  def next(self):
    self.do_next()
    return self.values

  def do_previous(self):
    if self.values != None:
      self.subtract_one()

  def previous(self):
    self.do_previous()
    return self.values

  def findArraysSummingTo(self, shouldSumTo=None):
    if not shouldSumTo:
      shouldSumTo = self.base
    if shouldSumTo > self.maxSum:
      print 'shouldSumTo', shouldSumTo, 'is greater than maxSum', self.maxSum
    # backup current values array
    valuesCopied = list(self.values)
    # reset values
    self.values      = [0]*self.arraySize
    # c=0
    arraysFound = []
    while 1:
      if not self.somaUm():
        break
      if sum(self.values) == shouldSumTo:
        # c+=1
        # print c, self.values
        arraysFound.append(list(self.values))
    # restore previous values array
    self.values = list(valuesCopied)
    return arraysFound

class RemaindersComb(NumberSystem):
  '''
  Class RemaindersComb inherits from class NumberSystem
  '''
  def __init__(self, arraySize, base, shouldSumTo=None):
    NumberSystem.__init__(self, arraySize, base)
    self.arraysFound = self.findArraysSummingTo(shouldSumTo)
  def index(self, combArray):
    return self.arraysFound.index(combArray)

def testRemaindersComb():
  # arraySize = 3 # remainders of 3
  base =  6 # ie, 6 dezenas
  remaindersOf = [2,3,4,5,6] #,7,8] #,12,15]
  for r in remaindersOf:
    rc = RemaindersComb(r, base)
    af = rc.arraysFound; c=0
    print r, len(af)
    for elem in af:
      c+=1
      print c, elem

def test_numberbaseconvertion(n, base):
  print 'n =', n, '; base =', base
  f = NS.convert_positive_dec_int_to_base
  strdigits = f(n, base)
  print strdigits

def adhoc_test2():
  f = test_numberbaseconvertion
  f(1024, 2)
  f(210, 5)
  f(210, 6)
  f(0, 6)
  f(1, 6)
  f(6, 6)
  f(7, 6)

def adhoc_test():
  ns = NumberSystem(5, 6); c=0
  array = ns.get_last()
  print 'last', array
  while array:
    c+=1
    print ns.form_strdigits(), 
    array = ns.previous()
  total = ns.get_total()
  print 'total', total, c 
  
def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()

