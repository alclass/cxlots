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
import fs.mathfs.combinatorics.IndicesCombiner_functions as iCf
import fs.mathfs.combinatorics.combinatoric_algorithms as ca


class TestLgiToCombination(unittest.TestCase):

  def test_lgi_to_from(self):
    n_elements, n_slots = 5, 3
    given_lgi = 3
    expected_comb = [1, 2, 3]
    returned_comb = lgi_tf.lgi_f_inv_from_b0idx_to_combination(given_lgi, n_elements=n_elements, n_slots=n_slots)
    returned_lgi = lgi_tf.calc_lgi_b0idx_from_comb_where_ints_start_at_0(expected_comb, n_elements=n_elements)
    self.assertEqual(given_lgi, returned_lgi)
    self.assertEqual(expected_comb, returned_comb)

  def test_lgi_borders_of_a_large_set(self):
    n_elements, n_slots = 60, 6
    made_firstcomb = iCf.make_the_first_or_minimum_combination(n_elements=n_elements, n_slots=n_slots)
    expected_firstcomb = list(range(n_slots))
    # t1 test "made first comb"
    self.assertEqual(expected_firstcomb, made_firstcomb)
    expected_lastcomb = list(range(n_elements - n_slots, n_elements))
    made_lastcomb = iCf.make_the_last_or_maximum_combination(n_elements=n_elements, n_slots=n_slots)
    # t2 test "made last comb"
    self.assertEqual(expected_lastcomb, made_lastcomb)
    ret_first_comb_idx_by_lgi = lgi_tf.calc_lgi_b0idx_from_comb_where_ints_start_at_0(made_firstcomb, n_elements=n_elements)
    ret_last_comb_idx_by_lgi = lgi_tf.calc_lgi_b0idx_from_comb_where_ints_start_at_0(made_lastcomb, n_elements=n_elements)
    total_combs = ca.combine_n_c_by_c_nonfact(n=n_elements, c=n_slots)
    expected_b0idx_lgi_for_first = total_combs - 1
    # t3 test first comb index (which is total comb size minus 1) with its returned value from the lgi function
    self.assertEqual(expected_b0idx_lgi_for_first, ret_first_comb_idx_by_lgi)
    expected_b0idx_lgi_for_last = 0
    # t4 test last comb index (which is 0) with its returned value from the lgi function
    self.assertEqual(expected_b0idx_lgi_for_last, ret_last_comb_idx_by_lgi)
    starter_elem_for_midcomb = (n_elements - n_slots) // 2
    a_middle_comb = [i+starter_elem_for_midcomb for i in range(n_slots)]
    # t5 test a_middle_comb's lgi is within 0 and total combs
    ret_midcomb_lgi = lgi_tf.calc_lgi_b0idx_from_comb_where_ints_start_at_0(a_middle_comb, n_elements=n_elements)
    self.assertTrue(0 < ret_midcomb_lgi < total_combs)

  def test_consistent_combinations(self):
    n_elements, n_slots = 60, 6
    made_firstcomb = iCf.make_the_first_or_minimum_combination(n_elements=n_elements, n_slots=n_slots)
    is_consistent = lgi_tf.is_combination_consistent_w_nelements(made_firstcomb, n_elements)
    # t1 test consistency of "first comb"
    self.assertTrue(is_consistent)
    made_lastcomb = iCf.make_the_last_or_maximum_combination(n_elements=n_elements, n_slots=n_slots)
    is_consistent = lgi_tf.is_combination_consistent_w_nelements(made_lastcomb, n_elements)
    # t2 test consistency of "last comb"
    self.assertTrue(is_consistent)
    starter_elem_for_midcomb = (n_elements - n_slots) // 2
    a_middle_comb = [i+starter_elem_for_midcomb for i in range(n_slots)]
    is_consistent = lgi_tf.is_combination_consistent_w_nelements(a_middle_comb, n_elements)
    # t3 test consistency of "a middle comb"
    self.assertTrue(is_consistent)
    inconsistent_comb = [0]*n_slots
    # t4 test that an inconsistenc combination (due to repeats) raises ValueError
    self.assertRaises(ValueError, lgi_tf.calc_lgi_b0idx_from_comb_where_ints_start_at_0, inconsistent_comb, n_elements)
    # t5 test that an inconsistenc combination (due to being desc) raises ValueError
    inconsistent_comb = list(reversed(made_firstcomb))
    self.assertRaises(ValueError, lgi_tf.calc_lgi_b0idx_from_comb_where_ints_start_at_0, inconsistent_comb, n_elements)
    # t6 test that an inconsistenc combination (due to going positively outbounds) raises ValueError
    inconsistent_comb = [i+n_elements for i in made_lastcomb]
    self.assertRaises(ValueError, lgi_tf.calc_lgi_b0idx_from_comb_where_ints_start_at_0, inconsistent_comb, n_elements)
    # t7 test that an inconsistenc combination (due to having negative numbers) raises ValueError
    inconsistent_comb = [i-n_elements for i in made_firstcomb]
    self.assertRaises(ValueError, lgi_tf.calc_lgi_b0idx_from_comb_where_ints_start_at_0, inconsistent_comb, n_elements)
    # t8 test that an inconsistenc combination (due to going outbounds) raises ValueError
    inconsistent_comb = list(made_lastcomb)
    inconsistent_comb[-1] += 1  # last element goes above its highest value
    self.assertRaises(ValueError, lgi_tf.calc_lgi_b0idx_from_comb_where_ints_start_at_0, inconsistent_comb, n_elements)


