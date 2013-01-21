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
import random, sys

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

def stuffStrWithZeros(subtokens, size=10):
  newTokens = []
  for token in subtokens:
    tam = len(token)
    toFill = size - tam
    token = token + '0'*toFill
    newTokens.append(token)
    #print token
  return newTokens

def getPermutations(subtokens):
  total = 0; allPerms = []
  for token in subtokens:
    tokenArray = [e for e in token]
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
  '''
  combineNbyC(n, c) is a function that computes the number R of combinations of an n-element set S, c by c elements.
   
  Ex. suppose S = [1,2,3]
  Combinations 2 by 2 of S are [1,2],[1,3] and [2,3]
  Hence, R, the resulting numbers of combinations, is 3.
  
  We can also see combineNbyC(n, c) by its factorial formula, which is n!/((n-c)!c!)
  
  In the simple example above, R = 3!/(2!1!) = 3 x 2 / 2 = 3
  
  In the more computing-intense Megasena example, we have R = combineNbyC(60, 6) = 60! / ((60-6)!6!) = ... =  50,063,860   
  
  The Python code implementation here does not use factorial in order to optimization/minimize computation efforts.
  '''
  if n < 0 or c < 0:
    errorMsg = 'Can not calculate combination with negative numbers (n=%d, c=%d).' %(n,c)
    raise ValueError, errorMsg
  # this condition below may be reformulation to an exception raising in the future (how can one combine more than one has?), for the time being, it's returning 0
  if n < c:
    return 0
  if c == 0:
    if n == 0:
      return 0
    #if n > 0: # no need for an "if" here, n > 0 is logically the condition fell into, if program flow passes by this point 
    return 1  # convention for "produtório", sequence-multiply
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

#passa=0
def generate_integer_partitions(soma, parcel=-1, acc=[]):
  '''
  geraSumComponents(soma, parcel=-1, acc=[]) is an [[[ Integer Partitions generator ]]]
  The name geraSumComponents() was given here before I came across the established term Integer Partitions
  
  Eg.  geraSumComponents(soma=4) results in:
  [[4], [3, 1], [2, 2], [2, 1, 1], [1, 1, 1, 1]]
   
  '''
  #global passa
  #passa += 1
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
    return generate_integer_partitions(soma, parcel-1, acc)
  # dif NOW
  dif = soma - parcel
  if dif == 1:
    acc += [[parcel, 1]]
    #print 'passa', passa, 'REC soma=%d parcel=%d dif=%d acc=%s' %(soma,parcel,dif,str(acc))
    return generate_integer_partitions(soma, parcel-1, acc)

  keptAcc = list(acc)
  newAcc = []
  #print 'passa', passa, 'ATT soma=%d parcel=%d dif=%d acc=%s' %(soma,parcel,dif,str(acc))
  subAcc = generate_integer_partitions(dif, dif, [])
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
    return generate_integer_partitions(soma, parcel-1, acc)
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

'''
===============================================
Below here is code that is somehow not used
===============================================
'''

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

def process():
  is_command_invalid = False
  try:
    if sys.argv[2]=='comb':
      n = int(sys.argv[3])
      c = int(sys.argv[4])
      result = combineNbyC(n, c)
      outdict = {'n':n, 'c':c, 'result':result}
      print 'combineNbyC(%(n)d, %(c)d) =  %(result)d' %outdict 
  except ValueError:
    is_command_invalid = True
  except ValueError:
    is_command_invalid = True
  if is_command_invalid:
    print 'Invalid command'


def adhoc_test1():
  # testAdHocRCombiner():
  rc=RCombiner(3)
  print rc  

def adhoc_test2():
  #def testAdHocRandomPermutation():
  n=9
  perm = range(n+2)
  randomPermutation(perm)
  print perm

def adhoc_test3():
  #def testAdHocPermuteN(arrayN):
  arrayN = range(3) # permutes [0,1,2]
  for i in xrange(3,5):
    arrayN = range(i)
    arr = permute(arrayN);count=0
    for a in arr:
      count+=1
      print count, a

def adhoc_test4():
  #def test_generate_integer_partitions():
  '''
  5 R: [[5], [4, 1], [3, 2], [3, 1, 1], [2, 2, 1], [2, 1, 1, 1], [1, 1, 1, 1, 1]]
  '''
  for soma in range(5,6):
    acc = generate_integer_partitions(soma, soma, [])
    # check it up
    for elem in acc:
      calcSoma = sum(elem)
      if soma <> calcSoma:
        print 'soma <> sum(elem):', soma, calcSoma
    print soma, 'R:', acc

  
def adhoc_tests_show():
  print '''
    algorithmsForCombinatorics.py -t <n>
      Where <n> is
    1 for test1: testAdHocRCombiner()
    2 for test2: testAdHocRandomPermutation()
    3 for test3: testAdHocPermuteN(arrayN=range[3])
    4 for test4: test_generate_integer_partitions()
  '''  

def adhoc_test():
  '''
  '''
  try:
    if sys.argv[2]=='showtests':
      return adhoc_tests_show()
    n_test = int(sys.argv[2])
    print 'Executing test', n_test
    funcname = 'adhoc_test%d()' %n_test
    exec(funcname)
    return
  except ValueError:
    pass
  except IndexError:
    pass
  adhoc_test1()

import unittest
class MyTest(unittest.TestCase):

  def test_1(self):
    pass

def look_up_cli_params_for_tests_or_processing():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()
    elif arg.startswith('-u'):
      # unittest complains if argument is available, so remove it from sys.argv
      del sys.argv[1]
      unittest.main()
    elif arg.startswith('-p'):
      process()

if __name__ == '__main__':
  look_up_cli_params_for_tests_or_processing()
