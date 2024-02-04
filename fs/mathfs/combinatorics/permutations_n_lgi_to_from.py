#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/permutations_n_lgi_to_from.py

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

==================

The explanation below is about finding a permutation set from a 0-based lgi (lexicographical index).

  given_lgi_b1idx = 978000
  given_lgi_b0idx = 979999
  expected_perm_arr = [2, 7, 3, 5, 0, 8, 4, 1, 9, 6]

  The step by step algorithmic formation of expected_perm_arr:

  First cycle (1): first dividor is (10-1)! ie (10-1)!=9!
  979999 // 9! = 2, remainder 979999 % 9! = 254239 (ie 979999 - 725760)
  From the initial set: {0 1 2 3 4 5 6 7 8 9} => S[2]=2 is removed (or moved to ongoing_result)
  so, this is the permutation 1st digit: 2 | append it: ongoing_result = [2]

  Next cycle (2), the remainder becomes the new dividend and the initial set is smaller one element
  254239 // 8! = 6, remainder 254239 % 8! = 12319 (ie 254239 - 241920)
  set: {0 1 3 4 5 6 7 8 9} => S[6]=7 is removed (or moved to ongoing_result)
  permutation 2nd digit: 7 | append it: ongoing_result = [2, 7]

  Next cycle (3), the remainder becomes the new dividend and so on
  12319 // 7! = 2, remainder 12319 % 7! = 2239 (ie 12319 - 10080)
  set: {0 1 3 4 5 6 8 9} => S[2]=3 is removed (or moved to ongoing_result)
  permutation 3rd digit: 3 | append it: ongoing_result = [2, 7, 3]

  Next cycle (4)
  2239 // 6! = 3, remainder 2239 % 6! = 79 (ie 2239 - 2160)
  set: {0 1 4 5 6 8 9} => S[3]=5 is removed (or moved to ongoing_result)
  permutation 4th digit: 5 | append it: ongoing_result = [2, 7, 3, 5]

  Next cycle (5)
  79 // 5! = 0, remainder 79 (ie 79 - 0)
  set: {0 1 4 6 8 9} => S[0]=0 is removed (or moved to ongoing_result)
  permutation 5th digit: 0 | append it: ongoing_result = [2, 7, 3, 5, 0]

  Next cycle (6)
  79 // 4! = 3, remainder 7 (ie 79 - 72)
  set: {1 4 6 8 9} => S[3]=8 is removed (or moved to ongoing_result)
  permutation 6th digit: 8 | append it: ongoing_result = [2, 7, 3, 5, 0, 8]

  Next cycle (7)
  7 // 3! = 1, remainder 1 (ie 7 - 6)
  set: {1 4 6 9} => S[1]=4 is removed (or moved to ongoing_result)
  permutation 7th digit: 4 | append it: ongoing_result = [2, 7, 3, 5, 0, 8, 4]

  Next cycle (8)
  1 // 2! = 0, remainder 1 (ie 1 - 0)
  set: {1 6 9} => S[0]=1 is removed (or moved to ongoing_result)
  permutation 8th digit: 1 | append it: ongoing_result = [2, 7, 3, 5, 0, 8, 4, 1]

  Next cycle (9)
  1 // 1! = 1, remainder 0 (ie 1 - 1)
  set: {6 9} => S[1]=9 is removed (or moved to ongoing_result)
  permutation 9th digit: 9 | append it: ongoing_result = [2, 7, 3, 5, 0, 8, 4, 1, 9]

  Next cycle (10)
  0 // 0! = 0, remainder 0 (ie 0 - 0)
  set: {6} => S[0]=6 is removed (or moved to ongoing_result)
  permutation 10th digit: 6 | append it: ongoing_result = [2, 7, 3, 5, 0, 8, 4, 1, 9, 6]
                              this is the last one

  In a nutshell, the permset whose lgi_b0idx is 979999 is [2, 7, 3, 5, 0, 8, 4, 1, 9, 6]

