#!/usr/bin/env python3
"""
fs/mathfs/metrics/graphshape_metric.py

@See also description below for a historical vision of this metric.

  At this version, this metric has become somewhat simplified.
The metric is a 2-D integer tuple that represents the sum of distances in x's and y's.

Let us see an example: suppose dozens = (4, 12, 23, 33, 45, 51)
The corresponding (col=x, row=y) points are: ((4, 1), (2,2), (3,3), (3, 4), (5,5), (1, 6))
  There will be a point P with a minimal x integer and also a minimum y integer.
    The x part of the metric is the sum of all x-distances to this minimum x.
    The y part of the metric is the sum of all y-distances to this minimum x.
The calculation is the following:
In the cardgame above:
  Point (1, 6) [dozen 51] contains the minimum x, which is 1, ie x=1
  Point (4, 1) [dozen 4] contains the minimum y, which is 1, ie y=1

The x-distances are: (4-1, 2-1, 3-1, 3-1. 5-1, 1-1)
  ie (3, 1, 2, 2, 4, 0) and its sum 12
The y-distances are: (1-1, 2-1, 3-1, 4-1, 5-1, 6-1)
  ie (0, 1, 2, 3, 4, 5) and its sum 15
The result is (12, 15)

==============================
@see also fs/mathfs/metrics/museum/former_graphshape_metric.py
  for a description of the metric's former version.
"""
import math


def from_arr_to_lgi(arr=None, base=10):
  """
  Though y (rows) needs only 6 digits, the inverse operation, afterwards,
   would not know which divider comes first
   (whether it's a 10**pos as a divider or a 6**pos, where pos is the exponent-position)

  So instead of S = dx1*10**0 + dy1*6**1 + dx2*10**2 + dy2*6**3 + ...
  It's the simpler 10-based number system:
    S = dx1*10**0 + dy1*10**1 + dx2*10**2 + dy2*10**3 + ...

  In the inverse function, log10(value) is used to determine the
    first exponent for the divider.

  """
  arr = [1, 2, 3, 1, 2, 4] if arr is None else arr
  # reverse is necessary because the exponents below are in ascending order
  arr = reversed(arr)
  soma = 0
  for i, n in enumerate(arr):
    soma += n * base ** i
  return soma


def from_lgi_to_arr(total_or_remainder=None, arr=None, expo=None, base=10):
  """
  if expo % 2 == 0:
    base = 10
  else:
    base = 6
  """
  # expo begins with arrsize is = 6
  if expo is None:
    # finding the first exponent, the subsequent ones
    # go recursively decremented via its parameter
    expo = math.floor(math.log10(total_or_remainder))
  arr = [] if arr is None else arr
  divider = base ** expo
  if divider == 1:
    arr.append(total_or_remainder)
    return arr
  backdigit = total_or_remainder // divider
  remainder = total_or_remainder % divider
  arr.append(backdigit)
  return from_lgi_to_arr(remainder, arr=arr, expo=expo-1)


def extract_x_y_from_dozen_intval(intval):
  dozendigit = math.floor((intval-1)/10) + 1
  colweight = intval % 10
  colweight = colweight if colweight > 0 else 10
  x, y = colweight, dozendigit
  return x, y


def calc_dist_as_dxdysum_dx_dy_to_refpoint(point, refpoint):
  x, y = point[0], point[1]
  rx, ry = refpoint[0], refpoint[1]
  dx = x - rx
  dy = y - ry
  dist_sum = dx + dy
  return dist_sum, dx, dy


def trans_dozens_to_upper_leftward_points2(dozens):
  xs_n_ys = list(map(lambda e: extract_x_y_from_dozen_intval(e), dozens))
  print(xs_n_ys)
  return xs_n_ys


def trans_dozens_to_points(dozens):
  xs_n_ys = list(map(lambda e: extract_x_y_from_dozen_intval(e), dozens))
  print(xs_n_ys)
  return xs_n_ys


def reduce_dozens_upper_leftward(dozens):
  one_one = (1, 1)
  for intval in dozens:
    x, y = extract_x_y_from_dozen_intval(intval)
    res = calc_dist_as_dxdysum_dx_dy_to_refpoint((x, y), one_one)
    print(intval, one_one, 'res', res)


