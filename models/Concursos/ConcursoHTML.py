#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import numpy #datetime
from sqlalchemy import Column, Float, Integer, Boolean #, DateTime # String,

import __init__
__init__.setlocalpythonpath()

import fs.dbfs.sqlfs.FieldsAndTypes as fat
import fs.datefs.converterForDateAndCurrency as conv

from ConcursoBase import ConcursoBase

class ConcursoHTML(ConcursoBase):
  '''
  This class, though it does not yet implement inheritance from dict,
    it has dict qualities with __setitem__() and __getitem__() 
  '''

  arrecadacao     = Column(Integer)
  ganhadoresSena  = Column(Integer)
  rateioSena      = Column(Float)
  ganhadoresQuina = Column(Integer)
  rateioQuina     = Column(Float)
  ganhadoresQuadra= Column(Integer)
  rateioQuadra    = Column(Float)
  foiAcumulado    = Column(Boolean)
  acumulado       = Column(Float)
  premioEstimado  = Column(Float)
  premioAcumNatal = Column(Float)
  
  concursoDict = {}
  
  def __init__(self):
    super(ConcursoHTML, self).__init__()
    self.concursoDict = {}
    self.fieldnamesInOrder = [] # this extra attribute will not be necessary in Python 3, for in Py3 it's possible to maintain order in a dict
    self.dezenas  = None  # self.dezenas is set "lazily"

  def transport_dict_into_attrs(self):
    '''
    fieldNamesInOrderStr 
    ==================== 
      nDoConc
      dataDoSorteio
      dezena1
      dezena2
      dezena3
      dezena4
      dezena5
      dezena6
      arrecadacaoTotal
      ganhadoresDaSena
      rateioDaSena
      ganhadoresDaQuina
      rateioDaQuina
      ganhadoresDaQuadra
      rateioDaQuadra
      acumuladoSimNao
      valorAcumulado
      estimativaDePremio
      acumuladoDeNatal
    '''
    self.formJogoCharOrigFromDictDezenas() # self.jogoCharOrig
    self.nDoConc         = self.concursoDict['nDoConc']
    self.date            = self.concursoDict['dataDoSorteio']
    self.arrecadacao     = self.concursoDict['arrecadacaoTotal']
    self.ganhadoresSena  = self.concursoDict['ganhadoresDaSena']
    self.rateioSena      = self.concursoDict['rateioDaSena']
    self.ganhadoresQuina = self.concursoDict['ganhadoresDaQuina']
    self.rateioQuina     = self.concursoDict['rateioDaQuina']
    self.ganhadoresQuadra= self.concursoDict['ganhadoresDaQuadra']
    self.rateioQuadra    = self.concursoDict['rateioDaQuadra']
    self.foiAcumulado    = self.concursoDict['acumuladoSimNao']
    self.acumulado       = self.concursoDict['valorAcumulado']
    self.premioEstimado  = self.concursoDict['estimativaDePremio']
    self.premioAcumNatal = self.concursoDict['acumuladoDeNatal']

  def transport_attrs_into_dict(self):
    self.splitJogoCharOrigIntoDictDezenas() # self.jogoCharOrig
    self.concursoDict['nDoConc'] = self.nDoConc
    self.concursoDict['dataDoSorteio'] = self.date
    self.concursoDict['arrecadacaoTotal'] = self.arrecadacao
    self.concursoDict['ganhadoresDaSena'] = self.ganhadoresSena
    self.concursoDict['rateioDaSena'] = self.rateioSena
    self.concursoDict['ganhadoresDaQuina'] = self.ganhadoresQuina
    self.concursoDict['rateioDaQuina'] = self.rateioQuina
    self.concursoDict['ganhadoresDaQuadra'] = self.ganhadoresQuadra
    self.concursoDict['rateioDaQuadra'] = self.rateioQuadra
    self.concursoDict['acumuladoSimNao'] = self.foiAcumulado
    self.concursoDict['valorAcumulado'] = self.acumulado
    self.concursoDict['estimativaDePremio'] = self.premioEstimado
    self.concursoDict['acumuladoDeNatal'] = self.premioAcumNatal

  def splitJogoCharOrigIntoDictDezenas(self):
    if self.jogoCharOrig != None and len(self.jogoCharOrig) == 2 * self.N_DE_DEZENAS:
      for i in range(1, 7):
        fieldname = 'dezena%d' %i
        index = (i - 1) * 2
        self.concursoDict[fieldname] = self.jogoCharOrig[index : index + 2]

  def formJogoCharOrigFromDictDezenas(self):
    self.jogoCharOrig = ''
    for i in range(1, 7):
      dezena_dictkeyname = 'dezena%d' %i
      dezena = self.concursoDict[dezena_dictkeyname]
      self.jogoCharOrig += str(dezena).zfill(2)
        
  def __setitem__(self, fieldname, value):
    shouldBeType = fat.getFieldType(fieldname)
    if type(value) != shouldBeType:
      raise TypeError, 'type error in __setitem__ attrName=%s and attrValue=%s type is %s, should be %s ' %(fieldname, str(value), str(type(value)), str(shouldBeType))
    self.concursoDict[fieldname] = value
    self.insertFieldnameInOrder(fieldname)

  def insertFieldnameInOrder(self, fieldname):
    # first case: if self.fieldnamesInOrder is empty, append it right away and return
    if len(self.fieldnamesInOrder) == 0:
      self.fieldnamesInOrder.append(fieldname)
      return
    indexPositionOfEnteringOne = fat.allowedFieldNamesInOriginalOrder.index(fieldname)
    indexPositionOfLastElement = fat.allowedFieldNamesInOriginalOrder.index(self.fieldnamesInOrder[-1])
    if indexPositionOfEnteringOne > indexPositionOfLastElement:
      # okay, problem solved, it can be appended (ie, inserted at the end) and routine should return
      self.fieldnamesInOrder.append(fieldname)
      return
    # the optimum time condition above did not happen, so let's loop thru it (it's not that big, so time is not a problem here)
    for i in range(0, len(self.fieldnamesInOrder)): 
      indexPositionOfCurrentElement = fat.allowedFieldNamesInOriginalOrder.index(self.fieldnamesInOrder[i])
      if indexPositionOfEnteringOne < indexPositionOfCurrentElement:
        self.fieldnamesInOrder.insert(i, fieldname)
        return
    # well, if program flow got to here, a exception should be raised
    raise IndexError, "could not insertFieldnameInOrder :: fieldname = %s " %fieldname 

  def __getitem__(self, fieldname):
    if fieldname in self.concursoDict.keys():
      return self.concursoDict[fieldname]
    return None

  def isDezenaInConcurso(self, dezena):
    if dezena in self.get_dezenas():
      return True
    return False
  
  def are_same_dezenas(self, compareDezenas):
    compareDezenas.sort()
    if compareDezenas == self.get_dezenas_in_orig_order():
      return True
    return False  

  def calcNDeAcertos(self, compareDezenas):
    nDeAcertos = 0
    for compareDezena in compareDezenas:
      if compareDezena in self.get_dezenas():
        nDeAcertos += 1
    return nDeAcertos 

  def is2ndPrize(self, compareDezenas):
    nDeAcertos = self.calcNDeAcertos(compareDezenas)
    if nDeAcertos == self.N_DE_SORTEADAS - 1:
      return True
    return False  

  def is3rdPrize(self, compareDezenas):
    nDeAcertos = self.calcNDeAcertos(compareDezenas)
    if nDeAcertos == self.N_DE_SORTEADAS - 2:
      return True
    return False  

  def isConcursoEqualTo(self, concurso2):
    for fieldname in self.fieldnamesInOrder:
      if self.concursoDict[fieldname] != concurso2[fieldname]:
        return False
    return True

  def get_contrajogos_as_dezenas_list_down_to_depth(self, depth=4, inclusive=True):
    '''
    This method is just a bypass to function get_contrajogos_as_dezenas_down_from(self, depth)
      in module ReadConcursosHistory in this 'models' package
    To avoid cross-importing, ReadConcursosHistory is imported dynamically here
    
    This bypassing is done in order to improve the class interface altogether
      and allow these contrajogos to be gotten at one sole instruction  
    '''
    if 0==1: # just to "deceive" the IDE, so that it'll not complain about ReadConcursosHistory being defined (it's a module that will be dynamically imported) 
      ReadConcursosHistory = None
