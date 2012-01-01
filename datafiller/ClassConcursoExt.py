#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 04/12/2011

@author: friend
'''
import sys # datetime

a=1
import ClassConcursoEtc as conc
import sqlLayer as sl
sys.path.insert(0, '..')
import statmetrics.Til as tilMod
import statmetrics.funcsForStringPatternsEtAl as ffStr 


class ConcursoExt(conc.Concurso):
  '''
  This class extension intends to incorporate method getTilN() into Concurso objects
    and avoid circular package-module importing (between datafiller.ClassConcursoEtc and statmetrics.Til) 
    
  This Class "design" is scheduled to be changed in the future, for it's not good
    to copy over attributes from parent object to child object
  
  For the time being it's tightly coupled now, but some better solution will come up, hopefully
  
  '''

  def __init__(self, concurso):
    self.checkInitParameterConcurso(concurso)
    conc.Concurso.__init__(self)
    self.copyParentObj(concurso)

  def checkInitParameterConcurso(self, concurso):
    '''
    There are 3 tests/checks here:
    1) check whether concurso is None, it cannot be None
    2) check whether concurso is not an Instance, it must be an Instance
    3) check, knowing that it's an Instance, that attribute _classId has the String 'Concurso'
    
    2 and 3 are a bit awkward, but type(obj) in Python only informs the object is of <type 'instance'>
    As a goal, this method is meant to raise ValueError if parameter "concurso" is "not good"
    '''
    baseErrorMsg = 'Attempt to instantiate a ConcursoExt object ran into error number: ' 
    if concurso == None:
      errorMsg = '1 of 3, ie, concurso as an __init__() parameter to parent object is None'
      errorMsg = baseErrorMsg + errorMsg 
      raise ValueError, errorMsg
    elif str(type(concurso)) != "<type 'instance'>":
      errorMsg = '2 of 3, ie concurso parent object as an __init__() parameter is NOT of type <instance> :: its type is %s' %(str(type(concurso)))
      errorMsg = baseErrorMsg + errorMsg 
      raise ValueError, errorMsg
    elif concurso._classId != 'Concurso':
      errorMsg = '3 of 3 concurso parent object as an __init__() parameter has NOT the _classId set with string "Concurso" :: its type is %s' %(str(type(concurso)))
      errorMsg = baseErrorMsg + errorMsg 
      raise ValueError, errorMsg
      
    
  def copyParentObj(self, concurso):
    self.concursoDict = concurso.concursoDict
    self.fieldnamesInOrder = concurso.fieldnamesInOrder 

  def getTilN(self, tilN=5):
    nDoConcurso = self.concursoDict['nDoConcurso']
    tilObj = tilMod.TilMaker(tilN, nDoConcurso)
    tilSets = tilObj.getTilSets()
    if tilSets == None:
      return None 
    # print 'tilSets', tilSets  
    dezenas = self.getDezenas()
    tilPatternList = [0]*tilN
    for dezena in dezenas:
      for i in range(len(tilSets)):
        if dezena in tilSets[i]:
          # print 'found', dezena, 'inside i=',i, tilSets[i]   
          tilPatternList[i] += 1
          break
    tilPatternStr = ffStr.listToStr(tilPatternList)
    return tilPatternStr

def showTilsForConcursos(concFrom=None, concTo=None, tilN=None):
  concursos = sl.getListAllConcursosObjs()
  if concTo == None:
    concTo = len(concursos)
  if concFrom == None:
    concFrom = concTo - 100
    if concFrom < 1:
      concFrom = 1
  if tilN == None:
    tilN = 5
  count=0; tilPatternDict = {}
  for concurso in concursos[concFrom - 1 : concTo]:
    count+=1
    concursoExt = ConcursoExt(concurso) # an empty obj, just to clue its getTilN() method into concurso obj.
    #tilPatternStr = concursoExt.getTilN(5)
    # concurso.getTilN = concursoExt.getTilN
    tilPatternStr = concursoExt.getTilN(tilN)
    if tilPatternStr == None:
      print 'tilPatternStr == None'
      continue
    if tilPatternStr in tilPatternDict.keys():
      tilPatternDict[tilPatternStr]+=1
    else:
      tilPatternDict[tilPatternStr]=1
    nDoConcurso = concursoExt['nDoConcurso']
    dezenasStr = concursoExt.getDezenasPrintableInOrder()
    print nDoConcurso, dezenasStr, tilPatternStr, 'sum =', tilMod.sumUpTilPattern(tilPatternStr)  
    #concursoExt.concurso.getTilN =
  patterns = tilPatternDict.keys()
  patterns.sort()
  for pattern in patterns:
    print pattern, 'happened', tilPatternDict[pattern], 'times'  
  
# test adhoc
# test()
  
def fromShellToShowTilsForConcursos():
  fromArg = None; toArg = None; tilArg = None  
  for arg in sys.argv:
    token = arg.find('from=')
    if token > -1:
      fromArg = int(arg[len(token):])
      continue
    token = arg.find('to=')
    if token > -1:
      toArg = int(arg[len(token):])
      continue
    token = arg.find('til=')
    if token > -1:
      tilArg = int(arg[len(token):])
      continue
    if fromArg != None and toArg != None and tilArg != None:
      break
  showTilsForConcursos(fromArg, toArg, tilArg)

if __name__ == '__main__':
  if '-til' in sys.argv:
    fromShellToShowTilsForConcursos()
  else:
    print '''
    Usage: "<thispymodulename> -til from=<n1> to=<n2> til=<n>
           arguments from, to and til are optional.
'''
    
