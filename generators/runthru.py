#/usr/bin/env python 

a=1
import LgiCombiner as lc
import funcs
#pourtouteslesclasses@yahoo.fr


def seeSomasInBetween(passed, jogo, **kargs):
  s1 = kargs['s1']
  s2 = kargs['s2']
  soma = sum(jogo)
  if soma >= s1 and soma <= s2:
    passed += 1
  return passed

def seeRem5(passed, jogo, **kargs):
  exclPatterns = kargs['exclPatterns']
  rem5pattern = funcs.calcRem5pattern(jogo)
  if rem5pattern not in exclPatterns:
    passed += 1
  return passed

passed = 0
def arcade(**kargs):
  func = kargs['func']
  jogo = lgiObj.first()
  while jogo:
    passed += func(passed, jogo, **kargs)
    jogo = lgiObj.next()
  print passed
  return passed


def prepForSeeSomasInBetween():
  s1In = sum(range(10,17))
  s2In = sum(range(45,45+7))
  arcade(func=seeSomasInBetween, s1=s1In, s2=s2In)
  return passed
  
def prepForSeeSomasInBetween():
  s1 = sum(range(10,17))
  s2 = sum(range(45,45+7))
  seeSomasInBetween(s1, s2)

if __name__ == "__main__":
  prepForSeeSomasInBetween()
  
