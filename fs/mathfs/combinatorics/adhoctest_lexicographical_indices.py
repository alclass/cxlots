#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/adhoctest_lexicographical_indices.py
  Contains adhoctests for class LgiCombiner and other related classes and functions
"""
import random
import sys
import IndicesCombiner as iCmb # for the comb(n, m) function
SUBINDO  = 2
DESCENDO = 1
counter = 0 # global


class Lexico:

  def __init__(self):
    self.counter = 0


def check_up_amount_in_array_carried(carried_array, lgi):
  size = len(carried_array); soma = 0
  for i in range(size):
    value = carried_array[i]
    pos_inv = size - i
    soma += iCmb.comb(value, pos_inv)
  if soma != lgi:
    errmsg = 'checkUpAmountInCarriedArray() ==>> soma (=%d) não igual a lgi (=%d) %s' %(soma, lgi, str(carried_array))
    raise ValueError(errmsg)


def transform_comb_in_lgi(comb_array, n_of_elems):
  lc = LgiCombiner(n_of_elems - 1, -1, comb_array)
  return lc.get_lgi()


def transform_lgi_in_comb(n_of_elems, size, lgi):
  lc = LgiCombiner(n_of_elems - 1, size)
  return lc.move_to(lgi)


def test_indices_combiner(upLimit, size):
  # signature IndsControl(upLimit=1, size=-1, overlap=True, iArrayIn=[])
  ind_comb = LgiCombiner(upLimit, size, True)
  c=0
  scrmsg = 'ind_comb = IndicesCombiner(%d, %d, True)' % (upLimit, size)
  print(scrmsg)
  s = ind_comb.first_given()
  set_with_ol = []
  while s:
    c+=1
    print(c, s)
    set_with_ol.append(list(s))
    s = ind_comb.next()
  set_without_ol = []
  ind_comb = LgiCombiner(upLimit, size, False)
  c=0
  scrmsg = 'ind_comb = IndicesCombiner(%d, %d, False)' % (upLimit, size)
  print(scrmsg)
  s = ind_comb.first_given()
  while s:
    c+=1
    print(c, s)
    set_without_ol.append(list(s))
    s = ind_comb.next()
  c=0; notThere = 0
  for w_ol in set_with_ol:
    c+=1
    print(c, w_ol,)
    if w_ol in set_without_ol:
      print(w_ol)
    else:
      notThere += 1
      print(notThere)

def pick_up_params():
  params = []
  up_limit = 5
  size    = 3
  for i in range(1, len(sys.argv)):
    params.append(sys.argv[i].lower())
  print('params', params)
  if '-uplimit' in params:
    index = params.index('-uplimit')
    print('index -uplimit', index)
    if index + 1 < len(params):
      try:
        up_limit = int(params[index + 1])
      except ValueError:
        pass
  if '-size' in params:
    index = params.index('-size')
    if index + 1 < len(params):
      try:
        size = int(params[index + 1])
      except ValueError:
        pass
  return up_limit, size

def adhoctest_shift_left(up_limit, size):
  ind_comb = LgiCombiner(up_limit, size, True, [2, 4, 5])
  scrmsg = 'ind_comb = IndicesCombiner(%d, %d, %s)' % (up_limit, size, ind_comb.overlap)
  print(scrmsg)
  print(ind_comb)
  scrmsg = 'adhoctest_shift_left()', ind_comb.shiftLeft()
  print(scrmsg)
  for i in range(7):
    next_i = ind_comb.next()
  print('next_i 7', next_i)
  print('adhoctest_shift_left()', ind_comb.shiftLeft())
  ind_comb = LgiCombiner(7, -1, True, [0,6,6,7,7])
  scrmsg = 'ind_comb = IndicesCombiner(%d, %d, %s)' % (up_limit, size, ind_comb.overlap)
  print(scrmsg)
  print(ind_comb)
  pos = 1
  vaium = ind_comb.vaiUmInPlace(pos)
  scrmsg = f'test pos={pos} vaium={vaium}'
  print(scrmsg)
  pos = 2
  lshift = ind_comb.shiftLeft(pos)
  scrmsg = f'test pos={pos} leftshift={lshift}'
  print(scrmsg)
  pos = 1
  scrmsg = 'test vai um(%d)' % (pos), ind_comb.vaiUmInPlace(pos)
  print(scrmsg)
  print('test vai um(%d)' %(pos), ind_comb.vaiUmInPlace(pos))
  print('test vai um(%d)' %(pos), ind_comb.vaiUmInPlace(pos))
  print('current', ind_comb.current())
  print('next_i', ind_comb.next())
  

def testPrevious(upLimit, size):
  ic = IndicesCombinerLgi(upLimit, size)
  print 'ic', ic
  print 'ic.next()', ic.next()
  print 'ic.previous()', ic.previous()
  for i in range(36):
    print i,'ic.next()', ic.next()
  for i in range(36):
    print i,'ic.previous()', ic.previous()


def testGetByLgi(upLimit, size):
  ic = LgiCombiner(upLimit, size)
  print 'ic', ic
  print 'ic.next()', ic.next()
  print 'ic.previous()', ic.previous()
  nOfComb = ic.n_of_combines
  #sys.exit(0)
  lgi = random.randint(0,nOfComb-1)
  msg = 'ic.move_to(lgi=%d)' %(lgi)
  #ans=raw_input(msg)
  #lgi = 31029 #21208
  #print 'ic.move_to(lgi=%d)' %(lgi), ic.move_to(lgi)
  for i in range(3):
    lgi = random.randint(0,nOfComb-1)
    ic.move_to(lgi)
    array = ic.currentSorted()
    array1 = ic.currentSortedFrom1()
    print i, 'ic.move_to(lgi=%d)' %(lgi), array, array1, 'lgi', ic.get_lgi()

def testTransforms():
  combArray = [14,10,5,1]; nOfElems = 20
  lgi = transform_comb_in_lgi(combArray, nOfElems)
  print 'lgi = transform_comb_in_lgi(combArray, nOfElems)', combArray, nOfElems, 'lgi', lgi
  nOfElems = 20; size = 4; lgi = 7
  combArray = transform_lgi_in_comb(nOfElems, size, lgi)
  print 'comb = transform_lgi_in_comb(nOfElems, size, lgi)', nOfElems, size, lgi, 'comb', combArray


def test_get_item():
  lgi_obj = LgiCombiner(59, 6)
  c=0
  for lgi in lgi_obj:
    print(lgi)
    c+=1
    if c>7:
      break


if __name__ == '__main__':
  pass
  test_get_item()
  '''
  lgiObj = LgiCombiner(59, 6)
  print lgiObj
  print lgiObj.current(), lgiObj.get_lgi()
  print lgiObj.next(), lgiObj.get_lgi()
  print lgiObj.move_to(100), lgiObj.get_lgi()
  print lgiObj.last(), lgiObj.get_lgi()
  print 'comb.comb(60,6)', comb.comb(60,6)

  nOfElems = 60
  upLimit, size = nOfElems-1, 6 #pick_up_params()
  print 'upLimit=%d :: size=%d ' %(upLimit, size)
  #ans = raw_input('ok ? ')
  #test_indices_combiner(upLimit, size)
  #testIndsControl()
  #adhoctest_shift_left(upLimit, size)
  #adhoctest_previous(upLimit, size)
  #testGetByLgi(upLimit, size)
  testTransforms()
  '''