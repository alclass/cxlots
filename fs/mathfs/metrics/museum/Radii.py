#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import math
import numpy, random

a=1
import CLClasses
import lambdas
import LgiCombiner as lc


'''
Created on 21/11/2011

@author: up15


This module has the calculatePathway() method, which is the main "business" method here
The other methods are services so to say to calculatePathway()

The calculatePathway() calculates the distance traversed from the dezena closest to
  the left upper corner to each subsequent closest dezena
 
  Eg.
  1,2,3,4,5,6
  The starting dezena is 1, for it's the closest to the left upper corner
  2 is the closest to 1, so the 2-D distance between 2 and 1 is 1.
 
  In this case it's easy to see that each one distances from the previous one from 1
  So all distances summed up (ie, the pathway metric) are 5
 
'''

def dist2d(point, xy):
  x1, y1 = point
  x2, y2 = xy
  return ((x1-x2)**2 + (y1-y2)**2)**(1/2.0)

pathway = []
totalDistance = 0
def findClosestPointInSet(fromPoint, xyPairs):
  global pathway, totalDistance
  leastDistance = 100000000; closestPair = None
  index = indexOfClosest = -1
  for xy in xyPairs:
    index += 1
    distance = dist2d(fromPoint, xy)
    if distance < leastDistance:
      leastDistance = distance
      closestPair = xy
      indexOfClosest = index
  del xyPairs[indexOfClosest]
  print 'leastDistance', leastDistance, 'from', fromPoint, 'to', closestPair, 'pairs', xyPairs
  pathway.append(closestPair)
  totalDistance += leastDistance  
  return closestPair, xyPairs

def recurse(fromPoint, xyPairs):
  if len(xyPairs) == 0:
    return
#    pathway.append(xyPairs[0])  
#    return xyPairs[0], []
  closestPair, xyPairs = findClosestPointInSet(fromPoint, xyPairs)
  return recurse(closestPair, xyPairs)

def calculatePathway(xyPairs):
  if (0,0) not in xyPairs:
    startPoint, xyPairs = findClosestPointInSet((0,0), xyPairs)
  else:
    startPoint = (0,0)
    pathway.append(xyPairs[0])  
    del xyPairs[0]
  recurse(startPoint, xyPairs)

def transformDezenaIntoXY(dezena):
  rightDigit = dezena % 10
  if rightDigit == 0:
    rightDigit = 10  
  x = rightDigit - 1
  y = (dezena - 1) / 10
  return x, y

def convertDezenasToXY(dezenas = [11, 6, 7, 53, 44, 32]):
  xyPairs = []
  for dezena in dezenas:
    x, y = transformDezenaIntoXY(dezena)
    xyPairs.append((x,y))
  return xyPairs
  #print 'x, y', x, y

def convertXYToDezenas(xyPair):
  dezenas = []
  for x, y in xyPair:
    rightDigit = x + 1
    leftDigit = y
    dezena = leftDigit * 10 + rightDigit
    dezenas.append(dezena)
  return dezenas   

def test1():
  global pathway, totalDistance
  #dezenas = [11, 6, 7, 53, 44, 32]
  dezenasSet = [[1,2,3,4,5,6], [1,11,21,31,41,51], [39, 44, 57, 12, 15, 4], [1, 12, 23, 34, 45, 56]]
  for dezenas in dezenasSet:
    pathway = []
    totalDistance = 0
    xyPairs = convertDezenasToXY(dezenas)
    print xyPairs
    calculatePathway(xyPairs)
    print 'pathway', pathway
    dezenasBack = convertXYToDezenas(pathway)
    print 'dezenasBack', dezenasBack
    print 'totalDistance', totalDistance

test1()


