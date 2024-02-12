#!/usr/bin/env python
"""
fs/mathfs/combinatorics/test_IndicesCombiner_functions.py
  Contains unit-tests for IndicesCombiner_functions.py in the same folder (package)

"""
import unittest
import fs.mathfs.combinatorics.IndicesCombiner_functions as iCf
import fs.mathfs.combinatorics.combinatoric_algorithms as ca  # ca.comb_n_by_m


class TestCombFunctions(unittest.TestCase):

  def test_get_decrescent_integer_sequence_summation_of_n(self):
    """
    Explanation:
      integer sequence for n-1 is [0, 1, 2, ..., n-1]
      but for the 'logical' summation, it's inverted, ie [n-1, n-2, ..., 2, 1, 0]
      of course, a summation is the same any way its constituents are placed, but here it's a logical positioning

    Example:
    f(0) = [0]
    f(1) = [1, 0]
    f(2) = [2, 1, 0]
    f(3) = [3, 2, 1, 0]
    f('blah') = None
    f(-2) = None
    """
    n, expected_seq = 0, [0]
    returned_seq = iCf.get_decrescent_integer_sequence_for_later_summation_of_n(n)
    self.assertEqual(expected_seq, returned_seq)
    n, expected_seq = 1, [1, 0]
    returned_seq = iCf.get_decrescent_integer_sequence_for_later_summation_of_n(n)
    self.assertEqual(expected_seq, returned_seq)
    n, expected_seq = 2, [2, 1, 0]
    returned_seq = iCf.get_decrescent_integer_sequence_for_later_summation_of_n(n)
    self.assertEqual(expected_seq, returned_seq)
    n, expected_seq = n, list(range(n, -1, -1))
    returned_seq = iCf.get_decrescent_integer_sequence_for_later_summation_of_n(n)
    self.assertEqual(expected_seq, returned_seq)
    n = 'foo bar'
    returned_seq = iCf.get_decrescent_integer_sequence_for_later_summation_of_n(n)
    self.assertIsNone(returned_seq)
    n = -2
    returned_seq = iCf.get_decrescent_integer_sequence_for_later_summation_of_n(n)
    self.assertIsNone(returned_seq)

  def test_get_distance_from_the_summation_scheme(self):
    """
    The decreasing integers (3, 2, 1, 0), seen in the summation, also show the 'distances within combinants', ie:
      '3' shows that there are 3 elements [0, n] (@see them either in docstring for add_one() or subtract_one())
      '2' shows that there are 2 elements [1, n]
      '1' shows that there are 1 element [2, n]
      '0' the one that does not have practical use
    This 'idea' can help in the strategy for subtract_one() (or previous())
    decrescent_integer_sequence = [3, 2, 1, 0]  # the ending zero is more theoretical than practical
    """
    # suppose IC(greatest_int_in_comb=3, n_slots=2)  # n_elements here is 4 (ie from 0 to 3)
    # ic = IndicesCombiner(3, 2) we have:
    # combination_elements = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]  # 6 total
    n_elements = 4
    pos_in_seq = 0  # expects 3 ie the distance may be 3 - 0 = 3 (seen in element [0, 3])
    expected_distance_at_pos_in_seq = 3  # dec_int_seq = [3, 2, 1, 0] # 3 is at pos=0
    returned_distance_at_pos_in_seq = iCf.get_distance_from_the_summation_scheme(n_elements, pos_in_seq)
    self.assertEqual(expected_distance_at_pos_in_seq, returned_distance_at_pos_in_seq)
    pos_in_seq = 1  # expects 3 ie the distance may be 3 - 0 = 3 (seen in element [0, 3])
    expected_distance_at_pos_in_seq = 2
    returned_distance_at_pos_in_seq = iCf.get_distance_from_the_summation_scheme(n_elements, pos_in_seq)
    self.assertEqual(expected_distance_at_pos_in_seq, returned_distance_at_pos_in_seq)
    pos_in_seq = 2  # expects 3 ie the distance may be 3 - 0 = 3 (seen in element [0, 3])
    expected_distance_at_pos_in_seq = 1
    returned_distance_at_pos_in_seq = iCf.get_distance_from_the_summation_scheme(n_elements, pos_in_seq)
    self.assertEqual(expected_distance_at_pos_in_seq, returned_distance_at_pos_in_seq)
    pos_in_seq = 3  # expects 3 ie the distance may be 3 - 0 = 3 (seen in element [0, 3])
    expected_distance_at_pos_in_seq = 0
    returned_distance_at_pos_in_seq = iCf.get_distance_from_the_summation_scheme(n_elements, pos_in_seq)
    self.assertEqual(expected_distance_at_pos_in_seq, returned_distance_at_pos_in_seq)
    pos_in_seq = 4  # expects None, position is outside of array
    returned_distance_at_pos_in_seq = iCf.get_distance_from_the_summation_scheme(n_elements, pos_in_seq)
    self.assertIsNone(returned_distance_at_pos_in_seq)
    # testing directly with the array
    max_value = n_elements - 1
    int_sequence_in_sum = iCf.get_decrescent_integer_sequence_for_later_summation_of_n(max_value)
    pos_in_seq = 0  # expects 2 ie the distance may be 3 - 1 = 2 (seen in element [1, 3])
    expected_distance_at_pos_in_seq = 3
    returned_distance_at_pos_in_seq = int_sequence_in_sum[pos_in_seq]
    self.assertEqual(expected_distance_at_pos_in_seq, returned_distance_at_pos_in_seq)
    pos_in_seq = 1  # expects 2 ie the distance may be 3 - 1 = 2 (seen in element [1, 3])
    expected_distance_at_pos_in_seq = 2
    returned_distance_at_pos_in_seq = int_sequence_in_sum[pos_in_seq]
    self.assertEqual(expected_distance_at_pos_in_seq, returned_distance_at_pos_in_seq)
    pos_in_seq = 2  # expects 1 ie the distance may be 3 - 2 = ' (seen in element [2, 3])
    expected_distance_at_pos_in_seq = 1
    returned_distance_at_pos_in_seq = int_sequence_in_sum[pos_in_seq]
    self.assertEqual(expected_distance_at_pos_in_seq, returned_distance_at_pos_in_seq)

  def test_add_one(self):
    """
    """
    # t1 expects the first combination from IC(greatest_int_in_comb=4, n_slots=3) which is [0, 1, 2]
    n_elements, n_slots = 4, 3
    nlist = iCf.make_the_first_or_minimum_combination(n_elements=n_elements, n_slots=n_slots)
    expected_nlist = [0, 1, 2]
    self.assertEqual(expected_nlist, nlist)
    # t2 expects the next() when a combination is added by one
    expected_added_one = [0, 1, 3]
    returned_added_one = iCf.add_one(nlist, n_elements=n_elements)
    self.assertEqual(expected_added_one, returned_added_one)
    # t3 expects the last combination [1, 2, 3]
    nlist = iCf.make_the_last_or_maximum_combination(n_elements=n_elements, n_slots=n_slots)
    expected_nlist = [1, 2, 3]
    self.assertEqual(expected_nlist, nlist)
    # t4 expects None when the last combination is added by one
    returned_added_one = iCf.add_one(nlist, n_elements=n_elements)
    self.assertIsNone(returned_added_one)

  def test_subtract_one(self):
    """
    """
    # t1 expects the last combination from IC(greatest_int_in_comb=4, n_slots=3) which is [2, 3, 4]
    n_elements, n_slots = 4, 3
    nlist = iCf.make_the_last_or_maximum_combination(n_elements=n_elements, n_slots=n_slots)
    expected_nlist = [1, 2, 3]
    self.assertEqual(expected_nlist, nlist)
    # t2 expects the previous() when a combination is subtracted by one
    expected_subtracted_one = [0, 2, 3]
    returned_subtracted_one = iCf.subtract_one(nlist, n_elements=n_elements)
    self.assertEqual(expected_subtracted_one, returned_subtracted_one)
    # t3 expects the first combination [0, 1, 2]
    nlist = iCf.make_the_first_or_minimum_combination(n_elements=n_elements, n_slots=n_slots)
    expected_nlist = [0, 1, 2]
    self.assertEqual(expected_nlist, nlist)
    # t4 expects None when the last combination is subtracted by one
    returned_subtracted_one = iCf.subtract_one(nlist, n_elements=n_elements)
    self.assertIsNone(returned_subtracted_one)

  def test_add_n_subtract_one(self):
    """
    Notice: the add_one() and subtract_one() "mutates" the input list.
      So caution must be taken to "freeze" the comparable list if needed.
    """
    # t1 expects the next() when a combination is added by one
    n_elements, n_slots = 5, 3
    nlist = [0, 1, 2, 3]
    expected_added_one = [0, 1, 2, 4]
    returned_added_one = iCf.add_one(nlist, n_elements=n_elements)
    self.assertEqual(expected_added_one, returned_added_one)
    # t2 "revert" the add_one() with a subtract_one()
    returned_reverted = iCf.subtract_one(expected_added_one, n_elements=n_elements)
    self.assertEqual(nlist, returned_reverted)
    # t3 add three times in a row
    nlist = [0, 1, 2, 4]
    added_one = iCf.add_one(nlist, n_elements=n_elements)
    expected_added_one = [0, 1, 3, 4]
    self.assertEqual(expected_added_one, added_one)
    added_two = iCf.add_one(added_one, n_elements=n_elements)
    expected_added_two = [0, 2, 3, 4]
    self.assertEqual(expected_added_two, added_two)
    added_three = iCf.add_one(added_two, n_elements=n_elements)
    expected_added_three = [1, 2, 3, 4]
    self.assertEqual(expected_added_three, added_three)
    # t4 subtract three times in a row
    returned_revert_to_2 = iCf.subtract_one(expected_added_three, n_elements=n_elements)
    self.assertEqual(expected_added_two, returned_revert_to_2)
    returned_revert_to_1 = iCf.subtract_one(expected_added_two, n_elements=n_elements)
    self.assertEqual(expected_added_one, returned_revert_to_1)
    # t5 subtract and add from the last combination
    nlist = [1, 2, 3, 4]
    lastcomb = list(nlist)
    subtracted_one = iCf.subtract_one(nlist, n_elements=n_elements)
    expected_penultimate = [0, 2, 3, 4]
    self.assertEqual(expected_penultimate, subtracted_one)
    added_one = iCf.add_one(expected_penultimate, n_elements=n_elements)
    self.assertEqual(lastcomb, added_one)
    # t6 another adding goes to None, ie the value undertaking the last combination in set
    added_one = iCf.add_one(added_one, n_elements=n_elements)
    self.assertIsNone(added_one)

  def test_add_one_until_last(self):
    """
    If parameters are changed in the test code,
      comment out the last subtest that is hardcoded with the combination set total size amount
    """
    # t1
    n_elements, n_slots = 4, 2
    all_expected_combs = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
    nlist = iCf.make_the_first_or_minimum_combination(n_elements=n_elements, n_slots=n_slots)
    all_returned_combs = [nlist]
    while nlist is not None:
      returned_added_one = iCf.add_one(nlist, n_elements=n_elements)
      if returned_added_one is None:
        break
      all_returned_combs.append(returned_added_one)
      # copy.copy() is not needed because a new one is out from add_one() above
      nlist = returned_added_one
    self.assertEqual(all_expected_combs, all_returned_combs)

  def test_add_one_until_last_larger_set(self):
    # t1 tests a larger set!
    # with a larger set, the four tests are: first, last, size and a "middle element" contained
    n_elements, n_slots = 10, 5  # C(10, 5) = 252!
    # pair(greatest_int_in_comb=19, n_slots=5) above generates 15504 combinations
    # (notice that, if still greater this number, it may slow down processing depending on CPU availability etc.)
    nlist = iCf.make_the_first_or_minimum_combination(n_elements=n_elements, n_slots=n_slots)
    all_returned_combs = [list(nlist)]
    while nlist is not None:
      returned_added_one = iCf.add_one(nlist, n_elements=n_elements)
      if returned_added_one is None:
        break
      all_returned_combs.append(returned_added_one)
      nlist = list(returned_added_one)  # list() used instead of copy.copy()
    firstcomb = list(range(n_slots))
    elem_min, elem_max = n_elements - n_slots, n_elements - 1
    lastcomb = list(range(elem_min, elem_max + 1))
    greatest_int = n_elements - 1
    displacement = int(greatest_int / 2)
    middlecomb = list(range(greatest_int - n_slots + 1 - displacement, greatest_int+1 - displacement))
    self.assertEqual(firstcomb, all_returned_combs[0])
    self.assertEqual(lastcomb, all_returned_combs[-1])
    self.assertTrue(middlecomb in all_returned_combs)
    n_combs = ca.combine_n_c_by_c_nonfact(n_elements, n_slots)
    self.assertEqual(n_combs, len(all_returned_combs))
    # if n_elements=20, n_slots=5 (ie, if they are not changed from above); n_combs=15504
    # yes, it was reduced to C(10, 5) = 252!
    # expected_size_calc_by_hand = 15504  # calculated aside  # n_combs = combine_n_c_by_c_nonfact(20, 5)
    # self.assertEqual(n_combs, expected_size_calc_by_hand)

  def test_subtract_one_until_first(self):
    """
    TO-DO
    If parameters are changed in the test code,
      comment out the last subtest that is hardcoded with the combination set total size amount
    """
    # t1 first: add one repeatedly until it gets maximum value
    all_expected_combs = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
    all_expected_combs = list(reversed(all_expected_combs))
    n_elements, n_slots = 4, 2
    nlist = iCf.make_the_last_or_maximum_combination(n_elements=n_elements, n_slots=n_slots)
    all_returned_combs = [list(nlist)]  # [[2, 3]] if n_elements, n_slots = 4, 2
    while nlist is not None:
      returned_subtracted_one = iCf.subtract_one(nlist, n_elements=n_elements)
      if returned_subtracted_one is None:
        break
      all_returned_combs.append(returned_subtracted_one)
      nlist = list(returned_subtracted_one)
    self.assertEqual(all_expected_combs, all_returned_combs)

  def test_subtract_one_w_larger_set(self):
    # t2 a larger set!
    # with a larger set, the four tests are: first, last, size and a "middle element" contained
    n_elements, n_slots = 10, 5  # C(10, 5) = 252
    # pair(greatest_int_in_comb=19, n_slots=5) above generates 15504 combinations
    # (notice that, if still greater this number, it may slow down processing depending on CPU availability etc.)
    nlist = iCf.make_the_last_or_maximum_combination(n_elements=n_elements, n_slots=n_slots)
    all_returned_combs = [list(nlist)]
    while nlist is not None:
      returned_subtracted_one = iCf.subtract_one(nlist, n_elements=n_elements)
      if returned_subtracted_one is None:
        break
      all_returned_combs.append(returned_subtracted_one)
      nlist = list(returned_subtracted_one)
    firstcomb = list(range(n_slots))
    elem_min, elem_max = n_elements - n_slots, n_elements - 1
    lastcomb = list(range(elem_min, elem_max + 1))
    greatest_int = n_elements - 1
    displacement = int(greatest_int / 2)
    middlecomb = list(range(greatest_int - n_slots + 1 - displacement, greatest_int+1 - displacement))
    self.assertEqual(lastcomb, all_returned_combs[0])
    self.assertEqual(firstcomb, all_returned_combs[-1])
    self.assertTrue(middlecomb in all_returned_combs)
    n_combs = ca.combine_n_c_by_c_nonfact(n_elements, n_slots)
    self.assertEqual(n_combs, len(all_returned_combs))
    # if n_elements=20, n_slots=5 (ie, if they are not changed from above); n_combs=15504
    # yes, it was reduced to C(10, 5) = 252!
    # expected_size_calc_by_hand = 15504  # calculated aside  # n_combs = combine_n_c_by_c_nonfact(20, 5)
    # self.assertEqual(n_combs, expected_size_calc_by_hand)

  def test_add_subtract_w_larger_set_at_margins(self):
    # t1 adds up all possible combinations until the last one
    n_elements, n_slots = 7, 4  # C(7, 4) = 35
    firstcomb = iCf.make_the_first_or_minimum_combination(n_elements=n_elements, n_slots=n_slots)
    lastcomb = iCf.make_the_last_or_maximum_combination(n_elements=n_elements, n_slots=n_slots)
    nlist = list(firstcomb)
    lastone = None
    while nlist is not None:
      nlist = iCf.add_one(nlist, n_elements=n_elements)
      if nlist is None:
        break
      # remind that nlist is mutated inside add_one(), so list() is necessary to avoid side effect
      lastone = list(nlist)
    self.assertEqual(lastcomb, lastone)
    # t2 subtracts down all possible combinations until the first one
    nlist = list(lastone)
    firstone = None
    while nlist is not None:
      nlist = iCf.subtract_one(nlist, n_elements=n_elements)
      if nlist is None:
        break
      # remind that nlist is mutated inside add_one(), so list() is necessary to avoid side effect
      firstone = list(nlist)
    self.assertEqual(firstcomb, firstone)

  def test_add_subtract_full_equivalent_w_smaller_set(self):
    # t1 adds up all possible combinations until the last one
    n_elements, n_slots = 7, 4  # C(7, 4) = 35
    firstcomb = iCf.make_the_first_or_minimum_combination(n_elements=n_elements, n_slots=n_slots)
    lastcomb = iCf.make_the_last_or_maximum_combination(n_elements=n_elements, n_slots=n_slots)
    full_asc_list = [firstcomb]
    nlist = list(firstcomb)
    while nlist is not None:
      nlist = iCf.add_one(nlist, n_elements=n_elements)
      if nlist is None:
        break
      # remind that nlist is mutated inside add_one(), so list() is necessary to avoid side effect
      curr_one = list(nlist)
      full_asc_list.append(curr_one)
    # t2 subtracts down all possible combinations until the first one
    full_desc_list = [lastcomb]
    nlist = list(lastcomb)
    while nlist is not None:
      nlist = iCf.subtract_one(nlist, n_elements=n_elements)
      if nlist is None:
        break
      # remind that nlist is mutated inside add_one(), so list() is necessary to avoid side effect
      curr_one = list(nlist)
      full_desc_list.append(curr_one)
    self.assertEqual(full_asc_list[-1], full_desc_list[0])
    self.assertEqual(full_asc_list[0], full_desc_list[-1])
    self.assertEqual(len(full_asc_list), len(full_desc_list))
    full_desc_list_reversed = list(reversed(full_desc_list))
    self.assertEqual(full_asc_list, full_desc_list_reversed)
