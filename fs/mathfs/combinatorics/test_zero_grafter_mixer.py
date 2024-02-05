#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/test_zero_grafter_mixer.py
  Unit-tests for fs/mathfs/combinatorics/zero_grafter_mixer.py
"""
import unittest
import fs.mathfs.combinatorics.zero_grafter_mixer as zgmx  # zg.ZeroesGraftAndCountsMixer


class TestCase1(unittest.TestCase):

  def test_zerograft_1(self):
    """
    @see more info about the grafting scheme in class ZeroesGraftAndCountsMixer

    An example of a grafting scheme with basecomb = [3, 2, 1] & graft_idx_positions = [1, 3]
      graft_size_cmbs = [[3, 0], [2, 1], [1, 2], [0, 3]]
      mask [3, None, 2, None, 1]  # ie None occupies index-positions 1 & 3
      results ('chunks') ['300021', '300201', '302001', '320001']

    Explanations:
      e1 for the first 'chunk' '300021'
        3 zeroes (000) grafted between 3 and 2 and 0 zeroes (none) between 2 and 1
      e2 for the second 'chunk' '300201'
        2 zeroes (00) grafted between 3 and 2 and 1 zero between 2 and 1
      and so on
    """
    basecomb, graft_idx_positions = [3, 2, 1], [1, 3]
    zg = zgmx.ZeroesGraftAndCountsMixer(basecomb=basecomb, graft_idx_positions=graft_idx_positions)
    expected_mask = [3, None, 2, None, 1]
    returned_mask = zg.mask
    # t1 test mask
    self.assertEqual(expected_mask, returned_mask)
    expected_graft_size_cmbs = [[3, 0], [2, 1], [1, 2], [0, 3]]
    returned_graft_size_cmbs = zg.graft_size_cmbs
    # t2 test grafting size combinations
    self.assertEqual(expected_graft_size_cmbs, returned_graft_size_cmbs)
    expected_grafted_strlist = ['300021', '300201', '302001', '320001']
    returned_grafted_strlist = zg.mix()
    # t3 test the strlist that is the result of grafting, called 'chunks' in the test-method's docstring
    self.assertEqual(expected_grafted_strlist, returned_grafted_strlist)

  def ztest_zerograft_2(self):
    """
    Same as test_zerograft_1 with a different input set

    Up til now, notice the "z" above in the test methodname, so that it's run until
      we find how to solve the combination input parameters below
    """
    basecomb, graft_idx_positions = [1, 3, 2], [1, 4]
    zg = zgmx.ZeroesGraftAndCountsMixer(basecomb=basecomb, graft_idx_positions=graft_idx_positions)
    expected_mask = [None, 4, None, 2, None]
    returned_mask = zg.mask
    # t1 test mask
    self.assertEqual(expected_mask, returned_mask)
    expected_graft_size_cmbs = [[3, 0], [2, 1], [1, 2], [0, 3]]
    returned_graft_size_cmbs = zg.graft_size_cmbs
    # t2 test grafting size combinations
    self.assertEqual(expected_graft_size_cmbs, returned_graft_size_cmbs)
    expected_grafted_strlist = ['300021', '300201', '302001', '320001']
    returned_grafted_strlist = zg.mix()
    # t3 test the strlist that is the result of grafting, called 'chunks' in the test-method's docstring
    self.assertEqual(expected_grafted_strlist, returned_grafted_strlist)
