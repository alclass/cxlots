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

def getTilPatternsFor(patternSize=10, patternSoma=6):
  '''
  The Til Patterns are found with the help of finding first the "Integer Partitions"
  Once having found the "Integer Partitions", two operations are called, ie:
  1) stuff the patterns with less than patternSize with 0 (zeros)
  2) those patterns that are greater in size than patternSize are filtered out
  The result set corresponds to the wanted Til Patterns
  
  Eg.
  eg1 getTilPatternsFor(patternSize=2, patternSoma=3) results in a 7-element array, ie:
  ----------------------------  
  06  60  15  51  24  42  33
  ----------------------------  
  
  eg1 getTilPatternsFor(patternSize=5, patternSoma=6) results in a 210-element array, ie:
  ----------------------------  
  00006 00060 00600 06000 60000 00015 00051 00105 00150 00501 00510 01005 01050 01500 05001
  05010 05100 10005 10050 10500 15000 50001 50010 50100 51000 00024 00042 00204 00240 00402
  00420 02004 02040 02400 04002 04020 04200 20004 20040 20400 24000 40002 40020 40200 42000
  00114 00141 00411 01014 01041 01104 01140 01401 01410 04011 04101 04110 10014 10041 10104
  10140 10401 10410 11004 11040 11400 14001 14010 14100 40011 40101 40110 41001 41010 41100
  00033 00303 00330 03003 03030 03300 30003 30030 30300 33000 00123 00132 00213 00231 00312
  00321 01023 01032 01203 01230 01302 01320 02013 02031 02103 02130 02301 02310 03012 03021
  03102 03120 03201 03210 10023 10032 10203 10230 10302 10320 12003 12030 12300 13002 13020
  13200 20013 20031 20103 20130 20301 20310 21003 21030 21300 23001 23010 23100 30012 30021
  30102 30120 30201 30210 31002 31020 31200 32001 32010 32100 01113 01131 01311 03111 10113
  10131 10311 11013 11031 11103 11130 11301 11310 13011 13101 13110 30111 31011 31101 31110
  00222 02022 02202 02220 20022 20202 20220 22002 22020 22200 01122 01212 01221 02112 02121
  02211 10122 10212 10221 11022 11202 11220 12012 12021 12102 12120 12201 12210 20112 20121
  20211 21012 21021 21102 21120 21201 21210 22011 22101 22110 11112 11121 11211 12111 21111
  ----------------------------  
  
  '''
  subtokens = geraSumComponents(6)
  subtokens = sumComponentsToListOfStrs(subtokens)
  subtokens = stuffStrWithZeros(subtokens, patternSize)
  subtokens = filterOutStringsGreaterThanSize(subtokens, patternSize)
  return getPermutations(subtokens)

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
   
if __name__ == '__main__':
  pass


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