def trans_dozens_to_upper_leftward_points(dozens):
  xs_n_ys = trans_dozens_to_points(dozens)
  ref_firstpoint = xs_n_ys[0]
  for point in xs_n_ys[1:]:
    triple = calc_dist_as_dxdysum_dx_dy_to_refpoint(point, ref_firstpoint)
    print('triple', triple, 'from', point, ref_firstpoint)
  xs = list(map(lambda e: e[0], xs_n_ys))
  ys = list(map(lambda e: e[1], xs_n_ys))
  max_x = min(xs)
  max_y = min(ys)
  # decide deltax and deltay

  print('min x min y', max_x, max_y)
  return xs, ys


def calc_graphshape_metric_w_cardgame(dozens):
  """

  The explanation of the graphshape metric may be seen by an example:

  Suppose dozens = (4, 12, 23, 33, 45, 51)
  Their corresponding points are: ((4, 1), (2,2), (3,3), (3, 4), (5,5), (1, 6))
    There will be an x-point with a minimal integer and also a minimum y-point.
      The x part of the metric is the sum of all x-distances to this minimum x.
      The y part of the metric is the sum of all y-distances to this minimum x.
  The calculation is the following:
  Point (1, 6) [dozen 51] contains the minimum x, ie x=1
  Point (4, 1) [dozen 4] contains the minimum y, ie y=1
    The x-distances are: (4-1, 2-1, 3-1, 3-1. 5-1, 1-1)
      ie (3, 1, 2, 2, 4, 0) and its sum 12
    The y-distances are: (1-1, 2-1, 3-1, 4-1, 5-1, 6-1)
      ie (0, 1, 2, 3, 4, 5) and its sum 15
  The result is then (12, 15) ie the x-distances sum and the y-distances sum
  """
  points = trans_dozens_to_points(dozens)
  xs = list(map(lambda e: e[0], points))
  ys = list(map(lambda e: e[1], points))
  min_x = min(xs)
  min_y = min(ys)
  xdistances = [x - min_x for x in xs]
  ydistances = [y - min_y for y in ys]
  metric_tuple = sum(xdistances), sum(ydistances)
  return metric_tuple


class GraphShapeFinder:

  def __init__(self, ord_sor_dozens):
    self.ord_sor_dozens = ord_sor_dozens
    self._asc_ord_dozens = None

  @property
  def asc_ord_dozens(self):
    if self._asc_ord_dozens is None:
      self._asc_ord_dozens = sorted(self.ord_sor_dozens)
    return self._asc_ord_dozens

  def process(self):
    pass

def adhoc_test():
  """
  """
  dozens = (1, 4, 12, 23, 45, 51)
  rx, ry = extract_x_y_from_dozen_intval(dozens[0])
  for dozen in dozens[1:]:
    x, y = extract_x_y_from_dozen_intval(dozen)
    point = x, y
    refpoint = rx, ry
    dist_sum, dx, dy = calc_dist_as_dxdysum_dx_dy_to_refpoint(point, refpoint)
    print('ref', dozens[0], dozen, 'distsum', dist_sum, 'dx', dx, 'dy', dy)
  xs, ys = trans_dozens_to_upper_leftward_points(dozens)
  print(dozens, xs, ys)
  dozens = sorted((10, 38, 11, 23, 45, 52))
  xs, ys = trans_dozens_to_upper_leftward_points(dozens)
  print(dozens, xs, ys)
  points = trans_dozens_to_points(dozens)
  print('dozens', dozens, 'points', points)
  dozens = (11, 38, 10, 23, 45, 52)
  xs, ys = trans_dozens_to_upper_leftward_points(dozens)
  print(dozens, xs, ys)
  points = trans_dozens_to_points(dozens)
  print('dozens', dozens, 'points', points)
  reduce_dozens_upper_leftward(dozens)
  metric_tuple = calc_graphshape_metric_w_cardgame(dozens)
  print('metric_tuple', metric_tuple)
  dozens = (4, 12, 23, 33, 45, 51)
  metric_tuple = calc_graphshape_metric_w_cardgame(dozens)
  print('metric_tuple', metric_tuple)

def adhoc_test2():
  # arr = [1, 2, 3, 1, 2, 4]
  arr = [2, 1]
  soma = from_arr_to_lgi(arr)
  print(arr, soma)
  arr = from_lgi_to_arr(total_or_remainder=soma, arr=None)
  print('back', soma, arr)
  arr = [2, 5, 3]
  soma = from_arr_to_lgi(arr)
  print(arr, soma)
  arr = from_lgi_to_arr(total_or_remainder=soma, arr=None)
  print('back', soma, arr)


if __name__ == '__main__':
  """
  list_dist_xysum_metric_thru_ms_history()
  """
  adhoc_test2()
  adhoc_test()
