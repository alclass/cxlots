#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/test_factoradic_to_from.py
  Unit-tests for fs/mathfs/combinatorics/factoradic_to_from.py

"""
import unittest
import math
import fs.mathfs.combinatorics.factoradic_to_from as ftf  # .calc_permutation_from_lgib0idx_by_lehmercode_inner


class TestForFactoradicsEtAl(unittest.TestCase):

  def test_forming_factoradic_numbers(self):
    """
    979,999(decimal) = 2623031010(factoradic)
    """
    quoc = 979999 // math.factorial(9)
    expected_quoc = 2
    self.assertEqual(expected_quoc, quoc)
    remainder = 979999 % math.factorial(9)
    expected_remainder = 254239
    # ==========
    self.assertEqual(expected_remainder, remainder)

  def test_calc_permutation_from_lgib1idx(self):
    # t1 tests the result permutation with a somewhat small workset and a given_lgi_b1idx
    workset = [0, 1, 2, 3]
    expected_perm_result, given_lgi_b1idx = [3, 0, 1, 2], 19
    ret_perm_result = ftf.calc_permutation_from_lgib1idx_by_lehmercode(given_lgi_b1idx, workset=workset)
    self.assertEqual(expected_perm_result, ret_perm_result)
    # t2 same as t1 with a different given_lgi_b1idx
    workset = [0, 1, 2, 3]
    expected_perm_result, given_lgi_b1idx = [1, 2, 3, 0], 10
    ret_perm_result = ftf.calc_permutation_from_lgib1idx_by_lehmercode(given_lgi_b1idx, workset=workset)
    self.assertEqual(expected_perm_result, ret_perm_result)
    # t3 uses a larger workset and calls the "inner" version with given_lgi_b0idx (index 0-based)
    workset = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    given_lgi_b0idx = 980000 - 1
    ret_perm_result = ftf.calc_permutation_from_lgib0idx_by_lehmercode_inner(given_lgi_b0idx, workset=workset)
    expected_perm_result = [2, 7, 3, 5, 0, 8, 4, 1, 9, 6]
    self.assertEqual(expected_perm_result, ret_perm_result)

  def test_3(self):
    pass
