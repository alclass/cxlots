#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import sys

SUBINDO  = 2
DESCENDO = 1
import IndicesCombiner as comb # for the comb(n, m) function
#import lambdas

counter = 0 # global
def checkUpAmountInArrayCarried(carriedArray, lgi):
  size = len(carriedArray); soma = 0
  for i in range(size):
    value = carriedArray[i]
    posInv = size - i
    soma += comb.comb(value, posInv)
  if soma <> lgi:
    msg = 'checkUpAmountInCarriedArray() ==>> soma (=%d) não igual a lgi (=%d) %s' %(soma, lgi, str(carriedArray))
    raise ValueError, msg
  #print 'checkUpAmountInCarriedArray() ==>> soma (=%d) igual a lgi (=%d)' %(soma, lgi)

def transformCombInLgi(combArray, nOfElems):
  lc = LgiCombiner(nOfElems-1,-1,combArray)
  return lc.getLgi()

def transformLgiInComb(nOfElems, size, lgi):
  lc = LgiCombiner(nOfElems-1,size)
  return lc.moveTo(lgi)

class LgiCombiner(object):
  '''

  LGI = LexicoGraphical Index
  From the Combinadics Theory


  Interface:

  first() ==>> sets combination to the first one and returns it
  last() ==>> sets combination to the last one and returns it
  next(jump=1) ==>> moves to the next 'jump' combinations ahead
  previous(jump=1) ==>> moves to the previous 'jump' combinations behind
  moveTo(lgi=0) ==>> moves to the combination corresponding to the LG Index 'lgi'
  lgiOf() ==>> returns the LG Index of the current combination
  setComb(array=[n-1,n-2,...,2,1,0])  ==>> sets the current combination to the one passed-in
  currentInAscendingOrder() ==> gets the current combination in Ascending/Crescent Order


  This class can be used as a combinadics functions, ie:

  f(lgi,ic(n,m)) = [comb]

  where:
    lgi is the LexicoGraphic Index
    ic(n,m) is the IndicesCombinerLgi object, n is number of elements, m is array size

  Eg. ==>> f(31029, ic(60,6)) = [19,15,13,11,5,4]
  because
    c(19,6)+c(15,5)+c(13,4)+c(11,3)+c(5,2)+c(4,1) = 31029

  It also finds the other way around, ie:
  fInv([19,15,13,11,5,4]) = 31029

  Operationally, the movesTo() is the first (direct) function, the getLgi() is the second (inverse) function

  Steps for that example:

  obj = IndicesCombinerLgi(59,6)
  obj.movesTo(31029) results in positioning iArray to [19,15,13,11,5,4] and returning it
  obj.getLgi() after that results in 31029

  To use getLgi giving an array, it can be done by instantiating the object with the array, ie:
  obj = IndicesCombinerLgi(59,6,[19,15,13,11,5,4])
  Then, obj.getLgi() will return the lgi for that array (ie, 31029)


  This class can also be explained by examples
  ============================================

  Example 1:
  indComb = IndicesCombiner(5, 3)
  indComb.first() results [2, 1, 0]
  indComb.firstGiven() in this case also results [2, 1, 0]
  aplying indComb.next() each time:
  [2, 1, 0]   [3, 1, 0]   [3, 2, 0]   [3, 2, 1]   [4, 2, 1]
  [4, 3, 1]   [4, 3, 2]   [5, 3, 2]   [5, 4, 2]
   ... the last one is [5, 4, 3]
  if a new indComb.next() is applied, None is returned

  The behavior expected is that of a Combination
  Mathematically, the total of produced arrays is:
    Combination(5,3) = 5! / ((5-3)!3!)

  (*) firstGiven() explanation
  when iArrayIn is passed with a consistent array
  firstGiven() returns that array



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
    File "./comb.py", line 237, in <module>
      testIndicesCombiner(upLimit, size)
    File "./comb.py", line 189, in testIndicesCombiner
      indComb = IndicesCombiner(upLimit, size, False); c=0
    File "./comb.py", line 80, in __init__
      raise ValueError, msg
  ValueError: Inconsistent IndicesCombiner upLimit(=1) must be at least size(=4) - 1 when overlap=False

  '''

  def __init__(self, upLimit=0, size=1, iArrayIn=[0]):
    if size < 1:
      size = 1
    if upLimit < 0:
      upLimit = 0
    self.upLimit = upLimit
    # yet to be checked True
    self.stillFirst  = False
    if iArrayIn == [0] and size > 1:
      self.iArray = range(size-1, -1, -1)
      self.stillFirst  = True
    else:
      self.iArray      = list(iArrayIn)
      if self.iArray == range(size-1, -1, -1):
        self.stillFirst  = True
    self.size        = len(self.iArray)
    self.checkArrayConsistency()
    self.nOfCombines = comb.comb(self.upLimit+1, self.size)
    self.iArrayGiven = list(self.iArray)

  def checkArrayConsistency(self):
    '''
    Checks the consistency of iArray
    Examples of inconsistent arrays:
    valid ==>> [2,1,0], [100,1,0]
    invalid ==>> [0,0,0], [3,2,2]
    '''
    for i in range(self.size-1):
      if self.iArray[i] <= self.iArray[i+1]:
        msg = 'Inconsistent array: next elem can not be greater or equal to a previous one %s' %(str(self.iArray))
        raise ValueError, msg

  def outputIArray(self, sortIt, isZeroless):
    iArray = list(self.iArray) # hard copy
    if sortIt:
      iArray.sort()
    if isZeroless:
      iArray = map(lambdas.plusOne, iArray)
    return iArray

  def current(self, sortIt=True, isZeroless=True):
    '''
    Returns the current iArray
    Notice that iArray is modified by methods like next() and first()
    '''
    return self.outputIArray(sortIt, isZeroless)

  def getLgi(self):
    lgi = 0
    for i in range(self.size):
      value =  self.iArray[i]
      posInv = self.size - i
      lgi += comb.comb(value, posInv)
    return lgi

  def first(self, sortIt=True, isZeroless=True):
    '''
    Moves the iArray to the top and returns it
    Eg
    overlap=True,  size=3 :: [0,0,0]
    overlap=False, size=4 :: [0,1,2,3]
    '''
    self.iArray = range(self.size-1,-1,-1)
    return self.outputIArray(sortIt, isZeroless)

  def firstGiven(self):
    '''
    Returns the firstGiven or restartAt array but does not change current position
    To change it, use positionToFirstGiven()
    '''
    return list(self.iArrayGiven) # output a hard-copy of it so that it (the reference) is not changed outside

  def positionToFirstGiven(self):
    '''
    Returns the firstGiven/restartAt array changing current position to it
    @see also firstGiven()
    '''
    self.iArray = list(self.iArrayGiven)

  def last(self, sortIt=True, isZeroless=True):
    '''
    Moves iArray position to the last one and returns it
    Eg
    size=4, upLimit=33 :: [33,32,31,30]
    '''
    for i in range(self.size):
      self.iArray[i] =  self.upLimit - i
    return self.outputIArray(sortIt, isZeroless)

  def moveTo(self, lgi=0, sortIt=True, isZeroless=True):
    if lgi<=0:
      if lgi==0:
        return self.first()
      return None
    maxIndex = self.nOfCombines - 1
    # print 'maxIndex', maxIndex
    if lgi >= maxIndex:
      if lgi==maxIndex:
        return self.last()
      return None
    # initializing arrayCarried
    arrayCarried = [-1] * self.size
    for pos in range(self.size):
      arrayCarried[pos] = self.size - pos - 1
    # if it got here, there are at least 3 elements, hence there's a midpoint
    pointInf = self.size - 1 - 0
    pointSup = self.upLimit
    pos      = 0
    self.iArray = self.approach(lgi, pointInf, pointSup, pos, arrayCarried)
    return self.outputIArray(sortIt, isZeroless)

  def approach(self, lgi, pointInf, pointSup, pos, arrayCarried, amount=0):
    global counter
    if pos == self.size:
      msg = 'Well, failed to get the LG Index. Reason: pos surpasses all available slots. (pos=%d, size=%d, pointInf=%d, pointSup=%d)' %(pos, self.size, pointInf, pointSup)
      print msg
      sys.exit(0)
      #raise ValueError, msg
    pointMid = pointInf + (pointSup - pointInf) / 2
    posInv = self.size - pos
    parcel = comb.comb(pointMid, posInv)
    amountCompare = amount + parcel

    parcelSup = comb.comb(pointSup, posInv)
    amountCompareSup = amount + parcelSup

    parcelInf = comb.comb(pointInf, posInv)
    amountCompareInf = amount + parcelInf

    #msg = 'i=%d inf=%d/%d mid=%d/%d sup=%d/%d pos=%d %s press [ENTER]' %(lgi, pointInf, amountCompareInf, pointMid, amountCompare, pointSup, amountCompareSup, pos, str(arrayCarried))
    #ans=raw_input(msg)
    #counter+=1 # global
    #print counter, msg
    if amountCompareSup < lgi:
      amount += parcelSup
      arrayCarried[pos] = pointSup
      pos += 1
      # renew pointInf and pointSup
      pointInf = self.size - 1 - pos
      pointSup = pointSup - 1 # limiteSup
      return self.approach(lgi, pointInf, pointSup, pos, arrayCarried, amount)

    if amountCompareSup == lgi: # ok, game over
      arrayCarried[pos] = pointSup
      # check for consistency
      checkUpAmountInArrayCarried(arrayCarried, lgi)
      return arrayCarried

    if amountCompare > lgi:
      # the following check avoids an infinite recursion and logically complements the desired functionality
      if pointMid >= pointSup-1 and parcelInf < lgi:
        amount += parcelInf
        arrayCarried[pos] = pointInf
        pos += 1
        # renew pointInf and pointSup
        pointSup = pointInf - 1 # limiteSup
        pointInf = self.size - 1 - pos
        return self.approach(lgi, pointInf, pointSup, pos, arrayCarried, amount)
      pointSup = pointMid
      return self.approach(lgi, pointInf, pointSup, pos, arrayCarried, amount)
    elif amountCompare < lgi:
      if pointMid >= pointSup - 1:
        if amountCompareSup < lgi:
          amount += parcelSup
          arrayCarried[pos] = pointSup
          pointSup = pointSup - 1 # limiteSup
        else:
          amount += parcel
          arrayCarried[pos] = pointMid
          pointSup = pointMid - 1 # limiteSup
        pos += 1
        # renew pointInf and pointSup
        pointInf = self.size - 1 - pos
        return self.approach(lgi, pointInf, pointSup, pos, arrayCarried, amount)
      pointInf = pointMid
      # pointSup is the same
      return self.approach(lgi, pointInf, pointSup, pos, arrayCarried, amount)
    else:  # ie, amountCompare == lgi ie, element has just been FOUND!
      arrayCarried[pos] = pointMid
      # check for consistency
      checkUpAmountInArrayCarried(arrayCarried, lgi)
      return arrayCarried

  def previous2(self):
    '''
    Moves iArray to the its previous consistent position and returns the array
    When the first one is current, None will be returned
    '''
    pos = self.size - 1
    if self.overlap:
      return self.minusOneOverlap(pos)
    else:
      return self.minusOneNonOverlap(pos)

  def ajustToTheRight(self, pos):
    for i in range(pos, self.size-1):
      self.iArray[i+1] = self.iArray[i]-1
    self.checkArrayConsistency()

  def subtractOne(self, pos=-1):
    if pos==-1:
      pos = self.size - 1
    leastAllowed = self.size - pos - 1
    if pos == 0:
      if self.iArray[0] == leastAllowed:
        return None
      self.iArray[0] -= 1
      self.ajustToTheRight(0)
      return 1 # self.iArray
    if self.iArray[pos] == leastAllowed:
      return self.subtractOne(pos-1)
    self.iArray[pos]-=1
    self.ajustToTheRight(pos)
    return 1 # self.iArray

  def addOne(self, pos=-1):
    '''
    This method can not be called from outside of the class
    More than that, only next() can call it, otherwise, inconsistencies may arise
    ie, the method should also have its first go with pos=-1
    '''
    if pos == 0:
      if self.iArray[0] == self.upLimit:
        #print 'self.iArray', self.iArray
        self.ajustToTheRight(0)
        return None
      self.iArray[0] += 1
      return 1  #self.iArray
    if pos==-1:
      pos = self.size - 1
    if self.iArray[pos]+1 == self.iArray[pos-1]:
      leastAllowed = self.size - pos - 1
      self.iArray[pos] = leastAllowed
      return self.addOne(pos-1)
    self.iArray[pos] += 1
    return 1 # self.iArray

  def next(self, quant=1, sortIt=True, isZeroless=True):
    '''
    Moves iArray position to the next consistent one and returns it
    When the last one is current, None will be returned
    '''

    if self.stillFirst:
      if quant == 1:
        # control flow is supposed to pass in here only once
        self.stillFirst = False
        return self.first(sortIt, isZeroless)
      elif quant > 1:
        quant -= 1
      # if quant > 1 or quant <> 1, next line will be executed
      self.stillFirst = False

    retVal = None
    for i in range(quant):
      retVal = self.addOne()
    # notice that self.iArray is never None, but (local) iArray can be None
    if not retVal:
      return None
    return self.outputIArray(sortIt, isZeroless)

  def __getitem__(self, itemIndex):
    '''
    itemIndex may either be an int or a slice
    logic should be implemented
    if type(itemIndex) == type(int):
      ok, do one
    if type(itemIndex) == type(int):
      think how to solve this, the slice has 3 params (x,y,z)
      like the range() params

    print 'itemIndex', itemIndex, type(itemIndex)
    if type(itemIndex) == slice:
      print repr(slice)
    '''
    return self.next()  # all defaults = 1, True, True

  def previous(self, quant=1, sortIt=True, isZeroless=True):
    '''
    Moves iArray position to the previous consistent one and returns it
    When the first one is current, None will be returned
    '''
    retVal = None
    for i in range(quant):
      retVal = self.subtractOne()
    if not retVal:
      return None
    return self.outputIArray(sortIt, isZeroless)

  def __str__(self):
    '''
    The string representation of the class
    '''
    outStr = 'array=%s upLimit=%d' %(str(self.iArray), self.upLimit)
    return outStr


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
  ic = IndicesCombinerLgi(upLimit, size)
  print 'ic', ic
  print 'ic.next()', ic.next()
  print 'ic.previous()', ic.previous()
  for i in range(36):
    print i,'ic.next()', ic.next()
  for i in range(36):
    print i,'ic.previous()', ic.previous()

