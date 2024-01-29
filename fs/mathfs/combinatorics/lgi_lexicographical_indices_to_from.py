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
import fs.mathfs.combinatorics.IndicesCombiner_functions as icfs  # icfs.add_one
import fs.mathfs.combinatorics.combinatoric_algorithms as ca  # ca.fact(n)


class LgiToCombination:
  """
  This class implements the "inverse lgi function".
    The direct/forward function finds the lgi of a combination.
    The inverse/backward function finds the combination from its lgi.

  The relation is a bijection, ie:
    f(lgi) = comb
    f_inv(comb) = lgi

  The direct/forward (math) function is implemented as a (program) function.
  The inverse/backward (math) function is implemented as a (program) class.
  """

  def __init__(self, lgi, n_elements, n_slots):
    self.lgi = lgi
    self.n_elements = n_elements
    self.n_slots = n_slots
    self.curr_comb = list(range(n_slots))
    self.pivot = None
    self.pivot_idx = None
    self.middle_comb = None
    self.total_combs = ca.combine_n_c_by_c_fact(n_elements, n_slots)

  def sweet_combination_thru_possible_coefs(self, lookup_comb, goal, ccoef, pos):
    slots_indices = [i for i in range(1, self.n_slots+1)]
    possible_countercoefs = [i+1 for i in range(self.n_elements)]
    if len(slots_indices) != len(possible_countercoefs):
      errmsg = f'len(slots_indices)={len(slots_indices)} != len(possible_countercoefs)={len(possible_countercoefs)}'
      raise ValueError(errmsg)
    for countercoef in possible_countercoefs:
      n = self.n_elements - countercoef
      m = slots_indices.pop()
      ca.combine_n_c_by_c_fact(n, m)

  def recurse_combination_amount_parcel(self, goal, ccoef, slot_fw_pos, ccoefs=None):
    ccoefs = [] if ccoefs is None else ccoefs
    n = self.n_elements - ccoef
    m = self.n_slots - slot_fw_pos
    amount = ca.combine_n_c_by_c_fact(n, m)
    if amount < goal:
      if slot_fw_pos < self.n_slots - 1:
        slot_fw_pos += 1
        if ccoef < self.n_elements:
          ccoef += 1
          return self.recurse_combination_amount_parcel(goal, ccoef, slot_fw_pos)
      # cannot recurse and ccoef was not found
      return None
    # amount is >= goal, return ccoef and remaining
    remaining = amount - goal
    ccoefs.append(ccoef)
    if remaining > 0:
      goal = self.find_goal_for_combparcel()
      return self.recurse_combination_amount_parcel(goal, ccoef, slot_fw_pos, ccoefs)
    return ccoefs

  def find_goal_for_combparcel(self):
    vmax = -1
    ms = [i for i in range(1, self.n_slots+1)]
    for ccoef in self.curr_comb:
      n = self.n_elements - ccoef
      m = ms.pop()  # greatest value pops up first
      parcel = ca.combine_n_c_by_c_fact(n, m)
      if parcel > vmax:
        vmax = parcel
    self.curr_comb = icfs.add_one(self.curr_comb, n_elements=self.n_elements)
    return vmax

  def process(self):
    ccoef = 1
    slot_fw_pos = 0
    goal = self.find_goal_for_combparcel()
    retval = self.recurse_combination_amount_parcel(goal, ccoef, slot_fw_pos)
    print(retval)

  def estimate_pivot(self):
    """
    The idea here is to find the greatest lgi_composite mapped to the pair (n, m)
      that composes the summation that found the lgi from the combination.

    Once it's found, it diminishes the lgi from the lgi_composite and recurse on,
      or, if function not recursive, loop on, until the original becomes
      zero being subtracted by its composits.

    The idea above is somehow connected to the composition of diferent systems as a power summation,
      for example, as a decimal number with powers of 10:
        S = d0*10**0 + d1*10**2 + d2*10**3 + ... + dN*10**N

    The similarity is that the lgi is composed of combinational-sums, ie:
      lgi = c(n0, m0) + c(n1, m1) + c(n2, m2) + ... + c(nN, mN)

    This underlying thesis, in order for it to work, should have the sum parcels
      above in descending order, ie:
        c(n0, m0) > c(n1, m1) > c(n2, m2) > ... > c(nN, mN)
    """
    slot_idx, lgi_computed = 0, 0
    for m in range(self.n_slots, 0, -1):
      fact_num = self.n_elements - (adjusted_plus1_cmb[slot_idx])
      fact_den = m
      sumparcel = ca.combine_n_c_by_c_fact(fact_num, fact_den)
      lgi_computed += sumparcel
      slot_idx += 1
    return lgi_computed

  def mount_middle_comb_with_pivot_n_pivotidx(self):
    if self.pivot > self.n_elements - self.n_slots:
      return None
    if self.pivot_idx > self.n_slots - 1:
      errmsg = f"pivot_idx (={self.pivot_idx}) > n_slots=({self.n_slots}) - 1"
      raise ValueError(errmsg)
    if self.pivot_idx == 0:
      middle_comb = [self.pivot+i for i in range(self.n_slots)]
      return middle_comb
    if self.pivot_idx == self.n_slots - 1:
      self.middle_comb = [self.pivot-(self.n_slots+i) for i in range(self.n_slots)]
      return self.middle_comb
    # pivot_idx > 0 and < n_slots - 1
    left_comb = [self.pivot-i for i in range(self.pivot_idx-1, -1, -1)]
    right_comb = [self.pivot+i for i in range(self.pivot_idx+1, self.n_slots)]
    middle_comb = left_comb + [self.pivot] + right_comb
    return middle_comb

  def calc_comb_from_lgi_b1idx_where_ints_start_at_0(self):
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
      lgi = calc_lgi_b0idx_from_comb_where_ints_start_at_0(comb, n_elements)
      remaining = remaining - lgi + 1
    return comb


