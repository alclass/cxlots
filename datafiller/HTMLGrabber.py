#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime #,  sys
import BeautifulSoup as bf

this_is_just_to_avoid_recursive_local_imports=1
from classesConcursoAndAttr import *
del this_is_just_to_avoid_recursive_local_imports


def mappingHtmlColumnsToSqlColumns():
  # html name versus sql name
  htmlColumns = '''
  
  '''

htmlDataFile = 'D_MEGA.HTM'
htmlDataFile = 'small.html'


fieldNamesStr='''Concurso
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
megasenaFieldNames=fieldNamesStr.split('\n')

class HtmlGrabberClass(object):
  def __init__(self, *args, **kwargs):
    object.__init__(self, *args, **kwargs)
    self.bsObj = None
    self.concursos = []
  def setHtmlDateFile(self, htmlDataFile):
    self.htmlDataFile = htmlDataFile
    self.htmlData = open(htmlDataFile).read()
    self.bsObj = bf.BeautifulSoup(text)
  def parseToDataStru(self):
    if self.bsObj <> None: 
      self.concursos = processRowsAcrossTable(self.bsObj)


def processColumnsAcrossRow(tr):
  tds = tr.fetch('td')
  COLUMN_TRACKER = 1; concurso = None
  for td in tds:
    value = td.string
    if COLUMN_TRACKER == 1:
      concurso = Concurso(value)
    attrName = fieldNames[ COLUMN_TRACKER - 1 ]
    print 'lin', nOfTheLine, 'col', COLUMN_TRACKER, attrName, value
    if concurso <> None:
      concurso.addAttr(attrName, value)
    COLUMN_TRACKER += 1
  return concurso

def processRowsAcrossTable(bsObj):
  # 1st level
  trs = self.bsObj.fetch('tr')
  nOfTheLine=1; concursos = []
  for tr in trs:
    # 2nd level
    concurso = processColumnsAcrossRow(tr)
    concursos.append(concurso)
    nOfTheLine+=1
  return concursos

if __name__ == '__main__':
  pass
