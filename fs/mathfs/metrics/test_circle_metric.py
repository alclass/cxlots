#!/usr/bin/env python3
"""
fs/mathfs/metrics/test_circle_metric.py
  Implements unit-tests to fs/mathfs/metrics/idxshapearea_circle_metric.py

From the latter, it's known that the metric "radius" is the same as colcomb and rowcomb.
Example:
  e1 It seems (still for better checking) that all cards that are (colcounts=222, rowcounts=33) are radius=158
  e2 All cards that are (colcounts=111111, rowcounts=6) are radius=223
  e2 All cards that are (colcounts=111111, rowcounts=6) are radius=203
Thus, the metric is reduced to a kind of "shape" (or figure-shape), ie:
  e1 is a 2*3 square (two rows & three columns)
  e2 is a 1*6 line (one row & six columns)

The metric might be seen as a triple where each component is equivalent, ie:
  e1 (colcomb=222, rowcomb=33, radius=158) is shape(2,3)
  e1 (colcomb=111111, rowcomb=6, radius=223) is shape(1,6)

All possible shapes are:
(1,6), (6,1)

"""
import unittest
import fs.mathfs.metrics.museum.idxshapearea_circle_metric as cm  # .extract_as_tupl_col1idx_n_row1idx_from_carddozen


class TestShapeMetric(unittest.TestCase):

  def test_separated_dozendigit_n_unitdigit_from_carddozen(self):
    limits = (1, 60)
    dezena = 15
    exp_doz_digit, exp_unit_digit = 1, 5
    ret_doz_digit, ret_unit_digit = cm.separate_as_tupl_dozen_n_unit_from_carddozen(dezena, limits)
    self.assertTrue((exp_doz_digit, exp_unit_digit), (ret_doz_digit, ret_unit_digit))
    dezena = 37
    exp_doz_digit, exp_unit_digit = 3, 7
    ret_doz_digit, ret_unit_digit = cm.separate_as_tupl_dozen_n_unit_from_carddozen(dezena, limits)
    self.assertTrue((exp_doz_digit, exp_unit_digit), (ret_doz_digit, ret_unit_digit))
    dezena = 3
    exp_doz_digit, exp_unit_digit = 0, 3
    ret_doz_digit, ret_unit_digit = cm.separate_as_tupl_dozen_n_unit_from_carddozen(dezena, limits)
    self.assertTrue((exp_doz_digit, exp_unit_digit), (ret_doz_digit, ret_unit_digit))
    dezena = 60
    exp_doz_digit, exp_unit_digit = 6, 0
    ret_doz_digit, ret_unit_digit = cm.separate_as_tupl_dozen_n_unit_from_carddozen(dezena, limits)
    self.assertTrue((exp_doz_digit, exp_unit_digit), (ret_doz_digit, ret_unit_digit))
    dezena = 61
    ret_doz_digit, ret_unit_digit = cm.separate_as_tupl_dozen_n_unit_from_carddozen(dezena, limits)
    self.assertTrue((None, None), (ret_doz_digit, ret_unit_digit))
    dezena = 0
    ret_doz_digit, ret_unit_digit = cm.separate_as_tupl_dozen_n_unit_from_carddozen(dezena, limits)
    self.assertTrue((None, None), (ret_doz_digit, ret_unit_digit))
    dezena = 'blah'
    ret_doz_digit, ret_unit_digit = cm.separate_as_tupl_dozen_n_unit_from_carddozen(dezena, limits)
    self.assertTrue((None, None), (ret_doz_digit, ret_unit_digit))

  def test_extract_row1idx_n_col1idx_from_carddozen(self):
    limits = (1, 60)
    dezena, exp_row1idx_digit, exp_col1idx_digit = 15, 2, 5
    ret_row1idx_digit, ret_row1idx_digit = cm.extract_as_tupl_col1idx_n_row1idx_from_carddozen(dezena, limits)
    self.assertTrue((exp_row1idx_digit, exp_col1idx_digit), (ret_row1idx_digit, ret_row1idx_digit))
    dezena, exp_row1idx_digit, exp_col1idx_digit = 10, 1, 0
    ret_row1idx_digit, ret_row1idx_digit = cm.extract_as_tupl_col1idx_n_row1idx_from_carddozen(dezena, limits)
    self.assertTrue((exp_row1idx_digit, exp_col1idx_digit), (ret_row1idx_digit, ret_row1idx_digit))
    dezena, exp_row1idx_digit, exp_col1idx_digit = 37, 4, 7  # dezena = 37
    ret_row1idx_digit, ret_row1idx_digit = cm.extract_as_tupl_col1idx_n_row1idx_from_carddozen(dezena, limits)
    self.assertTrue((exp_row1idx_digit, exp_col1idx_digit), (ret_row1idx_digit, ret_row1idx_digit))
    dezena, exp_row1idx_digit, exp_col1idx_digit = 13, 2, 3  # dezena = 3
    ret_row1idx_digit, ret_row1idx_digit = cm.extract_as_tupl_col1idx_n_row1idx_from_carddozen(dezena, limits)
    self.assertTrue((exp_row1idx_digit, exp_col1idx_digit), (ret_row1idx_digit, ret_row1idx_digit))
    dezena, exp_row1idx_digit, exp_col1idx_digit = 60, 6, 0
    ret_row1idx_digit, ret_row1idx_digit = cm.extract_as_tupl_col1idx_n_row1idx_from_carddozen(dezena, limits)
    self.assertTrue((exp_row1idx_digit, exp_col1idx_digit), (ret_row1idx_digit, ret_row1idx_digit))
    dezena = 61
    ret_row1idx_digit, ret_row1idx_digit = cm.extract_as_tupl_col1idx_n_row1idx_from_carddozen(dezena, limits)
    self.assertTrue((None, None), (ret_row1idx_digit, ret_row1idx_digit))
    dezena = 0
    ret_row1idx_digit, ret_row1idx_digit = cm.extract_as_tupl_col1idx_n_row1idx_from_carddozen(dezena, limits)
    self.assertTrue((None, None), (ret_row1idx_digit, ret_row1idx_digit))
    dezena = 'blah'
    ret_row1idx_digit, ret_row1idx_digit = cm.extract_as_tupl_col1idx_n_row1idx_from_carddozen(dezena, limits)
    self.assertTrue((None, None), (ret_row1idx_digit, ret_row1idx_digit))

  def test_col_n_row_stretches(self):
    """

    """
    dezenas = (1, 2, 3, 4, 5, 6)
    # colstretch should be 111111 and rowstretch 6
    exp_rowstretch = [6]
    exp_colstretch = [1, 1, 1, 1, 1, 1]
    ret_rowstretch, ret_colstretch = cm.get_col_n_row_1indices_inbetweenzerografted_from_cardarray(dezenas)
    self.assertTrue((exp_rowstretch, exp_colstretch), (ret_rowstretch, ret_colstretch))
    dezenas = (1, 3, 5, 6, 7, 9)
    # colstretch should be 101011101 and rowstretch 6
    # exp_rowstretch = [6]
    exp_colstretch = [1, 0, 1, 0, 1, 1, 1, 0, 1]
    ret_rowstretch, ret_colstretch = cm.get_col_n_row_1indices_inbetweenzerografted_from_cardarray(dezenas)
    self.assertTrue((exp_rowstretch, exp_colstretch), (ret_rowstretch, ret_colstretch))
    dezenas = (1, 12, 23, 34, 45, 56)
    # colstretch should be 111111 and rowstretch 111111
    exp_rowstretch = [1, 1, 1, 1, 1, 1]
    exp_colstretch = [1, 1, 1, 1, 1, 1]
    ret_rowstretch, ret_colstretch = cm.get_col_n_row_1indices_inbetweenzerografted_from_cardarray(dezenas)
    self.assertTrue((exp_rowstretch, exp_colstretch), (ret_rowstretch, ret_colstretch))
    dezenas = (1, 13, 15, 36, 57, 59)
    # colstretch should be 101011101 and rowstretch 120102
    exp_colstretch = [1, 2, 0, 1, 0, 2]
    ret_rowstretch, ret_colstretch = cm.get_col_n_row_1indices_inbetweenzerografted_from_cardarray(dezenas)
    self.assertTrue((exp_rowstretch, exp_colstretch), (ret_rowstretch, ret_colstretch))
    dezenas = (1, 13, 'blah', 36, 57, 59)
    # because of the 'blah' grafted into it, colstretch should be '' (in fact, []) and rowstretch '' (in fact, [])
    ret_rowstretch, ret_colstretch = cm.get_col_n_row_1indices_inbetweenzerografted_from_cardarray(dezenas)
    self.assertTrue(([], []), (ret_rowstretch, ret_colstretch))

  def test_col_n_row_stretches_pattstr(self):
    dezenas = (1, 2, 3, 4, 5, 6)
    # colstretch should be 111111 and rowstretch 6
    exp_rowstretch_str = '6'
    exp_colstretch_str = '1'*6
    ret_colstretch_str, ret_rowstretch_str = cm.get_asstr_col_n_row_1indices_inbetweenzerografted(dezenas)
    self.assertEqual((exp_colstretch_str, exp_rowstretch_str), (ret_colstretch_str, ret_rowstretch_str))
    dezenas = (1, 3, 5, 6, 7, 9)
    # colstretch should be 101011101 and rowstretch 6
    # exp_rowstretch_str = '6'
    exp_colstretch_str = '101011101'
    ret_colstretch_str, ret_rowstretch_str = cm.get_asstr_col_n_row_1indices_inbetweenzerografted(dezenas)
    self.assertEqual((exp_colstretch_str, exp_rowstretch_str), (ret_colstretch_str, ret_rowstretch_str))
    dezenas = (1, 12, 23, 34, 45, 56)
    # colstretch should be 111111 and rowstretch 111111
    exp_colstretch_str = '1'*6
    exp_rowstretch_str = '1'*6
    ret_colstretch_str, ret_rowstretch_str = cm.get_asstr_col_n_row_1indices_inbetweenzerografted(dezenas)
    self.assertEqual((exp_colstretch_str, exp_rowstretch_str), (ret_colstretch_str, ret_rowstretch_str))
    dezenas = (1, 13, 15, 36, 57, 59)
    # colstretch should be 101011101 and rowstretch the same as above
    exp_colstretch_str = '101011101'
    exp_rowstretch_str = '120102'
    ret_colstretch_str, ret_rowstretch_str = cm.get_asstr_col_n_row_1indices_inbetweenzerografted(dezenas)
    self.assertEqual((exp_colstretch_str, exp_rowstretch_str), (ret_colstretch_str, ret_rowstretch_str))
    dezenas = (5, 13, 15, 35, 37, 55)
    # colstretch should be 120102 and rowstretch 120102
    exp_colstretch_str = '10401'
    exp_rowstretch_str = '120201'
    ret_colstretch_str, ret_rowstretch_str = cm.get_asstr_col_n_row_1indices_inbetweenzerografted(dezenas)
    self.assertEqual((exp_colstretch_str, exp_rowstretch_str), (ret_colstretch_str, ret_rowstretch_str))
    dezenas = (14, 16, 18, 54, 56, 58)
    # colstretch should be 300003 and rowstretch 20202
    exp_colstretch_str = '20202'
    exp_rowstretch_str = '30003'
    ret_colstretch_str, ret_rowstretch_str = cm.get_asstr_col_n_row_1indices_inbetweenzerografted(dezenas)
    self.assertEqual((exp_colstretch_str, exp_rowstretch_str), (ret_colstretch_str, ret_rowstretch_str))
    dezenas = (1, 13, 'blah', 36, 57, 59)
    # because of the 'blah' grafted into it, colstretch should be '' (in fact, []) and rowstretch '' (in fact, [])
    ret_colstretch_str, ret_rowstretch_str = cm.get_asstr_col_n_row_1indices_inbetweenzerografted(dezenas)
    self.assertEqual(('', ''), (ret_colstretch_str, ret_rowstretch_str))

  def test_get_abstract_card_radius(self):
    jogos = []
    dezenas = (14, 16, 18, 54, 56, 58)

    jogos.append(dezenas)
    dezenas = (12, 14, 25, 16, 17, 18)
    jogos.append(dezenas)
    dezenas = (12, 14, 15, 16, 17, 18)
    jogos.append(dezenas)
    dezenas = (22, 24, 25, 26, 27, 28)
    jogos.append(dezenas)
    dezenas = (1, 11, 21, 31, 41, 51)
    jogos.append(dezenas)
    dezenas = (1, 2, 3, 11, 12, 13)
    jogos.append(dezenas)
    dezenas = (4, 5, 6, 14, 15, 16)
    jogos.append(dezenas)
