#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/test_IndicesCombiner.py
  Contains unit-tests to the class IndicesCombiner
    that models a combinadic object (@see also its docstring)
"""
import unittest
import fs.mathfs.combinatorics.IndicesCombiner as iCmb  # ic.IndicesCombiner


class TestIndicesCombiner(unittest.TestCase):

  def test_instantiate_indicescombiner(self):
    """
    Default parameters to IndicesCombiner
    ic = IndicesCombiner(greatest_index=0, size=1, overlap=True, i_array_in=None)
    Example:
      ic = iCmb.IndicesCombiner(2, 2, False)
    [0, 1]   [0, 2]   [1, 2]
    """
    # t1
    expected_set = [[0, 1], [0, 2], [1, 2]]
    ic = iCmb.IndicesCombiner(3, 2, False)
    expected_first = expected_set[0]
    self.assertEqual(expected_first, ic.first_comb)
    expected_last = expected_set[-1]
    self.assertEqual(expected_last, ic.last_comb)
    self.assertEqual(expected_set, list(ic.gen_all_sets()))
    # t2
    expected_set = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]
    ic = iCmb.IndicesCombiner(4, 3, False)
    expected_first = expected_set[0]
    self.assertEqual(expected_first, ic.first_comb)
    expected_last = expected_set[-1]
    self.assertEqual(expected_last, ic.last_comb)
    self.assertEqual(expected_set, list(ic.gen_all_sets()))

