#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/lgi_lexicographical_indices_to_from.py

Main functions here:
  calc_lgi_b0idx_from_comb_where_ints_start_at_0()
    Calculates the lexicographical index from a combination (n_elements, n_slots)
  calc_comb_from_lgi_b1idx_where_ints_start_at_0()
    Calculates, from the lexicographical index, a combination (n_elements, n_slots)

As hinted above, the relation (lgi, comb) forms a bijection, ie:
  f(lgi) = comb
  f_inv(comb) = lgi

The algorithm found in the Wikidepia (@see info and URL below) uses
  an ascending ordered combination but establishes the indices
  in descending order in contrast to an ascending combination order.

  Example:
    In combiner(n_elements=4, n_slots=3)
    the first combination, [0, 1, 2], has lgi 8 (which is also the total combinations)
    the last combination, [1, 2, 3], has lgi 1;
  Because of that, this system has chosen to use two index-types, they are:
    t1 the one described above (also the one found in Wikipedia)
    t2 the complement from the one described above
      (ie, in the example, 8 becomes 1 (which is 9-8) and 1 becomes 8 (9-1)
"""
import fs.mathfs.combinatorics.IndicesCombiner_functions as iCfs  # icfs.add_one
import fs.mathfs.combinatorics.combinatoric_algorithms as ca  # ca.fact(n)


class LgiToFromCombination:
  """
  This class implements the bijective lgi functions (foward and inverse).
    The direct/forward function finds the lgi of a combination.
    The inverse/backward function finds the combination from its lgi.

  The relation is a bijection, ie:
    f(lgi) = comb
    f_inv(comb) = lgi

  The direct/forward (math) function is implemented as a (program) function.
  The inverse/backward (math) function is implemented as a (program) class.

  This class is a kind of associator, ie when one is set, the other is calculated and set too,
    so if either of the two changes, the other changes too.

  Out of the four index-types, only b0_idx is settable, this derives the other three.
  """

  def __init__(self, n_elements, n_slots):
    """
    """
    self.n_elements = n_elements
    self.n_slots = n_slots
    self.total_combs = ca.combine_n_c_by_c_fact(n_elements, n_slots)
    # the following two are settable and setting one modifies the other
    self._b0idx_lgi = None
    self._combset = None

  @property
  def combset(self):
    return self._combset

  @combset.setter
  def combset(self, p_combset):
    """
    calls the "inverse lgi function"
      b0idx_lgi = calc_lgi_b0idx_from_comb_where_ints_start_at_0(cmbset, n_elements)
      setting both combset and its associated lgi
    """
    is_consistent = is_combination_consistent_w_nelements(p_combset, self.n_elements)
    if not is_consistent:
      errmsg = f'parameter combset {p_combset}, for finding its lgi, is not valid.'
      raise ValueError(errmsg)
    self._combset = list(p_combset)
    self._b0idx_lgi = calc_lgi_b0idx_from_comb_where_ints_start_at_0(self._combset, n_elements=self.n_elements)

  @property
  def b0idx_lgi(self):
    return self._b0idx_lgi

  @b0idx_lgi.setter
  def b0idx_lgi(self, p_b0idx_lgi):
    """
    calls the "forward lgi function"
      b0idx_lgi = calc_lgi_b0idx_from_comb_where_ints_start_at_0(cmbset, n_elements)
      setting both combset and its associated lgi
    """
    if p_b0idx_lgi < 0 or p_b0idx_lgi > self.size:
      errmsg = f'parameter b0idx_lgi {p_b0idx_lgi}, for finding its combset, is not valid.'
      raise ValueError(errmsg)
    self._b0idx_lgi = p_b0idx_lgi
    self._combset = lgi_f_inv_from_b0idx_to_combination(p_b0idx_lgi, self.n_slots, self.n_elements)

  @property
  def b1idx_lgi(self):
    if self._b0idx_lgi is not None:
      return self._b0idx_lgi + 1
    return None

  @property
  def b0idx_lgisimm(self):
    if self._b0idx_lgi is not None:
      return self.size - self._b0idx_lgi
    return None

  @property
  def b1idx_lgisimm(self):
    if self._b0idx_lgi is not None:
      return self.size - self.b1idx_lgisimm
    return None

  @property
  def size(self):
    return self.total_combs

  def __str__(self):
    outstr = f"LgiToFromComb {self.combset} | b0_idx={self.b0idx_lgi}"
    return outstr


def is_combination_consistent_w_nelements(cmbset, n_elements):
  """
  # check 1: cmbset should not be None or empty or with n_elements < 1
    (n_slots does not affect consistency though used for ordering checking)
  # check 2: combset should be in ascending order: valid [1,2,3], invalid [3,2,1]
  # check 3: first element should be greater than -1
             (resulting in all of them being non-negative, because they are in ascending order)
  # check 4: last element should be lesser than n_elements
             (resulting in every element being less than n_elements, for the same reason, ascending order)

  Former checkings removed because they were somehow redundant:
    # check the 'unit' (or least sized) set, ie if n_elements == 1, set is [0]
      => checks 3 and 4 cover this
    # should not have repeated elements: valid [1,2,3], invalid [1,2,2,3]
      => ascending order (check 2) covers this
    # should not have negative numbers: invalid [-3,-2,-1], though valid in asc order
      => suffice checking the first element (check 3), no need to check them all (because of ascending order)
    # should not have elements greater than upper limit, which is n_elements - 1
      => suffice checking the last element (check 4), idem

  Args:
    cmbset: list the combination set
    n_elements: int the number of elements in combination

  Returns:
    False | True
  """
  # check 1: cmbset should not be None or empty or with n_elements < 1
  if cmbset is None or len(cmbset) == 0 or n_elements < 1:
    # errmsg = f"combination (=[{cmbset}) is None or len(cmbset) == 0 or n_elements (={n_elements}) < 1."
    # raise ValueError(errmsg)
    return False
  n_slots = len(cmbset)  # n_slots is not a function's parameter, it's used for checking ascending order
  # check 2: combset should be in ascending order: valid [1,2,3], invalid [3,2,1]
  bool_list_chk_asc_order = [cmbset[i] < cmbset[i+1] for i in range(n_slots-1)]
  if False in bool_list_chk_asc_order:
    # errmsg = f"combination (=[{cmbset}) is not in ascending order."
    # raise ValueError(errmsg)
    return False
  # check 3: first element should be greater than -1 (resulting in all of them being non-negative)
  first_element = cmbset[0]
  if first_element < 0:
    # errmsg = f"combination (=[{cmbset}) has negative numbers."
    # raise ValueError(errmsg)
    return False
  # check 4: last element should be lesser than n_elements
  # (resulting in every element being less than n_elements)
  last_element = cmbset[-1]
  if last_element > n_elements - 1:
    # errmsg = f"combination (=[{cmbset}) has elements greater than upper limit."
    # raise ValueError(errmsg)
    return False
  return True


def calc_lgi_b0idx_from_comb_where_ints_start_at_0(cmbset, n_elements):
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

      2nd) the formula (or function) for finding the lgi_b1idx (n_elements=né, n_slots=ns)
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
  if not is_combination_consistent_w_nelements(cmbset, n_elements):
    errmsg = f"combination (={cmbset}) is not consistent with scheme:"
    errmsg += f" (n_elements={n_elements}, n_slots={n_slots})"
    raise ValueError(errmsg)
  # looking at the docstring above, comb [1, 2, 3, 4, 5, 6] comes in as 0-indices, ie [0, 1, 2, 3, 4, 5]
  # so the next "plus 1" adjustment is necessary
  adjusted_plus1_cmb = list(map(lambda e: e+1, cmbset))
  # if total_combs is None:
  #   total_combs = ca.combine_n_c_by_c_fact(n_elements, n_slots)
  slot_idx, lgi_computed = 0, 0
  for m in range(n_slots, 0, -1):
    coef_in_pos = adjusted_plus1_cmb[slot_idx]
    fact_num = n_elements - coef_in_pos
    fact_den = m
    sumparcel = ca.combine_n_c_by_c_fact(fact_num, fact_den)
    lgi_computed += sumparcel
    slot_idx += 1
  return lgi_computed


def calc_lgi_b1idx_from_comb_where_ints_start_at_0(cmbset, n_elements):
  lgi_b0idx = calc_lgi_b0idx_from_comb_where_ints_start_at_0(cmbset, n_elements)
  lgi_b1idx = lgi_b0idx + 1
  return lgi_b1idx


def calc_lgisimm_b0idx_from_comb_where_ints_start_at_0(cmbset, n_elements):
  lgi_computed = calc_lgi_b0idx_from_comb_where_ints_start_at_0(cmbset, n_elements)
  n_slots = len(cmbset)
  total_combs = ca.combine_n_c_by_c_fact(n_elements, n_slots)
  lgisimm_computed = total_combs - lgi_computed - 1
  return lgisimm_computed


def calc_lgisimm_b1idx_from_comb_where_ints_start_at_0(cmbset, n_elements):
  lgisimm_b0idx = calc_lgisimm_b0idx_from_comb_where_ints_start_at_0(cmbset, n_elements)
  lgisimm_b1idx = lgisimm_b0idx + 1
  return lgisimm_b1idx


def table_combs_size():
  """
  show number in the lgi formation of:
    0 [2, 3, 4]    1 [1, 3, 4]    2 [1, 2, 4]
    3 [1, 2, 3]    4 [0, 3, 4]    5 [0, 2, 4]
    6 [0, 2, 3]    7 [0, 1, 4]    8 [0, 1, 3]
    9 [0, 1, 2]
  """
  combs = [
    [2, 3, 4], [1, 3, 4], [1, 2, 4], [1, 2, 3], [0, 3, 4],
    [0, 2, 4], [0, 2, 3], [0, 1, 4], [0, 1, 3], [0, 1, 2],
  ]
  n_elements, n_slots = 5, 3
  lgis = []
  for comb in combs:
    ms = list(range(1, n_slots+1))
    lgi = 0
    adjusted_plus1_cmb = list(map(lambda e: e + 1, comb))
    for i, ccoef in enumerate(adjusted_plus1_cmb):
      n = n_elements - ccoef
      m = ms.pop()
      parcel = ca.combine_n_c_by_c_fact(n, m)
      scrmsg = f"{i} comb {n}, {m} = {parcel} ccoef={ccoef}"
      print(scrmsg)
      lgi += parcel
    lgis.append(lgi)
    print('-'*10, 'lgi', lgi, comb)
  print(lgis)


def adhoctest_f_inv():
  """
  lgi = 4
  comb = lgi_f_inv_from_b0idx_to_combination(lgi, n_slots=3, n_elements=5, acc_comb=None)
  scrmsg = f"f_inv given lgi={lgi} => found comb={comb}"
  print(scrmsg)

  """
  for lgi in range(10):
    comb = lgi_f_inv_from_b0idx_to_combination(lgi, n_slots=3, n_elements=5, acc_comb=None)
    scrmsg = f"f_inv given lgi={lgi} => found comb={comb}"
    print(scrmsg)
  print('='*20)
  for lgi in range(9, -1, -1):
    comb = lgi_f_inv_from_b0idx_to_combination(lgi, n_slots=3, n_elements=5, acc_comb=None)
    scrmsg = f"f_inv given lgi={lgi} => found comb={comb}"
    print(scrmsg)
  lgi = 50063859
  comb = lgi_f_inv_from_b0idx_to_combination(lgi, n_slots=6, n_elements=60, acc_comb=None)
  scrmsg = f"f_inv given lgi={lgi} => found comb={comb}"
  print(scrmsg)
  # ===========
  n_elements, comb = 60, [0, 1, 2, 3, 4, 5]
  lgi = calc_lgi_b0idx_from_comb_where_ints_start_at_0(comb, n_elements=n_elements)
  scrmsg = f" => given comb={comb} => found lgi={lgi}"
  print(scrmsg)
  # ===========
  lgi = 10000000
  comb = lgi_f_inv_from_b0idx_to_combination(lgi, n_slots=6, n_elements=60, acc_comb=None)
  scrmsg = f"f_inv given lgi={lgi} => found comb={comb}"
  print(scrmsg)


def calc_lgi_parcel(combint, pos, n_slots, n_elements):
  ccoef = combint + 1
  n = n_elements - ccoef
  m = n_slots - pos
  parcel = ca.combine_n_c_by_c_fact(n, m)
  return parcel


def find_int_n_lgiparcel_from_all_poss_ints(
    lgi_remains, pos, n_slots, n_elements, min_at_pos, max_at_pos
):
  """
  This function is (an inner) part of the algorithm for the lgi inversion function.

  It picks up the intvalue key, in a dict, that contains
    the closest value to lgi_remains that is not, at the same, greater than it.

  Example:
      Suppose lgi_remains = 10 and pos = 1

  Examining min_at_pos = [0, 1, 2] & max_at_pos = [2, 3, 4]
    pos 1 can contain a mininum of 1 and a maximum of 3

  Suppose now that poss_ints_n_lgis_dict is formed (just as an example) with:
    {1: 5, 2: 9, 3: 12}
  The algorithm must choose the lesser than 10 value closest to 10.
    In the dict above, that value is 9 and its key is 2, ie {2: 9}.
    That is also the pair (intguessed, ilgi) that will be returned.
      ie (intguessed=2, ilgi=9)

  Args:
    lgi_remains:
    pos:
    n_slots:
    n_elements:
    min_at_pos:
    max_at_pos:

  Returns:

  """
  all_poss_ints = list(range(min_at_pos, max_at_pos+1))
  # call a function getting all pairs (intvals, parcels)
  # chosen the one that fits! ie one that is less than lgi, but having its next follower greater than
  poss_ints_n_lgis_dict = {}
  for intguessed in all_poss_ints:
    ilgi = calc_lgi_parcel(intguessed, pos, n_slots, n_elements)
    poss_ints_n_lgis_dict[intguessed] = ilgi
  poss_ints_n_lgis_dict = dict(sorted(poss_ints_n_lgis_dict.items(), key=lambda e: e[1]))
  pair = (-1, -1)
  for intguessed in poss_ints_n_lgis_dict:
    ilgi = poss_ints_n_lgis_dict[intguessed]
    if ilgi <= lgi_remains:
      pair = (intguessed, ilgi)
    else:
      break
  if pair == (-1, -1):
    errmsg = f'Error in the algorithm: the function failed to find a remaining value for lgi "consumption"'
    raise ValueError(errmsg)
  intguessed, ilgi = pair
  return intguessed, ilgi


def lgi_f_inv_inner_from_b0idx_to_combination(
    lgi_remains, n_slots, n_elements, acc_comb, min_at_each_pos, max_at_each_pos
):
  """
    Implements the inverse lgi function, ie given a lgi, find a combination.

  This function has an "entrance function" and this follower one is recursive.
  The division of work, so to say, is the following:
    1 the "entrance function" validates parameters.
    2 this follower function does the computation.

  Because of this, it's important, if this functionality is needed,
    to call it indirectly via the "entrace one",
    so that parameters be treated before getting here. (*)

  (*) As a side note, the Python language does not enforce 'private' access,
     so, because of that, the programmer should observe
     the access to it via the entrance function (...).
  """
  pos = 0 if acc_comb is None else len(acc_comb)
  max_at_pos = max_at_each_pos[pos]
  min_at_pos = min_at_each_pos[pos]
  intguessed, ilgi = find_int_n_lgiparcel_from_all_poss_ints(
    lgi_remains, pos, n_slots, n_elements, min_at_pos, max_at_pos
  )
  acc_comb.append(intguessed)
  lgi_remains -= ilgi
  if pos == n_slots - 1:
    # finish condition (ie, combination was fully traversed from left to right)
    return acc_comb
  # recurse on with acc_comb, though appended not yet having n_slots size
  return lgi_f_inv_inner_from_b0idx_to_combination(
    lgi_remains, n_slots, n_elements, acc_comb, min_at_each_pos, max_at_each_pos
  )


def lgi_f_inv_from_b0idx_to_combination(lgi_remains, n_slots, n_elements, acc_comb=None):
  """
    Implements the inverse lgi function, ie given a lgi, find a combination

  This is the "entrance" function, ie lgi_f_inv_from_b0idx_to_combination.
  It treats parameters and dispatch to lgi_f_inv_inner_from_b0idx_to_combination(),
  the latter being recursive and doing the computation itself.
  """
  total_combs = ca.combine_n_c_by_c_nonfact(n_elements, n_slots)
  max_1based_combs_idx = total_combs - 1
  if lgi_remains > max_1based_combs_idx:
    errmsg = f"lgi_remains {lgi_remains} > max_1based_combs_idx {max_1based_combs_idx}"
    raise ValueError(errmsg)
  acc_comb = [] if acc_comb is None else acc_comb
  max_at_each_pos = iCfs.make_the_last_or_maximum_combination(n_elements=n_elements, n_slots=n_slots)
  min_at_each_pos = iCfs.make_the_first_or_minimum_combination(n_elements=n_elements, n_slots=n_slots)
  return lgi_f_inv_inner_from_b0idx_to_combination(
    lgi_remains, n_slots, n_elements, acc_comb, min_at_each_pos, max_at_each_pos
  )


def accompany_lgi():
  """
  1 (50063855, [53, 55, 56, 57, 58, 59])
  2 (50063855, [54, 55, 56, 57, 58, 59])
  """
  # ------------------
  n_elements, cmb = 4, [0, 1, 2]
  lgi = calc_lgi_b0idx_from_comb_where_ints_start_at_0(cmb, n_elements)
  scrmsg = f"n_elements {n_elements}, cmb {cmb}, lgi {lgi}"
  print(scrmsg)
  # ------------------
  lgisimm = calc_lgisimm_b0idx_from_comb_where_ints_start_at_0(cmb, n_elements)
  scrmsg = f"n_elements {n_elements}, cmb {cmb}, lgisimm {lgisimm}"
  print(scrmsg)
  # ------------------
  n_elements, cmb = 4, [0, 1, 3]
  lgi = calc_lgi_b0idx_from_comb_where_ints_start_at_0(cmb, n_elements)
  scrmsg = f"n_elements {n_elements}, cmb {cmb}, lgi {lgi}"
  print(scrmsg)
  # ------------------
  lgisimm = calc_lgisimm_b0idx_from_comb_where_ints_start_at_0(cmb, n_elements)
  scrmsg = f"n_elements {n_elements}, cmb {cmb}, lgisimm {lgisimm}"
  print(scrmsg)
  # ------------------
  n_elements, cmb = 4, [0, 2, 3]
  lgi = calc_lgi_b0idx_from_comb_where_ints_start_at_0(cmb, n_elements)
  scrmsg = f"n_elements {n_elements}, cmb {cmb}, lgi {lgi}"
  print(scrmsg)
  # ------------------
  lgisimm = calc_lgisimm_b0idx_from_comb_where_ints_start_at_0(cmb, n_elements)
  scrmsg = f"n_elements {n_elements}, cmb {cmb}, lgisimm {lgisimm}"
  print(scrmsg)
  # ------------------
  n_elements, cmb = 4, [1, 2, 3]
  lgi = calc_lgi_b1idx_from_comb_where_ints_start_at_0(cmb, n_elements)
  scrmsg = f"n_elements {n_elements}, cmb {cmb}, lgi b1idx {lgi}"
  print(scrmsg)
  # ------------------
  lgisimm = calc_lgisimm_b1idx_from_comb_where_ints_start_at_0(cmb, n_elements)
  scrmsg = f"n_elements {n_elements}, cmb {cmb}, lgisimm b1idx {lgisimm}"
  print(scrmsg)
  # ------------------
  n, m = 59, 55
  tot = ca.combine_n_c_by_c_fact(n, n-m)
  scrmsg = f"comb {n}, {n-m}, {m} is {tot}"
  print(scrmsg)


def adhoc_test():
  """
  lgi, n_elements, n_slots = 3, 4, 3
  lgi_o = LgiToCombination(lgi=lgi, n_elements=n_elements, n_slots=n_slots)
  lgi_o.process()
  """
  comb = [0, 1, 2]
  nextcomb = iCfs.add_one(comb, n_elements=4)
  print(comb, nextcomb)
  comb = list(nextcomb)
  nextcomb = iCfs.add_one(comb, n_elements=4)
  print(comb, nextcomb)
  comb = list(nextcomb)
  nextcomb = iCfs.add_one(comb, n_elements=4)
  print(comb, nextcomb)
  comb = list(nextcomb)
  nextcomb = iCfs.add_one(comb, n_elements=4)
  print(comb, nextcomb)
  nextcomb = iCfs.subtract_one(comb, n_elements=4)
  print('subtract', comb, nextcomb)
  comb = list(nextcomb)
  nextcomb = iCfs.subtract_one(comb, n_elements=4)
  print('subtract', comb, nextcomb)


if __name__ == '__main__':
  """
  adhoc_test()
  adhoc_test()
  accompany_lgi()

  """
  # table_combs_size()
  adhoctest_f_inv()
