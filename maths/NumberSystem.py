#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, sys
#import numpy
'''
algo
'''

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

class NumberSystem:
  '''
  This call models a number system. It's useful for some needs of the system.
    Eg. a combination sequence such as 0001, ..., 1234, ... , 4321, ..., 4444 works a base-4 system set 
  '''
  def __init__(self, arraySize, base):
    self.arraySize   = arraySize
    self.base        = base
    self.values      = [0]*self.arraySize
    self.lastElem    = [self.base]*self.arraySize
    self.maxSum      = sum(self.lastElem)
    print 'self.lastElem', self.lastElem
    print 'self.maxSum', self.maxSum

  def somaUm(self, pos=-2):
    if pos == -2:
      pos = len(self.values) - 1
    if pos == -1:
      return None
    self.values[pos] += 1
    if self.values[pos] > self.base:
      self.values[pos] = 0
      return self.somaUm(pos-1)
    return True

  '''
  def next(self):
    if not self.somaUm(self.values):
      return None
    return self.values
    '''

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

if __name__ == '__main__':
  pass

'''  
  tpVector = TillPatternVector(10,6)
  print 'tpVector', tpVector
  tpVector = TillPatternVector(10,3)
  print 'tpVector', tpVector
'''