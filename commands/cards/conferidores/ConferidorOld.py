#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, random, sys

import CLClasses
import funcsForCoincs as fCoincs
import lambdas
from cardprint import pprint


def getApostasFilename(sqlTable, nDoConc, ext='bet.txt'):
  apostasFilename = 'Apostas/%s-apostas-para-conc-%d.%s' %(sqlTable, nDoConc, ext)
  return apostasFilename

def initJogosObj(jogosObj):
  if type(jogosObj) == CLClasses.Jogos:
    return jogosObj
  if type(jogosObj) == str:
    standard2LetterName = jogosObj
    # an error will be raise in CLClasses.getJogosObj() if s2LN is inconsistent
    jogosObj = CLClasses.getJogosObj(standard2LetterName)
    return jogosObj
  # well, if it's neither types above, exception should be raised
  errorMsg = 'jogosObj is neither a CLClasses.Jogos nor a str %s' %(jogosObj)
  raise ValueError, errorMsg


def pickUpApostasFilenameParts(apostasFilename):
  filename = apostasFilename
  if apostasFilename.find('/'):
    filename = apostasFilename.split('/')[-1]
  filename = filename.rstrip('.bet.txt')
  pp = filename.split('-')
  sqlTable = pp[0]
  nDoConc  = int(pp[4])
  return sqlTable, nDoConc 


class Conferidor(object):

  def __init__(self, apostasFilename): #jogosObj, nDoConcDaAposta):
    '''
    Eg lf-apostas-para-conc-459.bet.txt
    '''
    if os.path.isfile(apostasFilename):
      self.apostasFilename = apostasFilename
    else:
      errorMsg = 'apostasFilename %s does not exist.' %(apostasFilename)
      raise ValueError, errorMsg
    
    sqlTable, nDoConc = pickUpApostasFilenameParts(self.apostasFilename)
    print 'sqlTable, nDoConc', sqlTable, nDoConc 
    self.jogosObj = initJogosObj(sqlTable)
    self.sqlTable = self.jogosObj.sqlTable
    self.nDoConcDaAposta = nDoConc
    self.nDoConc         = self.nDoConcDaAposta
    #self.apostasFilename = getApostasFilename(self.sqlTable, self.nDoConcDaAposta)
    self.initAcertosComPremio()
    self.checked = False

  def initAcertosComPremio(self):
    nDeDezenasSorteadas = self.jogosObj.nDeDezenasSorteadas
    self.acertosComPremio = [nDeDezenasSorteadas]
    if self.sqlTable == 'lf':
      self.acertosComPremio = range(11, nDeDezenasSorteadas + 1)
    elif self.sqlTable == 'ms':
      self.acertosComPremio = range(4, nDeDezenasSorteadas + 1)

  def confere(self):
    historyJogos = self.jogosObj.getJogos()
    ultimoNDoConc = len(historyJogos)
    if self.nDoConcDaAposta <= ultimoNDoConc:
      # ok history has it!
      self.historyTargetJogo = historyJogos[self.nDoConcDaAposta - 1]
      self.checkThru()
    else:
      self.checked = False


  def confereAgainstHistorico(self):
    self.nDePremiosAgainstHist = {}; self.totalDePremiosAgainstHist=0
    jogos = self.jogosObj.getJogos(); nDoJogo = 0
    for jogo in jogos:
      self.historyTargetJogo = list(jogo)
      self.historyTargetJogo.sort()
      nDoJogo += 1
      #print 'Checando contra Histórico nDoJogo', nDoJogo, self.historyTargetJogo
      self.checkThru()
      #self.showResults()
      self.acumPremios()
    print '*'*30
    print ' *** FINAL ***'
    premioTipos = self.nDePremiosAgainstHist.keys()
    for premioTipo in premioTipos:
      print 'premioTipo', premioTipo, ':', self.nDePremiosAgainstHist[premioTipo]
    print '*'*30


  def acumPremios(self):
    premioTipos = self.nDePremios.keys()
    for premioTipo in premioTipos:
      try:
        self.nDePremiosAgainstHist[premioTipo] += self.nDePremios[premioTipo]
      except KeyError:
        self.nDePremiosAgainstHist[premioTipo] = self.nDePremios[premioTipo]

  def checkThru(self):
    apostasFile = open(self.apostasFilename)
    nOfLines = 0; nDaAposta = 0
    line = apostasFile.readline()
    self.nDePremios = {}; self.totalDePremios=0
    while line:
      nOfLines += 1
      if line[0]=='#':
        line = apostasFile.readline()
        continue
      #print random.randint(0,9),
      jogo = pprint.trans_spacesep_numberstr_to_intlist(line)
      nDaAposta += 1
      #print nDaAposta, 'Conferindo aposta:', jogo
      nDeCoincs = fCoincs.getNOfCoincidences(self.historyTargetJogo, jogo)
      if nDeCoincs in self.acertosComPremio:
        self.totalDePremios+=1
        try:
          self.nDePremios[nDeCoincs] += 1 
        except KeyError:
          self.nDePremios[nDeCoincs] = 1 
      # below, print to screen last two premioTipos
      if nDeCoincs in self.acertosComPremio[-2:]:
        #print
        print self.totalDePremios,'/',nOfLines, 'nDeCoincs', nDeCoincs,'in',
        print pprint.number_list_to_str_commaless(jogo)
        #, 'against history', self.historyTargetJogo, 'in nDoConcDaAposta', self.nDoConcDaAposta
      line = apostasFile.readline()
    #print
    self.checked = True

  def showResults(self):
    if self.checked:
      self.printResults()
    else:
      print 'No results, probably sorteio has not yet occurred. self.checked:', self.checked

  def printResults(self):
    '''
    This method is private, how to mark it as thus in Python?
    '''
    print 'Results:'
    premioTipos = self.nDePremios.keys(); total = 0; totalMonetized = 0
    for premioTipo in premioTipos:
      subtotal = self.nDePremios[premioTipo]
      attr = 'rateio%d' %(premioTipo)
      value = self.jogosObj.getAttrFor(attr, self.nDoConc)
      monetized = subtotal * value
      print 'premioTipo', premioTipo, '=', subtotal,'valor', value, '$', monetized
      total += subtotal
      try:
        totalMonetized += float(monetized)
      except TypeError:
        pass
    print 'totalDePremios:', self.totalDePremios
    print 'totalDePremios:', total
    print 'totalMonetized', totalMonetized

def confere():
  if len(sys.argv) > 1:
    apostasFilename = sys.argv[1]
  else:
    print 'Por favor, entre o ficheiro (arquivo) de apostas a conferir.'
    sys.exit(0)
  doConfereAgainstHistorico = False
  conf = Conferidor(apostasFilename)
  if len(sys.argv) > 2:
    param = sys.argv[2]
    if param == '-a':
      doConfereAgainstHistorico = True
  if doConfereAgainstHistorico:
    conf.confereAgainstHistorico()
  else:
    conf.confere()
    conf.showResults()

if __name__ == '__main__':
  confere()
