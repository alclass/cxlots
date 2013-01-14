#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
SetsCombiner
'''
import sys

import __init__
__init__.setlocalpythonpath()

# from lib import lambdas
from IndicesCombiner import IndicesCombiner
import algorithmsForCombinatorics as afc


class WorkSet(object):
  '''
  The purpose of this class is to generate all combinations n by c of an n-element "workSet" combined c by c, where 0 < c <= n
  
  Each combination is "yielded" from each call to method next(). After the last combination, None is returned.
  
  The combination is done, under the hoods, by the IndicesCombiner attribute.  This happens in the line:
    combined_set = [self.workSet[i] for i in indices]
    
  Eg.

  The code fragment
  
  s = ['a','b','c']; combsize = 2
  ws = WorkSet(s, IndicesCombiner( len(s)-1, combsize, False))
  comb = ws.next()
  while comb:
    print comb
    comb = ws.next()
  
  Results in
    ['a', 'b']
    ['a', 'c']
    ['b', 'c']

  The IndicesCombiner generated the indices for s's subsets: 0,1; 0,2; and 1,2 
  '''

  def __init__(self, workSet, indicesCombiner):
    self.workSet = workSet
    self.total_combinations = None
    self.indicesCombiner = indicesCombiner
    self.restart()

  def restart(self):
    self.do_restart = True
    
  def get_total_combinations(self):
    '''
    total_combinations is a combination n by c, the same that is known by n!((n-c)!c!)
    where n is workSet's size and c is IndicesCombiner's quantity 
    '''
    if self.total_combinations != None:
      return self.total_combinations
    n = len(self.workSet)
    c = self.indicesCombiner.size
    self.total_combinations = afc.combineNbyC(n, c)
    return self.total_combinations

  def next(self):
    '''
    next_combination
    '''
    if self.do_restart:
      indices = self.indicesCombiner.first()
      self.do_restart = False
    else:
      indices = self.indicesCombiner.next()
    if indices == None:
      return None
    combined_set = [self.workSet[i] for i in indices]
    return combined_set

class SetsCombiner(object):
  '''
  This class works under a 2-way process:
  1) First, one or more of workSetWithQuantity tuples should be added to the object
  2) when all workSetWithQuantity tuples have been added to, calls to method next_combination() will "yield" one combination at a time, until None
  
  Eg.
  # ===========================================
  sc = SetsCombiner()
  workSetWithQuantity = ([1,2,3],2)
  sc.addSetWithQuantities(workSetWithQuantity)
  workSetWithQuantity = ([4,5],2)
  sc.addSetWithQuantities(workSetWithQuantity)
  workSetWithQuantity = ([6,7,8,9],3)
  sc.addSetWithQuantities(workSetWithQuantity)
  c=0
  for each in sc.next_combination():
    c+=1
    print c,'combination', each
  # ===========================================
  (( This piece of code results in: ))

  1 combination [1, 2, 4, 5, 6, 7, 8]
  2 combination [1, 2, 4, 5, 6, 7, 9]
  3 combination [1, 2, 4, 5, 6, 8, 9]
  4 combination [1, 2, 4, 5, 7, 8, 9]
  5 combination [1, 3, 4, 5, 6, 7, 8]
  6 combination [1, 3, 4, 5, 6, 7, 9]
  7 combination [1, 3, 4, 5, 6, 8, 9]
  8 combination [1, 3, 4, 5, 7, 8, 9]
  9 combination [2, 3, 4, 5, 6, 7, 8]
  10 combination [2, 3, 4, 5, 6, 7, 9]
  11 combination [2, 3, 4, 5, 6, 8, 9]
  12 combination [2, 3, 4, 5, 7, 8, 9]
  
  (( Individually, each workSet yields the sets below: ))
  
  workSetWithQuantity = ([1,2,3],2) yields
  [1, 2]
  [1, 3]
  [2, 3]
  ------------------------------
  workSetWithQuantity = ([4,5],2) yields
  [4, 5]
  ------------------------------
  workSetWithQuantity = ([6,7,8,9],3) yields
  [6, 7, 8]
  [6, 7, 9]
  [6, 8, 9]
  [7, 8, 9]

  The 3 cross-combined results in 12 sets (3*1*4=12)
  '''
  def __init__(self):
    self.workSetObjs = []
    # after the first call to method combine(), object must not add workSets anymore
    self.lock_workSets_insertion = False
    self.LAST_INDEX = None
    self.total_combinations = None

  def instantiateIndicesCombiner(self, workSet, quantity):
    indicesCombiner_upLimit = len(workSet) - 1  # ie, index of last element
    indicesCombiner_size = quantity  
    indicesCombiner_mode = False
    indicesCombiner = IndicesCombiner(indicesCombiner_upLimit, indicesCombiner_size, indicesCombiner_mode)
    return indicesCombiner 

  def isWorkSetWithQuantityValid(self, workSetWithQuantity):
    workSet = workSetWithQuantity[0]
    # workSet should not be empty, if it is, consider data invalid returning False 
    if len(workSet) == 0:
      return False
    quantity = workSetWithQuantity[1]
    # quantity must be greater than 0, however, if it is less than 1, just return, no exception raising for this case
    if quantity < 1 or quantity > len(workSet):
      return False
    return True

  def addSetWithQuantities(self, workSetWithQuantity):
    if self.lock_workSets_insertion:
      error_msg = 'lock_workSets_insertion is True, ie, an inconsistent action (either static or dynamic) was issued. First all workSets are added, then the first call to combine() locks further additions.'
      raise IndexError, error_msg
    if not self.isWorkSetWithQuantityValid(workSetWithQuantity):
      return
    workSet, quantity = workSetWithQuantity
    workSetObj = WorkSet(workSet, self.instantiateIndicesCombiner(workSet, quantity) )
    self.workSetObjs.append(workSetObj)
    
  def get_total_combinations(self):
    if self.total_combinations != None:
      return self.total_combinations
    self.total_combinations = 1
    for workSet in self.workSetObjs:
      self.total_combinations *= workSet.get_total_combinations() 
    return self.total_combinations

    return self.each_combiner_size_list

  def initialize_sets_to_join(self):
    self.sets_to_join = [[]] * len(self.workSetObjs)
    # self.horizontal_combined_sets = [] # to be used when it's desired to exchange the yield option for a memory-hungry solution
    # prepare first horizontal combined set!; run only once
    for i, workSetObj in enumerate(self.workSetObjs[:-1]):
      self.sets_to_join[i] = workSetObj.next()
    
  def join_sets(self):
    joint = []
    for s in self.sets_to_join:
      joint += s
    return joint

  def go_leftsideways_to_combine(self, depth):
    '''
    This (somewhat light-weight) method is recursive (however notice that the "heavy-weight" combination generator is NOT recursive in this class, though it uses recursive in a child class)
    '''
    self.workSetObjs[depth].restart()
    if depth < self.LAST_INDEX:
      # adjust self.sets_to_join for all slots, except the last (which already rounds in the combine() method) 
      self.sets_to_join[depth] = self.workSetObjs[depth].next()
    depth -= 1
    if depth < 0:
      # "Game Over" - processing is finished
      return False
    next_set = self.workSetObjs[depth].next()
    if next_set != None:
      self.sets_to_join[depth] = next_set
      return True
    else:
      return self.go_leftsideways_to_combine(depth)
    
  def next_combination(self):
    '''
    This method is not recursive. It has a while-loop with a "yield" (if right-most subset is formed not None) and go_leftsideways_to_combine() (when right-most subset is formed None)
    The exit from the 1-while-loop happens when go_leftsideways_to_combine() returns False, which indicates that all combinations have already been produced
    '''
    self.lock_workSets_insertion = True # from here onwards, no further workSet can be added
    self.LAST_INDEX = len(self.workSetObjs) - 1
    self.initialize_sets_to_join()
    while 1:
      next_set = self.workSetObjs[self.LAST_INDEX].next()
      if next_set != None:
        self.sets_to_join[self.LAST_INDEX] = next_set
        horizontal_combined_set = self.join_sets()
        #self.horizontal_combined_sets.append(horizontal_combined_set)
        self.horizontal_combined_set = horizontal_combined_set  
        yield horizontal_combined_set
      else:
        if self.go_leftsideways_to_combine(self.LAST_INDEX):
          continue
        else:
          break


class SetsCombinerMemoryIntensive(object):
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
    
    Another example:  Observe the follow piece of code:

      sc = SetsCombiner()
      sc.addSetWithQuantities(([1,2,3],2))
      sc.addSetWithQuantities(([4,5,6],2))
      sc.combineSets()
      print sc.allCombinations    
  
  The print-out result is the 9-element set:
  
      [[1, 2, 4, 5], [1, 2, 4, 6], [1, 2, 5, 6], [1, 3, 4, 5], [1, 3, 4, 6], [1, 3, 5, 6], [2, 3, 4, 5], [2, 3, 4, 6], [2, 3, 5, 6]]
    
   Observations on performance:
   1) With this class, SetsCombinerMemoryIntensive, (having recursion, plus buffering all combinations)    
      gencounter 1634688 expected 1634688
      real  0m10.812s
      user  0m9.985s
      sys  0m0.380s

   2) With class SetsCombiner (above, having while (instead of recursion), plus having "yield", instead of buffering all combinations)    
      gencounter 1634688 expected 1634688
      real  0m6.866s
      user  0m6.728s
      sys  0m0.064s

  Conclusion, use preferencially SetsCombiner instead of this class (SetsCombinerMemoryIntensive)  
  '''

  def __init__(self):

    self.workSetsWithQuantities = [] #  # workSetsWithQuantities was formerly listOfTuple2
    self.total_combinations = None  # this is set when non-recursive computing is chosen

  def addSetWithQuantities(self, tupleIn):
    self.workSetsWithQuantities.append(tupleIn)

  def getAllCombinationsRecursive(self, index, being_combined=[]):
    '''
    Memory-hungry !
    '''
    # the trick is here is to "imagine" a 2D assignment (the next loop goes vertically, the previous, horizontally)
    # print 'allCombinations', allCombinations, 'index', index 
    if index > len(self.workSetsWithQuantities) - 1 :
      return []
    workSetWithQuantity = self.workSetsWithQuantities[index] 
    for workSet in generateAllCombinationsForWorkDict(workSetWithQuantity):
      being_combined_loop_added = being_combined + workSet 
      received = self.getAllCombinationsRecursive(index + 1, being_combined_loop_added)
      # the "final" return, at the end, means return None; if so, ie, if received is None, just loop onwards, if it's not None, it's a combined set to be added to all combined sets
      if received != None: 
        being_combined_loop_added += received 
        self.allCombinations.append(being_combined_loop_added[:])
    return

  def getAllCombinations(self): # Entrance to recursive method getAllCombinationsRecursive()
    #return 
    self.allCombinations = []
    self.getAllCombinationsRecursive(index=0, being_combined=[])
    '''c=0
    for comb in self.allCombinations:
      c+=1
      print c, 'Combination', comb''' 
    return self.allCombinations

  def calculate_total_combinations(self):
    self.total_combinations = 1
    for workSetWithQuantity in self.workSetsWithQuantities:
      workSet = workSetWithQuantity[0]
      quantity = workSetWithQuantity[1]
      n_combinations_for_workSet = afc.combineNbyC(len(workSet), quantity)
      self.total_combinations *= n_combinations_for_workSet
    return self.total_combinations 

  def get_total_combinations(self):
    '''
    total_combinations is a combination n by c, the same that is known by n!((n-c)!c!)
    where n is workSet's size and c is IndicesCombiner's quantity 
    '''
    if self.total_combinations != None:
      return self.total_combinations
    self.calculate_total_combinations()
    return self.total_combinations

  def __len__(self):
    if self.allRecursiveCombinations != None:
      return len(self.allRecursiveCombinations)
    if self.total_combinations == None:
      self.calculate_total_combinations()
    return self.total_combinations


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
    set_under_indices = [workSet[i] for i in indicesArray]
    workSets.append(set_under_indices)
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