"""
import math


def adjust_factoradic_str_leftzeroes_if_needed(factoradic_str, n_elements):
  if len(factoradic_str) >= n_elements:
    return factoradic_str
  missing_zeroes = n_elements - len(factoradic_str)
  factoradic_str = missing_zeroes*'0' + factoradic_str
  return factoradic_str


def calc_placevalue_of_radix_n_highest_int_allowed(radixval):
  """
    Calculates the "place value" and the highest digit allowed from a radix value.

  The formula for the "place value":
    place_value = math.factorial(radixval - 1)
  The highest digit allowed is:
    highest_int_allowed = radixval - 1

  The context above is the one for factoradics, when there a composition
    of a decimal number "inside" a factoradic number.
  One application of these factoradic numbers are in permutation set generation
    and their corresponding lgi's (lexicographical indices).
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


"""
def calc_decimal_to_factoradic(intval, radix=1, remainders=None):
=======
"""


def calc_permutation_from_lgib0idx_by_lehmercode(lgi_b0idx, workset):
  """
    Computes the lgi_n_th permutation out of (original) workset
    Dispatches to calc_permutation_from_lgib1idx_by_lehmercode(lgi_b1idx, workset)
      that treats parameters, the latter dispatching to
        calc_permutation_from_lgib0idx_by_lehmercode_inner()
  Args:
    lgi_b0idx: int - the integer value that represents the permutation's lexicographical index
    workset: list - the permutation "base set"
  Returns:
    perm_result: list - the permutation "arrangement set" that corresponding to the input lgi
  """
  lgi_b1idx = lgi_b0idx + 1
  return calc_permutation_from_lgib1idx_by_lehmercode(lgi_b1idx, workset)


