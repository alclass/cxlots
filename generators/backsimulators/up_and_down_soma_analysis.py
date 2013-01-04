#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys #numpy, sys # , os, pickle, 

import localpythonpath
localpythonpath.setlocalpythonpath()

# import local_settings as ls

from models.ConcursoHTML import ConcursoHTML

class AnalyzerOfUpAndDownForSoma(object):
  
  def __init__(self):
    pass

def process():
  slider = ConcursoHTML()
  concursos = slider.get_all_concursos(); soma_anterior = None
  for concurso in concursos:
    soma = sum(concurso.get_dezenas())
    if soma_anterior == None:
      soma_anterior = soma
      continue
    difference = soma - soma_anterior
    word = '(%d, %d, %d)' %(soma_anterior, soma, difference)
    if difference > 0: # ie soma > soma_anterior:
      prefix = 'up' 
    elif difference == 0: # ie soma == soma_anterior:
      prefix = '~' 
    else: # difference < 0: # ie  soma < soma_anterior:
      prefix = 'down'
    print '%s%s' %(prefix, word) ,
    soma_anterior = soma


def adhoc_test():
  pass


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
