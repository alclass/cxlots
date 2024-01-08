#!/usr/bin/env python3
"""
maths2/combinatorics/combinatoric_algorithms.py

Main functions here:

-- permute(arrayN)
-- geraSumComponents(soma, parcel=-1, acc=[])
   Generates Integer Partitions
   (look for further explanation on the comments at the beginning of the function below)
-- getTilPatternsFor(patternSize=10, patternSoma=6)
   Uses geraSumComponents(patternSoma) then it stuffs zeroes
   and filters out larger strings than patternSize

"""
# import numpy, time, sys
import random
import sys


def fact_inner(n):
  """
    calculates recursively the factorial of a number.

    Obs:
      this function can only be called from fact(), below,
      which "protects" it from the input parameter being a non-int or less than 0.
  """
  if n < 2:
    return 1
  return n * fact_inner(n-1)


def fact(n):
  """
    calculates the factorial of a number.

    Obs:
      this function calls fact_inner(n) that does the computing recursively;
      it, however, "protects" the latter from the input parameter being a non-int or less than 0.
  """
  try:
    n = int(n)
  except (TypeError, ValueError):
    return None
  if n < 0:
    return None
  return fact_inner(n)


def permute_n(n):
  return fact(n)


def permute2_d(array2_d):
  """
  This function is called by permuteN(arrayN)
  It swaps x and y in a 2D-array 
  Eg permute2_d([1,2]) results in [[1, 2], [2, 1]]
  """
  x = array2_d[0]
  y = array2_d[1]
  if x == y:
    return [array2_d]
  return [[x, y], [y, x]]


def permute(array_n):
  """
    does permutations
  An n-size set generates n! (n factorial) permutations;
  permute() does its job recursively if n > 2,
    ie it diminishes n by 1 and recurse until it gets the 2-element pair swapped by permute2_d()

  Eg
  permuteN( range(3) ) results in:
  1 [0, 1, 2]
  2 [0, 2, 1]
  3 [1, 0, 2]
  4 [1, 2, 0]
  5 [2, 0, 1]
  6 [2, 1, 0]  
  """
  if len(array_n) == 0:
    return []
  if len(array_n) == 2:
    return permute2_d(array_n)
  result_array = []
  for i in range(len(array_n)):
    array_to_prepare = list(array_n)
    elem = array_to_prepare[i]
    if i > 0 and elem == array_to_prepare[i-1]:
      continue
    array_to_prepare = array_to_prepare[:i] + array_to_prepare[i+1:]
    sub_arrays = permute(array_to_prepare)  # recursive call
    for subArray in sub_arrays:
      array = [elem] + subArray
      result_array.append(array)
  return result_array


def gen_permute_via_indices(alist):
  """
  Permutates list alist yielding permuted-list-elements one by one (ie, a generator)
  Example:
    input: ['a', 'b', 'c']
    output: ['a', 'b', 'c'], ['a', 'c', 'b'], ['b', 'a', 'c'], ['b', 'c', 'a'], ['c', 'a', 'b'], ['c', 'b', 'a']
  """
  indices = list(range(len(alist)))
  permsets = permute(indices)
  for indset in permsets:
    yieldlist = [alist[i] for i in indset]
    yield yieldlist
  return


def get_genpermute_via_indices(alist):
  """
  returns as list the whole output of generator gen_permute_via_indices() above
  """
  return list(gen_permute_via_indices(alist))


def gen_permutations_o_str(astr):
  """
  Permutates string astr yielding permutated-string-elements one by one (ie, a generator)
  Example:
    input: 'abc'
    output: ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
  """
  for elist in gen_permute_via_indices(astr):
    estr = ''.join(elist)
    yield estr
  return


def get_genpermutations_o_str(astr):
  """
  returns as list the whole output of generator gen_permutations_o_str() above
  """
  return list(gen_permutations_o_str(astr))


def fill_right_zeroes_to_eachstr_in_list(strlist, each_str_size=10):
  """
  Example:
    input: strlist=['abc', 'xy', '4', 'e2e'], size=4
    output: ['abc0', 'xy00', '4000', 'e2e0']
  """
  outlist = []
  for estr in strlist:
    zeroes_to_fill = each_str_size - len(estr)
    estr = estr + '0'*zeroes_to_fill
    outlist.append(estr)
  return outlist


def get_permutations(subtokens):
  total, all_perms = 0, []
  for token in subtokens:
    token_array = [e for e in token]
    oa = permute(token_array)
    oa.sort()
    previous_word = ''
    for o_int in oa:
      o_str = map(str, o_int)
      word = ''.join(o_str)
      all_perms.append(word)
      if previous_word == word:
        # should be an error if it happens
        print(' ================ ')
        errmsg = f'previous_word (={previous_word}) == word (={word})'
        raise ValueError(errmsg)
      else:
        pass
      previous_word = word
    subtotal = len(oa)
    total += subtotal
  return all_perms


