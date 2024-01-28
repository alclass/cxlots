#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/adhoctest_IndicesCombiner.py
  Contains adhoctest to the class IndicesCombiner that models a combinadic object
  (@see ref @wikipedia below)

import copy
import fs.mathfs.combinatorics.combinatoric_algorithms as ca  # ca.fact(n)
import fs.mathfs.combinatorics.IndicesCombiner_functions as ICf  # ICf.project_last_combinationlist
"""
import datetime
import sys
import fs.mathfs.combinatorics.IndicesCombinerForCombinations as iCmb  # ic.IndicesCombiner


def adhoctest_indicescombiner(up_limit, size):
  # signature IndsControl(upLimit=1, size=-1, overlap=True, iArrayIn=[])
  ind_comb = iCmb.IndicesCombinerForCombinations(up_limit, size, True)
  c = 0
  scrmsg = 'ind_comb = IndicesCombiner(%d, %d, True)' % (up_limit, size)
  print(scrmsg)
  s = ind_comb.ini_comb_given
  set_with_ol = []
  while s:
    c += 1
    print(c, s)
    set_with_ol.append(list(s))
    s = ind_comb.next()
  set_without_ol = []
  ind_comb = iCmb.IndicesCombinerForCombinations(up_limit, size, False)
  c = 0
  scrmsg = 'ind_comb = IndicesCombiner(%d, %d, False)' % (up_limit, size)
  print(scrmsg)
  s = ind_comb.get_first_given()
  while s:
    c += 1
    print(c, s)
    set_without_ol.append(list(s))
    s = ind_comb.next()
  c = 0
  not_there = 0
  for wol in set_with_ol:
    c += 1
    print(c, wol)
    if wol in set_without_ol:
      print(wol)
    else:
      not_there += 1
      print(not_there)


def pick_up_params():
  params = []
  up_limit = 5
  size = 3
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


def adhoctest_shiftleft(up_limit, size):
  ind_comb = iCmb.IndicesCombinerForCombinations(up_limit, size, True, [2, 4, 5])
  c = 0
  scrmsg = 'ind_comb = IndicesCombiner(%d, %d, %s)' % (up_limit, size, ind_comb.overlap)
  print(scrmsg)
  print(ind_comb)
  print('adhoctest_shift_left()', ind_comb.foward_n_positions())
  next_i = None
  for i in range(7):
    next_i = ind_comb.next()
  print('next_i 7', next_i)
  print('adhoctest_shift_left()', ind_comb.foward_n_positions())
  ind_comb = iCmb.IndicesCombinerForCombinations(7, -1, True, [0, 6, 6, 7, 7])
  scrmsg = 'ind_comb = IndicesCombiner(%d, %d, %s)' % (up_limit, size, ind_comb.overlap)
  print(scrmsg)
  print(ind_comb)
  pos = 1
  vai_um = ind_comb.vai_um_in_place(pos)
  scrmsg = f'test pos={pos} vai_um={vai_um}'
  print(scrmsg)
  pos = 2
  shifleft = ind_comb.foward_n_positions(pos)
  scrmsg = f'adhoctest pos={pos} shift_left {shifleft}'
  print(scrmsg)
  pos = 1
  vai_um = ind_comb.vai_um_in_place(pos)
  scrmsg = f'adhoctest pos={pos} shift_left {shifleft}'
  print(scrmsg)
  vai_um = ind_comb.vai_um_in_place(pos)
  scrmsg = f'adhoctest pos={pos} shift_left {shifleft}'
  print(scrmsg)
  vai_um = ind_comb.vai_um_in_place(pos)
  scrmsg = f'adhoctest pos={pos} shift_left {shifleft}'
  print(scrmsg)
  print('current', ind_comb.current)
  print('next_i', ind_comb.next())
  

def adhoctest_previous(up_limit, size):
  ic = iCmb.IndicesCombinerForCombinations(up_limit, size, True, [0, 2, 12])
  print('ic', ic)
  print('ic.next()', ic.next())
  print('ic', ic)
  print('ic.previous()', ic.previous())
  for i in range(36):
    print('ic.previous()', ic.previous())


def adhoc_test3():
  """
  sc = SetsCombiner()
  worksetWithQuantity = ([1,2,3], 2)
  sc.addSetWithQuantities(worksetWithQuantity)
  worksetWithQuantity = ([4,5,6], 2)
  sc.addSetWithQuantities(worksetWithQuantity)
  for ws in sc.getAllSetsCombinationNonRecursively():
    print 'ws', ws
  """
  ic = iCmb.IndicesCombinerForCombinations(4, 2, False); c=0
  for ws in ic.gen_all_sets():
    c += 1
    print(c, ws)


def ynext():
  for i in range(10):
    yield i


def test_yield():
  for i in ynext():
    print(i)


def adhoc_test():
  ic = iCmb.IndicesCombinerForCombinations(3, 2, False)
  print(ic)
  print('first', ic.first_comb, 'last', ic.last_comb,  'size', ic.size)
  for i, comb in enumerate(ic.gen_all_cmbs_or_those_bw_ini_fim_if_given()):
    print(i, comb)
  ic = iCmb.IndicesCombinerForCombinations(4, 4, False)
  print(ic)
  print('first', ic.first_comb, 'last', ic.last_comb,  'size', ic.size)
  for i, comb in enumerate(ic.gen_all_cmbs_or_those_bw_ini_fim_if_given()):
    print(i, comb)
  ic = iCmb.IndicesCombinerForCombinations(5, 5, False)
  print(ic)
  print('first', ic.first_comb, 'last', ic.last_comb,  'size', ic.size)
  for i, comb in enumerate(ic.gen_all_cmbs_or_those_bw_ini_fim_if_given()):
    print(i, comb)
  ic = iCmb.IndicesCombinerForCombinations(6, 3, False)
  print(ic)
  print('first', ic.first_comb, 'last', ic.last_comb,  'size', ic.size)
  for i, comb in enumerate(ic.gen_all_cmbs_or_those_bw_ini_fim_if_given()):
    print(i, comb)


def adhoctest_output_combinations_for_megasena_large_set():
  # count execution time for the large MegaSena combination generation (next() with yield)
  start_time = datetime.datetime.now()
  ic = iCmb.IndicesCombinerForCombinations(60, 6, False)
  for i, comb in enumerate(ic.get_all_cmbs_or_those_bw_ini_fim_if_given(cut_off=10)):
    print(i, comb)
  print(ic)
  print('first', ic.first_comb, 'last', ic.last_comb,  'size', ic.size)
  print('='*30)
  end_time = datetime.datetime.now()
  time_elapsed = end_time - start_time
  print('end_time', end_time, 'start_time', start_time)
  print('time_elapsed', time_elapsed)


if __name__ == '__main__':
  """
  adhoc_test()
  """
  adhoctest_output_combinations_for_megasena_large_set()
