#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/test_zero_grafter_mixer.py
  Unit-tests for fs/mathfs/combinatorics/zero_grafter_mixer.py

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
import unittest
import fs.mathfs.combinatorics.zero_grafter_mixer as zgmx  # zg.ZeroesGraftAndCountsMixer


class TestCase1(unittest.TestCase):

  def test_zerografted_strs_w_grafting_coordlist(self):
    amounts_in_slots, n_slots = [3, 2, 1], 6
    grafting_coordlist = [[(1, 3)], [(1, 2), (2, 1)], [(1, 1), (2, 2)], [(2, 3)]]
    expected_zerograft_strs = ['300021', '300201', '302001', '320001']
    returned_zerograft_strs = zgmx.mount_zerografted_strs_w_grafting_coordlist(
      grafting_coordlist, amounts_in_slots=amounts_in_slots, n_slots=n_slots
    )
    # t1 test 'fuse' ie [[(1, 3)], [(1, 2), (2, 1)], [(1, 1), (2, 2)], [(2, 3)]]
    self.assertEqual(expected_zerograft_strs, returned_zerograft_strs)
    gaphole_position_list = [1, 2]
    n_elements, n_slots = 6, 6
    returned_zeroes_comblist = zgmx.get_gaphole_idxpos_list_for_zerografting_with(
      amounts_in_slots, n_elements=n_elements, n_slots=n_slots
    )
    expected_zeroes_comblist = [1, 2]
    graftzeroes_combination_list = [[3, 0], [2, 1], [1, 2], [0, 3]]
    # t2 test 'fuse' (the same as above)
    self.assertEqual(expected_zeroes_comblist, returned_zeroes_comblist)
    returned_fuse_coordlist = zgmx.fuse_combination_list_w_poslist(
      gaphole_position_list=gaphole_position_list, graftzeroes_combination_list=graftzeroes_combination_list
    )
    # t3
    self.assertEqual(grafting_coordlist, returned_fuse_coordlist)

  def test_zerograft_the_6_hypotheses(self):
    """

    Hypothesis 1:
      basecomp = [6]  # this means all 6 elements are in one row
      result: no possible zeroes-grafting
        (because zero-grafting is always "in-between")

    Hypothesis 2:
      basecomp = [5, 1]  # this means 5 elements in one row and 1 in another
      result:
        possible zeroes-grafting combinations: [
          [501, 5001, 50001, 500001]
        ] : 4 altogether

    Hypothesis 3:
      basecomp = [4, 1, 1]  # this means 4 elements in one row, 1 in another, 1 in yet another
      result:
        possible zeroes-grafting combinations: [
          4101, 4011, 41001, 40101, 40011,
          410001, 401001, 400101, 400011,
        ] : 9 altogether

    Hypothesis 4:
      basecomp = [4, 2]  # this means 4 elements in one row, 1 in another, 1 in yet another
      result is similar to basecomp = [5, 1] ie:
        possible zeroes-grafting combinations: [
          [402, 4002, 40002, 400002]
        ] : 4 altogether

    Hypothesis 5:
      basecomp = [3, 1, 1, 1]  # this means 4 elements in one row, 1 in another, 1 in yet another
      result:
        possible zeroes-grafting combinations: [
          31101, 31011, 31101, 301101, 300111,
        ] : 5 altogether

    Hypothesis 6:
      basecomp = [3, 2, 1]  # this means 4 elements in one row, 1 in another, 1 in yet another
      result is similar to basecomp = [4, 1, 1] ie:
        possible zeroes-grafting combinations: [
          3201, 3021, 32001, 30201, 30021,
          320001, 302001, 300201, 300021,
        ] : 9 altogether
    """
    # Hypothesis 1
    """
    amounts=[6], gapholes=[], comblist=[]
    ne=6, ns=6, coords=[]
    zerografted_strs = []
    """
    amounts_in_slots = [6]
    n_elements, n_slots = 6, 6
    zg = zgmx.ZeroesGraftAndCountsMixer(amounts_in_slots=amounts_in_slots, n_elements=n_elements, n_slots=n_slots)
    # 1 graftzeroes_combination_list
    expected_graftzeroes_combination_list = []
    returned_graftzeroes_combination_list = zg.graftzeroes_combination_list
    self.assertEqual(expected_graftzeroes_combination_list, returned_graftzeroes_combination_list)
    # 2 grafting_pos_n_zeroes_travlist
    expected_grafting_pos_n_zeroes_travlist = []
    returned_grafting_pos_n_zeroes_travlist = zg.grafting_pos_n_zeroes_travlist
    self.assertEqual(expected_grafting_pos_n_zeroes_travlist, returned_grafting_pos_n_zeroes_travlist)
    # 3 zerografted_strs
    expected_zerografted_strs = []
    returned_grafted_strlist = zg.zerograft_strs
    self.assertEqual(expected_zerografted_strs, returned_grafted_strlist)
    # Hypothesis 2
    """
    amounts=[5, 1], gapholes=[1], zerograft_comblist=[[4]]
    ne=6, ns=6, coords=[[(1, 4)]]
    zerografted_strs = ['500001']       
    """
    amounts_in_slots = [5, 1]  # this means 5 elements in one row and 1 in another
    zg = zgmx.ZeroesGraftAndCountsMixer(amounts_in_slots=amounts_in_slots, n_elements=n_elements, n_slots=n_slots)
    expected_graftzeroes_combination_list = [[4]]
    returned_graftzeroes_combination_list = zg.graftzeroes_combination_list
    self.assertEqual(expected_graftzeroes_combination_list, returned_graftzeroes_combination_list)
    expected_grafted_strlist = ['500001']
    returned_grafted_strlist = zg.zerograft_strs
    self.assertEqual(expected_grafted_strlist, returned_grafted_strlist)
    # Hypothesis 3
    """
    amounts=[4, 1, 1], gapholes=[1, 2] zerograft_comblist=[[3, 0], [2, 1], [1, 2], [0, 3]]
    ne=6, ns=6, coords=[[(1, 3)], [(1, 2), (2, 1)], [(1, 1), (2, 2)], [(2, 3)]]
    zerografted_strs = ['400011', '400101', '401001', '410001']
    """
    amounts_in_slots = [4, 1, 1]
    zg = zgmx.ZeroesGraftAndCountsMixer(amounts_in_slots=amounts_in_slots, n_elements=n_elements, n_slots=n_slots)
    expected_graftzeroes_combination_list = [[3, 0], [2, 1], [1, 2], [0, 3]]
    returned_graftzeroes_combination_list = zg.graftzeroes_combination_list
    self.assertEqual(expected_graftzeroes_combination_list, returned_graftzeroes_combination_list)
    expected_grafting_pos_n_zeroes_travlist = [[(1, 3)], [(1, 2), (2, 1)], [(1, 1), (2, 2)], [(2, 3)]]
    returned_grafting_pos_n_zeroes_travlist = zg.grafting_pos_n_zeroes_travlist
    self.assertEqual(expected_grafting_pos_n_zeroes_travlist, returned_grafting_pos_n_zeroes_travlist)
    expected_zerografted_strs = ['400011', '400101', '401001', '410001']
    returned_grafted_strlist = zg.zerograft_strs
    self.assertEqual(expected_zerografted_strs, returned_grafted_strlist)

    # Hypothesis 4
    """
    amounts=[4, 2], gapholes=[1], zerograft_comblist=[[4]]
    ne=6, ns=6, coords=[[(1, 4)]]
    zerografted_strs = ['400002']    
    """
    amounts_in_slots = [4, 1, 1]  # this means 4 elements in one row, 1 in another, 1 in yet another
    zg = zgmx.ZeroesGraftAndCountsMixer(amounts_in_slots=amounts_in_slots, n_elements=n_elements, n_slots=n_slots)
    # t1 test mask
    expected_graftzeroes_combination_list = [[4]]
    expected_grafting_coordlist = [[(1, 4)]]
    expected_zerografted_strs = ['400011', '400101', '401001', '410001']
    # self.assertEqual(expected_mask, returned_mask)
    # self.assertEqual(expected_grafted_strlist, returned_grafted_strlist)
    returned_grafted_strlist = zg.zerograft_strs
    self.assertEqual(expected_zerografted_strs, returned_grafted_strlist)

    # Hypothesis 6
    """
    amounts=[3, 2, 1], gapholes=[1, 2], comblist=[[3, 0], [2, 1], [1, 2], [0, 3]]
    ne=6, ns=6, coords=[[(1, 3)], [(1, 2), (2, 1)], [(1, 1), (2, 2)], [(2, 3)]]
    zerografted_strs = ['300021', '300201', '302001', '320001']    
    """
    amounts_in_slots = [3, 2, 1]
    n_elements, n_slots = 6, 6
    zg = zgmx.ZeroesGraftAndCountsMixer(amounts_in_slots=amounts_in_slots, n_elements=n_elements, n_slots=n_slots)
    # t1 test mask
    expected_graftzeroes_combination_list = [[3, 0], [2, 1], [1, 2], [0, 3]]
    returned_graftzeroes_combination_list = zg.graftzeroes_combination_list
    self.assertEqual(expected_graftzeroes_combination_list, returned_graftzeroes_combination_list)
    expected_gaphole_position_list = [1, 2]
    returned_gaphole_position_list = zg.gaphole_position_list
    self.assertEqual(expected_gaphole_position_list, returned_gaphole_position_list)
    expected_grafting_coordlist = [[(1, 3)], [(1, 2), (2, 1)], [(1, 1), (2, 2)], [(2, 3)]]
    returned_grafting_coordlist = zg.grafting_pos_n_zeroes_travlist
    self.assertEqual(expected_grafting_coordlist, returned_grafting_coordlist)
    expected_zerografted_strs = ['300021', '300201', '302001', '320001']
    returned_grafted_strlist = zg.zerograft_strs
    self.assertEqual(expected_zerografted_strs, returned_grafted_strlist)
