#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime #,  sys
import BeautifulSoup as bf
import sqlite3

this_is_just_to_avoid_recursive_local_imports=1
import ClassConcursoEtc as conc
import FieldsAndTypes as fat
del this_is_just_to_avoid_recursive_local_imports

htmlDataFilename = 'D_MEGA.HTM'
htmlDataFilename = 'small.html'

class HtmlGrabberClass():
  def __init__(self, htmlDataFilename='D_MEGA.HTM'):
    self.htmlDataFilename = htmlDataFilename
    self.parseToDataStru()
  def createSoupObj(self):
    htmlText = open(self.htmlDataFilename).read()
    '''
    Because of Portuguese accents in headers and in SIM/NÃO row values
      and the fact that the HTML is probably iso-8859-1 (Latin1) instead of UTF-8
    the unicode function raises UnicodeDecodeError
      if optional parameter errors is not set either to 'ignore' or 'replace'
      we chose 'ignore' because we only read the first character of field acumuladoSimNao,
      so it's either 'S' or 'N' coinciding with its ASCII/UTF-8 codes
    '''
    htmlText = unicode( htmlText , errors = 'ignore' ) 
    self.bsObj = bf.BeautifulSoup(htmlText)
  def parseToDataStru(self):
    self.createSoupObj()    
    if self.bsObj <> None: 
      self.concursos = processRowsAcrossTable(self.bsObj)
  def generateSqlInsert(self):
    outStr = '\n' + '='*30 + '\n'
    outStr += '============ Concursos ============'
    outStr += '\n' + '='*30 + '\n'
    for concurso in self.concursos:
      outStr += str(concurso.sqlInsert())
      outStr += '\n'
      #outStr += '\n' + '='*30 + '\n'
    outStr += 'Total: %d' %(len(self.concursos))
    return outStr
    
  def testPrintNDoConc(self):      
    outStr = '\n' + '='*30 + '\n'
    outStr += '============ testPrintNDoConc() ============'
    outStr += '\n' + '='*30 + '\n'
    for concurso in self.concursos:
      nDoConc = concurso['nDoConcurso']
      if nDoConc == None:
        nDoConc = -1
      outStr += '%d,' %nDoConc
    return outStr
  def __str__(self):
    outStr = '\n' + '='*30 + '\n'
    outStr += '============ Concursos ============'
    outStr += '\n' + '='*30 + '\n'
    for concurso in self.concursos:
      outStr += str(concurso)
      outStr += '\n' + '='*30 + '\n'
    outStr += 'Total: %d' %(len(self.concursos))
    return outStr

nOfTheLine = 0
def processColumnsAcrossRow(tr):
  global nOfTheLine
  nOfTheLine += 1
  tds = tr.fetch('td')
  COLUMN_TRACKER = 1; row = {}
  for td in tds:
    value = str(td.string) # this typecast is to avoid propagation of type(value)=<class 'BeautifulSoup.NavigableString'>
    fieldname = fat.allowedFieldNamesInOriginalOrder[COLUMN_TRACKER - 1]
    row[fieldname] = value
    COLUMN_TRACKER += 1
  # print 'row', row
  concurso = conc.convertRowListToConcursoObj(row)
  return concurso

def processRowsAcrossTable(bsObj):
  # 1st level
  trs = bsObj.fetch('tr')
  nOfTheLine=1; concursos = []
  for tr in trs:
    # 2nd level
    concurso = processColumnsAcrossRow(tr)
    if concurso != None:
      concursos.append(concurso)
      nOfTheLine+=1
  return concursos


def testGrabber():
  grabber = HtmlGrabberClass()
  # print grabber.testPrintNDoConc()


if __name__ == '__main__':
  pass
  testGrabber()