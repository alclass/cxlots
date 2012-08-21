#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''

#import datetime #,  
import BeautifulSoup as bf

import sys
import localpythonpath
localpythonpath.setlocalpythonpath()

import models.ConcursoHTML as conc
import models.FieldsAndTypes as fat
# import models.JogoSlider.JogoSlider
from models.ConcursoSlider import ConcursoSlider

import local_settings as ls
class ConcursoHTMLScraper(object):

  def __init__(self, htmlDataFilename = ls.MS_DATAFILE_ABSPATH):
    self.htmlDataFilename = htmlDataFilename
    self.concursoSlider = ConcursoSlider(conc.ConcursoHTML)
    self.process_flow()
    self.print_concursos()
    self.save_concursos_in_db()
    
  def process_flow(self):    
    self.parseToDataStru()
    self.convert_concursos_fieldtypes()

  def parseToDataStru(self):
    self.createSoupObj()    
    if self.bsObj <> None: 
      self.concursos = processRowsAcrossTable(self.bsObj)

  def convert_concursos_fieldtypes(self):
    for concurso in self.concursos:
      concurso.transport_dict_into_attrs()

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

  def print_concursos(self):      
    outStr = '\n' + '='*30 + '\n'
    outStr += '============ print_concursos() ============'
    outStr += '\n' + '='*30 + '\n'
    print outStr
    for concurso in self.concursos:
      nDoConc = concurso['nDoConc']
      if nDoConc == None:
        nDoConc = -1
      print nDoConc, concurso

  def save_concursos_in_db(self):
    print '========== save_concursos_in_db() ============'
    total_db_concursos = self.concursoSlider.get_total_concursos()
    total_html_concursos = len(self.concursos)
    print 'total_db_concursos', total_db_concursos
    print 'total_html_concursos', total_html_concursos
    if total_html_concursos <= total_db_concursos:
      return
    concursos_to_insert = []
    for nDoConc in range(total_db_concursos + 1 , total_html_concursos + 1):
      index = nDoConc - 1 
      concurso = self.concursos[index]
      expectedNDoConc = concurso['nDoConc']
      print 'expectedNDoConc', expectedNDoConc
      if expectedNDoConc == None:
        print 'Stopping expectedNDoConc == None.'
        sys.exit(0)
      concurso.transport_dict_into_attrs()
      concursos_to_insert.append(concurso)
    self.concursoSlider.bulk_insert(concursos_to_insert)

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
  concurso = conc.convertRowListToHTMLConcursoObj(row)
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
  ConcursoHTMLScraper()

def adhoc_test():
  testGrabber()

def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
