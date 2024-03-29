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
import copy
import random
import sys
import fs.mathfs.combinatorics.IndicesCombiner_functions as icfs  # icfs.add_one


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
  """
  Example:
    ...
  Args:
    subtokens:

  Returns:

  """
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


def combine_n_c_by_c_fact(n, c, turnoff_floatcheck=True):
  if n < 0 or c < 0:
    errmsg = f'Cannot calculate factorial with negative numbers ({n}, {c}).'
    raise ValueError(errmsg)
  # this condition below may be reformulation to an exception raising
  if n == 0 or c == 0:
    return 0  # empty set: review this when possible
  if n < c:
    return 0
  if n == c:
    return 1
  float_result = fact(n) / (fact(n - c) * fact(c))
  if not turnoff_floatcheck:
    rounded_float = round(float_result, 0)
    if float_result != rounded_float:
      errmsg = f'float_result={float_result} != round(float_result, 0)={rounded_float} in combination by factorial'
      raise ValueError(errmsg)
  return int(float_result)


def combine_n_c_by_c_nonfact(n, c):
  """

  combine_n_c_by_c_nonfact(n, c) is a function that computes the number R of
    combinations of an n-element set S, c by c elements.
   
  Ex. suppose S = [1,2,3]
  Combinations 2 by 2 of S are [1,2],[1,3] and [2,3]
  Hence, R, the resulting numbers of combinations, is 3.
  
  We can also see combine_n_c_by_c_nonfact(n, c) by its factorial formula, which is n!/((n-c)!c!)
  
  In the simple example above, R = 3!/(2!1!) = 3 x 2! / 2! = 3
  
  As a more computing-intense example, Megasena has:
    R = combine_n_c_by_c_nonfact(60, 6) = 60! / ((60-6)!6!) = ... =  50063860
  
  The Python code implementation here does not use factorial in order
     to optimization/minimize computation efforts.
  """
  if n < 0 or c < 0:
    errmsg = f'Cannot calculate factorial with negative numbers ({n}, {c}).'
    raise ValueError(errmsg)
  # this condition below may be reformulation to an exception raising
  # in the future (how can one combine more than one has?), for the time being, it's returning 0
  if n == 0 or c == 0:
    return 0
  if n < c:
    return 0
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


def mount_middle_comb_with_pivot_n_pivotidx(pivot, pivot_idx, n_elements, n_slots):
  if pivot > n_elements - n_slots:
    return None
  if pivot_idx > n_slots - 1:
    errmsg = f"pivot_idx (={pivot_idx}) > n_slots=({n_slots}) - 1"
    raise ValueError(errmsg)
  if pivot_idx == 0:
    middle_comb = [pivot+i for i in range(n_slots)]
    return middle_comb
  if pivot_idx == n_slots - 1:
    middle_comb = [pivot-(n_slots+i) for i in range(n_slots)]
    return middle_comb
  # pivot_idx > 0 and < n_slots - 1
  left_comb = [pivot-i for i in range(pivot_idx-1, -1, -1)]
  right_comb = [pivot+i for i in range(pivot_idx+1, n_slots)]
  middle_comb = left_comb + [pivot] + right_comb
  return middle_comb


def calc_comb_from_lgi_b1idx_where_ints_start_at_0(
    lgi, n_elements, n_slots, total_combs=None, comb=None, lastcomb=None, pivot=None, pivot_idx=None
):
  """
  This function is the inverse of calc_lgi_b0idx_from_comb_where_ints_start_at_0(cmbset, n_elements)
  """
  if lastcomb is None:
    lastcomb = list(range(54, 60))
  if comb is None:
    comb = list(lastcomb)
  if total_combs is None:
    total_combs = combine_n_c_by_c_fact(n_elements, n_slots)
  remaining = total_combs - lgi + 1
  if remaining == 1:
    return lastcomb
  pivot = n_elements if pivot is None else pivot
  pivot_idx = 0 if pivot_idx is None else pivot_idx
  comb = mount_middle_comb_with_pivot_n_pivotidx(pivot, pivot_idx)
  while remaining > 0:
    comb = icfs.subtract_one(comb, n_elements)
    # continue from here!
    lgi = calc_lgi_from_comb_where_ints_start_at_0(comb, n_elements)
    remaining = remaining - lgi + 1
  return comb


