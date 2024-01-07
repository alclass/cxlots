#!/usr/bin/env python3
import sys
import numpy
from ConcursoHTML import ConcursoHTML
from models.Files import ReadConcursosHistory


class ConcursoExt(ConcursoHTML):
  
  def __init__(self):
    """
    super(ConcursoHTML, self).__init__()
    """
    super().__init__()

  def get_contrajogos_as_dezenas_list_down_to_depth(self, depth=4, inclusive=True):
    """
    This method is just a bypass to function get_contrajogos_as_dezenas_down_from(self, depth)
      in module ReadConcursosHistory in this 'models' package
    To avoid cross-importing, ReadConcursosHistory is imported dynamically here
    
    This bypassing is done in order to improve the class interface altogether
      and allow these contrajogos to be gotten at one sole instruction  
    """
    if not inclusive:
      previous_concurso = self.get_previous()
      return previous_concurso.get_contrajogos_as_dezenas_list_down_to_depth(depth, inclusive=True)
    return ReadConcursosHistory.get_contrajogos_as_dezenas_down_from(self, depth)
  
    depth -= 1
    if depth < 0:
      return []
    numpy_dezenas = numpy.array(self.get_dezenas())
    if depth == 0:
      return numpy_dezenas
    contrajogos_as_dezenas_list = ReadConcursosHistory.get_contrajogos_as_dezenas_down_from(self, depth)
    contrajogos_as_dezenas_list.insert(0, numpy_dezenas)
    return contrajogos_as_dezenas_list
    

def process():
  pass

def adhoc_test():
  #testConcursoSample()
  slider = ConcursoExt()
  concurso = slider.get_last_concurso()
  print concurso.n_conc, concurso.date, concurso.get_dezenas()
  print 'inclusive', concurso.get_contrajogos_as_dezenas_list_down_to_depth(depth=4)
  print 'not inclusive', concurso.get_contrajogos_as_dezenas_list_down_to_depth(depth=4, inclusive=False)
  pass


import unittest
class MyTest(unittest.TestCase):

  def test_1(self):
    pass

def look_up_cli_params_for_tests_or_processing():
  for arg in sys.argv:
    if arg.startswith('-t'):
      del sys.argv[1]
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
