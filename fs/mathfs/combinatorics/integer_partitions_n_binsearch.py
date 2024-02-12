#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/integer_partitions_n_binsearch.py
  Contains, as the main functions in the module:
    => binarysearch_idxpos_n_niterations_f_array_n_value()
      returns the index position of searched item and how many steps it took to find it (~log2N)
    => get_integer_partitions_of()
      returns the integer partitions of N (a positive integer)

Updated on 10/02/2024 (with the two function above)
Created on 22/11/2011
@author: luizlewis
"""
import math
import random


def binarysearch_idxpos_n_niterations_recursive(array, value, pos=0, n_of_iterations=1):
  size = len(array)
  if value == array[0]:
    # recursion exit point
    found_pos = 0 + pos  # + 1
    return found_pos, n_of_iterations
  elif size == 1:  # and it was not found above, so n is not here, return None meaning "not found"
    # recursion exit point
    return None, n_of_iterations  # ie, not found
  last_position = size - 1
  if value == array[last_position]:
    # recursion exit point
    found_pos = last_position + pos  # + 1
    # recursion exit point
    return found_pos, n_of_iterations
  if size % 2 == 0:
    mid = size // 2 - 1
  else:
    mid = size // 2
  # print 'mid', mid, ' array[mid] elem =', array[mid]
  if array[mid] == value:
    # recursion exit point
    found_pos = mid + pos  # + 1
    return found_pos, n_of_iterations
  elif array[mid] > value:
    array = array[:mid]
    # recursive call 1 / 2
    return binarysearch_idxpos_n_niterations_recursive(array, value, pos, n_of_iterations + 1)
  else:  # array[mid] < n:
    array = array[mid+1:]
    # recursive call 2 / 2
    return binarysearch_idxpos_n_niterations_recursive(array, value, pos + mid + 1, n_of_iterations + 1)


def binarysearch_idxpos_n_niterations_f_array_n_value(array, value):
  """
  This is the entry point for the binarysearch_idxpos_n_niterations_recursive
  Some checkings and preparations happen here then the 'inner' function is issued at return-point
  """
  if array is None or len(array) == 0:
    # ie, array is either None or empty, so n is not found anyway :: 1 = nOfIterations
    return None, 1
  # okay, array was checked for "noneness" or emptiness
  # now, let's check if n is really integer, if not, make it a rounded integer
  value = get_as_int_or_none(value)
  # well, n is not a number at all! If so, obviously it cannot be found
  if value is None:
    return None, 1
  # as this is a preparing method for the recursive method,
  # some processing may be done to assure the array is in ascending order
  array.sort()
  if value < array[0] or value > array[-1]:
    return None, 1  # ie, n is either below the least integer or above the biggest integer in the array
  # if passed through above conditions, it's "good to go"
  return binarysearch_idxpos_n_niterations_recursive(array, value)


def combine_sum6_sixtils():
  """
  This function does a kind of brute-force combination for sum=6 (@see example below)
  There is another combinatorial "non-brute-force" aproach, IndicesCombiner,
    for example, does that.
  There is a second drawback to this approach, beyond being brute-forced,
    it's not a symmetrical combination (the example shows this lack of symmetry)

  Example:
      1 (0, 0, 0, 0, 0, 6)
      2 (0, 0, 0, 0, 1, 5)
      3 (0, 0, 0, 0, 2, 4)
              (...)
      460 (5, 0, 1, 0, 0, 0)
      461 (5, 1, 0, 0, 0, 0)
      462 (6, 0, 0, 0, 0, 0)
  """
  sum_target = 6
  n_of_combs_quintil = 0
  for d0 in range(0, 7):
    for d1 in range(0, 7):
      for d2 in range(0, 7):
        for d3 in range(0, 7):
          for d4 in range(0, 7):
            for d5 in range(0, 7):
              d = (d0, d1, d2, d3, d4, d5)
              s = sum(d)
              if s == sum_target:
                n_of_combs_quintil += 1
                print(n_of_combs_quintil, d)
  print('n_of_combs_quintil', n_of_combs_quintil)
  print('theory', 5+40+40+24+10+24+16+6+16+5)


def gen_integer_partitions_of(n):
  """
  An integer partition of n is constructed as:
    [1, 1, ..., 1, 1, 1] : n_sized
    [1, 1, ..., 1, 2] : (n-1)_sized
    [1, 1, ..., 3] : (n-2)_sized
      (...)
    [n] : 1_sized
      where all combined sets above have sum(i) = n

  An integer partition may be understood by the two examples below:
  e1 Example of an integer partition with n=3:
    0 [1, 1, 1]
    1 [1, 2]
    2 [3]
  e2 Example of an integer partition with n=6:
    0 [1, 1, 1, 1, 1, 1]
    1 [1, 1, 1, 1, 2]
    2 [1, 1, 1, 3]
    3 [1, 1, 2, 2]
    4 [1, 1, 4]
    5 [1, 2, 3]
    6 [1, 5]
    7 [2, 2, 2]
    8 [2, 4]
    9 [3, 3]
    10 [6]
  """
  arr = [0]*(n + 1)
  idx = 1
  arr[0] = 0
  arr[1] = n
  while idx != 0:
      x = arr[idx - 1] + 1
      y = arr[idx] - 1
      idx -= 1
      while x <= y:
          arr[idx] = x
          y -= x
          idx += 1
      arr[idx] = x + y
      outcomb = arr[:idx + 1]
      yield outcomb


def get_integer_partitions_of(n):
  """
  @see docstring in gen_integer_partitions_of(n)
  """
  iplist = list(gen_integer_partitions_of(n))
  return iplist


def get_as_int_or_none(n):
  try:
    n = int(n)
    return n
  except ValueError:
    pass
  return None


def adhoctest1():
  random_array = random.sample(range(100000), 17)
  random_array.sort()
  indices = list(range(len(random_array)))
  random.shuffle(indices)
  while len(indices) > 0:
    position = indices.pop()
    integer = random_array[position]
    print('integer', integer)
    position_returned, n_of_iterations_returned = binarysearch_idxpos_n_niterations_f_array_n_value(
      random_array, integer
    )
    print(random_array)
    print(
      'for', integer, '==>> position_returned,'
      ' n_of_iterations_returned', position_returned, n_of_iterations_returned
    )


def adhoctest2():
  for comb in gen_integer_partitions_of(4):
    print(comb)


def adhoctest3():
  """

  """
  # print(get_integer_partitions_of(5))
  array, value = list(range(1, 11)), 4
  for i in range(5):
    samp = random.sample(array, k=3)
    random.shuffle(array)
    print('samp', samp, array)
  bs = binarysearch_idxpos_n_niterations_f_array_n_value(array=array, value=value)
  scrmsg = f'binary_search({array}), {value} = bs {bs}'
  print(scrmsg)
  print('math.log(20,2)', math.log(20, 2))


if __name__ == '__main__':
  """
  list_dist_xysum_metric_thru_ms_history()
  adhoctest6()
  combine_sum6_sixtils()
  """
  adhoctest3()
