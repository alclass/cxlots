#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
algorithmsForPermutationEtAl.py


Main functions here:

-- permute(arrayN)
-- geraSumComponents(soma, parcel=-1, acc=[])
   Generates Integer Partitions (look for further explanation on the comments at the beginning of the function below) 
-- getTilPatternsFor(patternSize=10, patternSoma=6)
   Uses geraSumComponents(patternSoma) then it stuffs zeroes and filters out larger strings than patternSize) 

'''
# import numpy, time, sys
import random

def permute2D(array2D):
  '''
  This function is called by permuteN(arrayN)
  It swaps x and y in a 2D-array 
  Eg permute2D([1,2]) results in [[1, 2], [2, 1]]
  '''
  x = array2D[0]
  y = array2D[1]
  if x == y:
    return [array2D]
  return [[x,y],[y,x]]

# print permute2D([1,2])

def permute(arrayN):
  '''
  This function does Permutations.  A n-size set generates n! (n factorial) permutations
  permute() does its job recursively is n > 2, ie it diminished n by 1 and recurse until it gets the 2-element swap calling permute2D

  Eg.
  permuteN( range(3) ) results in:
  1 [0, 1, 2]
  2 [0, 2, 1]
  3 [1, 0, 2]
  4 [1, 2, 0]
  5 [2, 0, 1]
  6 [2, 1, 0]  
  '''
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
    subArrays = permute(arrayToPrepare) # recursive call
    for subArray in subArrays:
      array = [elem] + subArray
      resultArray.append(array)
  return resultArray

def testAdHocPermuteN(arrayN):
  arr = permute(arrayN);count=0
  for a in arr:
    count+=1
    print count, a
#testAdHocPermuteN(range(3))    

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

def testAdHocSumComponentsGerador():
  subtokensHandMade=['6','51','42','411','33','321','3111',\
    '222','2211','21111','111111']
  subtokens = geraSumComponents(6)
  subtokens = sumComponentsToListOfStrs(subtokens)
  print 'subtokensHandMade', subtokensHandMade
  print 'subtokens', subtokens
  print 'subtokensHandMade == subtokens', subtokensHandMade == subtokens

def getPermutations(subtokens):
  total = 0; allPerms = []
  for token in subtokens:
    tokenArray = strToList(token)
    oa = permute(tokenArray)
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

def combineNbyC(n, c):
  if n < 0 or c < 0:
    errorMsg = 'Can not calculate combination with negative numbers (n=%d, c=%d).' %(n,c)
    raise ValueError, errorMsg
  if n < c:
    return 0
  if n == 0 or c == 0:
    return 0
  if n == c:
    return 1
  mult = 1
  nOrig = n
  while n > nOrig - c:
    mult *= n
    n -= 1
  while c > 1:
    mult = mult / (0.0 + c)
    c -= 1
  return int(mult)

def randomPermutation(perm):
  n = len(perm)
  for i in range(1, n+1):
    perm[i]=i
  for i in range(1, n+1):
    j = i + random.randint(1, n+1) * (n + 1 - i)
    k = perm[i]
    perm[j] = k

def testAdHocRandomPermutation():
  n=9
  perm = range(n+2)
  randomPermutation(perm)
  print perm
# testAdHocRandomPerm

passa=0
def geraSumComponents(soma, parcel=-1, acc=[]):
  '''
  geraSumComponents(soma, parcel=-1, acc=[]) is an [[[ Integer Partitions generator ]]]
  The name geraSumComponents() was given here before I came across the established term Integer Partitions
  
  Eg.  geraSumComponents(soma=4) results in:
  [[4], [3, 1], [2, 2], [2, 1, 1], [1, 1, 1, 1]]
   
  '''
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

# test adhoc
# print geraSumComponents(4)

def filterOutStringsGreaterThanSize(words, size):
  filteredStrList = []
  for word in words:
    if len(word) <= size:
      filteredStrList.append(word)
  return filteredStrList


def testAdHocGetTilPatternsFor(patternSize=2, patternSoma=3):
  patterns=getTilPatternsFor(patternSize, patternSoma);count=0
  for pattern in patterns:
    count+=1
    print pattern,
#testAdHocGetTilPatternsFor()
#testAdHocGetTilPatternsFor(patternSize=5, patternSoma=6)

def testGeraSumComponents():
  '''
  5 R: [[5], [4, 1], [3, 2], [3, 1, 1], [2, 2, 1], [2, 1, 1, 1], [1, 1, 1, 1, 1]]
  '''
  for soma in range(5,6):
    acc = geraSumComponents(soma, soma, [])
    # check it up
    for elem in acc:
      calcSoma = sum(elem)
      if soma <> calcSoma:
        print 'soma <> sum(elem):', soma, calcSoma
    print soma, 'R:', acc
# testGeraSumComponents()   


'''
===============================================
Below here is code that is somehow not used
===============================================
'''

def permute2(array):
  '''
  This function does not work as it should (it is kept here for later study -- IT'S NOT IN USE anyway, the one IN USE is PermuteN() here)
  This function only does "half-way". Eg.permute2(range(4)) results "incorrectly" in 12 combinations, instead of the 4!=24 combinations 
  '''
  c=0
  #print c, array
  for n in range(len(array)):
    for i in range(len(array)-1):
      tmpElem    = array[i]
      array[i]   = array[i+1]
      array[i+1] = tmpElem
      c+=1
      print c, array
#permute2(range(4))

def fillArray(elem, combArray, upInt):
  '''
  called by method initCombArray in class RCombiner
  '''
  combArray[0]=elem
  soma = sum(combArray)
  if soma == upInt:
    return combArray
  return None

class RCombiner:
  def __init__(self, aSize, upInt=6):
    self.aSize = aSize
    self.upInt = upInt
    self.initCombArray()
  def initCombArray(self):
    self.combArray = [0] * self.aSize
    self.combArray = fillArray(self.aSize, self.combArray, self.upInt, )
  def __str__(self):
    outStr = 'size=%d upInt=%d combArray=%s' %(self.aSize, self.upInt, str(self.combArray))
    return outStr 

def testAdHocRCombiner():
  rc=RCombiner(3)
  print rc  

'''
def testC1():
  s='11222'
  arr=2*[1]+3*[2]
  print arr

def expand(n):
  if n - 1 == 1:
    return [1,1]
  for i in range(2,sumUpTo):
    expandArray = expand(i)
'''
  
  
if __name__ == '__main__':
  pass
  
