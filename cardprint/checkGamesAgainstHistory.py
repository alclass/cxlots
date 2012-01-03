#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 31/12/2011

@author: friend
'''
import sys

sys.path.insert(0,'..')
import datafiller.sqlLayer as sl
import statmetrics.algorithmsForCombinationsEtAl as algoComb

def pickUpDezenas(acceptAnyArraySize=False):
  '''
  This function reads shell arguments from the command line
  If acceptAnyArraySize it reads more the concurso size (number of dozens) for it's useful for betting more dozens
  '''
  dezenas = []
  for arg in sys.argv[2:]:
    dezena = int(arg)
    # protect against a repeat
    if dezena < 1 or dezena > 60:
      continue
    if dezena not in dezenas: 
      dezenas.append(dezena)
    else:
      continue
    if not acceptAnyArraySize and len(dezenas) == 6:
      break
  if not acceptAnyArraySize and len(dezenas) != 6:
    print 'len(dezenas=%s) != 6 ==>> program cannot continue.' %(str(dezenas))
    sys.exit(1)
  dezenas.sort()
  return dezenas

class CheckWithHistory:
  '''
  This class does the back-comparing taking as arguments a dozens set
    and the top number of concurso from where it is to be compared from top to bottom 
  '''

  def __init__(self, dezenasToCompare, upToConcursoN=None):
    self.dezenasToCompare = dezenasToCompare
    self.upToConcursoN    = upToConcursoN
    self.sameAsNDoConcs = []
    self.prize2NDoConcs = []
    self.prize3NDoConcs = []
    self.histogramNDeAcertos = {}
    self.checkAgainstHistory()

  def checkAgainstHistory(self):
    concursos = sl.getListAllConcursosUpTo(self.upToConcursoN)
    for concurso in concursos:
      nDeAcertos = concurso.calcNDeAcertos(self.dezenasToCompare)
      if nDeAcertos in self.histogramNDeAcertos.keys():
        self.histogramNDeAcertos[nDeAcertos] += 1
      else:
        self.histogramNDeAcertos[nDeAcertos] = 1
      if concurso.isSameGame(self.dezenasToCompare):
        self.sameAsNDoConcs.append(concurso['nDoConcurso'])
        #print dezenasToCompare, 'IS SAME AS', concurso['dezenas']
      elif concurso.is2ndPrize(self.dezenasToCompare):
        self.prize2NDoConcs.append(concurso['nDoConcurso'])
        #print dezenasToCompare, 'is2ndPrize (quina)', concurso['dezenas']
      elif concurso.is3rdPrize(self.dezenasToCompare):
        self.prize3NDoConcs.append(concurso['nDoConcurso'])
        #print dezenasToCompare, 'is3rdPrize (quadra)', concurso['dezenas']

def backComparator():
  '''
  Called from cli parameter 'backcomp'
  '''
  concursos = sl.getListAllConcursosObjs()
  for nDoConc in range(len(concursos), 1, -1):
    nDoConcMinusOneForIndex = nDoConcAnterior = nDoConc - 1
    concurso = concursos[nDoConcMinusOneForIndex] 
    checker = CheckWithHistory(concurso.getDezenasInOrder(), nDoConcAnterior)
    print 'for', nDoConc, concurso.getDezenasPrintableInOrder(), checker.sameAsNDoConcs, checker.prize2NDoConcs, checker.prize3NDoConcs, checker.histogramNDeAcertos

def compareFromUserFreeInputArgs(acceptAnyArraySize=False):  
  '''
  Entrance from check (or check+, via compareFromUserFreeInputArgsMoreDezenas()) cli argument
  The user enters a dozens set for comparison with History
  '''
  dezenasToCompare = pickUpDezenas(acceptAnyArraySize)
  checker = CheckWithHistory(dezenasToCompare)
  if acceptAnyArraySize:
    nDeDezenas = len(dezenasToCompare)
    print 'Comparing with', nDeDezenas, 'dozens :: combinações', algoComb.combineNbyC(nDeDezenas, 6)
  print 'for [shell input]', dezenasToCompare, checker.sameAsNDoConcs, checker.prize2NDoConcs, checker.prize3NDoConcs, checker.histogramNDeAcertos

def compareFromUserFreeInputArgsMoreDezenas():
  '''
  Entrance from check+ cli argument
  It sets acceptAnyArraySize to True and calls compareFromUserFreeInputArgs()
  The user enters a dozens set for comparison with History
  '''
  compareFromUserFreeInputArgs(acceptAnyArraySize=True)

def doStatsComparison():
  print 'doStatsComparison() IS NOT IMPLEMENTED YET.'
  
cliParameters = {'check':(compareFromUserFreeInputArgs, 'To check a combination-game against History'), \
                 'check+':(compareFromUserFreeInputArgsMoreDezenas, 'To check a combination-game against History'), \
                 'stats':(doStatsComparison, 'To doStatsComparison.'),\
                 'backcomp':(backComparator, 'To backComparator.'),\
                 } 

def showCliParameters():
  options = cliParameters.keys()
  options.sort()
  print '='*20
  print sys.argv[0], 'Options:'
  print '='*20
  for option in options:
    description = cliParameters[option][1]
    print option, '==>>', description

def processCliOptions():
  if len(sys.argv) > 1:
    optionIn = sys.argv[1].lower()
    options = cliParameters.keys()
    if optionIn in options:
      func = cliParameters[optionIn][0]
      func()
    else:
      showCliParameters()
  else:
    showCliParameters()

if __name__ == '__main__':
  processCliOptions()
