#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
SetsCombiner
'''
import sys

import localpythonpath
localpythonpath.setlocalpythonpath()
# from lib import lambdas
from IndicesCombiner import IndicesCombiner
import algorithmsForCombinatorics as afc


class SetsCombiner(object):
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
      
  '''

  def __init__(self):

    self.workSetsWithQuantities = [] #  # workSetsWithQuantities was formerly listOfTuple2
    self.allRecursiveCombinations = None  # this is set if the recursive computing method is called 
    self.total_combinations = None  # this is set when non-recursive computing is chosen

  def addSetWithQuantities(self, tupleIn):
    self.workSetsWithQuantities.append(tupleIn)

  '''
  def recursiveCombineSets(self):
    self.allRecursiveCombinations = doRecursiveSetsCombination(self.workSetsWithQuantities)

  def getAllCombinationsAfterRecursiveCombine(self):
    return self.allRecursiveCombinations
  '''

  def createWorkSetsWithIndicesCombiner(self, workSet, icObj):
    '''
    This method uses "yield"
    This method does not use "self"
    '''
    for indicesArray in icObj.iterate_all_sets(): # iterate_all_sets() yields its values 
      formingSet = []
      for indiceArray in indicesArray:
        formingSet.append(workSet[indiceArray])
      yield formingSet

  def generateAllCombinationsForWorkDictNonRecursivelyEntrance(self, workSetAndQuantity):
    workSet = workSetAndQuantity[0]
    quantity = workSetAndQuantity[1]
    if quantity > len(workSet):
      errorMsg = ' generateAllCombinationsForWorkDict(workSetAndQuantity) :: quantity=%d > len(workSet)=%d cannot happen ' %(quantity, len(workSet))
      raise ValueError, errorMsg 
    if quantity == 0:
      return []
    return None # None here means OK to continue processing input 

  def generateAllCombinationsForWorkDictNonRecursively(self, workSetAndQuantity):
    '''
    This method uses "yield"
    '''
    workSet = workSetAndQuantity[0]
    quantity = workSetAndQuantity[1]    
    if quantity == 1 and len(workSet) == 1:
      return  workSet[:]
    else:
      icObj = IndicesCombiner(len(workSet)-1, quantity, False)
      return createWorkSetsWithIndicesCombiner(workSet, icObj)

  def getAllSetsCombinationNonRecursively(self):
    '''
    This method uses "yield"
    '''
    if len(self.workSetsWithQuantities) == 0:
      yield [[]]
      return 
    allCombinations = [[]]
    workSetsWithQuantities = list(self.workSetsWithQuantities) # hard-copy for pop()'s would destroy it (pop out the copy's elements!)
    while len(workSetsWithQuantities) > 0:
      workSetAndQuantity = workSetsWithQuantities.pop()
      '''direction_to_take = self.generateAllCombinationsForWorkDictNonRecursivelyEntrance(workSetAndQuantity)
      if direction_to_take != None:
        return allCombinations'''
      # if direction_to_take == None
      for workSet in self.generateAllCombinationsForWorkDictNonRecursively(workSetAndQuantity):
        for eachCombination in allCombinations:
          #print 'summing', workSet, eachCombination
          newFormingSet = workSet + eachCombination
          newFormingSet.sort()
          yield newFormingSet 
          allCombinations.append(newFormingSet)

  def calculate_total_combinations(self):
    self.total_combinations = 0
    for workSetWithQuantity in self.workSetsWithQuantities:
      workSet = workSetWithQuantity[0]
      quantity = workSetWithQuantity[1]
      n_combinations_for_workSet = afc.combineNbyC(len(workSet), quantity)
      self.total_combinations += n_combinations_for_workSet
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

                          
def adhoc_test():
  sc = SetsCombiner()
  worksetWithQuantity = ([1,2,3], 2)
  sc.addSetWithQuantities(worksetWithQuantity)
  worksetWithQuantity = ([4,5,6], 2)
  sc.addSetWithQuantities(worksetWithQuantity)
  for ws in sc.getAllSetsCombinationNonRecursively():
    print 'ws', ws

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
