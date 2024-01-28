#!/usr/bin/env python
"""
fs/mathfs/combinatorics/IndicesCombinerForCombinations.py
  Contains the class IndicesCombiner that models a combinadic object (@see ref @wikipedia below)

Ref.: http://en.wikipedia.org/wiki/Combinadic
  combinadics Module
"""
import fs.mathfs.combinatorics.IndicesCombinerForCombinations as iCmb  # ic.IndicesCombiner


def adhoctest_instantiate_indicescombiner():
  """
  Default parameters to IndicesCombiner
  ic = IndicesCombiner(greatest_int_in_comb=0, size=1, overlap=True, i_array_in=None)
  Example:
    ic = iCmb.IndicesCombiner(2, 2, False)
  [0, 1]   [0, 2]   [1, 2]


  # print(ic.next())
  """
  ic = iCmb.IndicesCombinerForCombinations(4, 2, False)
  # print('IndicesCombiner object', ic)
  print('first', ic.first, ic.top)
  print('last', ic.last, ic.bottom)
  print('first_zeroless', ic.first_zeroless)
  print('get_first_given()', ic.get_first_given())
  print('all_set()', ic.all_sets_first_to_last())
  print('total_cmbs()', ic.total_cmbs)


def adhoctest():
  adhoctest_instantiate_indicescombiner()


if __name__ == '__main__':
  adhoctest()
