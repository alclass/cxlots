#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Ref.: http://en.wikipedia.org/wiki/Combinadic
  combinadics Module
'''
import sys

a=1
import IndicesCombiner as ic
sys.path.insert(0, '..')
import datafiller.frequencyMounting as fm

def test1():
  icObj = ic.IndicesCombiner(5,3, False)
  print 'icObj', icObj
  print 'icObj.current()', icObj.current()
  print 'icObj.next()', icObj.next()
  print 'icObj.next()', icObj.move_to_last_one()
  #print 'icObj.next_zeroless()', icObj.next_zeroless()
  print 'icObj.all_sets()', icObj.all_sets()
  
  icObj = ic.IndicesCombiner(4,3, False)
  result = ic.createWorkSetsWithIndicesCombiner([12, 15, 19, 21, 32], icObj)
  print 'result', result
  
  tupleWorkSetPlusQuantity = ([11, 37], 1); workSet = tupleWorkSetPlusQuantity[0]; quantity=tupleWorkSetPlusQuantity[1]
  icObj = ic.IndicesCombiner(len(workSet)-1, quantity, False)
  result = ic.createWorkSetsWithIndicesCombiner(workSet, icObj)
  print 'result', result
  
  print 'setCombinerObj = ic.SetsCombiner()'
  setCombinerObj = ic.SetsCombiner()
  setCombinerObj.addSetWithQuantities(([12, 15, 19, 21, 32, 33, 45], 3))
  setCombinerObj.addSetWithQuantities(([8, 25, 27, 28, 49], 2))
  setCombinerObj.addSetWithQuantities(([11, 37], 1))
  print 'setCombinerObj.combineSets()'
  setCombinerObj.combineSets()
  totalOfSets = len(setCombinerObj)
  print setCombinerObj.allCombinations
  print 'totalOfSets = len(setCombinerObj) =', totalOfSets
  

tilElement = fm.TilElement('03021')
combinerObj = ic.SetsCombinerWithTils(tilElement)
#print 'combinerObj.allCombinations', combinerObj.allCombinations
print 'len combinerObj.allCombinations', len(combinerObj.allCombinations)