def calc_lgi_from_comb_where_ints_start_at_0(cmbset, n_elements):
  """
    Outputs the lexicographical index representing the current_combination in the instance object

    IMPORTANT:
      i1 this implementation may not be the standard one if such a standard one exists;
      i2 the version here uses ascending order (lexicographical order) for combinations;
      i3 it also establishes ascending order for the lexicographical index itself;

    ie, in the case n_elements=60, n_slots=6:
      the first combination [1, 2, 3, 4, 5, 6] should have (1-based) index 1
      the last combination [54, 55, 56, 57, 58, 59, 60] should have (1-based) index 50063860

    The algorithm for finding the lgi_b1idx:

      1st) the combination must be in ascending order, ie:
           c1 < c2 < ... < c[ns-1] < c[ns]  where ns is the
        number of ints in cardgame (a combination set itself) or,
        in the nomeclature here, n_slots,
          and comb = [c1, c2, ..., c[ns-1], c[ns]]

      2nd) the formula (or function) for finding the lgi_b1idx (n_elements=ne, n_slots=ns)
           is the following:

      parcial = c(60-c1, 6) + c(60-c2, 5) + c(60-c3, 4) + c(60-c4, 3) + c(60-c5, 2) + c(60-c6, 1)
      lgi_b1idx(comb) = totalCombs(60, 6) - parcial

      and totalCombs(60, 6) = c(60, 6) = 60! / (54!*6!) =  50063860

      Obs:
        o1 the results form a "1-index" mapping to the combination set;
        o2 for a 0-index mapping suffices subtracting one to it (ie idx0[n]=idx1[n]-1);

      Example (for the MS case: n_elements=60, n_slots=6):
        Let us take a look at the combinations in ascending order (or lexicographical order):
          cmb1 = [1, 2, 3, 4, 5, 6] => its lgi_b1idx is 1 (under 1-index-mapping) or 0 (under 0-index-mapping)
          cmb2 = [1, 2, 3, 4, 5, 7] => its lgi_b1idx is 2 (or 1, 2-1)
          cmb3 = [1, 2, 3, 4, 5, 8] => its lgi_b1idx is 3 (or 2, 3-1)
          (...)
          cmbLast = [54, 55, 56, 57, 58, 59, 60] => its lgi_b1idx is 50063860 (or 50063859, 50063860-1)
      @see also the above algorithm in the module where its function is located.

  """
  n_slots = len(cmbset)
  # looking at the docstring above, comb [1, 2, 3, 4, 5, 6] comes in as 0-indices, ie [0, 1, 2, 3, 4, 5]
  # so the next "plus 1" adjustment is necessary
  adjusted_plus1_cmb = list(map(lambda e: e+1, cmbset))
  total_combs = combine_n_c_by_c_fact(n_elements, n_slots)
  slot_idx, lgi_computed = 0, 0
  for m in range(n_slots, 0, -1):
    fact_num = n_elements - (adjusted_plus1_cmb[slot_idx])
    fact_den = m
    sumparcel = combine_n_c_by_c_fact(fact_num, fact_den)
    lgi_computed += sumparcel
    slot_idx += 1
  lgi_computed = total_combs - lgi_computed
  return lgi_computed


def random_permutation(perm):
  n = len(perm)
  for i in range(1, n+1):
    perm[i] = i
  for i in range(1, n+1):
    j = i + random.randint(1, n+1) * (n + 1 - i)
    k = perm[i]
    perm[j] = k