def calc_decimal_to_factoradic(intval, radix=1, remainders=None):
  """
    Calculates a factoradic number from a decimal one.

  IMPORTANT:
    At this version, a factoradic number is limited to 9 digits and the digit 9 itself.
    This is because the factoradic number here is treat as a string without : (colon).
    TO-DO (in the future): treat the factoradic number as composed of parts separated by : (colon).
      It may probably be better done via a class.

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


def calc_lgi_b0idx_from_idx_permutation_set(permset=None):
  """
    Calculates the lgi_b0idx from a permutation set.

  Obs: the permutation set should contain "indices" (or lexicographical elements) and
       cannot have repeated elements.
      The initial set has lgi = 0 and is equivalent to list(range(n_elements)) (or its lexicographical equivalent)
        where n_elements is the size of each set.
      The last set has lgi = total_permutations - 1 | total_permutations = n_elements!

  Example:
    e1 - a small set
      permset = [1, 2, 0] => its lgi_b0idx is 3
      iniset = [0, 1, 2], lastset = [2, 1, 0], total_permutations = 6 (ie 3!)
    e1 - a larger set
      permset = [2, 7, 3, 5, 0, 8, 4, 1, 9, 6] => its lgi_b0idx is 979999
      iniset = [0, 1, 2, ..., 8, 9], lastset = [9, 8, 7, ..., 2, 1, 0], total_permutations = 10! (above 3MM)

    perm_set = [2, 3, 0, 1] if perm_set is None else perm_set
    perm_set = [2, 7, 3, 5, 0, 8, 4, 1, 9, 6] if perm_set is None else permset
  """
  _ = is_there_repeated_elements_in_list(permset, raises=True)
  n_elements = len(permset)
  if n_elements == 0:
    return None
  gabarito_firstset = list(range(n_elements))
  seq, ongoing_lgi = 0, 0
  for intval in permset:
    seq += 1
    quoc_as_idx = gabarito_firstset.index(intval)
    gabarito_firstset.remove(intval)  # or del gabarito_firstset[quoc_as_idx]
    n_for_fact = n_elements - seq
    facto = math.factorial(n_for_fact)
    ongoing_lgi += quoc_as_idx * facto
  # print('ongoing_lgi', ongoing_lgi, 'permset', permset, 'gabarito_firstset', gabarito_firstset)
  return ongoing_lgi


def is_there_repeated_elements_in_list(alist, raises=True):
  n_elements = len(alist)
  size_as_unique = len(set(alist))
  if n_elements != size_as_unique:
    if raises:
      errmsg = f"permset cannot have repeated elements => n_elements={n_elements} != size_as_unique={size_as_unique}"
      raise ValueError(errmsg)
    else:
      return True
  return False


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


def gen_lexicographical_permutations_w_initial_lgi_set(initial_lgi_set):
  n_elements = len(initial_lgi_set)
  for perm_idx_set in gen_permutations_from_nelements(n_elements):
    curr_perm_set = [initial_lgi_set[idx] for idx in perm_idx_set]
    yield curr_perm_set
  return None


def gen_permutations_from_nelements(n_elements=3):
  """
    Generates (with yield) "index" permutations
  It's "index", because the first (or start) permutation set is list(range(n_elements))

  Example (generating for n_elements=3):
    0 [0, 1, 2]
    1 [0, 2, 1]
    2 [1, 0, 2]
    3 [1, 2, 0]
    4 [2, 0, 1]
    5 [2, 1, 0]
    None (finishes) | total permutations is 3!=6

  @see function gen_lexicographical_permutations_w_initial_lgi_set()
    for generating (with yield) any lexicographical permutations provided
      the initial (ordered-conventioned) set is given.
  """
  curr_permset = list(range(n_elements))
  counter = 0
  while curr_permset is not None:
    # print(counter, curr_permset)
    yield curr_permset
    curr_permset = permute_next_arrangement(curr_permset)
    counter += 1
  return


def adhoctest1():
  permset = [0, 1, 2, 3]
  size = len(permset)
  print('ini', permset, 'size', size, 'factorial of size', math.factorial(size))
  counter = 0
  while permset:
    counter += 1
    print(counter, permset)
    permset = permute_next_arrangement(permset)


def adhoctest2():
  intval, ini_radix = 256, 1
  factoradic_as_str = calc_decimal_to_factoradic(intval, radix=ini_radix)
  scrmsg = f"intval={intval} ini_radix={ini_radix} factoradic_as_str={factoradic_as_str}"
  expected = [2, 0, 2, 2, 0, 0]
  print(scrmsg, expected)


def adhoctest3():
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


def adhoctest4():
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


def adhoctest5():
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


def adhoctest6():
  """
  First cycle (1): first dividor is (n-1)! ie (3-1)!=2!
  3 // 2! = 1, remainder 3 % 2! = 1 (ie 3 - 2)
  From the initial set: {0 1 2} => S[1]=1 is removed (or moved to ongoing_result)
  so, this is the permutation 1st digit: 1 | append it: ongoing_result = [1]

  Next cycle (2), the remainder becomes the new dividend and the initial set is smaller one element
  1 // 1! = 1, remainder 1 % 1! = 0 (ie 1 - 1)
  set: {0 2} => S[1]=2 is removed (or moved to ongoing_result)
  so, this is the permutation 2nd digit: 2 | append it: ongoing_result = [1, 2]

  Next cycle (3), the remainder becomes the new dividend and so on
  0 // 0! = 0, remainder 0 % 0! = 0 (ie 0 - 0)
  set: {0} => S[0]=0 is removed (or moved to ongoing_result)
  so, this is the permutation 3rd digit: 0 | append it: (last) ongoing_result = [1, 2, 0]
  """
  initial_set = [0, 1, 2]
  initial_set_cp = list(initial_set)
  expected_perm_arr = [2, 0, 1]
  result_perm_arr = []
  size = len(expected_perm_arr)
  lgi, orig_lgi = 4, 4
  for n_for_fact in range(size-1, -1, -1):
    fact = math.factorial(n_for_fact)
    quoc_as_idx_to_moveout = lgi // fact
    lgi = lgi % fact
    val_at_pos = initial_set[quoc_as_idx_to_moveout]
    result_perm_arr.append(val_at_pos)
    del initial_set[quoc_as_idx_to_moveout]
  print('initial_set', initial_set_cp, 'expected_perm_arr', expected_perm_arr, 'res', result_perm_arr)


def adhoctest7():
  n_elements = 0
  for i, permset in enumerate(gen_permutations_from_nelements(n_elements)):
    lgi = calc_lgi_b0idx_from_idx_permutation_set(permset)
    seq = i + 1
    print(seq, i, 'lgi', lgi, permset)
  initial_set = ['banana', 'beans', 'soy']
  for permset in gen_lexicographical_permutations_w_initial_lgi_set(initial_set):
    print(permset)


if __name__ == '__main__':
  """
  adhoctest1()
  adhoctest5()
  """
  adhoctest7()
