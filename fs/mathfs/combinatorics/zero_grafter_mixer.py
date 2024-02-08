#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/zero_grafter_mixer.py
  Contains class ZeroesGraftAndCountsMixer.

The class ZeroesGraftAndCountsMixer may be explained by an example:

The example and cases given below are for n_slots=6 & n_elements=6.
The MS (Megasena) case, as an example, uses both n_slots=6 & n_slots=10.
  ie, n_slots=6 for rows and n_slots=10 for columns.

Suppose basecomb is [3, 2, 1] and gapholes=[1, 2] (or formerly 'mask' = [3, None, 2, None 1])
  where None is a kind of placeholder for the later zero-grafting.
The zeroes_amount is the complement of slots_taken to slots_total, ie
  zeroes_amount = slots_total - slots_taken
  zeroes_amount = 6 - 3 (the 3 taken [3, 2, 1], ie len([3, 2, 1]))

Processing walks the following traversal coordinates:
    grafting_coordlist = [[(1, 3)], [(1, 2), (2, 1)], [(1, 1), (2, 2)], [(2, 3)]]

This means:
  1st item: 3 zeroes being grafted into the first gap, ie '321' becomes '300021'.
    As a list, the result is [3, 0, 0, 0, 2, 1]
  2nd item: 2 zeroes being grafted into the first gap and 1 zero into the second, ie '321' becomes '300201'.
    As a list, the result is [3, 0, 0, 2, 0, 1]
    Seen from the 'mask' [3, None, 2, None 1] (used formerly, not currently)
    Notice the substitution of None for the zeroes (2 zeroes for the 1st None, 1 zero for the 2nd None).

In a nutshell, the [3, 2, 1] set may be expanded to 4 combinations when n_slots is 6.
    The 4 zero-grafted strings are: ['300021', '300201' , '302001', '320001']
      The first above ['300021'] has zeroes_amount [3, 0]
      The second one ['300201'] has zeroes_amount [2, 1]
      The third above ['302001'] has zeroes_amount [1, 2]
      The fourth above ['320001'] has zeroes_amount [0, 3]

Another examples:

e2 Suppose basecomb is [3, 3].
Because giving the mask, it's seen that there can be only one possible set,
 ie, 'mask' is [4] and all possible zero-graftings are:
  [4], [3], [2], [1], [0]

e3 Suppose basecomb is [6]. In this case, there is no zero-grafting set.

e4 Suppose basecomb is [3, 1, 1, 1]
mask is [3, None, 1, None, 1, None, 1]
but notice that the sum of zeroes cannot be more than 2.
The possible masks are: [[2,0,0], [1,1,0], [1,0,1], [0,1,1],[0,0,2]]
This kind of combination can be done by the HanoiLike object available.

e4 Suppose basecomb is [2, 1, 1, 1, 1]
[2, None, 1, None, 1, None, 1, None, 1]
The possible masks are: [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]
Idem, this combination can be done by the HanoiLike object in here.