def combine_n_c_by_c(n, c):
  """

  combine_n_c_by_c(n, c) is a function that computes the number R of
    combinations of an n-element set S, c by c elements.
   
  Ex. suppose S = [1,2,3]
  Combinations 2 by 2 of S are [1,2],[1,3] and [2,3]
  Hence, R, the resulting numbers of combinations, is 3.
  
  We can also see combine_n_c_by_c(n, c) by its factorial formula, which is n!/((n-c)!c!)
  
  In the simple example above, R = 3!/(2!1!) = 3 x 2 / 2 = 3
  
  As a more computing-intense example, Megasena has:
    R = combine_n_c_by_c(60, 6) = 60! / ((60-6)!6!) = ... =  50,063,860
  
  The Python code implementation here does not use factorial in order
     to optimization/minimize computation efforts.
  """
  if n < 0 or c < 0:
    errmsg = f'Can not calculate combination with negative numbers ({n}, {c}).'
    raise ValueError(errmsg)
  # this condition below may be reformulation to an exception raising
  # in the future (how can one combine more than one has?), for the time being, it's returning 0
  if n < c:
    return 0
  if c == 0:
    if n == 0:
      return 0
    # if n > 0: # no need for an "if" here, n > 0 is logically the condition fell into, if program flow passes by this
    # point
    return 1  # convention for "produtório", sequence-multiply
  if n == c:
    return 1
  mult = 1
  n_orig = n
  while n > n_orig - c:
    mult *= n
    n -= 1
  while c > 1:
    mult = mult / (0.0 + c)
    c -= 1
  return int(mult)


def random_permutation(perm):
  n = len(perm)
  for i in range(1, n+1):
    perm[i] = i
  for i in range(1, n+1):
    j = i + random.randint(1, n+1) * (n + 1 - i)
    k = perm[i]
    perm[j] = k


def mount_all_integer_partitions_for(soma, parcel=-1, acc=None):
  """

  geraSumComponents(soma, parcel=-1, acc=[]) is an [[[ Integer Partitions generator ]]]
  The name geraSumComponents() was given here
    before I came across the established term Integer Partitions
    from the technical literature;
  
  Eg geraSumComponents(soma=4) results in:
    [[4], [3, 1], [2, 2], [2, 1, 1], [1, 1, 1, 1]]
   
  """
  acc = [] if acc is None else list(acc)
  if soma == 1:
    acc += [[1]]
    return acc
  if parcel == 1:
    acc += [[1]*soma]
    return acc
  # case where caller leaves 'parcel' to its initial supposed condition, ie, it's equal to 'soma'
  if parcel == -1:
    parcel = soma
  if parcel == soma:
    acc += [[parcel]]
    return mount_all_integer_partitions_for(soma, parcel - 1, acc)
  dif = soma - parcel
  if dif == 1:
    acc += [[parcel, 1]]
    return mount_all_integer_partitions_for(soma, parcel - 1, acc)
  kept_acc = list(acc)
  new_acc = []
  sub_acc = mount_all_integer_partitions_for(dif, dif, [])
  for sub in sub_acc:
    # well, the 'if' below was a tough decision to correct a repeat
    # eg. gera(5) was having [3,2] and [2,3]
    if parcel < sub[0]:
      continue
    sublista = [parcel] + sub
    new_acc.append(sublista)
  kept_acc += new_acc
  acc = kept_acc
  if parcel > 1:
    return mount_all_integer_partitions_for(soma, parcel - 1, acc)
  return acc


def filter_out_strings_greater_than_size(words, size):
  return list(filter(lambda s: len(s) <= size, words))


def stablish_base_int_partitions_for(elem, comb_array, up_int):
  """
  called by method init_comb_array in class RCombiner
  """
  intpartitions = mount_all_integer_partitions_for(up_int)
  comb_array_size = len(comb_array)
  intpartitions_size_of_comb_array = list(filter(lambda e: len(e)==comb_array_size, intpartitions))
  return intpartitions_size_of_comb_array


def comb_arrange(intpartition):
  """

  """
  ini_set = set(intpartition)
  return permute_n(intpartition)