class Radii(CLClasses.Base):
  '''
  Radii class
  '''
  def __init__(self, standard2LetterName):
    CLClasses.Base.__init__(self, standard2LetterName)
    self.nOfNonRedundantCols = self.nOfCols / 2
    self.nOfNonRedundantLins = self.nOfLins / 2
    self.allSquareDistances = None
    self.histG = {}
    self.c=0

  def getAllSquareDistances(self, reGetIt=False):
    if self.allSquareDistances == None or reGetIt:
      self.allSquareDistances = getAllSquareDistances(self.nOfNonRedundantLins, self.nOfNonRedundantCols)
    return self.allSquareDistances
    
  def calculatePathway(self, jogo, nonSquared=False):
    '''
    For example:
    MS ==>> Calculates the 15 (C(6,2)=15) radius element-by-element in the sixtuple
  
    D(P1,P2)=SQRT((X2-X1)^2+(Y2-Y1)^2)
    
    [Retaking this metric on 2009-10-17]
    
    The idea here is that each jogo has a "distance" connected to it
    This distance is the sum of square distances between points, so that this sum is a minimum
    The choice for squares is to use an integer metric instead of a floating-point one 
    
    Eg.
    In a 6-dezena jogo, there are 720 ways of making this path (ie, a permutation of 6 = 6! = 720)
    Among these 720 pathways, there is one (or some) with a minimum "distance"
    This minimum distance is the metric sought for
    
    IMPORTANT:
    Due to the complexity of the algorithm mentioned above, a sequential distance scheme
    will be used for time being
    
    ie, DistMetric = D(dzn1,dzn2) + D(dzn2,dzn3) + ... + D(dznN-1,dznN)
    
    '''
    self.c+=1
    pathway = 0
    #combsNto2 = generateCombNto2(jogo); leastDist = 100000
    for i in range(len(jogo)-1):
      dezenaI = jogo[i]
      dezenaJ = jogo[i+1]
      if nonSquared:
        pathway  += self.formPairAndCalcSquareDist(dezenaI, dezenaJ)**0.5
      else:
        pathway  += self.formPairAndCalcSquareDist(dezenaI, dezenaJ)
    #print 'dznI', dezenaI, 'dznJ', dezenaJ, pair,'dist', dist, 'pathway', pathway 
    #print 'dist',dezenaI, dezenaJ,'pathway', pathway 
    #for pair in combsNto2:
    return pathway

  def calculateIntercrossed(self, jogo, nonSquared=False):
    twoByTwoList = generateCombNto2(jogo)
    intercrossedDist = 0
    for two in twoByTwoList:
      dezenaI = two[0]
      dezenaJ = two[1]
      squareDist = self.formPairAndCalcSquareDist(dezenaI, dezenaJ)
      if nonSquared:
        intercrossedDist += squareDist ** 0.5
      else:
        intercrossedDist += squareDist
      #print 'dznI', dezenaI, 'dznJ', dezenaJ, 'sDist', squareDist, "interx'd", intercrossedDist
    return intercrossedDist
      
  def formPairAndCalcSquareDist(self, x, y):
    pair = self.formPair(x, y)
    squareDist = self.calculateSquareDist(pair)
    return squareDist

  def formPair(self, x1y1, x2y2):
    coordI  = self.xyPair(x1y1)
    coordJ  = self.xyPair(x2y2)
    pair = (coordI,  coordJ)
    return pair

  def xyPair(self, dzn):
    if self.sqlTable == 'lf':
      #  for LF, valid for any 5-column starting from 1
      x = (dzn - 1) / 5 + 1 # nOfLin
      y = (dzn - 1) % 5 + 1 # nOfCol
    # x = digito unidade (0 a 9)
    elif self.sqlTable == 'lm':
      #  for LM but also valid for any 10-column starting from 0
      x, y = xyPairDatumMinusOne(dzn)
    else:
      #  for MS but also valid for any 10-column starting from 1
      x, y = xyPair(dzn)
    # print 'xy', x,y
    return x, y

  def calculateSquareDist(self, coords2D):
    '''
    Distance is contextual, ie, 00 to 59 is not dx=9 and dy=5, rather, dx=1 and dy=1
    This is seen by continuation, 59 is 9 position right and five below
     but it is also 1 position left and 1 above
    The mininum path is the one to choose
    The implement for that is:
      if dx > 5: dx = 10 - dx
      and if dy > 3: dx = 6 - dx
    Notice also that dx and dy are non-negative (abs/module)
    '''
    x1 = coords2D[0][0]
    x2 = coords2D[1][0]
    dx = abs(x1 - x2)
    if dx > self.nOfNonRedundantCols:
      dx = self.nOfCols - dx
    squareX = dx**2
    y1 = coords2D[0][1]
    y2 = coords2D[1][1]
    dy = abs(y1 - y2)
    if dy > self.nOfNonRedundantLins:
      dy = self.nOfLins - dy
    squareY = dy**2
    squareDist = squareX + squareY
    #dist = math.sqrt(squareX+squareY)
    #print '%d+%d=%0.3f' %(squareX,squareY,dist)
    return squareDist

  def calculateDistance(self, coords2D):
    return self.calculateSquareDist(coords2D)**0.5


def getAllSquareDistances(nOfNonRedundantLins=3, nOfNonRedundantCols=5):
  '''
  There are 17 distinct square distances in the [0..9]x[0..5] plane
  '''
  
  dxs = range(1, nOfNonRedundantCols + 1)
  dys = range(4, nOfNonRedundantLins + 1)
  c=0; squareDists = []
  for dy in dys:
    for dx in dxs:
      if dy <= dx:
        squareDist = dx**2 + dy**2
        squareDists.append((squareDist, dx, dy))
  squareDists.sort()
  for squareDistTriple in squareDists:
    c+=1
    squareDist, dx, dy = squareDistTriple
    print '%02d x=%d y=%d SquareDistance=%d' %(c, dx, dy, squareDist)
    allSquareDistancesList.append(squareDist)
  print allSquareDistancesList

def xyPair(datum):
  # coord is a 2-n digit yx eg. 05, 00, 59, 15 (from 00 to 59)
  # y = digito dezena (0 a 5)
  y = datum / 10 # int division
  # x = digito unidade (0 a 9)
  x = datum % 10
  # print 'xy', x,y
  return x, y

def xyPairDatumMinusOne(datum):
  return xyPair(datum-1)

def squareDist(subList2D):
  coords = [(0,0)]*2
  for i in range(len(subList2D)):
    coord = subList2D[i]
    x , y = xyPairIndexFromZero(coord)
    coords[i] = x, y
  #print coords
  return calculateSquareDist(coords)

def generateCombNto2(lista):
  combs = []
  for i in range(len(lista)-1):
    for j in range(i+1, len(lista)):
      tupleComb = (lista[i], lista[j])
      combs.append(tupleComb)
  return combs


def testCombNto2():
  lista = range(1,7); print 'lista', lista
  combs = generateCombNto2(lista)
  print 'combs', combs, 'tam', len(combs)

def testRadii():
  tipoJogo = 'ms' #'lf'
  rad = Radii(tipoJogo)
  jogosObj = CLClasses.getJogosObj(tipoJogo)
  nDeCombs = jogosObj.getNDeCombs()
  lgiComb  = jogosObj.getGenericLgiComb()
  jogos = jogosObj.getJogos()
  for i in range(4):
    #lgi_b1idx = random.randint(0, nDeCombs-1)
    #jogo = lgiComb.move_to(lgi_b1idx)
    jogo = jogos[i]
    jogo.sort()
    # print 'jogo', jogo
    pathway = rad.calculatePathway(jogo, True)
    intercrossed = rad.calculateIntercrossed(jogo, True)
    print jogo, pathway, intercrossed

if __name__ == '__main__':
  testRadii()
  