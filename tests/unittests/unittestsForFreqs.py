#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 19/11/2011

@author: friend
'''

import unittest, sys

sys.path.insert(0, '..')
import frequencyMounting as fm
import sqlLayer as sl
import statmetrics.funcsForTil as fft


class Test(unittest.TestCase):
  
  def test_totalOfFreqsConsistency(self):
    '''
    This test does the following
    6 * n_concs_total = sum of each dezena's frequency at n_concs_total
    Eg
    given n_concs_total = 1330, it results:
    6 * 1330 = 7980 = f(1) + f(2) + ... + f(60)
    ie.
    the summation of every dezena frequency must equal 7980 
    '''
    concursos = sl.getListAllConcursosObjs()
    n_concs_total = len(concursos)
    #freqAtEachConcurso = fm.statsStore['freqAtEachConcurso']
    freqAtEachConcurso = fm.FrequenciesThruConcursos()
    for i in range(1, n_concs_total+1):
      shouldBeSum = 6 * i
      self.assertEqual(freqAtEachConcurso.sumUpTo(i), shouldBeSum)

  def test_initializeFreqDict(self):
    '''
    This test does the following
    In the 1st test case
    fm.initializeFreqDict(60) should return a dict d[k]=0 for k varying from 0 to 60
    In the 2nd test case, the ideia is to "force" an assertFalse, "polluting" so to say, the comparing dict
    
    More tests will vary data to compare with the return dict from fm.initializeFreqDict(60) 
    '''
    dictCompare = {}
    for i in range(61):
      dictCompare[i]=0
    self.assertEqual(fm.initializeFreqDict(60), dictCompare)
    dictCompare['blah']='blah'
    self.assertFalse(fm.initializeFreqDict(3), dictCompare)
    dictCompare['blah']='blah'
    self.assertFalse(fm.initializeFreqDict(3), dictCompare)
  
  def test_mountDezenasFrequencies(self):
    '''
    The fm.mountDezenasFrequencies() sums up all dezenas frequencies concurso by concurso
    The simplest case is for the very 1st concurso where any dezena frequency should be 1
    So the simplest case is a Test Case in here, the first one below
    
    The second Test Case is just to check if passing in parameter ate_concurso_n=0 will return the same as passing no parameter at all
    The two must equal and then pass the assertEqual
    
    Some other test combinations may be seen below 
    '''
    concursos = sl.getListAllConcursosObjs()
    concurso1 = concursos[0]
    dictForConc1 = {}
    for dezena in concurso1.getDezenas():
      dictForConc1[dezena] = 1
    self.assertEqual(fm.mountDezenasFrequencies(ate_concurso_n=1), dictForConc1)
    # self.assertEqual(type(mountDezenasFrequencies()), dict)
    self.assertEqual(fm.mountDezenasFrequencies(ate_concurso_n=0), fm.mountDezenasFrequencies())
  
  def test_calculateTilOfNForHistogram(self):
    tilProducer = fm.statsStore['tilProducer']
    tilPattern = tilProducer.getTilNForConcursoI(5, 101)
    # megasena has 6 dezenas
    self.assertEqual(fft.sum_digits(tilPattern), 6)
    
    pass


if __name__ == '__main__':
  unittest.main()

    