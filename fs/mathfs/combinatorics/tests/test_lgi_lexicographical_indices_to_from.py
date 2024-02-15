#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/test_lgi_lexicographical_indices_to_from.py
  Unit-tests to fs/mathfs/combinatorics/lgi_lexicographical_indices_to_from.py

  The main functionality involved here is the calculation of combinations and lgi's

    lgi = lexicographical index
    lgi's = lexicographical indices

  The relation lgi's<->combinations forms a bijections, ie, one computation may be "inversed".
"""
import unittest
import fs.mathfs.combinatorics.lgi_lexicographical_indices_to_from as lgi_tf
import fs.mathfs.combinatorics.IndicesCombiner_functions as iCf
import fs.mathfs.combinatorics.combinatoric_algorithms as ca


class TestLgiToCombination(unittest.TestCase):

  def test_consistent_combinations(self):
    n_elements, n_slots = 60, 6
    firstcomb_made = iCf.make_the_first_or_minimum_combination(n_elements=n_elements, n_slots=n_slots)
    is_consistent = lgi_tf.is_combination_consistent_w_nelements(firstcomb_made, n_elements)
    # t1 test consistency of "first comb"
    self.assertTrue(is_consistent)
    lastcomb_made = iCf.make_the_last_or_maximum_combination(n_elements=n_elements, n_slots=n_slots)
    is_consistent = lgi_tf.is_combination_consistent_w_nelements(lastcomb_made, n_elements)
    # t2 test consistency of "last comb"
    self.assertTrue(is_consistent)
    starter_elem_for_midcomb = (n_elements - n_slots) // 2
    a_middle_comb = [i+starter_elem_for_midcomb for i in range(n_slots)]
    is_consistent = lgi_tf.is_combination_consistent_w_nelements(a_middle_comb, n_elements)
    # t3 test consistency of "a middle comb"
    self.assertTrue(is_consistent)
    inconsistent_comb = [0]*n_slots
    # t4 test that an inconsistent combination (due to repeats) raises ValueError
    self.assertRaises(ValueError, lgi_tf.calc_lgi_b0idx_from_comb_where_ints_start_at_0, inconsistent_comb, n_elements)
    # t5 test that an inconsistent combination (due to being descending, reverse of ascending) raises ValueError
    inconsistent_comb = list(reversed(firstcomb_made))
    self.assertRaises(ValueError, lgi_tf.calc_lgi_b0idx_from_comb_where_ints_start_at_0, inconsistent_comb, n_elements)
    # t6 test that an inconsistent combination (due to going positively outbounds) raises ValueError
    inconsistent_comb = [i+n_elements for i in lastcomb_made]
    self.assertRaises(ValueError, lgi_tf.calc_lgi_b0idx_from_comb_where_ints_start_at_0, inconsistent_comb, n_elements)
    # t7 test that an inconsistent combination (due to having negative numbers) raises ValueError
    inconsistent_comb = [i-n_elements for i in firstcomb_made]
    self.assertRaises(ValueError, lgi_tf.calc_lgi_b0idx_from_comb_where_ints_start_at_0, inconsistent_comb, n_elements)
    # t8 test that an inconsistent combination (due to going outbounds) raises ValueError
    inconsistent_comb = list(lastcomb_made)
    inconsistent_comb[-1] += 1  # last element goes above its highest value (for lastcomb is 'touching' the upper limit)
    self.assertRaises(ValueError, lgi_tf.calc_lgi_b0idx_from_comb_where_ints_start_at_0, inconsistent_comb, n_elements)

  def test_lgi_to_from(self):
    n_elements, n_slots = 5, 3
    given_lgi = 3
    expected_comb = [1, 2, 3]
    returned_comb = lgi_tf.lgi_f_inv_from_b0idx_to_combination(given_lgi, n_elements=n_elements, n_slots=n_slots)
    returned_lgi = lgi_tf.calc_lgi_b0idx_from_comb_where_ints_start_at_0(expected_comb, n_elements=n_elements)
    # t1 test given_lgi with returned_lgi
    self.assertEqual(given_lgi, returned_lgi)
    # t2 test expected_comb with returned_comb, the latter coming from given_lgi
    self.assertEqual(expected_comb, returned_comb)

  def test_lgi_borders_of_a_large_set(self):
    n_elements, n_slots = 60, 6
    firstcomb_made = iCf.make_the_first_or_minimum_combination(n_elements=n_elements, n_slots=n_slots)
    expected_firstcomb = list(range(n_slots))
    # t1 test "made first comb"
    self.assertEqual(expected_firstcomb, firstcomb_made)
    expected_lastcomb = list(range(n_elements - n_slots, n_elements))
    lastcomb_made = iCf.make_the_last_or_maximum_combination(n_elements=n_elements, n_slots=n_slots)
    # t2 test "last comb made"
    self.assertEqual(expected_lastcomb, lastcomb_made)
    ret_first_comb_idx_by_lgi = lgi_tf.calc_lgi_b0idx_from_comb_where_ints_start_at_0(
      firstcomb_made, n_elements=n_elements
    )
    ret_last_comb_idx_by_lgi = lgi_tf.calc_lgi_b0idx_from_comb_where_ints_start_at_0(
      lastcomb_made, n_elements=n_elements
    )
    total_combs = ca.combine_n_c_by_c_nonfact(n=n_elements, c=n_slots)
    expected_b0idx_lgi_for_first = total_combs - 1
    # t3 test first comb index (which is total comb size minus 1) with its returned value from the lgi function
    self.assertEqual(expected_b0idx_lgi_for_first, ret_first_comb_idx_by_lgi)
    expected_b0idx_lgi_for_last = 0
    # t4 test last comb index (which is 0) with its returned value from the lgi function
    self.assertEqual(expected_b0idx_lgi_for_last, ret_last_comb_idx_by_lgi)
    starter_elem_for_midcomb = (n_elements - n_slots) // 2
    a_middle_comb = [i+starter_elem_for_midcomb for i in range(n_slots)]
    # t5 test that a_middle_comb's lgi should be within 0 and total_combs-1 excluding extremes
    ret_midcomb_lgi = lgi_tf.calc_lgi_b0idx_from_comb_where_ints_start_at_0(a_middle_comb, n_elements=n_elements)
    self.assertTrue(0 < ret_midcomb_lgi < expected_b0idx_lgi_for_first)

  def test_class_LgiToFromCombination_comb_to_lgi(self):
    n_elements, n_slots = 5, 3
    lgi_o = lgi_tf.LgiToFromCombination(n_elements=n_elements, n_slots=n_slots)
    firstcomb_made = iCf.make_the_first_or_minimum_combination(n_elements=n_elements, n_slots=n_slots)
    lgi_o.combset = firstcomb_made
    expected_b0idx = lgi_o.size - 1
    # t1 test first comb index (which is total comb size minus 1)
    self.assertEqual(expected_b0idx, lgi_o.b0idx_lgi)
    second_comb = iCf.add_one(firstcomb_made, n_elements=n_elements)
    lgi_o.combset = second_comb
    expected_b0idx -= 1
    # t2 test second comb index, the second comb is the one after the first comb
    self.assertEqual(expected_b0idx, lgi_o.b0idx_lgi)
    lastcomb_made = iCf.make_the_last_or_maximum_combination(n_elements=n_elements, n_slots=n_slots)
    lgi_o.combset = lastcomb_made
    expected_b0idx = 0
    # t3 test last comb index (which is 0)
    self.assertEqual(expected_b0idx, lgi_o.b0idx_lgi)

  def test_class_LgiToFromCombination_lgi_to_comb(self):
    n_elements, n_slots = 5, 3
    lgi_o = lgi_tf.LgiToFromCombination(n_elements=n_elements, n_slots=n_slots)
    lgi_o.b0idx_lgi = lgi_o.size - 1
    expect_the_first_comb = iCf.make_the_first_or_minimum_combination(n_elements=n_elements, n_slots=n_slots)
    # t1 test the first comb after given lgi as total comb size minus 1
    self.assertEqual(expect_the_first_comb, lgi_o.combset)
    firstcomb_made = iCf.make_the_first_or_minimum_combination(n_elements=n_elements, n_slots=n_slots)
    self.assertEqual(firstcomb_made, lgi_o.combset)
    # diminish one to lgi, adding one to combset
    lgi_o.b0idx_lgi -= 1
    expected_the_second_comb = iCf.add_one(expect_the_first_comb, n_elements=n_elements)
    # t2 test the second comb after given lgi
    self.assertEqual(expected_the_second_comb, lgi_o.combset)
    lastcomb_made = iCf.make_the_last_or_maximum_combination(n_elements=n_elements, n_slots=n_slots)
    # t3 test the last comb after given lgi as total comb size minus 1
    lgi_o.b0idx_lgi = 0
    self.assertEqual(lastcomb_made, lgi_o.combset)
    # test raise ValueError
    # find out how to test a 'setter'
    # self.assertRaises(ValueError, lgi_o.b0idx_lgi.setter, 'blah')
