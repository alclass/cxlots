#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/factoradic_to_from.py

https://stemhash.com/efficient-permutations-in-lexicographic-order/
The Factorial Number System

  Obs: to move the largest part of this docstring to a documentation-focused file.

The above URL explains how to find the lexicographical index of a permutation.
  It doesn't show an algorithm itself, but it explains it in detail and shows
  the evolution of division and remainders step by step (@see below).

The factorial number system or factoradic is a mixed radix numeral system.
 This means that the radix or base of each digit changes with its position.
 In contrast, our more familiar numeral systems -– such as decimal or binary -– keep
 the base fixed for all digits at each position.

The following table illustrates the factorial number system.
Radix 	      8 	7 	6 	5 	4 	3 	2 	1
Place value 	7! 	6! 	5! 	4! 	3! 	2! 	1! 	0!
Place value in decimal 	5040 	720 	120 	24 	6 	2 	1 	1
Highest digit allowed 	   7 	  6 	  5 	 4 	3 	2 	1 	0

  256 / 1 = 256, remainder 0
  256 / 2 = 128, remainder 0
  128 / 3 =  42, remainder 2
   42 / 4 =  10, remainder 2
   10 / 5 =   2, remainder 0
    2 / 6 =   0, remainder 2
    The process terminates when the quotient reaches zero.
      Reading the remainders backward gives 2:0:2:2:0:0!.
  This relationship or mapping is known as the Lehmer code.
  @see also Factorial number system
  Ref.: https://en.wikipedia.org/wiki/Factorial_number_system

For example, 463 can be transformed into a factorial representation
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
  ----------------------------------
    0 	    0:0:0! 	(0,1,2)
    1 	    0:1:0! 	(0,2,1)
    2 	    1:0:0! 	(1,0,2)
    3 	    1:1:0! 	(1,2,0)
    4 	    2:0:0! 	(2,0,1)
    5 	    2:1:0! 	(2,1,0)
