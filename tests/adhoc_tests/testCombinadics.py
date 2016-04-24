#!/usr/bin/env python
#-*-coding:utf8-*-

justAllocateSomeMemoryBeforeImporting = 1
import combinador
import Sena
'''
Ref.: http://en.wikipedia.org/wiki/Combinadic
'''

def findIndexFromCombination(dezenas):
  # Dezenas are from 1 to 60, they should be from 0 to 59, decreasing 1 below:	
  for i in range(6):
    dezenas[i] -= 1
  # Now check it is in descending order
  for i in range(1,6):
    if dezenas[i] > dezenas[i-1]:
      #raise 'Dezenas are not in descending order'
      dezenas.sort()
      dezenas.reverse()
      break
  #print dezenas
  index = 0
  for i in range(6):
    m = dezenas[i]
    r = 6 - i
    c=combinador.comb(m,r)
    index += c
    #print 'c(%d,%d)=%d' %(m,r,c)
  #print 'index', int(index)
  return index

def testIndexUpperLimit():
  total=0
  for r in range(6,0,-1):
    m = 53+r
    c=combinador.comb(m,r)
    print 'c(%d,%d)=%d' %(m,r,c)
    total+=c
  print 'total', total
  c=combinador.comb(60,6)
  print 'c=combinador.comb(60,6)', c
  print '(total == c-1)', total == c - 1

LIMITE_MAX_COMB60_6A6 = combinador.comb(60,6)
def findDezenasFromIndexNonRecursive(index, dezenasOut=[None]*6, soma=0, pos=6, MAX_LIMIT = LIMITE_MAX_COMB60_6A6 - 1):
  '''
  This method is sequential in nature, ie, it runs the indices upward one step at a time.
  There is an alternative (and recursive) method which does middle point searches aiming better speed.
  '''
  if index > MAX_LIMIT:
    errorMsg = 'Index given (%d) has extrapolated maximum possible index which is %d.' %(index, MAX_LIMIT)
    raise IndexError, errorMsg
  if index == 0:
    return [6,5,4,3,2,1]
  for pos in range(6,0,-1):
    ini = pos 
    for d in range(ini,62):  # 61 is just to allow the algorithm making d minus 1 after soma+adding is > index
      adding = combinador.comb(d-1,pos)
      #print 'adding', adding, 'soma', soma, 'd', d
      if soma + adding == index:
        #print 'adding + soma', adding + soma, 'd', d, 'pos', 6 - pos
        dezenasOut[6 - pos]=d
	if pos > 1:# and adding == 0:
	  for posJ in range(pos-1,0,-1):
            #print 'd', posJ,  'pos', 6 - posJ
	    dezenasOut[6-posJ]=posJ
	return dezenasOut
      elif soma + adding > index:
        #print 'adding + soma', adding + soma, 'd', d-1, 'pos', 6 - pos
        dezenasOut[6 - pos]=d-1
	soma = somaAnt
	break
      somaAnt = soma + adding
  # it's been checked that even if index is greater than Comb(60,6) or whatever max limit is, it's not gonna get here, so the solution was to raise error above (in fact, in findDezenasFromIndex1(...)
  errorMsg = 'It has extrapolated maximum possible index Comb(60,6).'
  raise IndexError, errorMsg

def finishUpFindDezenas(dezenasOut, pos, d):
  return dezenasOut

def findDezenasFromIndex(index, soma, somaAnt, d1, d, d2, pos, posAnt, dezenasOut):
  somaAnt = somaAnt
  soma += combinador.comb(d, pos)
  if soma == index:
    return finishUpFindDezenas(dezenasOut, pos, d)
  # this is the condition to move pos to the right ie pos -= 1
  if soma > index:
    if somaAnt < index:
      soma = somaAnt
      pos -= 1
      if pos == 0:
        errorMsg = 'Got to the end of the 6-array and could not equalize INDEX.'
        raise IndexError, errorMsg
      isSomaAntBelowIndex = False
      return FindDezenasFromIndex(indexIn,dezenasOut,soma,somaAnt,1,30,60,pos)
    else: # somaAnt is > index
      dAnt = d
      d = (d + d1) / 2
      d1 = dAnt
      somaAnt = soma
      return FindDezenasFromIndex(indexIn,dezenasOut,soma,somaAnt,d1,d,d2,pos)
  if soma < index:
    if somaAnt < index:
      dAnt = d
      d = (d + d2) / 2
      d2 = dAnt
      somaAnt = soma
      return FindDezenasFromIndex(indexIn,dezenasOut,soma,somaAnt,d1,d,d2,pos)
      soma = somaAnt
    if somaAnt > index:
      dAnt = d
      d = (d + d2) / 2
      if d==d2 or d+1==d2:
        dezenasOut[pos]=d
	somaAnt = None
	return FindDezenasFromIndex(indexIn,dezenasOut,soma,somaAnt,1,30,60,pos-1)
      d2 = dAnt
      somaAnt = soma
      return FindDezenasFromIndex(indexIn,dezenasOut,soma,somaAnt,d1,d,d2,pos)
    
    if d1 + 1 == d:
      errorMsg = 'Can not continue from here, d1 + 1 is = d.'
      raise IndexError, errorMsg
    dAnt = d
    d = (d + d1)/2  # middle-point again
    d2 = dAnt
  if soma < index and somaAnt < index:
    dAnt = d
    d = (d + d2)/2
    d1 = dAnt
    return FindDezenasFromIndex(index, soma, somaAnt, d1, d, d2, pos, posAnt, dezenasOut)


def test1():
  lastJogo = Sena.jogosPool.getLastJogo()
  print lastJogo
  FindIndexFromCombination(lastJogo.getDezenas())
  index = FindIndexFromCombination([1,2,3,4,5,6])
  assert(index, 0)
  FindIndexFromCombination([1,2,3,4,5,7])
  assert(index, 1)
  testIndexUpperLimit()

if __name__ == '__main__':
  #test1()
  a=50063849
  for i in range(a,a+11):#45057474,45057476):
    dezenas = findDezenasFromIndexNonRecursive(i)
    print 'index', i, dezenas,
    indexBack = findIndexFromCombination(dezenas)
    print 'asserting',i,'and', indexBack
    assert(i==indexBack)
