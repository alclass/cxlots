#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Ref.: http://en.wikipedia.org/wiki/Combinadic
  combinadics Module
'''
import sys

a=1
import lambdas

class IndicesCombiner(object):
  '''
  This class is explained by examples
  ========================================

  Example 1:
  indComb = IndicesCombiner(5, 3, False)
  indComb.first() results [0, 1, 2]
  indComb.firstGiven() in this case also results [0, 1, 2]
  aplying indComb.next() each time:
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
    if self.overlap:
      self.iArray = [self.upLimit] * self.size
      return self.iArray
    else:
      for i in range(self.size):
        backPos = self.size - i - 1
        self.iArray[i] =  self.upLimit - backPos
      return self.iArray

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
      iArrayToDiscard = self.moveToLastOne()
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
      iArrayToDiscard = self.moveToLastOne()
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
      iArrayToDiscard = self.moveToLastOne()
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
      self.iArray[pos] = upLimit
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
      self.iArray[pos] = upLimit - debitToUpLimit
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
    array = []
    s = self.first()
    workSet = list(s)
    while s:
      array.append(workSet)
      s = self.next()
      if s:
        workSet = list(s)
    return array

class SetsCombiner():
  '''
  This class has a "bridge" method called combineSets(self)
    that calls doRecursiveSetsCombination(self.listOfTuple2)
  The latter function receives the listOfTuple2 that keeps the following information:
    first tuple element is a set (list) with dezenas to be combined according to the 
    second tuple element which is the quantity (or size) of each combination
    Eg
    ([12, 23, 33, 42, 57], 3) generates:
    12 23 33, 12 23 42, 12 23 57 ... up to 33 42 57
    
    The final result is the combination of all sets
    
    With this functionality, one possible of this class's  
  '''
  def __init__(self):
    self.workSetsWithQuantities = [] #  # workSetsWithQuantities was formerly listOfTuple2
    self.allCombinations = None
  def addSetWithQuantities(self, tupleIn):
    self.workSetsWithQuantities.append(tupleIn)
  def combineSets(self):
    self.allCombinations = doRecursiveSetsCombination(self.workSetsWithQuantities)
  def __len__(self):
    if self.allCombinations == None:
      return 0
    return len(self.allCombinations)

class SetsCombinerWithTils(SetsCombiner):
  '''
  This class inherits from SetsCombiner
  The idea here is to automatically fill in self.workSetsWithQuantities from a tilObj
  So at object instantiation every is run at once
     and after instantiation the object has its combined sets available 
  '''
  def __init__(self, tilElement):
    SetsCombiner.__init__(self)
    self.tilElement = tilElement
    self.unpackTilObj()
    self.combineSets() # a parent class's method
  def unpackTilObj(self):
    self.workSetsWithQuantities = self.tilElement.getWorkSetsWithQuantities() 
    
    


def createWorkSetsWithIndicesCombiner(workSet, icObj):
  workSets = []
  for indicesArray in icObj.allSets(): # implement an iterator with yield in the future
    formingSet = []
    for indiceArray in indicesArray:
      formingSet.append(workSet[indiceArray])
    workSets.append(formingSet)
  return workSets
    
def generateAllCombinationsForWorkDict(workSetAndQuantity):
  workSet = workSetAndQuantity[0]
  quantity = workSetAndQuantity[1]
  if quantity > len(workSet):
    errorMsg = ' generateAllCombinationsForWorkDict(workSetAndQuantity) :: quantity=%d > len(workSet)=%d cannot happen ' %(quantity, len(workSet))
    raise ValueError, errorMsg 
  if quantity == 0:
    return []
  if quantity == 1 and len(workSet) == 1:
    return workSet[:]
  icObj = IndicesCombiner(len(workSet)-1, quantity, False)
  workSets = createWorkSetsWithIndicesCombiner(workSet, icObj)
  return workSets

def doRecursiveSetsCombination(workSetsAndQuantities, allCombinations=[[]]):
  if len(workSetsAndQuantities) == 0:
    return allCombinations
  workSetAndQuantity = workSetsAndQuantities.pop()
  workSets = generateAllCombinationsForWorkDict(workSetAndQuantity)
  newAllCombinations = []
  for workSet in workSets:
    for eachCombination in allCombinations:
      #print 'summing', workSet, eachCombination
      newFormingSet = workSet + eachCombination
      newFormingSet.sort()
      newAllCombinations.append(newFormingSet)
  return doRecursiveSetsCombination(workSetsAndQuantities, newAllCombinations)

def setCombine(workSet, piecesSize):
  indComb = IndicesCombiner(len(workSet)-1,piecesSize,False)
  print indComb
  print indComb.next()
  indexAllSets = indComb.allSets()
  realSets = []
  for indexSet in indexAllSets:
    realSet = []
    for index in indexSet:
      realSet.append(workSet[index])
    realSets.append(realSet)
  print realSets
  return realSets

def setMultiply(combineArray, cadeia=[], collected=[]):
  chunk = combineArray[0]
  if type(chunk) == type([]):
    listElem = list(chunk)
  else:
    listElem = [chunk]
  for elem in listElem:
    #print elem, cadeia, collected
    if len(combineArray) == 1:
      collected.append(list(cadeia)+[elem])
    else:
      nothing = setMultiply(combineArray[1:], list(cadeia)+[elem], collected)
  return collected
  
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

if __name__ == '__main__':
  pass
  '''
  upLimit, size = 12, 3 #pickUpParams()
  print 'upLimit=%d :: size=%d ' %(upLimit, size)
  #ans = raw_input('ok ? ')
  #testIndicesCombiner(upLimit, size)
  #testIndsControl()
  #testShiftLeft(upLimit, size)
  testPrevious(upLimit, size)
  '''
  # testAllSets()
  testPrevious(5, 7)