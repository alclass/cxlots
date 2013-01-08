#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Ref.: http://en.wikipedia.org/wiki/Combinadic
  combinadics Module
'''
import sys

import localpythonpath
localpythonpath.setlocalpythonpath()
from lib import lambdas
# import algorithmsForCombinatorics as afc

class IndicesCombiner(object):
  '''
  This class is explained by examples
  ========================================

  Example 1:
  indComb = IndicesCombiner(5, 3, False)
  indComb.first() results [0, 1, 2]
  indComb.firstGiven() in this case also results [0, 1, 2]
  applying indComb.next() each time:
  [0, 1, 2]   [0, 1, 3]   [0, 1, 4]   [0, 1, 5]   [0, 2, 3]
  [0, 2, 4]   [0, 2, 5]   [0, 3, 4]   [0, 3, 5]   [0, 4, 5]
  [1, 2, 3]   [1, 2, 4]  ... the last one is [3, 4, 5]
  if a new indComb.next() is applied, None is returned

  The behavior expected is that of a Combination
  Mathematically, the total of produced arrays is:
    Combination(5,3) = 5! / ((5-3)!3!)

  Example 2:
  Now the same example with overlap=True (in fact, 'True' is default)
  indComb = IndicesCombiner(5, 3, True)
  indComb.first() results [0, 0, 0]
  indComb.firstGiven() in this case also results [0, 0, 0]
  (*) firstGiven() is explained below
  aplying indComb.next() each time:
  [0, 0, 1]   [0, 0, 2]   [0, 0, 3]   [0, 0, 4]   [0, 0, 5]
  [0, 1, 1]   [0, 1, 2]   [0, 1, 3]   [0, 1, 4]   [0, 1, 5]
  [0, 2, 2] ... the last one is [5,5,5] after that, a None will be returned

  (*) firstGiven() explanation
  when iArrayIn is passed with a consistent array
  firstGiven() returns that array

  Example:

  indComb = IndicesCombiner(5, 3, True, [2,2,3])
  indComb.firstGiven() in this case results [2, 2, 3]
  [2, 2, 3] is called the "restartAt" array
  indComb.next() results [2, 2, 4]

  IMPORTANT: if indComb.first() is issued/called, the combiner is zeroed,
  so to speak, ie, it goes top to [0,0,0] or [0,1,2] depending whether
  overlap is True or False, respectively

  Error Handling
  ==============

  1) if a "bad" restartAt array is given, a ValueError Exception will be raised

  Example 1 (for when overlap=False)
  [0,2,2] ie there is a 2 following a 2 (only possible if overlap=True)

  Example 2 (for when either overlap=True or False)
  [0,10,9] ie there is a 9 following a 10

  2) when overlap=False, if both upLimit and size are positive (*),
     upLimit must be at least size - 1

  (*) if upLimit or size enters negative, they are changed to the default,
      ie, upLimit=0 and size=1

  Eg. upLimit = 2 and size = 3 :: this will result in
      only one combination [0,1,2] (with overlap=False)
  
  If the above fails, a ValueError Exception will be raised
  Notice that this restriction does not exist for overlap=True

  Test example:

  indComb = IndicesCombiner(1, 4, True)
  [0, 0, 0, 0]  [0, 0, 0, 1]  [0, 0, 1, 1]  [0, 1, 1, 1]  [1, 1, 1, 1]

  But
    [[[ indComb = IndicesCombiner(1, 4, False) ]]] will raise a ValueError:

  Traceback (most recent call last):
    File "./combinadics.py", line 237, in <module>
      testIndicesCombiner(upLimit, size)
    File "./combinadics.py", line 189, in testIndicesCombiner
      indComb = IndicesCombiner(upLimit, size, False); c=0
    File "./combinadics.py", line 80, in __init__
      raise ValueError, msg
  ValueError: Inconsistent IndicesCombiner upLimit(=1) must be at least size(=4) - 1 when overlap=False

  '''

  def __init__(self, upLimit=0, size=1, overlap=True, iArrayIn=[0]):
    if size < 1:
      size = 1
    if upLimit < 0:
      upLimit = 0
    if overlap not in [True, False]:
      overlap = True
    if not overlap:
      if upLimit + 1 < size:
        msg = 'Inconsistent IndicesCombiner upLimit(=%d) must be at least size(=%d) - 1 when overlap=False ' %(upLimit, size)
        raise ValueError, msg
    self.upLimit = upLimit
    self.overlap = overlap
    if iArrayIn == [0] and size > 1:
      if overlap:
        self.iArray = [0]*size
      else:
        self.iArray = range(size)
    else:
      self.iArray      = list(iArrayIn)
    self.size        = len(self.iArray)
    self.checkArrayConsistency()
    self.iArrayGiven = list(self.iArray)

  def checkArrayConsistency(self):
    '''
    Checks the consistency of iArray
    Examples of inconsistent arrays:
    1) for overlap=True
    valid ==>> [0,0,0], [0,1,1], [2,2,3]
    invalid ==>> [0,1,0], [10,0,0]
    2) for overlap=False
    valid ==>> [0,1,2], [0,1,100]
    invalid ==>> [0,0,0], [2,2,3] (these two valid when overlap=True)
    '''
    for i in range(self.size-1):
      raiseException = False
      if self.overlap:
        if self.iArray[i+1] < self.iArray[i]:
          raiseException = True
      else:
        if self.iArray[i+1] <= self.iArray[i]:
          raiseException = True
      if raiseException:
        if self.overlap:
          context = 'lesser'
        else:
          context = 'lesser or equal'
        msg = 'Inconsistent array: next elem can be %s than a previous one %s' %(context, str(self.iArray))
        raise ValueError, msg

  def current(self):
    '''
    Returns the current iArray
    Notice that iArray is modified by methods like next() and first()
    '''
    return self.iArray

  def first(self):
    '''
    Moves the iArray to the top and returns it
    Eg
    overlap=True,  size=3 :: [0,0,0]
    overlap=False, size=4 :: [0,1,2,3]
    '''
    size = self.size
    if self.overlap:
      self.iArray = [0] * size
    else:
      self.iArray = range(size)
    return self.iArray

  def top(self):
    '''
    The same as first()
    '''
    self.first()

  def firstZeroless(self):
    iArray = self.first()
    iArray = map(lambdas.plusOne, iArray)
    return iArray
    
  def firstGiven(self):
    '''
    Returns the firstGiven or restartAt array but does not change current position
    To change it, use positionToFirstGiven()
    '''
    return self.iArrayGiven

  def positionToFirstGiven(self):
    '''
    Returns the firstGiven/restartAt array changing current position to it
    @see also firstGiven()
    '''
    self.iArray = list(self.iArrayGiven)

  def moveToLastOne(self):
    '''
    Moves iArray position to the last one and returns it
    Eg
    overlap=True,  size=3, upLimit=15 :: [15,15,15]
    overlap=False, size=4, upLimit=33 :: [30,31,32,33]
    '''
    self.iArray = self.tell_last_iArray()
    return self.iArray

  def tell_last_iArray(self):
    '''
    @see self.moveToLastOne()
    '''
    last_iArray = [0]*self.size
    if self.overlap:
      last_iArray = [self.upLimit] * self.size
      return last_iArray
    else:
      for i in range(self.size):
        backPos = self.size - i - 1
        last_iArray[i] =  self.upLimit - backPos
      return last_iArray

  def tell_first_iArray(self):
    first_iArray = [0]*self.size
    if self.overlap:
      # first_iArray = [0] * self.size
      return first_iArray
    else:
      first_iArray = range(self.size)
      return first_iArray

  def move_to_position_by_iArray(self, iArray_in):
    if iArray_in == None or len(iArray_in) != self.size:
      raise TypeError, "iArray is None or it's been given having an incorrect size (of iArray)"
    if iArray_in != map(int, iArray_in):
      raise ValueError, 'parameter iArray_in was passed in containing non-integers'
    tmp_lambda_greater_than = lambda x, y : x > y
    last_iArray = self.tell_last_iArray()
    # if it's greater than last, move it to last
    if True in map(tmp_lambda_greater_than, iArray_in, last_iArray):
      self.moveToLastOne()
      return
    first_iArray = self.tell_first_iArray()
    tmp_lambda_less_than = lambda x, y : x < y
    # if it's less than first, move it to first
    if True in map(tmp_lambda_less_than, iArray_in, first_iArray):
      self.first()
      return
    self.iArray = iArray_in
  
  def correctRemainingToTheRightOverlapCase(self, pos):
    '''
    Recursive method
    When vaiUm() happens, the logical consistency of iArray should be kept
    In a way, it's similar to the adding algorithm we learn at school
    Eg
    vaiUm(pos=1) for [0,3,3] will result [0,4,3]
    This needs correction to [0,4,4]
    '''
    if pos+1 >= self.size:
      return
    if self.iArray[pos] > self.upLimit:
      msg = 'Index in Combiner exceeds upLimit(=%d). There is probably a bug. self.iArray[%d]=%d :: ' %(self.upLimit, pos, self.iArray[pos])
      msg += str(self)
      raise ValueError, msg
    self.iArray[pos+1] = self.iArray[pos]
    return self.correctRemainingToTheRightOverlapCase(pos+1)

  def correctRemainingToTheRightNonOverlapCase(self, pos):
    '''
    Recursive method
    When vaiUm() happens, the logical consistency of iArray should be kept
    In a way, it's similar to the adding algorithm we learn at school
    Eg
    vaiUm(pos=1) for [0,3,4] will result [0,4,4]
    This needs correction to [0,4,5]
    '''
    if pos+1 >= self.size:
      return
    # notice backPos here is POSITIVE ie eg. [0,1,3,...,10] backPos's are [10,9,...,0]
    backPos = self.size - pos - 1
    if self.iArray[pos] > self.upLimit - backPos:
      msg = 'Index in Combiner exceeds upLimit(=%d). There is probably a bug. self.iArray[%d]=%d :: ' %(self.upLimit, pos, self.iArray[pos])
      msg += str(self)
      raise ValueError, msg
    self.iArray[pos+1] = self.iArray[pos] + 1
    return self.correctRemainingToTheRightNonOverlapCase(pos+1)

  def shiftLeft(self, pos=-1): # , nOfPos=-1
    '''
    Left-shifts the iArray
    Eg
    overlap=True,  size=3, upLimit=15
    [1,1,1].shiftLeft(1) ==>> [2,2,2]
    overlap=False, size=4, upLimit=33
    [1,2,3,4].shiftLeft(2) ==>> [1,3,4,5]
    '''
    if pos == -1:
      pos = self.size - 1
    if pos == 0:
      # well, it's the last one, a left-shift can't happen,
      # so it goes to the last one
      self.moveToLastOne() #iArrayToDiscard = self.moveToLastOne()
      return None
    if self.overlap:
      if self.iArray[pos-1] == self.upLimit:
        return self.shiftLeft(pos-1)
      self.iArray[pos-1] += 1
      self.correctRemainingToTheRightOverlapCase(pos-1)
      return self.iArray
    else:
      posAnt = pos - 1
      backPosAnt = self.size - posAnt - 1
      if self.iArray[posAnt] == self.upLimit - backPosAnt:
        return self.shiftLeft(pos-1)
      self.iArray[pos-1] += 1
      self.correctRemainingToTheRightNonOverlapCase(pos-1)
      return self.iArray

  def vaiUmInPlaceOverlapCase(self, pos):
    '''
    Case of vaiUm when overlap=True
    '''
    if pos == 0 and self.iArray[pos] == self.upLimit:
      self.moveToLastOne() # iArrayToDiscard = self.moveToLastOne()
      return None
    if self.iArray[pos] == self.upLimit:
      return self.vaiUmInPlaceOverlapCase(pos-1)
    self.iArray[pos] += 1
    self.correctRemainingToTheRightOverlapCase(pos)
    return self.iArray

  def vaiUmInPlaceNonOverlapCase(self, pos):
    '''
    Case of vaiUm when overlap=False
    '''
    backPos = self.size - pos - 1
    if pos == 0 and self.iArray[pos] == self.upLimit - backPos:
      self.moveToLastOne() # iArrayToDiscard = self.moveToLastOne()
      return None
    if self.iArray[pos] == self.upLimit - backPos:
      return self.vaiUmInPlaceNonOverlapCase(pos-1)
    self.iArray[pos] += 1
    self.correctRemainingToTheRightNonOverlapCase(pos)
    return self.iArray

  def vaiUmInPlace(self, pos):
    '''
    Adds one in the i-th (pos) element
    Eg
    overlap=True,  size=3, upLimit=15
    [1,1,1].shiftLeft(1) ==>> [1,2,2]
    overlap=False, size=4, upLimit=33
    [1,2,3,4].shiftLeft(2) ==>> [1,2,4,5]
    '''
    if self.overlap:
      return self.vaiUmInPlaceOverlapCase(pos)
    else:
      return self.vaiUmInPlaceNonOverlapCase(pos)

  def minusOneOverlap(self, pos):
    '''
    Inner implementation of previous() for the overlap=True case
    see @previous()
    '''
    if pos == 0:
      if self.iArray[0] > 0:
        self.iArray[0] -= 1
        return self.iArray
      else: # if self.iArray[pos] == 0:
        self.first()
        return None
    if self.iArray[pos-1] == self.iArray[pos]:
      self.iArray[pos] = self.upLimit
      return self.minusOneOverlap(pos-1)
    else:
      self.iArray[pos] -= 1
      return self.iArray

  def minusOneNonOverlap(self, pos):
    '''
    Inner implementation of previous() for the overlap=False case
    see @previous()
    '''
    if pos == 0:
      if self.iArray[pos] > 0:
        self.iArray[pos] -= 1
        return self.iArray
    if self.iArray[pos] == pos:
      self.first()
      return None
    if self.iArray[pos-1]+1 == self.iArray[pos]:
      debitToUpLimit = self.size - pos - 1
      self.iArray[pos] = self.upLimit - debitToUpLimit
      return self.minusOneNonOverlap(pos-1)
    else:
      self.iArray[pos] -= 1
    return self.iArray

  def previous(self):
    '''
    Moves iArray to the its previous consistent position and returns the array
    When the first one is current, None will be returned
    '''
    pos = self.size - 1
    if self.overlap:
      return self.minusOneOverlap(pos)
    else:
      return self.minusOneNonOverlap(pos)
  def next(self, pos=-1):
    '''
    Moves iArray position to the next consistent one and returns it
    When the last one is current, a None will be returned
    '''
    if pos == -1:
      pos = self.size - 1
    #if self.iArray[pos]+1 > self.upLimit:
    if self.overlap:
      upLimit = self.upLimit
    else:
      upLimit = self.upLimit - (self.size - pos - 1)
    if self.iArray[pos]+1 > upLimit:

      def recurseIndicesWithOverlap(pos):
        '''
        This is an inner recursive help method
        For the case when overlap=True
        '''
        if pos == 0 and self.iArray[pos]+1 > self.upLimit:
          return None
        if self.iArray[pos]+1 > self.upLimit:
          if self.iArray[pos-1]+1 > self.upLimit:
            #self.iArray[pos]=self.iArray[pos-1]
            return recurseIndicesWithOverlap(pos-1)
          self.iArray[pos-1]+=1
          self.iArray[pos]=self.iArray[pos-1]
          return self.iArray[pos-1]
        return self.iArray[pos]+1

      def recurseIndicesWithoutOverlap(pos):
        '''
        This is an inner recursive help method
        For the case when overlap=False
        '''
        if pos == 0 and self.iArray[pos]+1 > self.upLimit - (self.size - pos - 1):
          return None
        if self.iArray[pos]+1 > self.upLimit - (self.size - pos - 1):
            tmp =recurseIndicesWithoutOverlap(pos-1)
            if tmp == None:
              return None
            self.iArray[pos] = tmp + 1
            return self.iArray[pos]
        self.iArray[pos]+=1
        return self.iArray[pos]

      if self.overlap:
        value = recurseIndicesWithOverlap(pos)
      else:
        value = recurseIndicesWithoutOverlap(pos)
      if value == None:
        return None
      self.iArray[pos] = value
    else:
      self.iArray[pos] += 1
    return self.iArray

  def nextZeroless(self):
    '''
    '''
    iArray = self.next()
    iArray = map(lambdas.plusOne, iArray)
    return iArray
  
  def __str__(self):
    '''
    The string representation of the class
    '''
    outStr = 'array=%s upLimit=%d overlap=%s' %(str(self.iArray), self.upLimit, self.overlap)
    return outStr

  def allSets(self):
    '''
    This method, though it's still here, should be used with caution in the sense the it's memory-hungry, so to say.
    It while-loops all self.next()'s into an output array.
    Because output may become very big, according to the size involved the process,
      a better approach is to "yield" each "workSet", one at a time, without buffering them into the "output array"
      This better approach is done by the following next method iterate_all_sets()
    '''
    array = []
    s = self.first()
    workSet = list(s) # hard-copy
    while s:
      array.append(workSet)
      s = self.next()
      if s:
        workSet = list(s)
    return array

  def iterate_all_sets(self):
    '''
    This method, though it's still here, should be used with caution in the sense the it's memory-hungry, so to say.
    It while-loops all self.next()'s into an output array.
    Because output may become very big, according to the size involved the process,
      a better approach is to "yield" each "workSet", one at a time, without buffering them into the "output array"
      This better approach is done by the following next method iterate_all_sets()
    '''
    workSet = self.first()
    while workSet:
      yield list(workSet) #  # hard-copy
      workSet = self.next()


  
def testIndicesCombiner(upLimit, size):
  # signature IndsControl(upLimit=1, size=-1, overlap=True, iArrayIn=[])
  indComb = IndicesCombiner(upLimit, size, True); c=0
  print 'indComb = IndicesCombiner(%d, %d, True)' %(upLimit, size)
  s = indComb.firstGiven()

  setWithOL = []
  while s:
    c+=1
    print c, s
    setWithOL.append(list(s))
    s = indComb.next()

  setWithoutOL = []
  indComb = IndicesCombiner(upLimit, size, False); c=0
  print 'indComb = IndicesCombiner(%d, %d, False)' %(upLimit, size)
  s = indComb.firstGiven()
  while s:
    c+=1
    print c, s
    setWithoutOL.append(list(s))
    s = indComb.next()

  c=0; notThere = 0
  for wOL in setWithOL:
    c+=1
    print c, wOL,
    if wOL in setWithoutOL:
      print wOL
    else:
      notThere += 1
      print notThere

def pickUpParams():
  params = []
  upLimit = 5
  size    = 3
  for i in range(1, len(sys.argv)):
    params.append(sys.argv[i].lower())
  print 'params', params
  if '-uplimit' in params:
    index = params.index('-uplimit')
    print 'index -uplimit', index
    if index + 1 < len(params):
      try:
        upLimit = int(params[index + 1])
      except ValueError:
        pass
  if '-size' in params:
    index = params.index('-size')
    if index + 1 < len(params):
      try:
        size = int(params[index + 1])
      except ValueError:
        pass
  return upLimit, size

def testShiftLeft(upLimit, size):
  indComb = IndicesCombiner(upLimit, size, True, [2,4,5]); c=0
  print 'indComb = IndicesCombiner(%d, %d, %s)' %(upLimit, size, indComb.overlap)
  print indComb
  print 'testShiftLeft()', indComb.shiftLeft()
  for i in range(7):
    next = indComb.next()
  print 'next 7', next
  print 'testShiftLeft()', indComb.shiftLeft()
  
  indComb = IndicesCombiner(7, -1, True, [0,6,6,7,7]); c=0
  print 'indComb = IndicesCombiner(%d, %d, %s)' %(upLimit, size, indComb.overlap)
  print indComb
  pos = 1
  print 'test vai um(%d)' %(pos), indComb.vaiUmInPlace(pos)
  pos = 2
  print 'testShiftLeft(%d)' %(pos), indComb.shiftLeft(pos)
  pos = 1
  print 'test vai um(%d)' %(pos), indComb.vaiUmInPlace(pos)
  print 'test vai um(%d)' %(pos), indComb.vaiUmInPlace(pos)
  print 'test vai um(%d)' %(pos), indComb.vaiUmInPlace(pos)
  print 'current', indComb.current()
  print 'next', indComb.next()
  
def testPrevious(upLimit, size):
  ic = IndicesCombiner(upLimit, size, True, [0,2,12])
  print 'ic', ic
  print 'ic.next()', ic.next()
  print 'ic', ic
  print 'ic.previous()', ic.previous()
  for i in range(36):
    print 'ic.previous()', ic.previous()
  #for i in range(32):
    #print 'ic.next()', ic.next()
                          
def adhoc_test():
  ic = IndicesCombiner(4, 2, False); c=0
  for ws in ic.iterate_all_sets():
    c+=1
    print c, ws
  '''sc = SetsCombiner()
  worksetWithQuantity = ([1,2,3], 2)
  sc.addSetWithQuantities(worksetWithQuantity)
  worksetWithQuantity = ([4,5,6], 2)
  sc.addSetWithQuantities(worksetWithQuantity)
  for ws in sc.getAllSetsCombinationNonRecursively():
    print 'ws', ws'''

def ynext():
  for i in xrange(10):
    yield i

def test_yield():
  for i in ynext():
    print i

def adhoc_test2():
  test_yield()
  
def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
