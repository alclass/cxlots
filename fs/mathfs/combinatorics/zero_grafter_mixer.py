#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/zero_grafter_mixer.py
  Contains class ZeroesGraftAndCountsMixer.

The class ZeroesGraftAndCountsMixer may be explained by an example:

Suppose basecomb is [3, 2, 1]
  and 'mask' is [3, None, 2, None 1]
  where None is a kind of placeholder for the later zero-grafting.
Now, suppose the zeroes-amount is represented by [2, 1]
Processing:
  This means 2 zeroes being grafted to the first None in the mask and 1 zero to the second.
  The result in this case is [3, 0, 0, 2, 0, 1]
    Notice the substitution of None for the zeroes (2 zeroes for the 1st None, 1 zero for the 2nd None).

The example above is for one single combination.
  The [3, 2, 1] set may be expanded into many more combinations.
  More examples: ['300021', '300201' (this is the one above), '302001', '320001', ...]
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

  def __init__(self, basecomb, graft_idx_positions, nslots=6):
    self.basecomb, self.graft_idx_positions = basecomb, graft_idx_positions
    self.nslots = nslots
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

  def mix(self):
    chunks = []
    for hanoi_comb in self.hanoi_like_mover.traversal_combinations:
      print('hanoicomb', hanoi_comb)
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


if __name__ == '__main__':
  """
  list_dist_xysum_metric_thru_ms_history()
  """
  adhoc_test()