class DecrescentCombiner:
  def __init__(self, startint=3, nslots=5, upto=6):
    self.startint, self.nslots, self.upto = startint, nslots, upto
    self.combs = []
    self.ongoingcomb = [self.startint]

  @property
  def soma(self):
    return sum(self.ongoingcomb)

  def move_to_leftplace_n_diminish_1(self):
    if len(self.ongoingcomb) < 1:
      return False
    self.ongoingcomb.pop()  # last digit was stripped out
    if len(self.ongoingcomb) < 1:
      return False
    leftdigit = self.ongoingcomb[-1]
    if leftdigit < 2:
      return self.move_to_leftplace_n_diminish_1()
    leftdigit -= 1
    self.ongoingcomb[-1] = leftdigit
    return True

  def diminish_1_on_last_pos_n_leftpropagate_if_needed(self):
    ondigit = self.ongoingcomb[-1]
    if ondigit < 2:
      return self.move_to_leftplace_n_diminish_1()
    ondigit -= 1
    self.ongoingcomb[-1] = ondigit
    return True

  def recurs_combine_n_make_sumsets(self):
    if self.soma >= self.upto:
      if self.soma == self.upto:
        self.combs.append(copy.copy(self.ongoingcomb))
      boolret = self.diminish_1_on_last_pos_n_leftpropagate_if_needed()
      if not boolret:
        return
      return self.recurs_combine_n_make_sumsets()
    # self.soma < self.upto:
    # duplicate digit and recurse
    ondigit = self.ongoingcomb[-1]
    if len(self.combs) == self.nslots + 1:  # cannot grow larger at this point, but can move left
      boolret = self.diminish_1_on_last_pos_n_leftpropagate_if_needed()
      if not boolret:
        return
    self.ongoingcomb.append(ondigit)
    return self.recurs_combine_n_make_sumsets()

  def __str__(self):
    outstr = f"""DecrescentCombiner object
    upto={self.upto} nslots={self.nslots} startint={self.startint}
    {self.combs}
    """
    return outstr


def get_combine_sumsets(guide=3, upto=6, stack=None, results=None):
  """
  """
  if guide > upto:
    return get_combine_sumsets(guide-1, upto, stack, [])
  elif guide < 1:
    return results
  stack = [] if stack is None else stack
  results = [] if results is None else results
  if sum(stack) + guide > upto:
    return get_combine_sumsets(guide-1, upto, stack, results)
  elif sum(stack) + guide == upto:
    stack.append(guide)
    results.append(copy.copy(stack))
    if guide > 1:
      stack.pop()
      return get_combine_sumsets(guide-1, upto, stack, results)
    else:  # guide is 1 at here
      # move left
      digit = stack.pop()
      while digit > 1 and len(stack) > 0:
        digit = stack.pop()
      if len(stack) > 0:
        return get_combine_sumsets(guide-1, upto, stack, results)
  # else:  # ie sum(stack) + guide < upto
  stack.append(guide)
  return get_combine_sumsets(guide, upto, stack, results)


def get_all_complements_to_sum(ongoidx, target_sum):
  """
  Example:
    e1 => get_all_complements_to_sum(ongoidx=4, target_sum=6)
      The output is: [4, 2], [4, 1, 1]
    e2 => get_all_complements_to_sum(ongoidx=3, target_sum=6)
      The output is: [3, 3], [3, 2, 1], [3, 1, 1, 1]
    (etc)
  Args:
    ongoidx:
    target_sum:

  Returns:

  """
  diff = target_sum - ongoidx
  ints = list(range(diff+1))
  sets = get_combine_sumsets(ints, upto=target_sum)
  complements = []
  for i in range(len(ints), 0, -1):
    pass


def gen_all_integer_partitions_for(ongoidx=6, target_sum=6, up_to_slots=6):
  # start by one full slot
  if ongoidx == target_sum:
    elem = f'{ongoidx}'
    yield elem
    ongoidx -= 1
    return gen_all_integer_partitions_for(ongoidx, target_sum, up_to_slots)
  complements = get_all_complements_to_sum(ongoidx, target_sum)
  idx1integers = list(up_to_slots+1)
  # first element
  firstcount = idx1integers.pop()

  for amount in list(range(up_to_slots-1, 0, -1)):
    pass

