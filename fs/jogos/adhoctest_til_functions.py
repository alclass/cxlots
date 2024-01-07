#!/usr/bin/env python3
"""
fs/jogos/adhoctest_til_functions.py

import maths2.combinatorics.combinatoric_algorithms as combinatorics
"""
import fs.jogos.til_functions as tf  # .sum_digits


def do_adhoc_test(n_slots, psoma):
  scrmsg =  'get_all_possible_til_patterns_for(n_slots=%d, psoma=%d) ' %(n_slots, psoma)
  print(scrmsg)
  all_possible_til_patterns = tf.get_all_possible_til_patterns_for(n_slots, psoma)
  scrmsg = 'all_possible_til_patterns ' + str(all_possible_til_patterns)
  print(scrmsg)
  print('size', len(all_possible_til_patterns))


def adhoc_test():
  n_slots, psoma = 4, 6
  do_adhoc_test(n_slots, psoma)
  n_slots, psoma = 10, 6
  do_adhoc_test(n_slots, psoma)


def process():
  adhoc_test()


if __name__ == '__main__':
  process()
