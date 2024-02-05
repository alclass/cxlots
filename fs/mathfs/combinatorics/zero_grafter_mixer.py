#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/zero_grafter_mixer.py
  Contains class ZeroesGraftAndCountsMixer.

The class ZeroesGraftAndCountsMixer may be explained by an example:

The example and cases given below are for n_slots=6.
The MS (Megasena) case, as an example, also uses n_slots=10.
  ie, n_slots=6 for rows and n_slots=10 for columns.

Suppose basecomb is [3, 2, 1] and 'mask' is [3, None, 2, None 1]
  where None is a kind of placeholder for the later zero-grafting.
Now, suppose the zeroes-amount is represented by [2, 1]
Processing:
  This means 2 zeroes being grafted into the first None in the mask and 1 zero to the second.
  The result in this case is [3, 0, 0, 2, 0, 1]
    Notice the substitution of None for the zeroes (2 zeroes for the 1st None, 1 zero for the 2nd None).

The example above is for one single combination.
  The [3, 2, 1] set may be expanded into other combinations when n_slots is 6.
    The other "graftings": [
      '300021', '300201' (this is the one above),
      '302001', '320001',
    ]
    The first above ['300021'] has zeroes_amount [3, 0]
    The second one is the example above [2, 1]
    The third above ['302001'] has zeroes_amount [1, 2]
    The fourth above ['320001'] has zeroes_amount [0, 3]

  Notice that the zeroes-amount combinations are: [3, 0], [2, 1], [1, 2], [0, 3]

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
import copy
import fs.mathfs.combinatorics.hanoi_like_tower_piecemover as pm  # pm.HanoiLikeTowerPieceMover


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

  def __init__(self, basecomb, graft_idx_positions, n_slots=6):
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

    Args:
      basecomb:
      graft_idx_positions:
      n_slots:
    """
    self.basecomb, self.graft_idx_positions = basecomb, graft_idx_positions
    self.nslots = n_slots
    self._mask = None
    self.max_zeroes_size = self.nslots - len(basecomb)
    self.graft_slots_size = len(graft_idx_positions)
    # TO-DO: change from the HanoiLikeTowerPieceMover to the DecrescentCombinerZerografter
    self.hanoi_like_mover = pm.HanoiLikeTowerPieceMover(npieces=self.max_zeroes_size, nslots=self.graft_slots_size)
    self.hanoi_like_mover.process()
    self.countdict = {}
    self.gap_ranges_tuplelist = []
    self.grafted_combs = []

  @property
  def mask(self):
    if self._mask is None:
      basecomb = copy.copy(self.basecomb)
      self._mask = []
      if len(basecomb) > 0:
        elem = basecomb[0]
        del basecomb[0]
        self._mask.append(elem)
      for i in range(1, self.nslots):
        if i in self.graft_idx_positions:
          self._mask.append(None)
          continue
        if len(basecomb) > 0:
          elem = basecomb[0]
          del basecomb[0]
          self._mask.append(elem)
        else:
          break
    return self._mask

  @property
  def graft_size_cmbs(self):
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
    return self.hanoi_like_mover.traversal_combinations

  def mix(self):
    chunks = []
    for hanoi_comb in self.graft_size_cmbs:
      # print('hanoicomb', hanoi_comb)
      hanoi_reversed_for_pop = list(reversed(hanoi_comb))
      outstr = ''
      for elem in self.mask:
        if elem is None:
          if len(hanoi_reversed_for_pop) == 0:
            break
          n_zeroes = hanoi_reversed_for_pop.pop()
          if n_zeroes == 0:
            continue
          zeroes_str = '0' * n_zeroes
          outstr += zeroes_str
          continue
        outstr += str(elem)
      chunks.append(outstr)
    return chunks

  def determine_graft_ranges(self, countdict):
    self.countdict = countdict
    indices = self.countdict.keys()
    sorted(indices)
    prev_idx = -1
    self.gap_ranges_tuplelist = []
    while len(indices) > 0:
      idx = indices.pop()
      if prev_idx < 0:
        prev_idx = idx
        continue
      if idx - prev_idx > 1:
        trange = (prev_idx+1, idx-1)
        self.gap_ranges_tuplelist.append(trange)

  def graft_zeroes(self):
    self.grafted_combs = []
    indices = self.countdict.keys()
    sorted(indices)
    # countlist = [self.countdict[i] for i in indices]
    out_str_combs = []
    for comb in self.hanoi_like_mover.allcombs:
      # patt = ''.join(comb)
      for i, nzeroes in enumerate(comb):
        zeroes_str = '0' * nzeroes
        # trange = self.gap_ranges_tuplelist[i]
        out_str_combs.append(zeroes_str)


def adhoc_test():
  """
  """
  basecomb, graft_idx_positions = [3, 2, 1], [1, 3]
  zg = ZeroesGraftAndCountsMixer(basecomb=basecomb, graft_idx_positions=graft_idx_positions)
  chunks = zg.mix()
  print('chunks', chunks, 'mask', zg.mask)


def adhoc_test2():
  basecomb = [3, 1, 1, 1]
  graft_idx_positions = [1, 2, 3, 4]
  zg = ZeroesGraftAndCountsMixer(basecomb=basecomb, graft_idx_positions=graft_idx_positions)
  chunks = zg.mix()
  print('chunks', chunks, 'mask', zg.mask)


if __name__ == '__main__':
  """
  list_dist_xysum_metric_thru_ms_history()
  """
  adhoc_test2()
