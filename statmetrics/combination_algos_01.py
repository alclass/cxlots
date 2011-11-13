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

n=9
perm = range(n+2)
randomPermutation(perm)
print perm