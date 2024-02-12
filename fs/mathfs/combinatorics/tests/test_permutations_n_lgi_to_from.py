#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/test_permutations_n_lgi_to_from.py
  Unit-tests for fs/mathfs/combinatorics/permutations_n_lgi_to_from.py

"""
import unittest
import math
import fs.mathfs.combinatorics.permutations_n_lgi_to_from as ftf  # .calc_permutation_from_lgib0idx_by_lehmercode_inner


class TestForFactoradicsEtAl(unittest.TestCase):

  def test_forming_factoradic_numbers(self):
    """
    979,999 (decimal) = 2623031010 (factoradic)
    TO-DO: the factoradic, in the future, will be represented as "nN:n(N-1):...:n(2):n(1):n(0)!"
    In the example above:
    2623031010 (factoradic) should be written as 2:6:2:3:0:3:1:0:1:0!
    This way it's written now, it cannot be greater than a 9-digit number,
      though it's close to 10! or 11! (the theory says that 11!-1 is equal to all summing 10:9:8...:0!
      a bit like 2**4 - 1 = 2**3 + 2**2 + 2**1 + 2**0
      (but a factoradic number having 10 (or greater) in it cannot be written here at the time of this writing)
    """
    # t1
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

  def test_calc_lgib0idx_from_permutation(self):
    # t1 tests the result lgi from a permutation
    given_permset, expected_lgi_b0idx = [3, 0, 1, 2], 18
    returned_lgi_b0idx = ftf.calc_lgi_b0idx_from_idx_permutation_set(given_permset)
    self.assertEqual(expected_lgi_b0idx, returned_lgi_b0idx)
    # t2 same as t1 with a different permset
    given_permset, expected_lgi_b0idx = [1, 2, 3, 0], 9
    returned_lgi_b0idx = ftf.calc_lgi_b0idx_from_idx_permutation_set(given_permset)
    self.assertEqual(expected_lgi_b0idx, returned_lgi_b0idx)
    # t3 uses a larger lgi with a larger workset, but testing with the "initial set"
    given_permset, expected_lgi_b0idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 0
    returned_lgi_b0idx = ftf.calc_lgi_b0idx_from_idx_permutation_set(given_permset)
    self.assertEqual(expected_lgi_b0idx, returned_lgi_b0idx)
    # t4 uses a larger lgi with an arbitrary "middle" workset
    given_permset, expected_lgi_b0idx = [2, 7, 3, 5, 0, 8, 4, 1, 9, 6], 980000 - 1
    returned_lgi_b0idx = ftf.calc_lgi_b0idx_from_idx_permutation_set(given_permset)
    self.assertEqual(expected_lgi_b0idx, returned_lgi_b0idx)
    # t5 uses a larger lgi with a larger workset, but testing with the "last set"
    given_permset = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    n_elements = len(given_permset)
    expected_lgi_b0idx = math.factorial(n_elements) - 1
    returned_lgi_b0idx = ftf.calc_lgi_b0idx_from_idx_permutation_set(given_permset)
    self.assertEqual(expected_lgi_b0idx, returned_lgi_b0idx)

  def test_convention_lexicographical_nonnumbers_permutation(self):
    # t1 tests the generation function that permutes from a lexicographical conventioned initial set
    expected_perms = [
      ['banana', 'beans', 'soy'],
      ['banana', 'soy', 'beans'],
      ['beans', 'banana', 'soy'],
      ['beans', 'soy', 'banana'],
      ['soy', 'banana', 'beans'],
      ['soy', 'beans', 'banana'],
    ]
    initial_conventioned_set = ['banana', 'beans', 'soy']
    returned_perms = []
    for permset in ftf.gen_lexicographical_permutations_w_initial_lgi_set(initial_conventioned_set):
      returned_perms.append(permset)
    self.assertEqual(expected_perms, returned_perms)
