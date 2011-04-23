#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from statlib import stats

def legacy():
  patts = stats.ltrimboth(patts, 0.1) # statlib.
  #patts = statlib.stats.ltrimboth(patts, 0.1) # statlib.
  print 'len(patts)', len(patts)
  #stats.writecc([patts,patts],'test.txt')
  alist = range(1,6)
  print 'sum(alist)', sum(alist)
  print 'cumsum(alist)', stats.cumsum(alist)
  print 'geometricmean(alist)', stats.geometricmean(alist)


def testFiltre():
  alist = []
  for i in range(20):
    r = random.randint(0,100)
    alist.append(r)
  print 'alist', alist
  score = stats.scoreatpercentile(alist, 0.1)
  print 'score', score

if __name__ == '__main__':
  testFiltre()