class RCombiner:
  """
  fs.maths.combinatorics.combinatoric_algorithms.RCombiner
    This classes organized arrangements of integer partitions that sum up to a certain target value.
    One possible application of this class is in the Megasena game
    (@see the two 'expand' methods below which contain a bit more information/explanation).
  """

  def __init__(self, a_size, up_int=6):
    self.a_size = a_size
    self.up_int = up_int
    self.base_intpartitions = None
    self.init_comb_array()

  def init_comb_array(self):
    """
    Example
    size=3 upInt=6 base_intpartitions=[[4, 1, 1], [3, 2, 1], [2, 2, 2]]
    This means the base_intpartitions have all combinations (not arrangements) that makes up a sum of 6
    """
    self.base_intpartitions = [0] * self.a_size
    self.base_intpartitions = stablish_base_int_partitions_for(self.a_size, self.base_intpartitions, self.up_int)

  def expand_base_intpartitions_as_arrangements(self):
    """
    Example
    size=3 upInt=6 base_intpartitions=[[4, 1, 1], [3, 2, 1], [2, 2, 2]]
    expanded = [[4, 1, 1], [1, 4, 1], [1, 1, 4], [3, 2, 1], [3, 1, 2],
                [2, 3, 1], [2, 1, 3], [1, 3, 2], [1, 2, 3], [2, 2, 2]]
    This means the expanded intpartitions have all arrangements, ie [4, 1, 1] is different from [1, 4, 1]
      that makes up a sum of 6
    """
    outlist = []
    for intpartition in self.base_intpartitions:
      arranges = permute(intpartition)
      outlist += arranges
    return outlist

  def expand_base_intpartitions_to_slots(self, n_slots=6):
    """
    Example
    size=3 upInt=6 base_intpartitions=[[4, 1, 1], [3, 2, 1], [2, 2, 2]]
    Let's see two case of expansion by slots.
    1) with slots=6 (or 6rows), there are 200 sets
    expanded = [[[4, 1, 1, 0, 0, 0], [4, 1, 0, 1, 0, 0], [4, 1, 0, 0, 1, 0], [4, 1, 0, 0, 0, 1], ...]
    2) with slots=10 (or 6 columns), there are 1200 sets
    expanded = [[4, 1, 1, 0, 0, 0, 0, 0, 0, 0], [4, 1, 0, 1, 0, 0, 0, 0, 0, 0], [4, 1, 0, 0, 1, 0, 0, 0, 0, 0],...]

    One application of this mounting is to form "one possible metric" for the "Megasena" game
      which has a matrix of 6 rows and 10 columns.
    The application is as following:
    - suppose a dozens draw with 6 numbers
    - all these 6 numbers may be cast into one arranged set above, eg, [4, 1, 0, 0, 1, 0, 0, 0, 0, 0];
    - the above example 'column' set means: 4 dozens happened in the first column, one in the second, one in the fifth.
    - a database of this mentioned metric for all history games may be recorded and then analysed looking for patterns,
      if some pattern exists.
    """
    outlist = []
    for intpartition in self.base_intpartitions:
      n_zeroes = n_slots - len(intpartition)
      partition_w_zeroes = intpartition + [0]*n_zeroes
      arranges = permute(partition_w_zeroes)
      outlist += arranges
    return outlist

  def __str__(self):
    outstr = 'size=%d upInt=%d base_intpartitions=%s' % (self.a_size, self.up_int, str(self.base_intpartitions))
    return outstr


def adhoc_test1():
  # testAdHocRCombiner():
  rc = RCombiner(3)
  print(rc)
  allsets = rc.expand_base_intpartitions_as_arrangements()
  print(allsets)
  allsets = rc.expand_base_intpartitions_to_slots(n_slots=6)
  print('6 rows', len(allsets), allsets)
  allsets = rc.expand_base_intpartitions_to_slots(n_slots=10)
  print('10 columns', len(allsets), allsets)


def adhoc_test2():
  n = 9
  perm = list(range(n+2))
  random_permutation(perm)
  print(perm)


def adhoc_test3():
  for i in range(3, 5):
    array_n = range(i)
    arr = permute(array_n)
    count = 0
    for a in arr:
      count += 1
      print(count, a)


def adhoc_test4():
  """
  5 R: [[5], [4, 1], [3, 2], [3, 1, 1], [2, 2, 1], [2, 1, 1, 1], [1, 1, 1, 1, 1]]
  """
  for soma in range(5, 6):
    acc = mount_all_integer_partitions_for(soma, soma, [])
    # check it up
    for elem in acc:
      calc_soma = sum(elem)
      if soma != calc_soma:
        scrmsg = f'soma {soma} != sum(elem) = {calc_soma}'
        print(scrmsg)
    scrmsg = f"soma {soma} {acc}"
    print(scrmsg)

  
def adhoc_tests_show():
  scrmsg = '''
    combinatoric_algorithms.py -t <n>
      Where <n> is
    1 for test1: testAdHocRCombiner()
    2 for test2: testAdHocRandomPermutation()
    3 for test3: testAdHocPermuteN(arrayN=range[3])
    4 for test4: test_generate_integer_partitions()
  '''
  print(scrmsg)


def adhoc_test():
  try:
    if sys.argv[2] == 'showtests':
      return adhoc_tests_show()
    n_test = int(sys.argv[2])
    print('Executing test', n_test)
    funcname = 'adhoc_test%d()' % n_test
    exec(funcname)
    return
  except (IndexError, ValueError):
    pass
  adhoc_test1()


def process():
  is_command_invalid = False
  try:
    if sys.argv[2] == 'comb':
      n = int(sys.argv[3])
      c = int(sys.argv[4])
      result = combine_n_c_by_c(n, c)
      outdict = {'n': n, 'c': c, 'result': result}
      scrmsg = 'combine_n_c_by_c(%(n)d, %(c)d) =  %(result)d' % outdict
      print(scrmsg)
  except ValueError:
    is_command_invalid = True
  if is_command_invalid:
    print('Invalid command')


def adhoc_test5():
  n_combs = combine_n_c_by_c(20, 5)
  print('ca.combine_n_c_by_c(70, 7)', n_combs)


if __name__ == '__main__':
  """
  """
  adhoc_test1()
