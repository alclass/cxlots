#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Ref.: http://en.wikipedia.org/wiki/Combinadic
'''
import IndicesCombiner as ic
import CLClasses
import infodata

class Info(CLClasses.Base):

  def __init__(self, standard2LetterName):
    CLClasses.Base.__init__(self, standard2LetterName)
    self.comoJogo = infodata.lotsComoJogar[self.standard2LetterName]
    self.probs    = infodata.lotsProbs[self.standard2LetterName]
    self.faixasDeAcerto = self.probs.keys()
    self.faixasDeAcerto.sort()
    self.faixasDeAcerto.reverse()

  def __str__(self):
    outStr = CLClasses.Base.__str__(self)
    outStr += '\n probs: ' + str(self.probs)
    return outStr

class InfoJogo(Info):

  def __init__(self, nDoConc, standard2LetterName):
    Info.__init__(self, standard2LetterName)
    self.nDoConc = nDoConc

  def getPremio(self, nDeAcertos):
    table = self.standard2LetterName.lower()
    premio, nDeGanhadores = getPremioAndNDeGanhares(table, self.nDoConc, nDeAcertos)
    return premio

  def getNDeGanhadores(self, nDeAcertos):
    premio, nDeGanhadores = getPremioAndNDeGanhares(self.standard2LetterName.lower(), self.nDoConc, nDeAcertos)
    return nDeGanhadores

  def getValorAcumulado(self):
    valorAcumulado = 1
    return valorAcumulado

  def info(self):
    outStr = ''
    for nDeAcertos in self.faixasDeAcerto:
      premio, nDeGanhadores = getPremioAndNDeGanhares(self.standard2LetterName.lower(), self.nDoConc, nDeAcertos)      
      outStr += 'nDeAcertos=%d nDeGanhadores=%d premio=%f \n' \
        %(nDeAcertos, nDeGanhadores, premio)
    return outStr

  def __str__(self):
    return self.info()


def getPremioAndNDeGanhares(table, nDoConc, nDeAcertos):
  premio, nDeGanhadores = None, None
  premioField = 'premio' + str(nDeAcertos)
  nDeGanhadoresField = 'nDeGanhadores' + str(nDeAcertos)
  sql = "select `%(premioField)s`, `%(nDeGanhadoresField)s` from `%(table)s` where `nDoConc` =  `%(nDoConc)d`;" %{'premioField':premioField,'table':table,'nDoConc':nDoConc}
  conn = sf.getConnection()
  cursor = conn.cursor()
  cursor.execute(sql)
  rows = cursor.__rows
  if len(rows) == 1:
    premio = rows[0][0]
    nDeGanhadores = rows[0][1]
  return premio, nDeGanhadores

def testInfoClass():
  for standard2LetterName in CLClasses.standardNames:
    info = Info(standard2LetterName)
    print info

if __name__ == '__main__':
  testInfoClass()