"""
import math


def calc_placevalue_of_radix_n_highest_int_allowed(radixval):
  """

  """
  if radixval < 1:
    errmsg = f"radix of factoradic cannot be less than 1, it was {radixval}"
    raise ValueError(errmsg)
  n_for_fact = radixval - 1
  place_value = math.factorial(n_for_fact)
  highest_int_allowed = n_for_fact
  return place_value, highest_int_allowed


def calc_permutation_from_lgib0idx_by_lehmercode_inner(lgi_b0idx, workset, perm_result=None):
  """
    Computes the lgi_n_th permutation out of (original) workset

  Consider this "inner" function as private, being called from
    calc_permutation_from_lgib1idx_by_lehmercode()
  or another function that treats its parameter "downstream" here

  Example: the 980,000th permutation in {0123456789} is {2735084196}
  Ref.: https://stemhash.com/efficient-permutations-in-lexicographic-order/
  """
  perm_result = [] if perm_result is None else perm_result
  size_minus_1 = len(workset) - 1
  divisor = math.factorial(size_minus_1)
  quoc = lgi_b0idx // divisor
  remainder = lgi_b0idx % divisor
  dig = workset[quoc]
  perm_result.append(dig)
  if len(workset) > 1:
    del workset[quoc]
  else:
    return perm_result
  return calc_permutation_from_lgib0idx_by_lehmercode_inner(remainder, workset, perm_result)


def calc_permutation_from_lgib1idx_by_lehmercode(lgi_b1idx, workset):
  """
    Computes the lgi_n_th permutation out of (original) workset

  This is the entrance function to calc_permutation_from_lgib0idx_by_lehmercode_inner()
    Obs:
      o1 in the entrance function, the input lgi is a base-1 index integer
      o2 in the inner function, the input lgi is a base-0 index integer
    ie
      lgi_b0idx = lgi_b1idx - 1

  This entrance function treats input parameters
    and the inner function does the computation recursively.
  """
  set_size = len(workset)
  perm_size = math.factorial(set_size)
  if lgi_b1idx > perm_size:
    errmsg = f"lgi_b1idx (={lgi_b1idx}) > perm_size (={perm_size}) ={set_size}! {workset}"
    raise ValueError(errmsg)
  perm_result = []
  lgi_b0idx = lgi_b1idx - 1
  return calc_permutation_from_lgib0idx_by_lehmercode_inner(lgi_b0idx, workset, perm_result)


def calc_decimal_to_factoradic(intval, radix=1, remainders=None):
  """
  resulted_perm_arr = [2, 7, 3, 5, 0, 8, 4, 1, 9, 6]

  The step by step algorithmic formation of resulted_perm_arr:

  Initial set: {0 1 2 3 4 5 6 7 8 9}
  979999 / 9! = 2, remainder 254239 (ie 979999 - 725760)
  permutation 1st digit: 2 | append it: ongoing_result = [2]

  set: {0 1 3 4 5 6 7 8 9} <= 2 (former idx 2) got out
  254239 / 8! = 6, remainder 12319 (ie 254239 - 241920)
  permutation 2nd digit: 7 | append it: ongoing_result = [2, 7]

  set: {0 1 3 4 5 6 8 9} <= 7 (former idx 6) got out
  12319 / 7! = 2, remainder 2239 (ie 12319 - 10080)
  permutation 3rd digit: 3 | append it: ongoing_result = [2, 7, 3]

  set: {0 1 4 5 6 8 9} <= 3 (former idx 2) got out
  2239 / 6! = 3, remainder 79 (ie 2239 - 2160)
  permutation 4th digit: 5 | append it: ongoing_result = [2, 7, 3, 5]

  set: {0 1 4 6 8 9} <= 5 (former idx 3) got out
  79 / 5! = 0, remainder 79 (ie 79 - 0)
  permutation 5th digit: 0 | append it: ongoing_result = [2, 7, 3, 5, 0]

  set: {1 4 6 8 9} <= 0 (former idx 0) got out
  79 / 4! = 3, remainder 7 (ie 79 - 72)
  permutation 6th digit: 8 | append it: ongoing_result = [2, 7, 3, 5, 0, 8]

  set: {1 4 6 9} <= 6 (former idx 3) got out
  7 / 3! = 1, remainder 1 (ie 7 - 6)
  permutation 7th digit: 4 | append it: ongoing_result = [2, 7, 3, 5, 0, 8, 4]

  set: {1 6 9} <= 4 (former idx 1) got out
  1 / 2! = 0, remainder 1 (ie 1 - 0)
  permutation 8th digit: 1 | append it: ongoing_result = [2, 7, 3, 5, 0, 8, 4, 1]

  set: {6 9} <= 1 (former idx 0) got out
  1 / 1! = 1, remainder 0 (ie 1 - 1)
  permutation 9th digit: 9 | append it: ongoing_result = [2, 7, 3, 5, 0, 8, 4, 1, 9]

  set: {6} <= 9 (former idx 1) got out, idx 0 is removed at this step
  0 / 0! = 0, remainder 0 (ie 0 - 0)
  permutation 10th digit: 6 | append it: ongoing_result = [2, 7, 3, 5, 0, 8, 4, 1, 9, 6]
                                                          its lgi_b0idx is 979999

  Returns:
    int | the decimal int value corresponding to input fatoradic number
  """
  remainders = [] if remainders is None else remainders
  newintval = intval // radix
  remainder = intval % radix
  remainders.append(remainder)
  if newintval == 0:
    rev_rem = list(reversed(remainders))
    factoradic_as_str = ''.join(map(str, rev_rem))
    return factoradic_as_str
  return calc_decimal_to_factoradic(newintval, radix=radix + 1, remainders=remainders)


def calc_decimal_from_permutation_fatoradic():
  pass


def adjust_factoradic_str_leftzeroes_if_needed(factoradic_str, n_elements):
  if len(factoradic_str) >= n_elements:
    return factoradic_str
  missing_zeroes = n_elements - len(factoradic_str)
  factoradic_str = missing_zeroes*'0' + factoradic_str
  return factoradic_str


def permset_from_a_factoradic_n_nelements(factoradic_str, n_elements):
  """
  Ref. https://en.wikipedia.org/wiki/Factorial_number_system
  especially in the middle where a schematic shows the traversal of the factoradic number
  """
  output_permset = []
  consumable_set = list(range(n_elements))
  factoradic_str = adjust_factoradic_str_leftzeroes_if_needed(factoradic_str, n_elements)
  factoradic_list = list(map(int, factoradic_str))
  for dig in factoradic_list:
    extracted_int = consumable_set[dig]
    del consumable_set[dig]
    output_permset.append(extracted_int)
  return output_permset


def permute_next_arrangement(permset=None):
  """

  step 1) Find the largest index i such that s[i] < s[i+1]
   If we can't find such an index, it means we are at the last permutation of the sequence

  step 2) Find the largest index j that is greater than i, such that s[i] < s[j]

  step 3) Swap the value of s[i] with that of s[j]

  step 4) Reverse the sequence from s[i+1] up to and including the last element

  Example: {012} {021} {102} {120} {201} {210}
  """
  # permset = [0, 1, 2] if permset is None else permset
  # print('ini', permset)
  largest_i = -1
  for i in range(len(permset)-1):
    if permset[i] < permset[i+1]:
      largest_i = i
  if largest_i < 0:
    return None
  # print('largest_i', largest_i)
  largest_j = -1
  for j in range(len(permset)):
    if permset[largest_i] < permset[j]:
      largest_j = j
  # print('largest_j', largest_j)
  if largest_j < 0:
    return None
  # swap them
  tmpval = permset[largest_i]
  permset[largest_i] = permset[largest_j]
  permset[largest_j] = tmpval
  # print('largest_i', largest_i, permset)
  preset = permset[: largest_i+1]
  subset = permset[largest_i+1:]
  permset = preset + list(reversed(subset))
  return permset


def gen_permutations_from_nelements(n_elements=3):
  """
  Generates (with yield) "index" permutations
  It's "index", because the first (or start) permutation set is list(range(n_elements))

  Example:
    0 [0, 1, 2]
    1 [0, 2, 1]
    2 [1, 0, 2]
    3 [1, 2, 0]
    4 [2, 0, 1]
    5 [2, 1, 0]
    None (finishes)
  """
  curr_permset = list(range(n_elements))
  counter = 0
  while curr_permset is not None:
    print(counter, curr_permset)
    yield curr_permset
    curr_permset = permute_next_arrangement(curr_permset)
    counter += 1
  return


def adhoc_test1():
  permset = [0, 1, 2, 3]
  size = len(permset)
  print('ini', permset, 'size', size, 'factorial of size', math.factorial(size))
  counter = 0
  while permset:
    counter += 1
    print(counter, permset)
    permset = permute_next_arrangement(permset)


def adhoc_test2():
  intval, ini_radix = 256, 1
  factoradic_as_str = calc_decimal_to_factoradic(intval, radix=ini_radix)
  scrmsg = f"intval={intval} ini_radix={ini_radix} factoradic_as_str={factoradic_as_str}"
  expected = [2, 0, 2, 2, 0, 0]
  print(scrmsg, expected)


def adhoc_test3():
  """
  Example:
    perm_result = calc_permutation_from_lgib1idx_by_lehmercode(980000, workset=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    expected_perm_result = [2, 7, 3, 5, 0, 8, 4, 1, 9, 6]
  """
  workset = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
  lgival = 980000 - 1
  perm_result = calc_permutation_from_lgib1idx_by_lehmercode(lgival, workset=workset)
  expected_perm_result = [2, 7, 3, 5, 0, 8, 4, 1, 9, 6]
  print(lgival, perm_result, 'expected', expected_perm_result)
  # ==========
  workset = [0, 1, 2, 3]
  lgi_b1idx = 19
  perm_result = calc_permutation_from_lgib1idx_by_lehmercode(lgi_b1idx, workset=workset)
  expected_perm_result = [3, 0, 1, 2]
  print('lgi_b1idx', lgi_b1idx, perm_result, 'expected', expected_perm_result)
  # ==========
  workset = [0, 1, 2, 3]
  lgi_b1idx = 10
  perm_result = calc_permutation_from_lgib1idx_by_lehmercode(lgi_b1idx, workset=workset)
  expected_perm_result = [1, 2, 3, 0]
  print('lgi_b1idx', lgi_b1idx, perm_result, 'expected', expected_perm_result)


def adhoc_test4():
  input_perm = [2, 7, 3, 5, 0, 8, 4, 1, 9, 6]
  soma = 0
  expected_lgi_b0idx = 980000 - 1
  for radixval in range(1, len(input_perm)+1):
    placevalue, _ = calc_placevalue_of_radix_n_highest_int_allowed(radixval)
    # dig = input_perm[-radixval]
    dig = input_perm[radixval-1]
    val_at_pos = dig * placevalue
    soma += val_at_pos
    print(dig, '*', placevalue, '=', val_at_pos, soma)
  print(expected_lgi_b0idx)
  workset = [2, 3, 0, 1]  # result for lgi=10 is [3, 0, 1, 2]
  lgi_b1idx = 10
  result_perm = calc_permutation_from_lgib1idx_by_lehmercode(lgi_b1idx, workset)
  print('lgi_b1idx', lgi_b1idx, 'calc_permutation_from_lgib1idx_by_lehmercode', result_perm)
  # assign list again for it was "consumed" ongoing in the algorithm
  workset = [2, 3, 0, 1]  # result for lgi=10 is [3, 0, 1, 2]
  lgi_b1idx = 24
  result_perm = calc_permutation_from_lgib1idx_by_lehmercode(lgi_b1idx, workset)
  print('lgi_b1idx', lgi_b1idx, 'calc_permutation_from_lgib1idx_by_lehmercode', result_perm)
  intval = 2982
  factoradic = calc_decimal_to_factoradic(intval)
  print('intval', intval, 'factoradic', factoradic)


def adhoc_test5():
  factoradic_str, n_elements = '4041000', 7
  result_permset = permset_from_a_factoradic_n_nelements(factoradic_str, n_elements)
  print(factoradic_str, 'permset_from_a_factoradic_n_nelements', result_permset)
  # result = (4, 0, 6, 2, 1, 3, 5)
  for i in range(1, 21):
    factoradic_str = calc_decimal_to_factoradic(i)
    result_permset = permset_from_a_factoradic_n_nelements(factoradic_str, n_elements)
    print(i, factoradic_str, 'permset_from_a_factoradic_n_nelements', result_permset)
    # result = (4, 0, 6, 2, 1, 3, 5)
  orig_perm = list(range(3))
  results = permute_next_arrangement(permset=list(orig_perm))
  print(orig_perm, 'results', results)
  orig_perm = list(results)
  results = permute_next_arrangement(permset=results)
  print(orig_perm, 'results', results)
  for curr_perm in gen_permutations_from_nelements():
    for dig in curr_perm:
      _ = dig
      pass
  n_elements = 3
  for i in range(6):
    factoradic_str = calc_decimal_to_factoradic(i)
    res = permset_from_a_factoradic_n_nelements(factoradic_str=factoradic_str, n_elements=n_elements)
    print('lgi', i, 'factoradic', factoradic_str, 'permset_from_a_factoradic_n_nelements', res)


if __name__ == '__main__':
  """
  adhoc_test1()
  adhoc_test2()
  adhoc_test3()
  adhoc_test4()
  """
  adhoc_test5()