def is_combination_consistent_w_nelements(cmbset, n_elements):
  if cmbset is None or n_elements < 1:
    return False
  # check the 'unit' (or least sized) set
  if n_elements == 1 and list(cmbset) != [0]:
    # errmsg = f"when n_elements == 1, cmbset must be [0]. It's = {cmbset}."
    # raise ValueError(errmsg)
    return False
  # check repeated elements: valid [1,2,3], invalid [1,2,2,3]
  n_slots = len(cmbset)
  cmbset_as_set = set(cmbset)
  if n_slots != len(cmbset_as_set):
    # errmsg = f"combination (=[{cmbset}) is invalid for having repeated elements (as_set={cmbset_as_set})."
    # raise ValueError(errmsg)
    return False
  # check ascending order: valid [1,2,3], invalid [3,2,1]
  bool_list_chk_asc_order = [cmbset[i] < cmbset[i+1] for i in range(n_slots-1)]
  if False in bool_list_chk_asc_order:
    # errmsg = f"combination (=[{cmbset}) is not in ascending order."
    # raise ValueError(errmsg)
    return False
  # check minimal n_elements (ne)
  # this (minimal n_elements) check is reduced to the last one (check ascending order)
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
  for i in range(4, 7):
    n, m = i + 3, i
    tot = ca.combine_n_c_by_c_fact(n, m)
    scrmsg = f"comb {n}, {n-m} is {tot}"
    print(scrmsg)


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
  nextcomb = icfs.add_one(comb, n_elements=4)
  print(comb, nextcomb)
  comb = list(nextcomb)
  nextcomb = icfs.add_one(comb, n_elements=4)
  print(comb, nextcomb)
  comb = list(nextcomb)
  nextcomb = icfs.add_one(comb, n_elements=4)
  print(comb, nextcomb)
  comb = list(nextcomb)
  nextcomb = icfs.add_one(comb, n_elements=4)
  print(comb, nextcomb)
  nextcomb = icfs.subtract_one(comb, n_elements=4)
  print('subtract', comb, nextcomb)
  comb = list(nextcomb)
  nextcomb = icfs.subtract_one(comb, n_elements=4)
  print('subtract', comb, nextcomb)


if __name__ == '__main__':
  """
  adhoc_test()
  accompany_lgi()
  table_combs_size()
  """
  adhoc_test()
