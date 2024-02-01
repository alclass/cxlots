#!/usr/bin/env python
"""
fs/mathfs/combinatorics/permutations_n_lgis.py

This module contains two small function from:
  algorithm for lexicographical permutation
  https://www.nayuki.io/res/next-lexicographical-permutation-algorithm/nextperm.py

@see module:
  fs/mathfs/combinatorics/factoradic_to_from.py
for a more comprehension explanation to finding lgi's for permutations.

Next lexicographical permutation algorithm (Python)
by Project Nayuki, 2014. Public domain.
https://www.nayuki.io/page/next-lexicographical-permutation-algorithm

# -- Basic version --

Computes the next lexicographical permutation
  of the specified list in place,
returning whether a next permutation existed.
  (Returns False when the argument
  is already the last possible permutation.)
"""


def next_permutation(arr):
  # Find non-increasing suffix
  i = len(arr) - 1
  while i > 0 and arr[i - 1] >= arr[i]:
    i -= 1
  if i <= 0:
    return False

  # Find successor to pivot
  j = len(arr) - 1
  while arr[j] <= arr[i - 1]:
    j -= 1
  arr[i - 1], arr[j] = arr[j], arr[i - 1]
  # Reverse suffix
  arr[i:] = arr[len(arr) - 1: i - 1: -1]
  return True


# Example:
#   arr = [0, 1, 0]
#   next_permutation(arr)  (returns True)
#   arr has been modified to be [1, 0, 0]


# -- Comparator version --
#
# Computes the next lexicographical
# permutation of the specified list in place,
# returning whether a next permutation existed. (Returns False when the argument
# is already the last possible permutation.)
#
# comp is a comparison function - comp(x, y) returns a negative number if x is considered to be less than y,
# a positive number if x is considered to be greater than y, or 0 if x is considered to be equal to y.
#

def ret_ifless_minus1_ifequal_0_ifgreater_1(x, y):
  """
  This function enters as a parameter to next_permutation_comp()

  Args:
    x: int | object => that implements ordering
    y: int | object => that implements ordering

  Returns: boolean => True (a next one was found) | False (sequence has ended)
  """
  if x < y:
    return -1
  if x > y:
    return 1
  return 0


def next_permutation_comp(arr, comp=None):
  comp = comp if comp is not None else ret_ifless_minus1_ifequal_0_ifgreater_1
  # Find non-increasing suffix
  i = len(arr) - 1
  while i > 0 and comp(arr[i - 1], arr[i]) >= 0:
    i -= 1
  if i <= 0:
    return False

  # Find successor to pivot
  j = len(arr) - 1
  while comp(arr[j], arr[i - 1]) <= 0:
    j -= 1
  arr[i - 1], arr[j] = arr[j], arr[i - 1]

  # Reverse suffix
  arr[i:] = arr[len(arr) - 1: i - 1: -1]
  return True


def adhoctest():
  arr = [0, 1, 2]
  original_arr = list(arr)
  boolres = next_permutation_comp(arr)
  scrmsg = f"arr={original_arr} result={arr} boolres={boolres}"
  print(scrmsg)


if __name__ == '__main__':
  """
  adhoctest()
  """
  adhoctest()
