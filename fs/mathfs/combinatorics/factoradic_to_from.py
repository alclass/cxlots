#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/factoradic_to_from.py

@see also Factorial number system
Ref.: https://en.wikipedia.org/wiki/Factorial_number_system

For example, 46310 can be transformed into a factorial representation by these successive divisions:
  463 ÷ 1 = 463, remainder 0
  463 ÷ 2 = 231, remainder 1
  231 ÷ 3 = 77, remainder 0
  77 ÷ 4 = 19, remainder 1
  19 ÷ 5 = 3, remainder 4
  3 ÷ 6 = 0, remainder 3
The process terminates when the quotient reaches zero.
  Reading the remainders backward gives 3:4:1:0:1:0!.

Permutations

There is a natural mapping between the integers 0, 1, ..., n! − 1 (or equivalently the numbers with n digits in factorial representation) and permutations of n elements in lexicographical order, when the integers are expressed in factoradic form. This mapping has been termed the Lehmer code (or inversion table). For example, with n = 3, such a mapping is
decimal 	factoradic 	permutation
010 	0:0:0! 	(0,1,2)
110 	0:1:0! 	(0,2,1)
210 	1:0:0! 	(1,0,2)
310 	1:1:0! 	(1,2,0)
410 	2:0:0! 	(2,0,1)
510 	2:1:0! 	(2,1,0)
"""


def calc_permutation_fatoradic_from_decimal():
  pass


def calc_decimal_from_permutation_fatoradic():
  pass



def adhoc_test():
  pass


if __name__ == '__main__':
  """
  """
  adhoc_test()
