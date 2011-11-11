#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

this_var_is_just_to_avoid_recursive_local_imports=1
import valueCheckers
import HTMLGrabber
del this_var_is_just_to_avoid_recursive_local_imports

typeDict = {'nDoConcurso':int, 'dataDoSorteio':datetime.date}

for i in range(1, 7):
  fieldname = 'dezena%d' %i
  typeDict[fieldname]=int

typeDict['arrecadacaoTotal']=float

for postfix in ['DaSena', 'DaQuina', 'DaQuadra']:
  fieldname = 'ganhadores%s' %postfix
  typeDict[fieldname]=int

for postfix in ['DaSena', 'DaQuina', 'DaQuadra']:
  fieldname = 'rateio%s' %postfix
  typeDict[fieldname]=float

for postfix in ['DaSena', 'DaQuina', 'DaQuadra']:
  fieldname = 'ganhadores%s' %postfix

typeDict['acumuladoSimNao'] = int
typeDict['valorAcumulado']  = float
typeDict['estimativaDePremio'] = float
typeDict['acumuladoDeNatal'] = float

def getFieldType(fieldname):
  return typeDict[fieldname]

def returnMegasenaFieldNamesStr():
  return '''nDoConcurso
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
acumuladoDeNatal'''

fieldNames = []
def getFieldName(pos):
  global fieldNames
  if fieldNames == []:
    fieldNames = returnMegasenaFieldNamesStr()
  if pos < len(fieldNames):
    return fieldNames[pos]
  return None

class Attribute(dict):
  
  def __init__(self, name, value=None):
    self.__init__(name, value)
  def __set__(self, name, value):
    pass
  def fillInIsCurrencyIsDateIsInteger(self):
    if self.name.lower().startswith('data'):
      self.isDate = True
      return
    for phrase in ['ganhadores', 'dezena']:
      if self.name.lower().startswith('dezena'):
        self.isInteger = True
        return
    for phrase in ['rateio', 'arrecadacao', 'estimativa', 'valor']:
      if self.name.lower().startswith(phrase):
        attrObj.isCurrency = True
        return
    # if program flow gets here, it didn't find the datum's type
    print 'self', self.name
    raise ValueError, "it could not determine whether it's currency, it's date or it's integer"
  def setAttr(self, value):
    if self.isInteger():
      if not valueCheckers.checkIfValueIsInteger(value):
        raise TypeError, 'type error having an integer'
    if attrObj.isCurrency():
      if valueCheckers.checkIfValueIsCurrency(value):
        raise TypeError, 'type error having a currency'
      value = valueCheckers.normalizeDate(value)
    self.value = value
  def putIntoParamListAttrValueInOrder(values):
    index = HTMLGrabber.megasenaFieldNames.index(self.name)
    if len(values) < index:
      values[index] = self.value
    else:
      raise IndexError, 'index error in putIntoParamListAttrValueInOrder(values)'
  def __str__(self):
    outStr = '(attr: %s = %s)' %(self.name, self.value)

def test():
  c = Attribute(1)
  c.addAttr('dezena1', 25)
  
if __name__ == '__main__':
  test()



def returnMegasenaFieldLongNamesStr():
  return '''Concurso
Data Sorteio
1ª Dezena
2ª Dezena
3ª Dezena
4ª Dezena
5ª Dezena
6ª Dezena
Arrecadacao_Total
Ganhadores_Sena
Rateio_Sena
Ganhadores_Quina
Rateio_Quina
Ganhadores_Quadra
Rateio_Quadra
Acumulado
Valor_Acumulado
Estimativa_Prêmio
Acumulado_Natal'''

def getDBFieldLongNames():
  megasenaFieldNames = returnMegasenaFieldLongNamesStr().split('\n')
  return megasenaFieldNames

def mappingHtmlColumnsToSqlColumns():
  # html name versus sql name
  htmlColumns = '''
  
  '''
  return htmlColumns
