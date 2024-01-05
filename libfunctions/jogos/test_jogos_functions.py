#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
import unittest
import libfunctions.jogos.jogos_functions as jf  # .get_n_acertos


class MyTest(unittest.TestCase):

  def test_1(self):
    # t1
    contrajogos =[]
    contrajogo = (1, 2, 3, 4, 5, 6)
    contrajogos.append(contrajogo)
    contrajogo = (1, 7, 8, 9, 11, 12)
    contrajogos.append(contrajogo)
    contrajogo = (1, 13, 14, 15, 17, 18)
    contrajogos.append(contrajogo)
    jogo_as_dezenas = (1, 7, 13, 19, 25, 26)
    repeats_array = jf.get_array_n_repeats_with_m_previous_games(jogo_as_dezenas, contrajogos)
    # ie, 3 dozens repeating once (d = 1, 7 & 13),
    #     1 dozen repeats (at least) twice (d=1),
    #     1 dozen repeats 3 times (d = 1)
    expected_result = [3, 1, 1]
    scrmsg = ('expected_result must equal repeats_array'
              ' from get_array_n_repeats_with_m_previous_games(jogo_as_dezenas, contrajogos)')
    self.assertEqual(repeats_array, expected_result, scrmsg)
    # t2
    contrajogos = []
    contrajogo = (1, 2, 3, 4, 5, 6)
    contrajogos.append(contrajogo)
    contrajogo = (1, 7, 8, 9, 11, 12)
    contrajogos.append(contrajogo)
    contrajogo = (1, 13, 14, 15, 17, 18)
    contrajogos.append(contrajogo)
    contrajogo = (1, 2, 3, 4, 5, 6)
    contrajogos.append(contrajogo)
    jogo_as_dezenas = (1, 6, 7, 13, 19, 25)
    repeats_array = jf.get_array_n_repeats_with_m_previous_games(jogo_as_dezenas, contrajogos)
    # ie, 4 dozens repeating once (d=1,6,7 & 13), 2 dozen repeats twice (d=1&6),
    # 1 dozen repeats 3 times (d=1), 1 dozen repeats 3 times (d=1),
    expected_result = [4, 2, 1, 1]
    self.assertEqual(repeats_array, expected_result, scrmsg)