def testGetByLgi(upLimit, size):
  ic = LgiCombiner(upLimit, size)
  print 'ic', ic
  print 'ic.next()', ic.next()
  print 'ic.previous()', ic.previous()
  nOfComb = ic.nOfCombines
  #sys.exit(0)
  lgi = random.randint(0,nOfComb-1)
  msg = 'ic.moveTo(lgi=%d)' %(lgi)
  #ans=raw_input(msg)
  #lgi = 31029 #21208
  #print 'ic.moveTo(lgi=%d)' %(lgi), ic.moveTo(lgi)
  for i in range(3):
    lgi = random.randint(0,nOfComb-1)
    ic.moveTo(lgi)
    array = ic.currentSorted()
    array1 = ic.currentSortedFrom1()
    print i, 'ic.moveTo(lgi=%d)' %(lgi), array, array1, 'lgi', ic.getLgi()

def testTransforms():
  combArray = [14,10,5,1]; nOfElems = 20
  lgi = transformCombInLgi(combArray, nOfElems)
  print 'lgi = transformCombInLgi(combArray, nOfElems)', combArray, nOfElems, 'lgi', lgi
  nOfElems = 20; size = 4; lgi = 7
  combArray = transformLgiInComb(nOfElems, size, lgi)
  print 'comb = transformLgiInComb(nOfElems, size, lgi)', nOfElems, size, lgi, 'comb', combArray

def testGetItem():
  lgiObj = LgiCombiner(59, 6)
  c=0
  for lgi in lgiObj:
    print lgi
    c+=1
    if c>7:
      break

if __name__ == '__main__':
  pass
  testGetItem()
  '''
  lgiObj = LgiCombiner(59, 6)
  print lgiObj
  print lgiObj.current(), lgiObj.getLgi()
  print lgiObj.next(), lgiObj.getLgi()
  print lgiObj.moveTo(100), lgiObj.getLgi()
  print lgiObj.last(), lgiObj.getLgi()
  print 'comb.comb(60,6)', comb.comb(60,6)

  nOfElems = 60
  upLimit, size = nOfElems-1, 6 #pickUpParams()
  print 'upLimit=%d :: size=%d ' %(upLimit, size)
  #ans = raw_input('ok ? ')
  #testIndicesCombiner(upLimit, size)
  #testIndsControl()
  #testShiftLeft(upLimit, size)
  #testPrevious(upLimit, size)
  #testGetByLgi(upLimit, size)
  testTransforms()
  '''