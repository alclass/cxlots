#!/usr/bin/env python3
"""
fs/jogos/test_til_functions.py
  Contains unit-tests for fs/jogos/til_functions.py
"""
import unittest
import fs.jogos.til_functions as tf  # .sum_digits


class Test(unittest.TestCase):

  def test_sum_digits(self):
    expected = 6  # eg 1+0+2+2+1=6
    for pattern in ['10221', '11112', '600000000', '111111', '0000000000000051']:
      self.assertEqual(tf.sum_digits(pattern), expected)
    for pattern in ['310221', '911112', '1600000000', '9111111', '30000000000000051', '0']:
      # expected is still the same above, ie 6
      self.assertNotEqual(tf.sum_digits(pattern), expected)
    for pattern in ['a10221', 'string', 1.23, ['blah', 'blah'], '-1', '+0']:
      self.assertIsNone(tf.sum_digits(pattern))

  def test_get_all_possible_til_patterns_for(self):
    """

    """
    # t1
    n_slots, psoma = 0, 3
    expected_tilpattern = []
    returned_tilpattern = tf.get_all_possible_til_patterns_for(n_slots=n_slots, psoma=psoma)
    self.assertEqual(expected_tilpattern, returned_tilpattern)
    # t2
    n_slots, psoma = 1, 9
    expected_tilpattern = ['9']
    returned_tilpattern = tf.get_all_possible_til_patterns_for(n_slots=n_slots, psoma=psoma)
    self.assertEqual(expected_tilpattern, returned_tilpattern)
    # t3
    n_slots, psoma = 1, 10
    expected_tilpattern = []
    returned_tilpattern = tf.get_all_possible_til_patterns_for(n_slots=n_slots, psoma=psoma)
    self.assertEqual(expected_tilpattern, returned_tilpattern)
    # t4
    n_slots, psoma = 2, 10
    expected_tilpattern = ['']
    returned_tilpattern = tf.get_all_possible_til_patterns_for(n_slots=n_slots, psoma=psoma)
    self.assertEqual(expected_tilpattern, returned_tilpattern)
    # t4
    n_slots, psoma = 2, 6
    expected_tilpattern = ['06', '60', '15', '51', '24', '42', '33']
    returned_tilpattern = tf.get_all_possible_til_patterns_for(n_slots=n_slots, psoma=psoma)
    self.assertEqual(expected_tilpattern, returned_tilpattern)
    # t2 get_all_possible_til_patterns_for()
    n_slots, psoma = 2, 5
    expected_tilpattern = ['05', '50', '14', '41', '23', '32']
    returned_tilpattern = tf.get_all_possible_til_patterns_for(n_slots=n_slots, psoma=psoma)
    self.assertEqual(expected_tilpattern, returned_tilpattern)
    # t3 get_all_possible_til_patterns_for()
    n_slots, psoma = 3, 3
    # sorted is used because the expected tilpattern has not been put in the function order
    expected_tilpattern = sorted(['003', '030', '300', '012', '102', '120', '210', '201', '021', '111'])
    returned_tilpattern = sorted(tf.get_all_possible_til_patterns_for(n_slots=n_slots, psoma=psoma))
    self.assertEqual(expected_tilpattern, returned_tilpattern)
    # t4 get_all_possible_til_patterns_for()
    n_slots, psoma = 5, 6
    # sorted is not used because the expected tilpattern has been put in the same function order
    expected_tilpattern = [
        '00006', '00060', '00600', '06000', '60000', '00015', '00051', '00105', '00150', '00501', '00510', '01005',
        '01050', '01500', '05001', '05010', '05100', '10005', '10050', '10500', '15000', '50001', '50010', '50100',
        '51000', '00024', '00042', '00204', '00240', '00402', '00420', '02004', '02040', '02400', '04002', '04020',
        '04200', '20004', '20040', '20400', '24000', '40002', '40020', '40200', '42000', '00114', '00141', '00411',
        '01014', '01041', '01104', '01140', '01401', '01410', '04011', '04101', '04110', '10014', '10041', '10104',
        '10140', '10401', '10410', '11004', '11040', '11400', '14001', '14010', '14100', '40011', '40101', '40110',
        '41001', '41010', '41100', '00033', '00303', '00330', '03003', '03030', '03300', '30003', '30030', '30300',
        '33000', '00123', '00132', '00213', '00231', '00312', '00321', '01023', '01032', '01203', '01230', '01302',
        '01320', '02013', '02031', '02103', '02130', '02301', '02310', '03012', '03021', '03102', '03120', '03201',
        '03210', '10023', '10032', '10203', '10230', '10302', '10320', '12003', '12030', '12300', '13002', '13020',
        '13200', '20013', '20031', '20103', '20130', '20301', '20310', '21003', '21030', '21300', '23001', '23010',
        '23100', '30012', '30021', '30102', '30120', '30201', '30210', '31002', '31020', '31200', '32001', '32010',
        '32100', '01113', '01131', '01311', '03111', '10113', '10131', '10311', '11013', '11031', '11103', '11130',
        '11301', '11310', '13011', '13101', '13110', '30111', '31011', '31101', '31110', '00222', '02022', '02202',
        '02220', '20022', '20202', '20220', '22002', '22020', '22200', '01122', '01212', '01221', '02112', '02121',
        '02211', '10122', '10212', '10221', '11022', '11202', '11220', '12012', '12021', '12102', '12120', '12201',
        '12210', '20112', '20121', '20211', '21012', '21021', '21102', '21120', '21201', '21210', '22011', '22101',
        '22110', '11112', '11121', '11211', '12111', '21111']
    returned_tilpattern = tf.get_all_possible_til_patterns_for(n_slots=n_slots, psoma=psoma)
    self.assertEqual(expected_tilpattern, returned_tilpattern)
