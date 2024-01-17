#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/test_decrescent_combiner.py
  Contains unit-tests for fs/mathfs/combinatorics/decrescent_combiner.py

"""
import unittest
import fs.mathfs.combinatorics.decrescent_combiner as dc  # dc.DecrescentCombiner


class TestDecrescentCombiner(unittest.TestCase):

  def test_1(self):
    """
    cmber = DecrescentCombiner(startint=7, nslots=4, upto=6)
    cmber.recurs_combine_n_make_sumsets()
    print(cmber)
    cmber = DecrescentCombiner(startint=12, nslots=3, upto=4)
    cmber.recurs_combine_n_make_sumsets()
    print(cmber)
    """
    # t1
    startint, nslots, upto = 3, 6, 6
    cmber = dc.DecrescentCombiner(startint=startint, nslots=nslots, upto=upto)
    cmber.recurs_combine_n_make_sumsets()
    returned_combs = cmber.combs
    expected_combs = [[3, 3], [3, 2, 1], [3, 1, 1, 1], [2, 2, 2], [2, 2, 1, 1], [2, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]
    self.assertEqual(expected_combs, returned_combs)
    not_greater_than_slots = list(filter(lambda e: len(e) <= nslots, returned_combs))
    # t1 derived: there should not exist a comb with more than 'nslots' elements
    self.assertEqual(len(not_greater_than_slots), len(returned_combs))
    for eachcomb in returned_combs:
      not_greater_than_startint = list(filter(lambda e: e <= startint, eachcomb))
      # t1 derived: there should not exist a comb with an element more than 'startint'
      self.assertEqual(len(not_greater_than_startint), len(eachcomb))
    # t2 as t1 with another parameter input set
    startint, nslots, upto = 7, 4, 6
    cmber = dc.DecrescentCombiner(startint=startint, nslots=nslots, upto=upto)
    cmber.recurs_combine_n_make_sumsets()
    returned_combs = cmber.combs
    expected_combs = [[6], [5, 1], [4, 2], [4, 1, 1], [3, 3], [3, 2, 1], [3, 1, 1, 1], [2, 2, 2], [2, 2, 1, 1]]
    self.assertEqual(expected_combs, returned_combs)
    # t3 as t1 with another parameter input set
    startint, nslots, upto = 12, 3, 4
    cmber = dc.DecrescentCombiner(startint=startint, nslots=nslots, upto=upto)
    cmber.recurs_combine_n_make_sumsets()
    returned_combs = cmber.combs
    expected_combs = [[4], [3, 1], [2, 2], [2, 1, 1]]
    self.assertEqual(expected_combs, returned_combs)