#    try:
#      dir(ReadConcursosHistory)
#    except NameError:
#      
#       dynamic import
#      exec('import ReadConcursosHistory')
    if not inclusive:
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
    
  def __str__(self):
    self.transport_attrs_into_dict()
    outStr = ''
    for fieldname in self.concursoDict.keys():
      outStr += fieldname + ':' + str(self.concursoDict[fieldname]) + '; '
    outStr = outStr[ : -2]
    return outStr 

def convertRowListToHTMLConcursoObj(row):
  # the HTML nDoConc field must be an int number first of all, check this first
  try:
    value = row['nDoConc']
    try:
      value = int(value)
    except ValueError:
      return None
  except KeyError:
    return None
  concurso = ConcursoHTML()
  for fieldname in row.keys():
    value = row[fieldname]
    shouldBeType = fat.getFieldType(fieldname)
    if type(value) == shouldBeType:
      concurso[fieldname]=value
      continue
    # special case of 
    if fieldname == 'nDoConc':
      value = int(row[fieldname])
      concurso[fieldname]=value
      continue
    if fieldname.startswith('dezena'):
      value = int(row[fieldname])
      concurso[fieldname]=value
      continue
    if fieldname.startswith('ganhadoresDaQuadra'):
      value = int(row[fieldname])
      concurso[fieldname]=value
      continue
    if fieldname.startswith('ganhadoresDaQuina'):
      value = int(row[fieldname])
      concurso[fieldname]=value
      continue
    if fieldname.startswith('ganhadoresDaSena'):
      value = int(row[fieldname])
      concurso[fieldname]=value
      continue
    if fieldname == 'acumuladoSimNao':
      if value.lower().startswith('s'): # s = sim
        value = 1
      elif value.lower().startswith('n'): # n = não
        value = 0
      else:
        # dirty value
        raise ValueError, "dirty value in fieldname %s = %s" %(fieldname, str(value))
      concurso[fieldname]=value
      continue
    elif fieldname == 'dataDoSorteio':
      value = conv.convertToDatetimeDate(value)
      concurso[fieldname]=value
      continue
    elif shouldBeType == float:
      value = conv.convertToFloatAMoneyCurrencyNotInEnglishFormat(value)
      concurso[fieldname]=value
    else:
      # last try: see if it will enter as a string
      if type(value) == str:
        concurso[fieldname]=value
        continue
      raise ValueError, "could not enter value in a fieldname according the type rules :: value = %s type=%s" %(str(value), str(type(value)))
  return concurso

def testConcursoSample():
  c = ConcursoHTML()
  c['valorAcumulado']=1000000.00
  c['dezena6']=15
  c['nDoConc']=200
  c['dezena1']=25
  print c

def processConcursoHtmlRetrieval():
  concurso = ConcursoHTML()
  concurso = concurso.get_concurso_by_nDoConc()
  print 'concurso nº (last)', concurso
  nDoConc = 1411
  concurso = concurso.get_concurso_by_nDoConc(nDoConc)
  print 'concurso nº', nDoConc, concurso


def process():
  processConcursoHtmlRetrieval()

def adhoc_test():
  #testConcursoSample()
  slider = ConcursoHTML()
  concurso = slider.get_last_concurso()
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
