#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/test_soma_media_dsvpdr_etal.py
  Unit-tests for fs/mathfs/combinatorics/soma_media_dsvpdr_etal.py

import statistics as sta
"""
import unittest
import fs.mathfs.metrics.soma_media_dsvpdr_etal as smd  # smd.EnclosingAroundPointFinder


class TestCase1(unittest.TestCase):

  def test_surrounding_ints_in_a_10x6matrix_card(self):
    """
    (Unit-)Tests the integer numbers that are around (in 8 geographical positions:
      east, west, south, north, southeast, southwest, northeast and northwest) a specific 'source' number
      in a cardgame matrix.

    Example:
      intval=35 is surrounded, in a 10x6 cardmatrix, by:
        {'east': 36, 'west': 34, 'south': 45, 'north': 25,
         'southeast': 46, 'southwest': 44, 'northeast': 26, 'northwest': 24}

    The first method below has tests for the default 10x6 cardmatrix, having 10 columns and 6 rows.
    The second method in continuation tests under a different 2D cardmatrix size.
    """
    # t1 the top-leftmost edge
    dozen = 1
    expected_surrounding_dict = {
      'east': 2, 'west': 10, 'south': 11, 'north': 51,
      'southeast': 12, 'southwest': 20, 'northeast': 52, 'northwest': 60,
    }
    surround_finder = smd.EightAdjacentSurroundingNumberFinder(dozen)
    returned_surrounding_dict = surround_finder.surrounding_dict
    self.assertEqual(expected_surrounding_dict, returned_surrounding_dict)
    expected_surrounding_ints = sorted(expected_surrounding_dict.values())
    returned_surrounding_ints = surround_finder.surrounding_ints
    self.assertEqual(expected_surrounding_ints, returned_surrounding_ints)
    # t2 the top-rightmost edge
    dozen = 10
    expected_surrounding_dict = {
      'east': 1, 'west': 9, 'south': 20, 'north': 60,
      'southeast': 11, 'southwest': 19, 'northeast': 51, 'northwest': 59,
    }
    surround_finder = smd.EightAdjacentSurroundingNumberFinder(dozen)
    returned_surrounding_dict = surround_finder.surrounding_dict
    self.assertEqual(expected_surrounding_dict, returned_surrounding_dict)
    expected_surrounding_ints = sorted(expected_surrounding_dict.values())
    returned_surrounding_ints = surround_finder.surrounding_ints
    self.assertEqual(expected_surrounding_ints, returned_surrounding_ints)
    # t3 the bottom-leftmost edge
    dozen = 51
    expected_surrounding_dict = {
      'east': 52, 'west': 60, 'south': 1, 'north': 41,
      'southeast': 2, 'southwest': 10, 'northeast': 42, 'northwest': 50,
    }
    surround_finder = smd.EightAdjacentSurroundingNumberFinder(dozen)
    returned_surrounding_dict = surround_finder.surrounding_dict
    self.assertEqual(expected_surrounding_dict, returned_surrounding_dict)
    expected_surrounding_ints = sorted(expected_surrounding_dict.values())
    returned_surrounding_ints = surround_finder.surrounding_ints
    self.assertEqual(expected_surrounding_ints, returned_surrounding_ints)
    # t4 the bottom-rightmost edge
    dozen = 60
    expected_surrounding_dict = {
      'east': 51, 'west': 59, 'south': 10, 'north': 50,
      'southeast': 1, 'southwest': 9, 'northeast': 41, 'northwest': 49,
    }
    surround_finder = smd.EightAdjacentSurroundingNumberFinder(dozen)
    returned_surrounding_dict = surround_finder.surrounding_dict
    self.assertEqual(expected_surrounding_dict, returned_surrounding_dict)
    expected_surrounding_ints = sorted(expected_surrounding_dict.values())
    returned_surrounding_ints = surround_finder.surrounding_ints
    self.assertEqual(expected_surrounding_ints, returned_surrounding_ints)
    # t5 a cardmiddle value
    dozen = 35
    expected_surrounding_dict = {
      'east': 36, 'west': 34, 'south': 45, 'north': 25,
      'southeast': 46, 'southwest': 44, 'northeast': 26, 'northwest': 24,
    }
    surround_finder = smd.EightAdjacentSurroundingNumberFinder(dozen)
    returned_surrounding_dict = surround_finder.surrounding_dict
    self.assertEqual(expected_surrounding_dict, returned_surrounding_dict)
    expected_surrounding_ints = sorted(expected_surrounding_dict.values())
    returned_surrounding_ints = surround_finder.surrounding_ints
    self.assertEqual(expected_surrounding_ints, returned_surrounding_ints)

  def test_surrounding_ints_in_a_8x3matrix_card(self):
    """
    Same test-method as above but changing the default 10x6 for one with 8x3

    """
    # t1 the top-leftmost edge
    dozen = 1
    expected_surrounding_dict = {
      'east': 2, 'west': 8, 'south': 11, 'north': 21,
      'southeast': 12, 'southwest': 18, 'northeast': 22, 'northwest': 28,
    }
    maxcol, maxrow = 8, 3
    surround_finder = smd.EightAdjacentSurroundingNumberFinder(dozen, maxcol=maxcol, maxrow=maxrow)
    returned_surrounding_dict = surround_finder.surrounding_dict
    self.assertEqual(expected_surrounding_dict, returned_surrounding_dict)
    expected_surrounding_ints = sorted(expected_surrounding_dict.values())
    returned_surrounding_ints = surround_finder.surrounding_ints
    self.assertEqual(expected_surrounding_ints, returned_surrounding_ints)
    # t2 the top-rightmost edge
    dozen = 8
    expected_surrounding_dict = {
      'east': 1, 'west': 7, 'south': 18, 'north': 28,
      'southeast': 11, 'southwest': 17, 'northeast': 21, 'northwest': 27,
    }
    surround_finder = smd.EightAdjacentSurroundingNumberFinder(dozen, maxcol=maxcol, maxrow=maxrow)
    returned_surrounding_dict = surround_finder.surrounding_dict
    self.assertEqual(expected_surrounding_dict, returned_surrounding_dict)
    expected_surrounding_ints = sorted(expected_surrounding_dict.values())
    returned_surrounding_ints = surround_finder.surrounding_ints
    self.assertEqual(expected_surrounding_ints, returned_surrounding_ints)
    # t3 the bottom-leftmost edge
    dozen = 21
    expected_surrounding_dict = {
      'east': 22, 'west': 28, 'south': 1, 'north': 11,
      'southeast': 2, 'southwest': 8, 'northeast': 12, 'northwest': 18,
    }
    surround_finder = smd.EightAdjacentSurroundingNumberFinder(dozen, maxcol=maxcol, maxrow=maxrow)
    returned_surrounding_dict = surround_finder.surrounding_dict
    self.assertEqual(expected_surrounding_dict, returned_surrounding_dict)
    expected_surrounding_ints = sorted(expected_surrounding_dict.values())
    returned_surrounding_ints = surround_finder.surrounding_ints
    self.assertEqual(expected_surrounding_ints, returned_surrounding_ints)
    # t4 the bottom-rightmost edge
    dozen = 28
    expected_surrounding_dict = {
      'east': 21, 'west': 27, 'south': 8, 'north': 18,
      'southeast': 1, 'southwest': 7, 'northeast': 11, 'northwest': 17,
    }
    surround_finder = smd.EightAdjacentSurroundingNumberFinder(dozen, maxcol=maxcol, maxrow=maxrow)
    returned_surrounding_dict = surround_finder.surrounding_dict
    self.assertEqual(expected_surrounding_dict, returned_surrounding_dict)
    expected_surrounding_ints = sorted(expected_surrounding_dict.values())
    returned_surrounding_ints = surround_finder.surrounding_ints
    self.assertEqual(expected_surrounding_ints, returned_surrounding_ints)
    # t5 a cardmiddle value
    dozen = 15
    expected_surrounding_dict = {
      'east': 16, 'west': 14, 'south': 25, 'north': 5,
      'southeast': 26, 'southwest': 24, 'northeast': 6, 'northwest': 4,
    }
    surround_finder = smd.EightAdjacentSurroundingNumberFinder(dozen, maxcol=maxcol, maxrow=maxrow)
    returned_surrounding_dict = surround_finder.surrounding_dict
    self.assertEqual(expected_surrounding_dict, returned_surrounding_dict)
    expected_surrounding_ints = sorted(expected_surrounding_dict.values())
    returned_surrounding_ints = surround_finder.surrounding_ints
    self.assertEqual(expected_surrounding_ints, returned_surrounding_ints)
