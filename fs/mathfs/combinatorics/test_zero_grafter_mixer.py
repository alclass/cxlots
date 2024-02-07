#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/test_zero_grafter_mixer.py
  Unit-tests for fs/mathfs/combinatorics/zero_grafter_mixer.py
"""
import unittest
import fs.mathfs.combinatorics.zero_grafter_mixer as zgmx  # zg.ZeroesGraftAndCountsMixer


class TestCase1(unittest.TestCase):

  def test_zerografted_strs_w_grafting_coordlist(self):
    # t1 test 'fuse'
    amounts_in_slots = [3, 2, 1]
    grafting_coordlist = [[(1, 3)], [(1, 2), (2, 1)], [(1, 1), (2, 2)], [(2, 3)]]
    returned_zerograft_strs = zgmx.mount_zerografted_strs_w_grafting_coordlist(grafting_coordlist, amounts_in_slots)
    expected_zerograft_strs = ['300021', '300201', '302001', '320001']
    self.assertEqual(expected_zerograft_strs, returned_zerograft_strs)
    # t2 test 'fuse'
    gaphole_position_list = [1, 2]
    n_elements, n_slots = 6, 6
    returned_zeroes_comblist = zgmx.get_gaphole_idxpos_list_for_zerografting_with(
      amounts_in_slots, n_elements=n_elements, n_slots=n_slots
    )
    expected_zeroes_comblist = [1, 2]
    graftzeroes_combination_list = [[3, 0], [2, 1], [1, 2], [0, 3]]
    self.assertEqual(expected_zeroes_comblist, returned_zeroes_comblist)
    returned_fuse_coordlist = zgmx.fuse_combination_list_w_poslist(
      gaphole_position_list=gaphole_position_list, graftzeroes_combination_list=graftzeroes_combination_list
    )
    self.assertEqual(grafting_coordlist, returned_fuse_coordlist)

  def test_zerograft_1st_hypothesis(self):
    """
    @see more info about the grafting scheme in class ZeroesGraftAndCountsMixer

    The subtests in this test-method encompass the following hypothesis:
      grafting scheme with:
        basecomb = [3, 2, 1]
        graft_idx_positions = [1, 3]
    The expected values are:
      graft_size_cmbs = [[3, 0], [2, 1], [1, 2], [0, 3]]
      mask = [3, None, 2, None, 1]  # ie None occupies index-positions 1 & 3
      results = ('chunks') ['300021', '300201', '302001', '320001']

    Explanations:
      e1 for the first 'chunk' '300021'
        3 zeroes (000) grafted between 3 and 2 and 0 zeroes (none) between 2 and 1
      e2 for the second 'chunk' '300201'
        2 zeroes (00) grafted between 3 and 2 and 1 zero between 2 and 1
      and so on


    Fields for comparison
    =====================

    amounts_in_slots={self.amounts_in_slots} | gaphole_position_list={self.gaphole_position_list}
    graftzeroes_combination_list={self.graftzeroes_combination_list}
    grafting_coordlist={self.grafting_pos_n_zeroes_travlist}
    zerograft strs={self.zerograft_strs}

    """
    amounts_in_slots = [3, 2, 1]
    n_elements, n_slots = 6, 6
    zg = zgmx.ZeroesGraftAndCountsMixer(amounts_in_slots=amounts_in_slots, n_elements=n_elements, n_slots=n_slots)
    # t1 test mask
    expected_graftzeroes_combination_list = [[3, 0], [2, 1], [1, 2], [0, 3]]
    expected_grafting_coordlist = [[(1, 3)], [(1, 2), (2, 1)], [(1, 1), (2, 2)], [(2, 3)]]
    expected_zerografted_strs = ['300021', '300201', '302001', '320001']
    # self.assertEqual(expected_mask, returned_mask)
    # self.assertEqual(expected_grafted_strlist, returned_grafted_strlist)
    returned_grafted_strlist = zg.zerograft_strs
    self.assertEqual(expected_zerografted_strs, returned_grafted_strlist)

  def ztest_zerograft_2nd_hypothesis(self):
    """
    The subtests in this test-method encompass the following hypothesis:
      grafting scheme with:
        basecomb = [3, 1, 1, 1]
        graft_idx_positions = [1, 2, 3, 4]
    The expected values are:
      graft_size_cmbs = [[2, 0, 0, 0], [2, 1], [1, 2], [0, 3]]
      mask = [3, None, 2, None, 1]  # ie None occupies index-positions 1 & 3
      results = ('chunks') ['300021', '300201', '302001', '320001']

    Explanations:
      e1 for the first 'chunk' '300021'
        3 zeroes (000) grafted between 3 and 2 and 0 zeroes (none) between 2 and 1
      e2 for the second 'chunk' '300201'
        2 zeroes (00) grafted between 3 and 2 and 1 zero between 2 and 1
      and so on
    """
    basecomb, graft_idx_positions = [3, 3], [4]
    zg = zgmx.ZeroesGraftAndCountsMixer(amounts_in_slots=basecomb, graft_idx_positions=graft_idx_positions)
    expected_mask = [3, 3]  # [3, None, 3]
    returned_mask = zg.mask
    # t1 test mask
    self.assertEqual(expected_mask, returned_mask)
    expected_graft_size_cmbs = [[4], [3], [2], [1], [0]]
    returned_graft_size_cmbs = zg.graft_size_cmbs
    # t2 test grafting size combinations
    self.assertEqual(expected_graft_size_cmbs, returned_graft_size_cmbs)
    expected_grafted_strlist = ['300003', '30003', '3003', '303', '33']
    returned_grafted_strlist = zg.produce_the_zerografted_strs()
    # t3 test the strlist that is the result of grafting, called 'chunks' in the test-method's docstring
    self.assertEqual(expected_grafted_strlist, returned_grafted_strlist)
