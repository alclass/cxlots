#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy, pickle, sys, time


import __init__
__init__.setlocalpythonpath()

import FilterConstants as filtercte
import local_settings as ls

from fs.gen.filters.filters import filter_functions
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
  

class FilterQueueProcessor(object):
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


def instantiate_FiltreFILT_by_FilterName(filtre_name, jogosObj):
  if filer in filtercte.FilterList:
    handle = 'Filtre' + FilterNamesDict[filtre] + '(jogosObj)'
    checkerObj = eval(handle)
    return checkerObj
  return None


class FiltreFILTSOMA(Filtre):
  '''
  FiltreFILTSOMA(Filtre):
  '''

  def __init__(self, jogosObj):
    Filtre.__init__(self, jogosObj) 
    self.chooser = Chooser.ChooserSoma()
    self.excludedForSomaN  = {}
    self.lowLimitForSomaN  = {}
    self.highLimitForSomaN = {}
    self.logFile = funcs.mountLogFile(self, self.jogosObj)

  def getExcludedForSomaN(self, n):
    if n not in self.excludedForSomaN[n]:
      self.excludedForSomaN[n] = self.chooser.getExcludedForSomaN(n)
    return self.excludedForSomaN[n]

  def getLowLimit(self, n):
    if n not in self.lowLimitForSomaN[n]:
      self.lowLimitForSomaN[n] = self.chooser.getLowLimitForSomaN(n)
    self.lowLimitForSomaN[n]

  def getHighLimit(self, n):
    if n not in self.highLimitForSomaN[n]:
      self.highLimitForSomaN[n] = self.chooser.getHighLimitForSomaN(n)
    self.highLimitForSomaN[n]

  def check(self, jogo):
    '''
    SomaN check
    '''
    for n in Stat.somaNList: # Stat.somaNList = [1, 3, 7, 15]  (may change there)
      exec('self.calcSoma%d(jogo)' %(n))
      r = self.compareWithExcluded(n) # or compareWithRanges
      if not r:
        return False
      r = self.compareWithLowAndHigh(n)
      if not r:
        return False
    return True

  def calcSomaN(self, jogo, n):
    jogos = self.jogosObj.getJogos()
    soma = Stat.calcSomaN(jogo, jogos, n)
    exec('self.soma%d += soma' %(n))
    self.somaDict[n] += soma 

  def compareWithExcluded(self, n):
#    somaN = eval('self.soma%d' %(n))
#    if somaN in self.getExcludedForSomaN(n):
    if self.somaDict[n] in self.getExcludedForSomaN(n): 
      return False
    return True

  def compareWithLowAndHigh(self, n):
    somaN = eval('self.soma%d' %(n))
    if self.somaN < self.getLowLimit(n):
      return False
    if self.somaN > self.getLowLimit(n):
      return False
    return True


class FiltreFILTREMAINDERS(Filtre):
  '''
  FiltreFILTREMAINDERS(Filtre):
  '''
  def __init__(self, jogosObj):
    Filtre.__init__(self, jogosObj) 
    self.logFile = funcs.mountLogFile(self, self.jogosObj)



class FiltreFILTREPEATS(Filtre):
  '''
  **
  '''
  def __init__(self, jogosObj):
    Filtre.__init__(self, jogosObj) 
    self.logFile = funcs.mountLogFile(self, self.jogosObj)


class FiltreFILTTILS(Filtre):

  def __init__(self, jogosObj):
    Checker.__init__(self, jogosObj) 
    self.logFile = funcs.mountLogFile(self, self.jogosObj)


  def check(self, jogo):
    '''
    Til Controller
    '''
    tilNpattern = self.tilNobj.generateLgiForJogoVsTilFaixas(jogo)
    r = self.compareWithExcluded(tilNpattern)
    if not r:
      return False
    r = self.compareWithRanges(tilNpattern)
    if not r:
      return False
    return True

  def write(self, jogoObj):
    '''
    in class Stream
    '''
    lgi = jogoObj.get_lgi()
    if self.streamType == STREAM_FILE:
      line = '%d\n' %(lgi)
      outFile.write(line)
      return jogo
    elif self.streamType == STREAM_SQL:
      sql = "insert into `%(table)s` (`lgi`) values ('%(lgi)d');" \
        %{'table':table,'lgi':lgi}
      #print rCount, c, 'insert', sql
      self.insert(sql)
    if self.c % 50000 == 0:
      print 'rCount', rCount, c,'til5pattern',til5pattern,'r',r
      print 'lgi', lgi, jogo


def printOut(c):
  print 'gone up to', c, #, consecDict
  print datetime.datetime.now()

def printOutMultiples(c):
    c+=1
    if c % 100000 == 0:
      if c > 999999:
        if c % 1000000 == 0:
          printOut(c)
      else:
        printOut(c)
    return c

