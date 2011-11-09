#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime #,  sys
import BeautifulSoup as bf

this_is_just_to_avoid_recursive_local_imports=1
from classesConcursoAndAttr import *
import constantsEtc
del this_is_just_to_avoid_recursive_local_imports

htmlDataFilename = 'D_MEGA.HTM'
htmlDataFilename = 'small.html'

class HtmlGrabberClass(object):
  def __init__(self, *args, **kwargs):
    object.__init__(self, *args, **kwargs)
    self.bsObj = None
    self.concursos = []
  def setHtmlDateFile(self, htmlDataFilename):
    self.htmlDataFilename = htmlDataFilename
    self.createSoupObj()
  def createSoupObj(self):
    htmlText = open(self.htmlDataFilename).read()
    self.bsObj = bf.BeautifulSoup(htmlText)
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
    attrName = constantsEtc.getFieldName( COLUMN_TRACKER - 1 )
    # print 'lin', nOfTheLine, 'col', COLUMN_TRACKER, attrName, value
    if concurso <> None:
      concurso.addAttr(attrName, value)
    COLUMN_TRACKER += 1
  return concurso

def processRowsAcrossTable(bsObj):
  # 1st level
  trs = bsObj.fetch('tr')
  nOfTheLine=1; concursos = []
  for tr in trs:
    # 2nd level
    concurso = processColumnsAcrossRow(tr)
    concursos.append(concurso)
    nOfTheLine+=1
  return concursos

if __name__ == '__main__':
  pass
