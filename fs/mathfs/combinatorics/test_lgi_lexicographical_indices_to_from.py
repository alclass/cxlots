#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/test_lgi_lexicographical_indices_to_from.py
  Unit-tests to fs/mathfs/combinatorics/lgi_lexicographical_indices_to_from.py

  The main functionality envolved here is the calculation of combinations and lgi's

    lgi = lexicographical index
    lgi's = lexicographical indices

  The relation lgi's<->combinations forms a bijections, ie, one computation may be "inversed".
"""
import unittest
import fs.mathfs.combinatorics.lgi_lexicographical_indices_to_from as lgi_tf  # lgi_tf.lgi_f_inv_from_b0idx_to_combination


class TestLgiToCombination(unittest.TestCase):

  def test_lgi_to_from(self):
    n_elements, n_slots = 5, 3
    given_lgi = 3
    expected_comb = [1, 2, 3]
    returned_comb = lgi_tf.lgi_f_inv_from_b0idx_to_combination(given_lgi, n_elements=n_elements, n_slots=n_slots)
    returned_lgi = lgi_tf.calc_lgi_b0idx_from_comb_where_ints_start_at_0(expected_comb, n_elements=n_elements)
    self.assertEqual(given_lgi, returned_lgi)
    self.assertEqual(expected_comb, returned_comb)