e5 Suppose basecomb is [1, 1, 1, 1, 1, 1]
This case has no mask and no zero-grafting possibility.
"""
import fs.mathfs.combinatorics.hanoi_like_tower_piecemover as pm  # pm.HanoiLikeTowerPieceMover


def mount_zerografted_strs_w_grafting_coordlist(grafting_coordlist, amounts_in_slots, n_slots):
  """
  Example:
    grafting_coordlist = [[(1, 3)], [(1, 2), (2, 1)], [(1, 1), (2, 2)], [(2, 3)]]
      which means:
        the first combination (element/item) has 3 zeroes at betweenpos 1
          ie a000bc from [(1, 3)]
        the second combination (element/item) has 2 zeroes at bwpos 1 & 1 at bwpos 2
          ie a00b0c from [(1, 2), (2, 1)]
        the third combination (element/item) has 1 zero at bwpos 1 & 2 at bwpos 2
          ie a0b00c from [(1, 1), (2, 2)]
        the fouth combination (element/item) has 3 zeroes at betweenpos 2
          ie ab000c from [(2, 3)]

  Example input/output:
    input:
      grafting_coordlist = [[(1, 3)], [(1, 2), (2, 1)], [(1, 1), (2, 2)], [(2, 3)]]
      amounts_in_slots = [3, 2, 1]
    output:
      zerografted_strs = ['300021', '300201' , '302001', '320001']

  Args:
    grafting_coordlist: list - a tuple list containing positions with number of graftzeroes
    amounts_in_slots: list - the base list that will form the zerografted_strs
  Returns:
    zerografted_strs: list - the result with the zerografted combined strings
  """
  zerografted_strs = []
  # example  grafting_coordlist = [[(1, 3)], [(1, 2), (2, 1)], [(1, 1), (2, 2)], [(2, 3)]]
  for graftcoordunit in grafting_coordlist:
    ongo_amounts = list(amounts_in_slots)
    total_graft_pos = 0
    for graftcoord in graftcoordunit:
      pos = graftcoord[0]
      free_slots = n_slots - len(amounts_in_slots)
      n_zeroes_coord = graftcoord[1]
      n_zeroes_cutoff = n_zeroes_coord if n_zeroes_coord <= free_slots else free_slots
      zeroes_str = '0' * n_zeroes_cutoff
      ongo_amounts.insert(pos + total_graft_pos, zeroes_str)
      total_graft_pos += 1
    combstr = ''.join(map(str, ongo_amounts))
    zerografted_strs.append(combstr)
  return zerografted_strs


def get_graftzeroes_combination_list(max_zeroes_size, n_gapholes):
  """
  The graftzeroes_combination_list is mounted from a HanoiLike list by list moving
  Example:
    input:
      max_zeroes_size = 4
      n_gapholes = 3
    output: (the HanoiLike movings list)
      graftzeroes_combination_list = []
  """
  if max_zeroes_size == 0 or n_gapholes == 0:
    return []
  hmover = pm.HanoiLikeTowerPieceMover(npieces=max_zeroes_size, nslots=n_gapholes)
  graftzeroes_combination_list = hmover.allcombs
  return graftzeroes_combination_list

def graft_zeroes_with_zeroamountlist_n_gapholepositionlist(
    zeroamount_tuplelist, gaphole_position_list, amounts_in_slots, n_elements, n_slots
  ):
  """
  Example:
    input:
      zeroamount_tuplelist = [[3, 0], [2, 1], [1, 2], [0, 3]]
      gaphole_position_list = [1, 2]
      amounts_in_slots = [3, 2, 1]
      n_elements = 6
      n_slots = 6
    output:
      300021 300201 302001 320001
  """
  allcombs = []
  zeroamount_tuplelist_pop = list(reversed(zeroamount_tuplelist))
  while len(zeroamount_tuplelist_pop) > 0:
    _ = zeroamount_tuplelist_pop.pop()
    pairs_for_grafting = zip(zeroamount_tuplelist_pop, gaphole_position_list)
    graftcombs = mount_zerografted_strs_w_grafting_coordlist(
      pairs_for_grafting, amounts_in_slots=amounts_in_slots
    )
    allcombs += graftcombs
  return allcombs


def get_gaphole_idxpos_list_for_zerografting_with(amounts_in_slots, n_elements, n_slots):
  """
  @see docstring for function get_n_holes_for_zerografting_with()
  Example:
    input:
      amounts_in_slots = [3,2,1]
    output:
      gapholes = [1, 2]
  """
  n_holes = get_n_holes_for_zerografting_with(amounts_in_slots, n_elements, n_slots)
  gapholes = list(range(1, n_holes+1))
  return gapholes


def graft_zeroes_into_comb_with_n_zeroes(amounts_in_slots, n_zeroes, pos=1):
  """
  @see docstring for function get_n_holes_for_zerografting_with()
  Example:
    input:
      amounts_in_slots = [3,2,1];  n_zeroes = 3;  pos = 1
    output:
      comb_zerografted_str = '300021'  # ie 3 zeroes grafted into index position 1
  """
  prestr = ''.join(map(str, amounts_in_slots[: pos]))
  poststr = ''.join(map(str, amounts_in_slots[pos:]))
  zeroes_str = '0' * n_zeroes
  comb_zerografted_str = prestr + zeroes_str + poststr
  return comb_zerografted_str


def get_combs_with_decreasing_n_zeroes(amounts_in_slots, max_zeroes, n_slots, pos=1):
  """
  Example:
    input:
      amounts_in_slots: [3, 2, 1]
      max_zeroes: 3
      n_slots: 6
      pos: 1
    output:
      gaphole_combinations: ['300021', '30021', '3021']

  Args:
    amounts_in_slots: list - informs quantities in slots
    max_zeroes: int - informs the maximum of zeroes to be grafted into postion
    n_slots: int - informs the slot size (number of slots)
    pos: int - informs the array index position into which the zeroes_str will be grafted

  Returns:
    gaphole_combinations: list - it's amounts_in_slots zeroes-grafted
  """
  gaphole_combinations = []
  n_used_slots = len(amounts_in_slots)
  n_free_slots = n_slots - n_used_slots
  prestr = ''.join(map(str, amounts_in_slots[: pos]))
  poststr = ''.join(map(str, amounts_in_slots[pos:]))
  cutoff_max_zeroes = n_free_slots if max_zeroes >= n_free_slots else max_zeroes
  for n_zeroes in range(cutoff_max_zeroes, 0, -1):
    zeroes_str = '0' * n_zeroes
    comb_zerografted_str = prestr + zeroes_str + poststr
    gaphole_combinations.append(comb_zerografted_str)
  return gaphole_combinations


def get_n_holes_for_zerografting_with(amounts_in_slots, n_elements, n_slots):
  """
  Calculates how many grafting holes there might occur
    in the scheme (amounts_in_slots, n_elements, n_slots)

  The general rule is: n_holes = len(amounts_in_slots) - 1
  Example: if amounts_in_slots = [3, 2, 1], then n_holes = 3 - 1 = 2
            Seen in the former mask = [3, None, 2, None, 1] where None represents a gaphole

  -------------------------------
  The docstring below is to be moved to its more appropriate place...
  -------------------------------
  This function may be explained by an example.
    Notice also that number of holes is an int, but, conceptionally,
      it may be a like in the form list(range(1, n_holes+1))

  Example: suppose n_elements=6, n_slots=6
    Combine all possible amounts in the slots, we have:

    6 6 if amounts_in_slots=[6] => result ghindices=[]
    6 6 if amounts_in_slots=[5, 1] => result ghindices=[1]
    6 6 if amounts_in_slots=[4, 1, 1] => result ghindices=[1, 2]
    6 6 if amounts_in_slots=[4, 2] => result ghindices=[1]
    6 6 if amounts_in_slots=[3, 2, 1] => result ghindices=[1, 2]
    6 6 if amounts_in_slots=[2, 2, 2] => result ghindices=[1, 2]
    6 6 if amounts_in_slots=[2, 2, 1, 1] => result ghindices=[1, 2, 3]
    6 6 if amounts_in_slots=[2, 1, 1, 1, 1] => result ghindices=[1, 2, 3, 4]
    6 6 if amounts_in_slots=[1, 1, 1, 1, 1, 1] => result ghindices=[]

  Interpretation for the gaphole indices:
    i1 Let's take this instance:
      6 6 amounts_in_slots=[2, 2, 1, 1] => result ghindices=[1, 2, 3]
    so, in the result [1, 2, 3]:
      the first element, 1, means that between [2, 2], there may occur a gaphole: [2, None, 2]
      the second element, 2, means that between [2, 1], there may occur a gaphole: [2, None, 1]
      the third element, 3, means that between [1, 1], there may occur a gaphole: [1, None, 1]
    * None above symbolizes a gaphole
    Notice that the last element (3) in ghindices also characterizes it (gapholes are always a sequence),
      ie, instead of returning [1, 2, ..., 'n'], it suffices to return 'n';

    i2 Let's take this other instance:
      6 6 if amounts_in_slots=[5, 1] => result ghindices=[1]
    this means that there can occur only one gaphole: [5, None, 1]

    Also notice that this function does not combine the gapholes themselves,
      ie when more than one can occur,
      nonetheless, this extra functionality is left for another function.
  """
  if amounts_in_slots[0] == n_elements:
    return 0
  if len(amounts_in_slots) == n_slots:
    return 0
  soma = sum(amounts_in_slots)
  if soma != n_elements:
    errmsg = f"soma (={soma}) != n_elements (={n_elements})"
    raise ValueError(errmsg)
  return len(amounts_in_slots) - 1
  # amounts_for_pop = list(reversed(amounts_in_slots))
  # n_holes = 0
  # while 1:
  #   _ = amounts_for_pop.pop()
  #   if len(amounts_for_pop) >= 1:
  #     n_holes += 1
  #   else:
  #     break
  # return n_holes


def fuse_combination_list_w_poslist(
  gaphole_position_list, graftzeroes_combination_list
):
  """
  Mounts a tuple list that composed a coordinate pair with index-position & zeroes amount at it
  Example:
    input:
      gaphole_position_list = [1, 2]
      graftzeroes_combination_list = [[3, 0], [2, 1], [1, 2], [0, 3]]
    output:
      grafting_coordlist = [[(1, 3)], [(1, 2), (2, 1)], [(1, 1), (2, 2)], [(2, 3)]]
        ie meaning:
         one 'go' (first sublist) with 3 zeroes at pos 1,
         another 'go' with 1 zero at pos 1 and 2 zeroes at pos 2
         another 'go' with 2 zeroes at pos 1 and 2 zeroeat pos 2
         another 'go' (last sublist) with 3 zeroes at pos 2

  Args:
    gaphole_position_list:
    graftzeroes_combination_list:
  Returns:
  """
  traversal_grafting_pairs = []
  for slot_list in graftzeroes_combination_list:  # ex [[3, 0], [2, 1], [1, 2], [0, 3]]
    grafting_pairs = zip(gaphole_position_list, slot_list)
    grafting_pairs = list(filter(lambda coordpair: coordpair[1] != 0, grafting_pairs))
    traversal_grafting_pairs.append(grafting_pairs)
  return traversal_grafting_pairs


class ZeroesGraftAndCountsMixer:
  """
    # TO-DO: change from the HanoiLikeTowerPieceMover to the DecrescentCombinerZerografter

    This first prototype (version) of this class, used basecomb = [3, 2, 1]
      and the following traversal_combinations (from the HanoiLikeTowerMover):
        hanoicomb [3, 0]
        hanoicomb [2, 1]
        hanoicomb [1, 2]
        hanoicomb [0, 3]
    The mixing result is:
      chunks ['300021', '300201', '302001', '320001'] mask [3, None, 2, None, 1]
    ie:
      the first one has 3 zeroes at graft pos 1 (@see also property 'mask' below)
      the second has 2 zeroes at graftpos 1 and 1 at graftpos 2
    The property 'mask', the 'helper' for the mixing, is [3, None, 2, None 1]
      ie, None is a sort of placeholder for the zero-grafting: None is substituted for the zero(es).

    The Change/Update from HanoiLikeTowerPieceMover to DecrescentCombinerZerografter
    The idea is to complement the remaining result chunks like so:
      chunks ['321', '3021', '3201', ..., '300021', '300201', '302001', '320001'] mask [3, None, 2, None, 1]
    ie the result is to combine all 'shapes' (@see also metric 'shape').
  """

  def __init__(self, amounts_in_slots, n_elements=6, n_slots=6):
    """
    Consider the case where n_slots=6 and n_elements=6

    Hypothesis 1:
      basecomp = [6]  # this means all 6 elements are in one row
      result: no possible zeroes-grafting
        (because zero-grafting is always "in-between")

    Hypothesis 2:
      basecomp = [5, 1]  # this means 5 elements in one row and 1 in another
      result:
        possible zeroes-grafting combinations: [
          [501, 5001, 50001, 500001]
        ] : 4 altogether

    Hypothesis 3:
      basecomp = [4, 1, 1]  # this means 4 elements in one row, 1 in another, 1 in yet another
      result:
        possible zeroes-grafting combinations: [
          4101, 4011, 41001, 40101, 40011,
          410001, 401001, 400101, 400011,
        ] : 9 altogether

    Hypothesis 4:
      basecomp = [4, 2]  # this means 4 elements in one row, 1 in another, 1 in yet another
      result is similar to basecomp = [5, 1] ie:
        possible zeroes-grafting combinations: [
          [402, 4002, 40002, 400002]
        ] : 4 altogether

    Hypothesis 5:
      basecomp = [3, 1, 1, 1]  # this means 4 elements in one row, 1 in another, 1 in yet another
      result:
        possible zeroes-grafting combinations: [
          31101, 31011, 31101, 301101, 300111,
        ] : 5 altogether

    Hypothesis 6:
      basecomp = [3, 2, 1]  # this means 4 elements in one row, 1 in another, 1 in yet another
      result is similar to basecomp = [4, 1, 1] ie:
        possible zeroes-grafting combinations: [
          3201, 3021, 32001, 30201, 30021,
          320001, 302001, 300201, 300021,
        ] : 9 altogether

    """
    self.amounts_in_slots = amounts_in_slots
    self.n_elements = n_elements
    self.n_slots = n_slots
    self.max_zeroes_size = self.n_slots - len(amounts_in_slots)
    self._grafting_pos_n_zeroes_travlist = None  # example [[(1, 3)], [(1, 2), (2, 1)], [(1, 1), (2, 2)], [(2, 3)]]
    self._gaphole_position_list = None  # eg [1, 2]
    self._graftzeroes_combination_list = None  # eg the HanoiLike [[3, 0], [2, 1], [1, 2], [0, 3]]
    self._zerograft_strs = None


  @property
  def graftzeroes_combination_list(self):
    """
    This list is obtained by the combination of the Hanoi Like Mover class.
    """
    if self._graftzeroes_combination_list is None:
      if self.max_zeroes_size == 0 or self.n_gapholes == 0:
        self._graftzeroes_combination_list = []
        return []
      hmover = pm.HanoiLikeTowerPieceMover(npieces=self.max_zeroes_size, nslots=self.n_gapholes)
      self._graftzeroes_combination_list = hmover.allcombs
    return self._graftzeroes_combination_list

  @property
  def n_gapholes(self):
    return len(self.gaphole_position_list)

  @property
  def gaphole_position_list(self):
    """
    Gaphole is in relation to self.amounts_in_slots
    Example:
      gaphole_position_list = [1, 2] its number is 2
    Example explanation:
      suppose amounts_list = [3, 2, 1] & n_slots = 6
      Then, two gapholes may occur, they are when None appears: [3, None, 2, None, 1]
    Also, a gaphole is completely identified by its last integer, ie:
      gaphole_position_list = [1] its number is 1
      gaphole_position_list = [1, 2] its number is 2
      gaphole_position_list = [1, 2, 3] its number is 3
      and so on
    """
    if self._gaphole_position_list is None:
      self._gaphole_position_list = get_gaphole_idxpos_list_for_zerografting_with(
        self.amounts_in_slots, n_elements=self.n_elements, n_slots=self.n_slots
      )
    return self._gaphole_position_list

  @property
  def max_zeroes(self):
    return self.n_slots - len(self.amounts_in_slots)

  def get_gaphole_combinations(self):
    # gaphole_combinations = []
    if self.n_gapholes == 0:
      return []
    if self.n_gapholes == 1:
      gaphole_combinations = get_combs_with_decreasing_n_zeroes(self.amounts_in_slots, self.max_zeroes, pos=1)
      return gaphole_combinations
      # suppose [5, 1] with [1] and (n_elements=6, n_slots=6)
      # all possible zero-graftings are: ['501', '5001', '50001', '500001
    gaphole_combinations = []
    for i, gaphole_position in enumerate(self.gaphole_position_list):  # ex position list [1, 2]
      for n_zeroes in range(self.max_zeroes, 0, -1):
        gaphole_combinations += get_combs_with_decreasing_n_zeroes(
          self.amounts_in_slots, self.max_zeroes, gaphole_position
        )
      # suppose [3, 2, 1] with [1, 2] and (n_elements=6, n_slots=6)
      # all possible zero-graftings are:
      # '300021' (ie [3, 0]), '300201' (ie [2, 1]), and so on
    hmover = pm.HanoiLikeTowerPieceMover(npieces=self.max_zeroes, nslots=self.n_gapholes)
    for zeroamountlist in hmover.allcombs:
      gaphole_combinations += graft_zeroes_with_zeroamountlist_n_gapholepositionlist(
        zeroamountlist, self.gaphole_position_list
      )

    return gaphole_combinations

  @property
  def grafting_pos_n_zeroes_travlist(self):
    """
    This property is a list of all possible combinations of zero graftings
      It uses object 'hanoi_like_mover' with its list 'traversal_combinations'

    Example:
      for chunks ['300021', '300201', '302001', '320001'] & mask [3, None, 2, None, 1]
      this list is:
        hanoi_comb [3, 0]
        hanoi_comb [2, 1]
        hanoi_comb [1, 2]
        hanoi_comb [0, 3]
      ie the graft positions list, in the example above, is [[3, 0], [2, 1], [1, 2], [0, 3]]
    """
    if self._grafting_pos_n_zeroes_travlist is None:
      self._grafting_pos_n_zeroes_travlist = fuse_combination_list_w_poslist(
        gaphole_position_list=self.gaphole_position_list, graftzeroes_combination_list=self.graftzeroes_combination_list
    )
    return self._grafting_pos_n_zeroes_travlist

  @property
  def zerograft_strs(self):
    if self._zerograft_strs is None:
      self._zerograft_strs = mount_zerografted_strs_w_grafting_coordlist(
        grafting_coordlist=self.grafting_pos_n_zeroes_travlist,
        amounts_in_slots=self.amounts_in_slots, n_slots=self.n_slots
      )
    return self._zerograft_strs

  def produce_the_zerografted_strs(self):
    """
    Example:
      amounts_in_slots = [3, 2, 1]
      grafting_coordlist = [[(1, 3)], [(1, 2), (2, 1)], [(1, 1), (2, 2)], [(2, 3)]]
    Returns:

    """
    combstrs = mount_zerografted_strs_w_grafting_coordlist(
      grafting_coordlist=self.grafting_pos_n_zeroes_travlist, amounts_in_slots=self.amounts_in_slots
    )
    return combstrs

  def __str__(self):
    qtdzeroes = self.max_zeroes
    outstr = f"""ZeroesGraftAndCountsMixer n_elem={self.n_elements} | n_slots={self.n_slots} | qtdzeroes={qtdzeroes}
    amounts_in_slots={self.amounts_in_slots} | gaphole_position_list={self.gaphole_position_list}
    graftzeroes_combination_list={self.graftzeroes_combination_list}
    grafting_coordlist={self.grafting_pos_n_zeroes_travlist}
    zerograft strs={self.zerograft_strs}