def mount_all_integer_partitions_for(soma, parcel=-1, acc=None):
  """
This function 'mounts' the integer partitions recursively.
TODO a non-recursive equivalent.

  geraSumComponents(soma, parcel=-1, acc=[]) is
    an [[[ Integer Partitions generator ]]]
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
  fs.mathfs.combinatorics.combinatoric_algorithms.RCombiner
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
      Notice that it also "arranges" sequences starting with zeroes:
        eg  [0, 1, 0, 0, 4, 0, 0, 0, 1, 0]
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

  def expand_slotpartitions_to_inbetween_graftedzeroes(self, n_slots=6):
    """
    The set produces here is the same as:
      expand_base_intpartitions_to_slots(self, n_slots=6)
    excluding the ones that have beginning zeroes or ending zeroes.
    Example:
      In the "expand_base" above, we saw that, as an example,
        set [0, 1, 0, 0, 4, 0, 0, 0, 1, 0] in include.
      However, the "inbetween_graftedzeroes" set does not contain
         elements (sets in themselves) having starting or ending zeroes,
         so that one must not be included.

    Args:
      n_slots:

    Returns:

    """


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
    funcname = 'list_dist_xysum_metric_thru_ms_history%d()' % n_test
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
      result = combine_n_c_by_c_nonfact(n, c)
      outdict = {'n': n, 'c': c, 'result': result}
      scrmsg = 'combine_n_c_by_c_nonfact(%(n)d, %(c)d) =  %(result)d' % outdict
      print(scrmsg)
  except ValueError:
    is_command_invalid = True
  if is_command_invalid:
    print('Invalid command')


def adhoc_test5():
  """
  n_combs = combine_n_c_by_c_nonfact(20, 5)
  print('ca.combine_n_c_by_c_nonfact(70, 7)', n_combs)
  Returns:
  guide = 3
  results = get_combine_sumsets(guide, upto=6)
  print('guideint', guide, 'results', results)
  results = get_combine_sumsets2(leftmost=guide, upto=6, slots=3)
  print('guide', guide, 'results', results)
  """
  cmber = DecrescentCombiner(startint=3, nslots=6, upto=6)
  cmber.recurs_combine_n_make_sumsets()
  print(cmber)


def adhoctest_sumlgi(comb):
  total = 0
  m = 7
  for n in comb:
    m -= 1
    comb = combine_n_c_by_c_nonfact(60 - n, m)
    total += comb
    scrmsg = f"comb(n={60-n}, m={m})={comb} | total={50063860-total}"
    print(scrmsg)


def adhoc_test6():
  """
    Eg ==>> f(31029, ic(60,6)) = [19,15,13,11,5,4]
    because
      c(19,6)+c(15,5)+c(13,4)+c(11,3)+c(5,2)+c(4,1) = 31029

  """
  comb = list(range(1, 7))
  print('='*20, comb)
  adhoctest_sumlgi(comb)
  #
  comb = comb[:5] + [7]
  print('='*20, comb)
  adhoctest_sumlgi(comb)
  #
  comb = sorted([19, 15, 13, 11, 5, 4])
  print('='*20, comb)
  adhoctest_sumlgi(comb)
  #
  comb = list(reversed(comb))
  print('='*20, comb)
  adhoctest_sumlgi(comb)
  #
  comb = list(range(1, 7))
  print('='*20, comb)
  adhoctest_sumlgi(comb)
  #
  comb = list(reversed(comb))
  print('='*20, comb)
  adhoctest_sumlgi(comb)
  #
  comb = [7] + comb[1:]
  print('='*20, comb)
  adhoctest_sumlgi(comb)
  #
  comb = list(range(54, 61))
  print('='*20, comb)
  adhoctest_sumlgi(comb)


def table_combs_size():
  for i in range(4, 7):
    n, m = i + 3, i
    tot = combine_n_c_by_c_fact(n, m)
    scrmsg = f"comb {n}, {n-m} is {tot}"
    print(scrmsg)


def accompany_lgi():
  """
  1 (50063855, [53, 55, 56, 57, 58, 59])
  2 (50063855, [54, 55, 56, 57, 58, 59])
  """
  tupl = (50063855, [53, 55, 56, 57, 58, 59])
  retval = calc_lgi_from_comb_where_ints_start_at_0(tupl[1], n_elements=60)
  print(retval, tupl)
  tupl = (50063855, [54, 55, 56, 57, 58, 59])
  retval = calc_lgi_from_comb_where_ints_start_at_0(tupl[1], n_elements=60)
  print(retval, tupl)
  n, m = 59, 54
  tot = combine_n_c_by_c_fact(n, n-m)
  scrmsg = f"comb {n}, {n-m}, {m} is {tot}"
  print(scrmsg)
  n, m = 59, 55
  tot = combine_n_c_by_c_fact(n, n-m)
  scrmsg = f"comb {n}, {n-m}, {m} is {tot}"
  print(scrmsg)


if __name__ == '__main__':
  """
  adhoc_test6()
  """
  accompany_lgi()
  table_combs_size()

