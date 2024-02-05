#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/test_hanoi_like_tower_piecemover.py
  Unit-tests for fs/mathfs/combinatorics/hanoi_like_tower_piecemover.py
"""
import unittest
import fs.mathfs.combinatorics.hanoi_like_tower_piecemover as hlt  # hlt.HanoiLikeTowerPieceMover


class TestCase1(unittest.TestCase):

  def test_1(self):
    # t1 tests the HanoiLike mover (initially with low values for npieces & nslots, forming 2 elements)
    npieces, nslots = 1, 2
    mover = hlt.HanoiLikeTowerPieceMover(npieces=npieces, nslots=nslots)
    expected_combinations = [[1, 0], [0, 1]]  # 2 elements
    self.assertEqual(expected_combinations, mover.all_combinations)
    self.assertEqual(len(expected_combinations), mover.size)
    # t2 same as t1 with different init parameters (forming 4 elements)
    npieces, nslots = 3, 2
    mover = hlt.HanoiLikeTowerPieceMover(npieces=npieces, nslots=nslots)
    expected_combinations = [[3, 0], [2, 1], [1, 2], [0, 3]]  # 4 elements
    self.assertEqual(expected_combinations, mover.all_combinations)
    self.assertEqual(len(expected_combinations), mover.size)
    # t3 same as t1 with different init parameters (forming 5 elements)
    npieces, nslots = 4, 2
    mover = hlt.HanoiLikeTowerPieceMover(npieces=npieces, nslots=nslots)
    expected_combinations = [[4, 0], [3, 1], [2, 2], [1, 3], [0, 4]]  # 5 elements
    self.assertEqual(expected_combinations, mover.all_combinations)
    self.assertEqual(len(expected_combinations), mover.size)
    # t4 same as t1 with different init parameters (forming 9 elements)
    npieces, nslots = 4, 3
    mover = hlt.HanoiLikeTowerPieceMover(npieces=npieces, nslots=nslots)
    expected_combinations = [
      [4, 0, 0], [3, 1, 0], [2, 2, 0], [1, 3, 0], [0, 4, 0],
      [0, 3, 1], [0, 2, 2], [0, 1, 3], [0, 0, 4]
    ]  # 9 elements
    self.assertEqual(expected_combinations, mover.all_combinations)
    self.assertEqual(len(expected_combinations), mover.size)
    # t5 same as t1 with different init parameters (forming 13 elements)
    npieces, nslots = 3, 5
    mover = hlt.HanoiLikeTowerPieceMover(npieces=npieces, nslots=nslots)
    expected_combinations = [
      [3, 0, 0, 0, 0], [2, 1, 0, 0, 0], [1, 2, 0, 0, 0], [0, 3, 0, 0, 0], [0, 2, 1, 0, 0],
      [0, 1, 2, 0, 0], [0, 0, 3, 0, 0], [0, 0, 2, 1, 0], [0, 0, 1, 2, 0], [0, 0, 0, 3, 0],
      [0, 0, 0, 2, 1], [0, 0, 0, 1, 2], [0, 0, 0, 0, 3]
    ]  # 13 elements
    self.assertEqual(expected_combinations, mover.all_combinations)
    self.assertEqual(len(expected_combinations), mover.size)
