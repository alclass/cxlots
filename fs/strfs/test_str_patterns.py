#!/usr/bin/env python
"""
fs/strfs/test_str_patterns.py
  Contains unit-tests for fs/strfs/str_patterns.py

"""
import unittest
import fs.strfs.str_patterns as strp  # .trans_intlist_to_zfillstrlist


class TestCase1(unittest.TestCase):

  def test_trans_intlist_to_zfillstrlist(self):
    """
    This function converts an int (used for dozens) list to a zfilled string
      whose items are space-separated
    Example:
      f([1, 2, 3, 4, 5, 6]) => '01 02 03 04 05 06
    """
    # t1 given an input_list (an intlist) and the default with zfill as None & dosort as False
    input_list = [6, 2, 1, 4, 5, 3]
    expected_strlist = '6 2 1 4 5 3'
    returned_strlist = strp.trans_intlist_to_zfillstrlist(input_list)  # default zfill=None, dosort=False
    self.assertEqual(expected_strlist, returned_strlist)
    # t2 variation of t1 reusing its input_list with zfill as 2 & dosort as True
    zfill, dosort = 2, True
    expected_strlist = '01 02 03 04 05 06'
    returned_strlist = strp.trans_intlist_to_zfillstrlist(input_list, zfill=zfill, dosort=dosort)
    self.assertEqual(expected_strlist, returned_strlist)
    # t3 variation of t1
    input_list = [6, 254, 1, 44, 5, 3]
    expected_strlist = '6 254 1 44 5 3'
    returned_strlist = strp.trans_intlist_to_zfillstrlist(input_list)  # default zfill=None, dosort=False
    self.assertEqual(expected_strlist, returned_strlist)
    # t4 an empty input list will return the empty string ''
    input_list = []
    expected_strlist = ''
    returned_strlist = strp.trans_intlist_to_zfillstrlist(input_list)
    self.assertEqual(expected_strlist, returned_strlist)
    # t5 non-int's will be removed
    input_list = ['blah bla', 'foo bar']
    expected_strlist = ''
    returned_strlist = strp.trans_intlist_to_zfillstrlist(input_list)
    self.assertEqual(expected_strlist, returned_strlist)
    # t6 a variation of t5: int numbers mixed with string, non-int's will be removed, int's remain
    input_list = ['blah bla', 9, 'foo bar']
    expected_strlist = '9'
    returned_strlist = strp.trans_intlist_to_zfillstrlist(input_list)
    self.assertEqual(expected_strlist, returned_strlist)
    # t7 a variation with zfill=4
    input_list = [344, 1, 55]
    expected_strlist = '0001 0055 0344'
    zfill, dosort = 4, True
    returned_strlist = strp.trans_intlist_to_zfillstrlist(input_list, zfill=zfill, dosort=dosort)
    self.assertEqual(expected_strlist, returned_strlist)
    # t8 a number overtaking zfillspace (zfill=2 limits int's up to 99) will be removed from the output
    input_list = [55, 9344, 3]
    expected_strlist = '55 03'
    zfill, dosort = 2, False
    returned_strlist = strp.trans_intlist_to_zfillstrlist(input_list, zfill=zfill, dosort=dosort)
    self.assertEqual(expected_strlist, returned_strlist)
    # t9 this last test is a bit obvious due to the former one, but it's just to emphasize the element removal
    intlist_obeying_zfill = [1, 55]  # 9344 is REMOVED
    self.assertEqual(len(intlist_obeying_zfill), len(returned_strlist.split(' ')))

  def test_trans_intlist_to_descendant_stair_strlist(self):
    """
    Example:
      f([1, 3, 4, 2, 6, 5]) => '0123456'

    """
    pass

  def test_trans_intlist_spacesep_printable_str(self):
    """
    Example:
      f([1, 2, 3, 4, 5, 6]) => '01 02 03 04 05 06'

    This test repeats testing of trans_intlist_to_zfillstrlist()
      ie, trans_intlist_spacesep_printable_str() calls the latter.
    """
    intlist = [1, 2, 3, 4, 5, 6]
    expected_str = '01 02 03 04 05 06'
    returned_str = strp.trans_intlist_spacesep_printable_str(intlist, zfill=2)
    self.assertEqual(expected_str, returned_str)

  def test_trans_spacesep_numberstr_to_intlist(self):
    """
    Example:
      f('01 02 03 04 05 06') => [1,2,3,4,5,6]
    """
    # t1 given a numberstr formed with zfill=2
    numberstr = '01 02 03 04 05 06'
    expected_intlist = [1, 2, 3, 4, 5, 6]
    returned_intlist = strp.trans_spacesep_numberstr_to_intlist(numberstr)
    self.assertEqual(expected_intlist, returned_intlist)
    # t2 variation of t1 without zfill=2
    numberstr = '1 2 3 4 5 6'
    expected_intlist = [1, 2, 3, 4, 5, 6]
    returned_intlist = strp.trans_spacesep_numberstr_to_intlist(numberstr)
    self.assertEqual(expected_intlist, returned_intlist)
    # t3 variation of t1 & t2 with non-numbers mixed in, notice also repeated numbers are valid
    numberstr = '9 7 blah 4 foo 6 bar 6'
    expected_intlist = [9, 7, 4, 6, 6]
    returned_intlist = strp.trans_spacesep_numberstr_to_intlist(numberstr)
    self.assertEqual(expected_intlist, returned_intlist)
