#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, sys
#import numpy
'''
algo
'''

class Mixer:
  def __init__(self, sumUpTo, expandUpTo):
    self.sumUpTo    = sumUpTo
    self.expandUpTo = expandUpTo
  def process(self):
    elems=[sumUpTo]
  def recur(self, at, runningSet=[]):
    if at==0:
      return
    runningSet.append(at)
    missing=sumUpTo-at
    if missing == 1:
      runningSet.append(1)
      return elem

class NumberSystem:
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

  def next(self):
    if not somaUm(self.values):
      return None
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

def fillArray(elem, combArray):
  combArray[0]=elem
  soma = sum(combArray)
  if soma == upInt:
    return combArray
  
def permute2(array):
  c=0
  #print c, array
  for n in range(len(array)):
    for i in range(len(array)-1):
      tmpElem    = array[i]
      array[i]   = array[i+1]
      array[i+1] = tmpElem
      c+=1
      print c, array

def permute2D(array2D):
  x = array2D[0]
  y = array2D[1]
  if x == y:
    return [array2D]
  return [[x,y],[y,x]]

def permuteN(arrayN):
  if len(arrayN) < 2:
    raise IndexError, 'Array can not be 1D!'
  if len(arrayN) == 2:
    return permute2D(arrayN)
  resultArray = []
  for i in range(len(arrayN)):
    arrayToPrepare = list(arrayN)
    elem = arrayToPrepare[i]
    if i>0 and elem == arrayToPrepare[i-1]:
      continue
    #del arrayToPrepare[i] # now it's one dimension smaller
    # another option: arrayToPrepare = arrayToPrepare[:i] + [i+1:]
    arrayToPrepare = arrayToPrepare[:i] + arrayToPrepare[i+1:]
    subArrays = permuteN(arrayToPrepare) # recursive call
    for subArray in subArrays:
      array = [elem] + subArray
      resultArray.append(array)
  return resultArray

def permute(array):
  origArray = list(array)
  c=0
  #print c, array
  size=len(array)
  for i in range(size-1, 0, -1):
    if i < size:
      array = swap(array, i,i-1)
    c+=1
    print c, array
    tmpElem    = array[i]
    array[i]   = array[i-1]
    array[i-1] = tmpElem
    c+=1
    print c, array
    array = list(origArray)


class RCombiner:
  def __init__(self, aSize, upInt=6):
    self.aSize = aSize
    self.upInt = upInt
  def initCombArray(self):
    combArray = [0] * self.aSize
    fillArray(upInt, combArray)
    
def testC1():
  s='11222'
  arr=2*[1]+3*[2]
  print arr

def expand(n):
  if n - 1 == 1:
    return [1,1]
  for i in range(2,sumUpTo):
    expandArray = expand(i)

def stuffStrWithZeros(subtokens, size=10):
  newTokens = []
  for token in subtokens:
    tam = len(token)
    toFill = size - tam
    token = token + '0'*toFill
    newTokens.append(token)
    #print token
  return newTokens

def strToList(s):
  lista = []
  for c in s:
    lista.append(c)
  return lista

def sumComponentsToListOfStrs(intLists):
  outList = []
  for elem in intLists:
    strList = map(str, elem)
    outList.append(''.join(strList))
  return outList

def testSumComponentsGerador():
  subtokensHandMade=['6','51','42','411','33','321','3111',\
    '222','2211','21111','111111']
  subtokens = geraSumComponents(6)
  subtokens = sumComponentsToListOfStrs(subtokens)
  #print 'subtokensHandMade', subtokensHandMade
  #print 'subtokens', subtokens
  #print 'subtokensHandMade == subtokens', subtokensHandMade == subtokens

def getTilPatternsFor(patternSize=10, patternSoma=6):
  #array = range(1,4)
  #wordForArray = 'xyyzzzzzzz'
  subtokens = geraSumComponents(6)
  subtokens = sumComponentsToListOfStrs(subtokens)
  subtokens = stuffStrWithZeros(subtokens, patternSize)
  #print subtokens
  #wordForArray = '222000000'
  #sys.exit(0)
  return getPermutations(subtokens)

def getPermutations(subtokens):
  total = 0; allPerms = []
  for token in subtokens:
    tokenArray = strToList(token)
    oa = permuteN(tokenArray)
    oa.sort()
    previousWord = ''
    for oInt in oa:
      oStr = map(str, oInt)
      word = ''.join(oStr)
      allPerms.append(word)
      #print word,
      if previousWord == word:
        # should be an error if it happens
        print ' ================ '
        raise ValueError, 'previousWord == word'
      else:
        pass
        #print
      previousWord = word
    subtotal = len(oa)
    total += subtotal
    #print subtotal
  #print 'total', total
  return allPerms