"""
    return outstr


def adhoc_test():
  """
  """
  basecomb, graft_idx_positions = [3, 2, 1], [1, 3]
  zg = ZeroesGraftAndCountsMixer(amounts_in_slots=basecomb, graft_idx_positions=graft_idx_positions)
  chunks = zg.produce_the_zerografted_strs()
  print('chunks', chunks, 'mask', zg.mask)


def adhoctest2():
  basecomb = [3, 1, 1, 1]
  n_slots = 6
  zg = ZeroesGraftAndCountsMixer(amounts_in_slots=basecomb, n_slots=n_slots)
  chunks = zg.produce_the_zerografted_strs()
  print('chunks', chunks, 'mask', zg.mask)


def adhoctest3():
  n_elements, n_slots = 6, 6
  amounts_in_slots = [3, 2, 1]
  zg = ZeroesGraftAndCountsMixer(amounts_in_slots=amounts_in_slots, n_elements=6, n_slots=6)
  zg.calc_gaphole_indices()
  gaps = zg.gaphole_indices
  print('='*20, amounts_in_slots, gaps)
  amounts_in_slots = [4, 1, 1, 1]
  zg = ZeroesGraftAndCountsMixer(amounts_in_slots=amounts_in_slots, n_elements=6, n_slots=6)
  zg.calc_gaphole_indices()
  gaps = zg.gaphole_indices
  print('='*20, amounts_in_slots, gaps)
  amounts_in_slots = [3, 3]
  zg = ZeroesGraftAndCountsMixer(amounts_in_slots=amounts_in_slots, n_elements=6, n_slots=6)
  zg.calc_gaphole_indices()
  gaps = zg.gaphole_indices
  print('='*20, amounts_in_slots, gaps)
  amounts_in_slots = [6]
  zg = ZeroesGraftAndCountsMixer(amounts_in_slots=amounts_in_slots, n_elements=6, n_slots=6)
  zg.calc_gaphole_indices()
  gaps = zg.gaphole_indices
  print('='*20, amounts_in_slots, gaps)


def adhoctest4():
  """
  zg = ZeroesGraftAndCountsMixer(amounts_in_slots, n_elements, n_slots)
  ghcombs = zg.get_gaphole_combinations()
  print(ghcombs)
  """
  amounts_in_slots = [3, 2, 1]
  n_elements, n_slots = 6, 6
  zeroamount_tuplelist = [[3, 0], [2, 1], [1, 2], [0, 3]]
  gaphole_position_list = [1, 2]
  allcombs = graft_zeroes_with_zeroamountlist_n_gapholepositionlist(
    zeroamount_tuplelist, gaphole_position_list, amounts_in_slots, n_elements, n_slots
  )
  print(allcombs)


def adhoctest5():
  amounts_in_slots, n_elements, n_slots = [3, 2, 1], 6, 6
  gapholes = get_gaphole_idxpos_list_for_zerografting_with(amounts_in_slots, n_elements=n_elements, n_slots=n_slots)
  n_gapholes = len(gapholes)
  max_zeroes_size = n_slots - len(amounts_in_slots)
  graftzeroes_combination_list = get_graftzeroes_combination_list(
    max_zeroes_size=max_zeroes_size, n_gapholes=n_gapholes
  )
  grafting_coordlist = fuse_combination_list_w_poslist(
    gapholes, graftzeroes_combination_list=graftzeroes_combination_list
  )
  combstrs = mount_zerografted_strs_w_grafting_coordlist(
    grafting_coordlist, amounts_in_slots, n_slots=n_slots
  )
  scrmsg = f"{amounts_in_slots} gholes={gapholes} comblist={graftzeroes_combination_list}"
  print(scrmsg)
  scrmsg = f"ne={n_elements} ns={n_slots} coords={grafting_coordlist}"
  print(scrmsg)
  combstrs = mount_zerografted_strs_w_grafting_coordlist(grafting_coordlist, amounts_in_slots, n_slots)
  print(combstrs)
  n_elements, n_slots = 6, 6
  # amounts_in_slots = [6]
  # res = get_n_holes_for_zerografting_with(amounts_in_slots, n_elements=n_elements, n_slots=n_slots)
  # scrmg = f"n_elements={n_elements} n_slots={n_slots} res={res}"
  # print(scrmg)
  # zg = ZeroesGraftAndCountsMixer(amounts_in_slots, n_elements=n_elements, n_slots=n_slots)
  # print('zg', zg)
  print('='*30)
  gaphole_position_list = [1, 2]
  graftzeroes_combination_list = [[3, 0], [2, 1], [1, 2], [0, 3]]
  res = fuse_combination_list_w_poslist(gaphole_position_list, graftzeroes_combination_list)
  print(res)
  fused = fuse_combination_list_w_poslist(
    gaphole_position_list=gaphole_position_list, graftzeroes_combination_list=graftzeroes_combination_list
  )
  print('fused', fused)


def adhoctest6():
  amounts_in_slots = [3, 2, 1]
  n_elements, n_slots = 6, 6
  zg = ZeroesGraftAndCountsMixer(amounts_in_slots=amounts_in_slots, n_elements=n_elements, n_slots=n_slots)
  print(zg)


if __name__ == '__main__':
  """
  list_dist_xysum_metric_thru_ms_history()
  """
  adhoctest6()
  adhoctest5()