def getAllConsecs():
  nOfCombs = 3268760; total = 0
  cDict = {'b97531': 3960, 'c9642': 495, '8421': 138600, 'a642': 13860, 'b8531': 7920, '8531': 69300, '754321': 9240, 'c9754321': 990, 'dcba987654321': 110, 'b85321': 7920, '975321': 13860, 'a54321': 2310, '4': 330, '6321': 13860, 'c96421': 990, '7531': 9240, '931': 13860, 'b852': 3960, 'db97531': 110, 'b8521': 3960, 'c975321': 990, '54321': 110, 'b8654321': 7920, '94321': 13860, 'a86421': 9240, 'b864321': 7920, 'a75321': 27720, 'b8642': 3960, '51': 9240, '52': 3960, '63': 4620, '531': 990, 'b74321': 3960, 'db987654321': 110, '7321': 46200, 'dba987654321': 110, '964321': 55440, 'c96321': 495, '9754321': 13860, '7654321': 1320, '4321': 11, 'c97531': 990, 'a63': 9240, 'db975321': 110, 'ca987654321': 990, '854321': 34650, 'ca8642': 495, '9631': 55440, 'b854321': 3960, '83': 69300, '8654321': 13860, '81': 2310, '8321': 34650, '84': 11550, '84321': 46200, '74321': 27720, '831': 138600, '85321': 69300, '82': 34650, 'a8642': 4620, '521': 3960, '7': 1320, '421': 110, '864321': 13860, '963': 9240, '75321': 9240, 'db97654321': 110, 'cba987654321': 495, '9521': 83160, 'a864321': 9240, 'c987654321': 495, 'c9631': 990, '9642': 27720, 'b7321': 1320, 'c963': 165, '841': 138600, '821': 13860, 'a621': 9240, 'a742': 13860, 'edcba987654321': 11, '642': 1980, 'b987654321': 3960, 'b7654321': 1320, '73': 46200, 'a64321': 27720, 'ba987654321': 1320, 'b7421': 7920, '621': 27720, '741': 27720, 'a7421': 27720, 'b7531': 3960, '9531': 83160, '61': 34650, '62': 41580, '6421': 3960, 'c97654321': 990, '9321': 2772, '5321': 990, 'b741': 3960, '731': 138600, 'b742': 3960, '852': 34650, '86421': 13860, 'a51': 9240, 'b75321': 3960, 'a52': 13860, '6': 4620, 'b975321': 3960, 'a987654321': 2310, '631': 27720, 'a8654321': 9240, 'db9754321': 110, 'a7531': 27720, 'a87654321': 9240, '842': 69300, 'a62': 13860, '93': 9240, 'a7654321': 13860, '94': 13860, 'c9654321': 495, '96421': 55440, 'a631': 55440, 'a754321': 27720, '95321': 83160, 'b731': 3960, 'a6321': 27720, '721': 46200, '954321': 27720, '87654321': 2310, '9654321': 27720, '742': 27720, 'ca86421': 990, 'a6421': 27720, 'a741': 13860, 'b86421': 7920, '96321': 27720, '64321': 3960, 'b97654321': 3960, '8521': 34650, 'c964321': 990, '951': 27720, 'ca87654321': 990, '952': 83160, '42': 55, 'ca8654321': 990, '41': 495, '5': 2772, '9421': 55440, 'ca864321': 990, 'b9754321': 3960, 'b73': 1320, '7421': 55440, '987654321': 2772, 'a654321': 9240, 'b87654321': 3960, '97654321': 13860, 'a5': 462, '72': 92400, '71': 27720, 'a5321': 9240, 'a521': 13860, 'b754321': 3960, 'a531': 9240, '942': 27720, 'a74321': 13860, '941': 83160, '654321': 495, '97531': 13860, '8642': 6930}
  consecValues = cDict.values()
  total = sum(consecValues)
  assert(nOfCombs == total)
  return cDict

def seeConsecutives(lgiObj, tipoJogo):
  consecDict = {}
  jogo = lgiObj.first(); c=0
  print 'Please, wait ::', tipoJogo,'nOfCombines =' #, lgiObj.nOfCombines
  while jogo:
    if type(jogo) == CLClasses.ShapeAreaCircleCalculator:
      jogo = jogo.jogo
    consec = funcs.calc_consec(jogo)
    #print jogo, consec
    try:
      consecDict[consec]+=1
    except KeyError:
      consecDict[consec]=1
    c = printOutMultiples(c)
    jogo = lgiObj.next()
  print c, consecDict
  pprint.print_dict(consecDict)
  return consecDict

#jogosObj = CLClasses.getJogosObj('lf')
#til5obj = tilc.Til(jogosObj, 5)
#til6obj = tilc.Til(jogosObj, 6)
#til10obj = tilc.Til(jogosObj, 10)
def seeTils(lgiObj, tipoJogo):
  jogo = lgiObj.first(); c=0
  print 'Please, wait ::', tipoJogo,'nOfCombines =' #, lgiObj.nOfCombines
  while jogo:
    patt = til5obj.generateLgiForJogoVsTilFaixas(jogo)
    c+=1
    print c, jogo, patt
    #if c % 10000 == 0:
      #print c, consecDict
    jogo = lgiObj.next()



  def doesItPass(self, til5pattern):
    for pos in range(len(til5pattern)):
      c = til5pattern[pos]
      n = int(c)
      if n < self.low(pos):
        return False
      if n > self.high(pos):
        return False
    return True


class RulerRepeat(object):
  pass

'''
  # singleton
  _instance = None
  def __new__(self, *args, **kargs):
    if self._instance is None: 
      self._instance = object.__new__(self, *args, **kargs)
      self._instance.initializeAttributes()
    return self._instance
  def initializeAttributes(self):
    self.tupleMaxQuantOfRepeatsNJogosAgo  = 1, 3 
    self.tupleMinQuantOfRepeatsNJogosAgo  = 2, 25 
    #self.mJogosFor1Repeat     = 
    #self.nOfXRepeatsForMJogos = 
    #self.mJogosForXRepeat     = 
    #self.valueOfXRepeats      = 
    self.maxAllowedRepeat     = 4
    self.minImposedRepeat     = 3 
'''

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
  filtro_obj = Filtre(jogoGerador, filter_function_list, pickled_fileobj)
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