passa=0
def geraSumComponents(soma, parcel=-1, acc=[]):
  global passa
  passa += 1
  if soma == 1:
    acc += [[1]]
    #dif=-1
    #print 'passa', passa, 'RET parcel,soma,acc', parcel, soma, acc
    return acc
  if parcel == 1:
    acc += [[1]*soma]
    #dif=-1
    #print 'passa', passa, 'RET parcel,soma,acc', parcel, soma, acc
    return acc
  # case where caller leaves 'parcel' to its initial supposed condition, ie, it's equal to 'soma'
  if parcel == -1:
    parcel = soma
  if parcel == soma:
    acc += [[parcel]]
    #dif=-1
    #print 'passa', passa, 'REC soma=%d parcel=%d dif=%d acc=%s' %(soma,parcel,dif,str(acc))
    return geraSumComponents(soma, parcel-1, acc)
  # dif NOW
  dif = soma - parcel
  if dif == 1:
    acc += [[parcel, 1]]
    #print 'passa', passa, 'REC soma=%d parcel=%d dif=%d acc=%s' %(soma,parcel,dif,str(acc))
    return geraSumComponents(soma, parcel-1, acc)

  keptAcc = list(acc)
  newAcc = []
  #print 'passa', passa, 'ATT soma=%d parcel=%d dif=%d acc=%s' %(soma,parcel,dif,str(acc))
  subAcc = geraSumComponents(dif, dif, [])
  for sub in subAcc:
    # well, the 'if' below was a tough decision to correct a repeat
    # eg. gera(5) was having [3,2] and [2,3]
    if parcel < sub[0]:
      continue
    #print 'adding', parcel, 'to', sub,
    sublista = [parcel] + sub
    #print '=', sublista
    newAcc.append(sublista)
  keptAcc += newAcc
  acc = keptAcc
  if parcel > 1:
    #print 'passa', passa, 'REC soma=%d parcel=%d dif=%d acc=%s' %(soma,parcel,dif,str(acc))
    return geraSumComponents(soma, parcel-1, acc)
    #print 'passa', passa, 'RF  soma=%d parcel=%d dif=%d acc=%s' %(soma,parcel,dif,str(acc))
  return acc


class TillPatternVector(object):
  '''
  This class is a helper around Til Patterns.
  
  Objects can be created two ways:
  
  1) without the 'wordPattern' parameter
  2) with the 'wordPattern' parameter
  
  
  1) without the 'wordPattern' parameter

    Eg.
    1.1) 1233 has 12 permutions
    1.2) the complete set of til pattern for patternSize=10 and soma=6
         is 5005
    
  2) with the 'wordPattern' parameter
  
    Eg. 'xyyzzzzzzz' ie 1 x, 2 y's and 7 z's
    2.1) This is the same as 1223333333 or 0112222222
    2.2) It has 360 permutations
  
  '''

  def __init__(self, patternSize, soma, wordPattern=None):
    self.wordPattern = wordPattern
    if wordPattern == None:
      self.patternSize = patternSize
      self.soma   = soma
      self.vector = None
      self.initVector()
      return
    # second case, a initialPattern was entered
    if type(wordPattern) == list:
      if len(wordPattern) > 0:
        wordPattern = wordPattern[0]
    if type(wordPattern) <> str:
        errorMsg = 'wordPattern should be a str <> ' + str(wordPattern)
        raise ValueError, errorMsg
    if len(wordPattern) == 0:
      errorMsg = 'wordPattern is empty. It should have at least one char'
      raise ValueError, errorMsg
    chrDict = {}
    for c in wordPattern:
      chrDict[c]=1
    self.soma = sum(range(len(chrDict)))
    self.patternSize = len(wordPattern)
    listPattern = [wordPattern]
    self.vector = getPermutations(listPattern)

  def initVector(self):
    self.vector = getTilPatternsFor(self.patternSize, self.soma)
  
  def getVectorSize(self):
    if self.vector:
      return len(self.vector)
    return 0
  
  def __str__(self):
    outStr = 'TillPatternVector(patternSize=%d soma=%d vectorSize=%d)' %(self.patternSize, self.soma, self.getVectorSize())
    if self.wordPattern:
      outStr += ' wordPattern=%s' %(self.wordPattern)
    return outStr

def testGeraSumComponents():
  for soma in range(5,6):
    acc = geraSumComponents(soma, soma, [])
    # check it up
    for elem in acc:
      calcSoma = sum(elem)
      if soma <> calcSoma:
        print 'soma <> sum(elem):', soma, calcSoma
    print soma, 'R:', acc
   
if __name__ == '__main__':
  pass
  tpVector = TillPatternVector(10,6)
  print 'tpVector', tpVector
  tpVector = TillPatternVector(10,3)
  print 'tpVector', tpVector

  '''

  perms = getTilPatternsFor(10,3)
  print perms, len(perms)

  print 'def getPermutations(subtokens):'
  vect = ['xyyzzzzzzz']
  perms = getPermutations(vect)
  print perms, len(perms)

  tpVector = TillPatternVector(-1,-1,vect)
  print tpVector


  #intsToSum(soma=6)
  #testGeraSumComponents()


  perms = getTilPatternsFor()
  print perms, len(perms)

  testSumComponentsGerador()
  print time.ctime()
  prepForPermuteN()
  print time.ctime()

  #expand()
  #testRemaindersComb()
  #testC1()
  #array = [1,2,3,4,5]
  #array = ['a','b','c','d','e']
  '''