def simulate_set_multiply():
  # ===========================================
  # sc = SetsCombiner()
  sc = SetsCombinerMemoryIntensive()
  workSetWithQuantity = ([1,2,3],2)
  sc.addSetWithQuantities(workSetWithQuantity)
  workSetWithQuantity = ([4,5],2)
  sc.addSetWithQuantities(workSetWithQuantity)
  workSetWithQuantity = ([6,7,8,9],3)
  sc.addSetWithQuantities(workSetWithQuantity)
  c=0
  for each in sc.getAllCombinations():#sc.next_combination():
    c+=1
    print c,'combination', each

  print 'total comb',  sc.get_total_combinations()


def test_yield():
  for i in ynext():
    print i
   
def adhoc_test1():
  simulate_set_multiply()
  
def adhoc_test2():
  # sc = SetsCombiner()
  sc = SetsCombinerMemoryIntensive()
  worksetWithQuantity = ([1,2,3], 2)
  sc.addSetWithQuantities(worksetWithQuantity)
  worksetWithQuantity = ([4,5,6], 2)
  sc.addSetWithQuantities(worksetWithQuantity)
  for ws in sc.getAllSetsCombinationNonRecursively():
    print 'ws', ws

def ynext():
  for i in xrange(10):
    yield i

def adhoc_test3():
  
  combiner = SetsCombiner()
  
  
  s = ['a','b','c']; combsize = 2
  ws = WorkSet(s, IndicesCombiner( len(s)-1, combsize,False))
  comb = ws.next()
  while comb:
    print comb
    comb = ws.next()

  print '-'*30
  combiner.addSetWithQuantities((s, combsize))

  s = [4,5]; combsize = 2
  ws = WorkSet(s, IndicesCombiner( len(s)-1, combsize,False))
  comb = ws.next()
  while comb:
    print comb
    comb = ws.next()

  print '-'*30
  combiner.addSetWithQuantities((s, combsize))

  s = [6,7,8,9]; combsize = 3
  ws = WorkSet(s, IndicesCombiner( len(s)-1, combsize,False))
  comb = ws.next()
  while comb:
    print comb
    comb = ws.next()

  print '-'*30
  combiner.addSetWithQuantities((s, combsize))
  for comb in combiner.next_combination():
    print comb
  
  total_combinations = combiner.get_total_combinations()
  print 'total_combinations =', total_combinations

def adhoc_test4():
  test_yield()

def adhoc_test():
  adhoc_test3()

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
      pass
      # process()

if __name__ == '__main__':
  look_up_cli_params_for_tests_or_processing()
