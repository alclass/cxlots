#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy, pickle, sys, time

import __init__
__init__.setlocalpythonpath()

import local_settings as ls

from fs.filters import filter_functions # get_line_patterns, get_column_patterns etc.
from generators.GeradorIter import Gerador 

class FunctionModel(object):
  '''
  This class helps "encapsulate" a function to be executed later on in the filtering queued processes
  A function is kept in the object as well as the parameters to it
  The method apply() executes the function returning the function's return variable(s) 
  '''
  def __init__(self, name):
    self.name = name
  
  def set_function(self, func):
    self.func = func
    
  def set_params(self, *params):
    self.params = params
    
  def apply(self, jogo):
    return self.func(jogo, *self.params)
  

class FilterQueuer(object):
  '''
  This class stores:
  - a jogoGenerator object
  - a queue with filter functions
  - a pickled object for saving the filtered-in games
  
  Each game provided by jogoGenerator goes thru the queue and at the first False it gets from the filters,
  it abandons the function queue and loops onward to the next game from jogoGenerator.
  
  If game survives the entire filtering queue, it is saved via the pickled object.
   
  '''
  def __init__(self, jogoGenerator, filter_function_list, result_pickled_fileobj):
    # self.jogosObj = funcs.returnJogosObj(eitherJogosObjOrS2)
    self.jogoGenerator          = jogoGenerator
    self.filter_function_list   = filter_function_list
    self.result_pickled_fileobj = result_pickled_fileobj
    self.n_filter_passed_games  = 0

  def process(self):
    counter = 0
    try:
      for jogo in self.jogoGenerator:
        jogo = numpy.array(jogo)
        counter += 1
        print self.n_filter_passed_games, '/', counter, 'jogo', jogo
        if self.does_it_pass_filter_functions(jogo):
          self.save(jogo)
    except KeyboardInterrupt:
      print ' Closing pickled result_pickled_fileobj at' , jogo
      # self.result_pickled_fileobj.close()

  def does_it_pass_filter_functions(self, jogo):
    for func in self.filter_function_list:
      print ' [does_it_pass_filter_functions()]', func.name,
      if not func.apply(jogo):
        print 'False'
        return False
      print 'True'
    return True

  def save(self, jogo):
    self.n_filter_passed_games += 1
    print '-'*30
    print self.n_filter_passed_games, ' Saving jogo', jogo
    print '-'*30
    self.result_pickled_fileobj.dump(jogo)

  # ENDS class FunctionModel(object)


def adhoc_test():
  # jogo = range(1, 7);
  # jogo = [1,1,1,1,1,1]
  jogo = [2,2,2,2,2,2]
  in_between=(4,5)

  # bool_result = filter_functions.filter_within_n_impares(jogo, in_between)
  # print 'filter_within_n_impares(',jogo,',', in_between, ') ==>>', bool_result

  filter_function_list = []
  # instanciate
  funct = FunctionModel('filter_within_n_impares')
  funct.set_function(filter_functions.filter_within_n_impares)
  in_between = 3,3
  funct.set_params(in_between) 
  filter_function_list.append(funct)
  # instanciate
  funct = FunctionModel('filter_sum_within')
  funct.set_function(filter_functions.filter_sum_within)
  in_between = 201,201
  funct.set_params(in_between) 
  filter_function_list.append(funct)
  # instanciate
#  funct = FunctionModel('filter_in_within_line_patterns')
#  funct.set_function(filter_functions.filter_in_within_line_patterns)
#  line_patterns = ['102021']  
  funct = FunctionModel('filter_in_within_line_drawing')
  funct.set_function(filter_functions.filter_in_within_line_drawings)
  line_drawings = ['2211']  
  funct.set_params(line_drawings) 
  filter_function_list.append(funct)
  # instanciate
#  funct = FunctionModel('filter_in_within_column_patterns')
#  funct.set_function(filter_functions.filter_in_within_column_patterns)
#  column_patterns = ['1101001110']  
  # instanciate
  funct = FunctionModel('filter_in_within_column_drawing')
  funct.set_function(filter_functions.filter_in_within_column_drawings)
  column_drawings = ['111111']  
  funct.set_params(column_drawings) 
  filter_function_list.append(funct)

  # instanciate
  funct = FunctionModel('filter_in_within_column_drawing')
  funct.set_function(filter_functions.filter_in_within_column_drawings)
  column_drawings = ['111111']  
  funct.set_params(column_drawings) 
  filter_function_list.append(funct)

  
  jogoGerador = Gerador()
  outputFilename = ls.GENERATED_DATA_DIR + str(time.time()) + '.blob'
  outputFileObj  = open(outputFilename, 'w')
  pickled_fileobj = pickle.Pickler(outputFileObj, pickle.HIGHEST_PROTOCOL) 
  filtro_obj = FilterQueuer(jogoGerador, filter_function_list, pickled_fileobj)
  filtro_obj.process()
   
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
      pass
      # process()

if __name__ == '__main__':
  look_up_cli_params_for_tests_or_processing()
