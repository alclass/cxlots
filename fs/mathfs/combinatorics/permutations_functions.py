#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/permutations_functions.py
  This module contains two small function from:
    algorithm for lexicographical permutation
  https://www.nayuki.io/res/next-lexicographical-permutation-algorithm/nextperm.py

Notice for lgi's functions:
  there are functions to-from lgi's-to-permutations-and-viceversa in
    module permutations_n_lgi_to_from.py

@see module:
  fs/mathfs/combinatorics/permutations_n_lgi_to_from.py
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


def gen_permutation_indices_via_nayuki_algo(n_elements=3):
  """
  Generates (with yield) permutation indices via 'nayuki algorithm' in this module
    Obs:
      there is a second version of this same generator in module permutations_n_lgi_to_from.py

  For 'index permutations' as difference than 'index combinations':
    for permutations: n_elements = n_slots
    for combinations: n_elements >= n_slots
  """
  curr_perm = list(range(n_elements))  # firstperm = list(curr_perm)
  boolres, i = True, 0
  while boolres:
    # previous = list(curr_perm)
    yield list(curr_perm)  # a copy is 'yielded' because curr_perm 'mutates' at each step
    boolres = next_permutation_comp(curr_perm)
    # scrmsg = f"{i} perm={previous} is_there_next={boolres}"
    # print(scrmsg)
    i += 1
  return None


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


def next_permutation_comp(arr, comp=None):
  """

  """
  # default the function parameter 'comp', when it comes in as None, to the function above
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


def ret_ifless_minus1_ifequal_0_ifgreater_1(x, y):
  """
  This function returns -1 if x < y; 0 if x = y; and 1 if x > y.
    It is used in function next_permutation_comp() below

  Args:
    x: int | object that implements ordering and the two parameters having the same type
    y: int | object that implements ordering and the two parameters having the same type

  Returns: boolean => True (a next one was found) | False (sequence has ended)
  """
  if x < y:
    return -1
  if x > y:
    return 1
  return 0


def adhoctest():
  arr = [0, 1, 2]
  original_arr = list(arr)
  boolres = next_permutation_comp(arr)
  scrmsg = f"arr={original_arr} next={arr} boolres={boolres}"
  print(scrmsg)


def adhoctest2():
  n_elements = 4
  print('gen_permutation_indices_via_nayuki_algo, n_elements =', n_elements)
  for i, perm in enumerate(gen_permutation_indices_via_nayuki_algo(n_elements=n_elements)):
    print(i, perm)


if __name__ == '__main__':
  """
  adhoctest()
  """
  adhoctest2()
