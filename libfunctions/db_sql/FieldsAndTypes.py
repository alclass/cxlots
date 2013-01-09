#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
'''

Functionality to be EXPORTED to other modules:
==============================================

This module keeps two data sets:

1) a list called allowedFieldNamesInOriginalOrder

This list just stores the fields in a Sena HTML table but with different names, for names were standardized here


2) a dict (hash map) called typeDict

This dict keeps the pair fieldname and its expected python-type. Example: {nDoConcuso:int},
   this means the variable nDoConcuso must be of the int type.


Functionality NOT to be EXPORTED to other modules:
==============================================

[1]
At the end, there is a string with all standardized names just to be used for comparison with allowedFieldNamesInOriginalOrder
If something differs, either order in which the fields must happpen, or fields quantity differs, execution will break.

[2]
A second comparison is to done again the HTML as it is updated when a new zip file is downloaded
This test should only run when a new HTML is in place.

It is a behind-the-scenes functionality with the purpose of revealing that an update to this script should happen.
'''

fieldNamesInOrderStr = '''nDoConc
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

allowedFieldNamesInOriginalOrder = fieldNamesInOrderStr.split('\n')

typeDict = {'nDoConc':int, 'dataDoSorteio':datetime.date}

for i in range(1, 7):
  fieldname = 'dezena%d' %i
  typeDict[fieldname] = int

fieldname = 'arrecadacaoTotal'
typeDict[fieldname] = float

for postfix in ['DaSena', 'DaQuina', 'DaQuadra']:
  fieldname = 'ganhadores%s' %postfix
  typeDict[fieldname]=int

for postfix in ['DaSena', 'DaQuina', 'DaQuadra']:
  fieldname = 'rateio%s' %postfix
  typeDict[fieldname]=float

for postfix in ['DaSena', 'DaQuina', 'DaQuadra']:
  fieldname = 'ganhadores%s' %postfix

fieldname = 'acumuladoSimNao'
typeDict[fieldname] = int

fieldname = 'valorAcumulado'
typeDict[fieldname] = float

fieldname = 'estimativaDePremio'
typeDict[fieldname] = float

fieldname = 'acumuladoDeNatal'
typeDict[fieldname] = float

if len(typeDict) != len(allowedFieldNamesInOriginalOrder):
  raise IndexError, "len(typeDict)=%d != len(allowedFieldNamesInOriginalOrder=%d)" %(len(typeDict), len(allowedFieldNamesInOriginalOrder))

def getFieldType(fieldname):
  return typeDict[fieldname]


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
Acumulado_Mega_da_Virada'''

def getDBFieldLongNames():
  megasenaFieldNames = returnMegasenaFieldLongNamesStr().split('\n')
  return megasenaFieldNames

def mappingHtmlColumnsToSqlColumns():
  # html name versus sql name
  htmlColumns = '''
  
  '''
  return htmlColumns

if __name__ == '__main__':
  pass
  print allowedFieldNamesInOriginalOrder
  print typeDict
