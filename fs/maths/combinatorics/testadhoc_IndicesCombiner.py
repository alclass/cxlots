#!/usr/bin/env python
"""
fs/maths/combinatorics/IndicesCombiner.py
  Contains the class IndicesCombiner that models a combinadic object (@see ref @wikipedia below)

Ref.: http://en.wikipedia.org/wiki/Combinadic
  combinadics Module
"""
import copy
import sys
import unittest
import fs.maths.combinatorics.IndicesCombiner as iCmb  # ic.IndicesCombiner


def adhoctest_instantiate_indicescombiner():
  """
  Default parameters to IndicesCombiner
  ic = IndicesCombiner(up_limit=0, size=1, overlap=True, i_array_in=None)
  Example:
    ic = iCmb.IndicesCombiner(2, 2, False)
  [0, 1]   [0, 2]   [1, 2]
  """
  ic = iCmb.IndicesCombiner(4, 2, False)
  print('IndicesCombiner object', ic)
  print('current', ic.current())
  print('i_array', ic.i_array)
  # print(ic.next())
  print('first', ic.first)
  print('last', ic.last)
  print('first_zeroless', ic.first_zeroless)
  print('get_first_given()', ic.get_first_given())
  print('move_to_last_one()', ic.move_to_last_one())
  print('all_set()', ic.all_sets())
  print('total_comb()', ic.total_comb)


def adhoctest():
  adhoctest_instantiate_indicescombiner()


if __name__ == '__main__':
  adhoctest()
