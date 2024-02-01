#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/factoradic_to_from.py

https://stemhash.com/efficient-permutations-in-lexicographic-order/
The Factorial Number System

  Obs: move the largest part of this docstring to a documentation-focused file.

The above URL explains how to find the lexicographical index from a permutation.
  It doesn't show an algorithm, but it explains it in detail and show
  the evolution of division and remainders step by step.

The factorial number system or factoradic is a mixed radix numeral system.
 This means that the radix or base of each digit changes with its position.
 In contrast, our more familiar numeral systems–such as decimal or binary–keep
 the base fixed for all digits at each position.

The following table illustrates the factorial number system.
Radix 	8 	7 	6 	5 	4 	3 	2 	1
Place value 	7! 	6! 	5! 	4! 	3! 	2! 	1! 	0!
Place value in decimal 	5040 	720 	120 	24 	6 	2 	1 	1
Highest digit allowed 	7 	6 	5 	4 	3 	2 	1 	0

  256 / 1 = 256, remainder 0
  256 / 2 = 128, remainder 0
  128 / 3 =  42, remainder 2
   42 / 4 =  10, remainder 2

   10 / 5 =   2, remainder 0
    2 / 6 =   0, remainder 2

This relationship or mapping is known as the Lehmer code.
@see also Factorial number system
Ref.: https://en.wikipedia.org/wiki/Factorial_number_system

For example, 46310 can be transformed into a factorial representation
by these successive divisions:
  463 ÷ 1 = 463, remainder 0
  463 ÷ 2 = 231, remainder 1
  231 ÷ 3 = 77, remainder 0
  77 ÷ 4 = 19, remainder 1
  19 ÷ 5 = 3, remainder 4
  3 ÷ 6 = 0, remainder 3
The process terminates when the quotient reaches zero.
  Reading the remainders backward gives 3:4:1:0:1:0!.

Permutations

There is a natural mapping between the integers 0, 1, ..., n! − 1
  (or equivalently the numbers with n digits in factorial representation)
  and permutations of n elements in lexicographical order, when the integers
  are expressed in factoradic form. This mapping has been termed the Lehmer code
  (or inversion table). For example, with n = 3, such a mapping is
  decimal 	factoradic 	permutation

010 	0:0:0! 	(0,1,2)
110 	0:1:0! 	(0,2,1)
210 	1:0:0! 	(1,0,2)
310 	1:1:0! 	(1,2,0)
410 	2:0:0! 	(2,0,1)
510 	2:1:0! 	(2,1,0)
"""


def calc_permutation_fatoradic_from_decimal():
  """
  Initial set: {0 1 2 3 4 5 6 7 8 9}
  979,999 / 9! = 2, remainder 254,239
  permutation 1st digit: 2

  set: {0 1 3 4 5 6 7 8 9} <= 2 (former idx 2) got out
  254239 / 8! = 6, remainder 12,319
  permutation 2nd digit: 7

  set: {0 1 3 4 5 6 8 9} <= 7 (former idx 6) got out
  12319 / 7! = 2, remainder 2,239
  permutation 3rd digit: 3

  set: {0 1 4 5 6 8 9} <= 3 (former idx 2) got out
  2239 / 6! = 3, remainder 79
  permutation 4th digit: 5

  set: {0 1 4 6 8 9} <= 5 (former idx 3) got out
  79 / 5! = 0, remainder 79
  permutation 5th digit: 0

  set: {1 4 6 8 9} <= 0 (former idx 0) got out
  79 / 4! = 3, remainder 7
  permutation 6th digit: 8

  set: {1 4 6 9} <= 6 (former idx 3) got out
  7 / 3! = 1, remainder 1
  permutation 7th digit: 4

  set: {1 6 9} <= 4 (former idx 1) got out
  1 / 2! = 0, remainder 1
  permutation 8th digit: 1

  set: {6 9} <= 1 (former idx 0) got out
  1 / 1! = 1, remainder 0
  permutation 9th digit: 9

  set: {6} <= 9 (former idx 1) got out, idx 0 is removed at this step
  0 / 0! = 0, remainder 0
  permutation 10th digit: 6
  Returns:
  """
  pass


def calc_decimal_from_permutation_fatoradic():
  pass


def adhoc_test():
  pass


if __name__ == '__main__':
  """
  """
  adhoc_test()
