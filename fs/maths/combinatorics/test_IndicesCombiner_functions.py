#!/usr/bin/env python
"""
fs/maths/combinatorics/test_IndicesCombiner_functions.py
  Contains unit-tests for IndicesCombiner_functions.py in the same folder (package)

"""
import unittest
import fs.maths.combinatorics.IndicesCombiner_functions as iCf  # icf.get_decrescent_integer_sequence_summation_of_n
import fs.maths.combinatorics.combinatoric_algorithms as ca  # ca.comb_n_by_m


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
    returned_seq = iCf.get_decrescent_integer_sequence_summation_of_n(n)
    self.assertEqual(expected_seq, returned_seq)
    n, expected_seq = 1, [1, 0]
    returned_seq = iCf.get_decrescent_integer_sequence_summation_of_n(n)
    self.assertEqual(expected_seq, returned_seq)
    n, expected_seq = 2, [2, 1, 0]
    returned_seq = iCf.get_decrescent_integer_sequence_summation_of_n(n)
    self.assertEqual(expected_seq, returned_seq)
    n, expected_seq = n, list(range(n, -1, -1))
    returned_seq = iCf.get_decrescent_integer_sequence_summation_of_n(n)
    self.assertEqual(expected_seq, returned_seq)
    n = 'foo bar'
    returned_seq = iCf.get_decrescent_integer_sequence_summation_of_n(n)
    self.assertIsNone(returned_seq)
    n = -2
    returned_seq = iCf.get_decrescent_integer_sequence_summation_of_n(n)
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
    # suppose IC(up_limit=3, n_slots=2)  # n_elements here is 4 (ie from 0 to 3)
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
    int_sequence_in_sum = iCf.get_decrescent_integer_sequence_summation_of_n(max_value)
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
    # t1 expects the first combination from IC(up_limit=4, n_slots=3) which is [0, 1, 2]
    up_limit, n_slots = 4, 3
    nlist = iCf.project_first_combinationlist(up_limit=up_limit, n_slots=n_slots)
    expected_nlist = [0, 1, 2]
    self.assertEqual(expected_nlist, nlist)
    # t2 expects the next() when a combination is added by one
    expected_added_one = [0, 1, 3]
    returned_added_one = iCf.add_one(nlist, up_limit=up_limit)
    self.assertEqual(expected_added_one, returned_added_one)
    # t3 expects the last combination from IC(up_limit=4, n_slots=3) which is [2, 3, 4]
    nlist = iCf.project_last_combinationlist(up_limit=up_limit, n_slots=n_slots)
    expected_nlist = [2, 3, 4]
    self.assertEqual(expected_nlist, nlist)
    # t4 expects None when the last combination is added by one
    returned_added_one = iCf.add_one(nlist, up_limit=up_limit)
    self.assertIsNone(returned_added_one)

  def test_subtract_one(self):
    """
    """
    # t1 expects the last combination from IC(up_limit=4, n_slots=3) which is [2, 3, 4]
    up_limit, n_slots = 4, 3
    nlist = iCf.project_last_combinationlist(up_limit=up_limit, n_slots=n_slots)
    expected_nlist = [2, 3, 4]
    self.assertEqual(expected_nlist, nlist)
    # t2 expects the previous() when a combination is subtracted by one
    expected_subtracted_one = [1, 3, 4]
    returned_subtracted_one = iCf.subtract_one(nlist, up_limit=up_limit)
    self.assertEqual(expected_subtracted_one, returned_subtracted_one)
    # t3 expects the first combination from IC(up_limit=4, n_slots=3) which is [0, 1, 2]
    nlist = iCf.project_first_combinationlist(up_limit=up_limit, n_slots=n_slots)
    expected_nlist = [0, 1, 2]
    self.assertEqual(expected_nlist, nlist)
    # t4 expects None when the last combination is added by one
    returned_subtracted_one = iCf.subtract_one(nlist, up_limit=up_limit)
    self.assertIsNone(returned_subtracted_one)

  def test_add_one_until_last(self):
    """
    If parameters are changed in the test code,
      comment out the last subtest that is hardcoded with the combination set total size amount
    """
    # t1
    all_expected_combs = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
    up_limit, n_slots = 3, 2
    nlist = iCf.project_first_combinationlist(up_limit=up_limit, n_slots=n_slots)
    all_returned_combs = [nlist]
    while nlist is not None:
      returned_added_one = iCf.add_one(nlist, up_limit=up_limit)
      if returned_added_one is None:
        break
      all_returned_combs.append(returned_added_one)
      # copy.copy() is not needed because a new one is out from add_one() above
      nlist = returned_added_one
    self.assertEqual(all_expected_combs, all_returned_combs)
    # t2 a larger set!
    # with a larger set, the four tests are: first, last, size and a "middle element" contained
    up_limit, n_slots = 19, 5
    # pair(up_limit=19, n_slots=5) above generates 15504 combinations
    # (notice that, if still greater this number, it may slow down processing depending on CPU availability etc.)
    nlist = iCf.project_first_combinationlist(up_limit=up_limit, n_slots=n_slots)
    all_returned_combs = [nlist]
    while nlist is not None:
      returned_added_one = iCf.add_one(nlist, up_limit=up_limit)
      if returned_added_one is None:
        break
      all_returned_combs.append(returned_added_one)
      # copy.copy() is not needed because a new one is out from add_one() above
      nlist = returned_added_one
    firstelem = list(range(n_slots))
    lastelem = list(range(up_limit - n_slots + 1, up_limit+1))
    displacement = int(up_limit / 2)
    middle_elem = list(range(up_limit - n_slots + 1 - displacement, up_limit+1 - displacement))
    self.assertEqual(firstelem, all_returned_combs[0])
    self.assertEqual(lastelem, all_returned_combs[-1])
    self.assertTrue(middle_elem in all_returned_combs)
    n_elements = up_limit + 1
    n_combs = ca.combine_n_c_by_c(n_elements, n_slots)
    self.assertEqual(n_combs, len(all_returned_combs))
    # OBS comment out this last subtest if line "up_limit, n_slots = 19, 5" is changed above
    # (or alternatively recalculate it) (it's been commented out though the two parameters above were not updated)
    # expected_size_calc_by_hand = 15504  # calculated sideways  # n_combs = combine_n_c_by_c(20, 5)
    # self.assertEqual(n_combs, expected_size_calc_by_hand)

  def test_subtract_one_until_first(self):
    """
    TO-DO
    If parameters are changed in the test code,
      comment out the last subtest that is hardcoded with the combination set total size amount
    """
    # t1
    all_expected_combs = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
    up_limit, n_slots = 3, 2
    nlist = iCf.project_first_combinationlist(up_limit=up_limit, n_slots=n_slots)
    all_returned_combs = [nlist]
    while nlist is not None:
      returned_added_one = iCf.add_one(nlist, up_limit=up_limit)
      if returned_added_one is None:
        break
      all_returned_combs.append(returned_added_one)
      # copy.copy() is not needed because a new one is out from add_one() above
      nlist = returned_added_one
    self.assertEqual(all_expected_combs, all_returned_combs)
    # t2 a larger set!
    # with a larger set, the four tests are: first, last, size and a "middle element" contained
    up_limit, n_slots = 19, 5
    # pair(up_limit=19, n_slots=5) above generates 15504 combinations
    # (notice that, if still greater this number, it may slow down processing depending on CPU availability etc.)
    nlist = iCf.project_first_combinationlist(up_limit=up_limit, n_slots=n_slots)
    all_returned_combs = [nlist]
    while nlist is not None:
      returned_added_one = iCf.add_one(nlist, up_limit=up_limit)
      if returned_added_one is None:
        break
      all_returned_combs.append(returned_added_one)
      # copy.copy() is not needed because a new one is out from add_one() above
      nlist = returned_added_one
    firstelem = list(range(n_slots))
    lastelem = list(range(up_limit - n_slots + 1, up_limit+1))
    displacement = int(up_limit / 2)
    middle_elem = list(range(up_limit - n_slots + 1 - displacement, up_limit+1 - displacement))
    self.assertEqual(firstelem, all_returned_combs[0])
    self.assertEqual(lastelem, all_returned_combs[-1])
    self.assertTrue(middle_elem in all_returned_combs)
    n_elements = up_limit + 1
    n_combs = ca.combine_n_c_by_c(n_elements, n_slots)
    self.assertEqual(n_combs, len(all_returned_combs))
    # OBS comment out this last subtest if line "up_limit, n_slots = 19, 5" is changed above
    # (or alternatively recalculate it) (it's been commented out though the two parameters above were not updated)
    # expected_size_calc_by_hand = 15504  # calculated sideways  # n_combs = combine_n_c_by_c(20, 5)
    # self.assertEqual(n_combs, expected_size_calc_by_hand)
