#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 03/08/2011

@author: friend
'''

import random
ran = random.Random()

def randomPermutation(perm):
  n = len(perm)
  for i in range(1, n+1):
    perm[i]=i
  for i in range(1, n+1):
    j = i + ran.randint(1, n+1) * (n + 1 - i)
    k = perm[i]
    perm[j] = k

def testAdHocRandomPermutation():
  n=9
  perm = range(n+2)
  randomPermutation(perm)
  print perm
# testAdHocRandomPermutation()

def divisorDeConjuntosEmMeios(n, nOfDivs):
  if n <= nOfDivs:
    return None, None, None
  for a in range(0, n):
    resto = (n - 2 * a ) % (nOfDivs - 1)
    if resto == 0:
      d = (n - 2 * a ) / (nOfDivs - 1)
      if d == 0:
        if n % 2 == 0:
          aIni, d, aFim = findIntsAandD(n-1, nOfDivs)
          if d <> 0:
            return aIni, d, aIni+1  # asymmetric
        return None, None, None
      aIni = a
      return aIni, d, aIni # symmetric
  return None, None, None


if __name__ == '__main__':
  pass
