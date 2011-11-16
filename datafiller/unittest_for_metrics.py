#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import sys
import unittest
'''
Created on 15/11/2011

@author: friend
'''
a=1
import metricsRepository as mr

class TestMetrics(unittest.TestCase):
  def test_cleanUpRepeatsAndPutInOrder(self):
    numbers = [1,2,3,4,5,6]
    self.assertEqual(mr.cleanUpRepeatsAndPutInOrder(numbers),  [1,2,3,4,5,6])
    numbers =  [2,1,4,3,6,5]
    self.assertEqual(mr.cleanUpRepeatsAndPutInOrder(numbers),  [1,2,3,4,5,6])
    numbers =  'string'
    self.assertRaises(TypeError, mr.cleanUpRepeatsAndPutInOrder(numbers))

  def test_iguaisComOAnterior(self):
    concurso = [1,2,3,4,5,6]
    concursos = [[1,2,3,4,5,6]]
    self.assertEqual(mr.iguaisComOAnterior(concurso, concursos), 6)
    concurso = [1,2,3,4,5,6]
    concursos = [[7,8,9,10,11,12]]
    self.assertEqual(mr.iguaisComOAnterior(concurso, concursos), 0)
    concurso = [1,2,3,4,5,6]
    concursos = [[1,2,3,4,5,6],[1,2,3,4,5,6]]
    self.assertEqual(mr.iguaisComOAnterior(concurso, concursos), 6)
    concurso = [1,2,3,4,5,6]
    concursos = [[7,8,9,10,11,12],[7,8,9,10,11,12]]
    self.assertEqual(mr.iguaisComOAnterior(concurso, concursos), 0)
    concurso = [-1,2,3,4,5,6]
    concursos = [[7,8,9,10,11,12],[7,8,9,10,11,12]]
    self.assertRaises(TypeError, mr.iguaisComOAnterior(concurso, concursos))
    concurso = [1,2,3,4,5,6]
    concursos = [[0,8,9,10,11,12],[7,8,9,10,11,12]]
    self.assertRaises(TypeError, mr.iguaisComOAnterior(concurso, concursos))
    concurso = [1,2,3,4,5,6]
    concursos = [[7,8,9,10,11,12],[-7,8,9,10,11,12]]
    self.assertRaises(TypeError, mr.iguaisComOAnterior(concurso, concursos))
    concurso = [1,2,3,4,5,6]
    concursos = [[1,2,3,40,50,60],[10,20,30,40,5,6]]
    self.assertEqual(mr.iguaisComOAnterior(concurso, concursos), 5)
    

