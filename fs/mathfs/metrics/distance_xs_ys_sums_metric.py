#!/usr/bin/env python3
"""
fs/mathfs/metrics/distance_xs_ys_sums_metric.py
  Contains functions and class for calculating the xs ys distance sum metric for an arbitrary cardgame.

Also, it contains a function for listing this metric for the whole MS history.

(At this version, this metric becomes somewhat simplified. @See former graph_shape_metric at the 'museum' subpackage.)

The metric is a 2-D integer tuple that represents the sum of distances in x's and y's.

Let us see an example: suppose dozens = (4, 12, 23, 33, 45, 51)
The corresponding points are: ((4, 1), (2,2), (3,3), (3, 4), (5,5), (1, 6))
  There will be an x-point with a minimal integer and also, perhaps a different one, with a minimum y-point.
    The x part of the metric is the sum of all x-distances to this minimum x.
    The y part of the metric is the sum of all y-distances to this minimum y.

The calculation is the following:
    Using the points above:
  Point (1, 6) [dozen 51] contains the minimum x, ie x=1
  Point (4, 1) [dozen 4] contains the minimum y, ie y=1
    The x-distances are: (4-1=3, 2-1=1, 3-1=2, 3-1=2. 5-1=4, 1-1=0)
    ie (3, 1, 2, 2, 4, 0) and its sum is 12
    The y-distances are: (1-1=0, 2-1=1, 3-1=2, 4-1=3, 5-1=4, 6-1=5)
    ie (0, 1, 2, 3, 4, 5) and its sum is 15
  The result is (12, 15)

Examples from running the class:
  MetricDistanceXsYsSummer cardgame=[4, 12, 23, 33, 45, 51] sum_x_y=(12, 15)
  MetricDistanceXsYsSummer cardgame=[10, 11, 23, 38, 45, 52] sum_x_y=(23, 15)

As of 2024-01-19, a histogram fragment follows:
histogram_x {
  4: 1, 41: 1, 43: 1, 40: 1, 3: 1, 42: 2, 39: 2, 5: 2, 38: 3, 37: 4, 6: 6, 36: 7, 7: 8, 8: 9,
  35: 18, 9: 21, 34: 25, 33: 34, 10: 36, 32: 49, 11: 50, 31: 54, 12: 55, 30: 55, 13: 72, 14: 80, 29: 83, 27: 103,
  15: 103, 28: 117, 26: 125, 17: 139, 25: 140, 16: 144, 18: 149, 19: 150, 22: 154, 23: 160, 20: 166, 21: 167, 24: 177
}
histogram_y {
  24: 2, 2: 2, 1: 2, 23: 4, 22: 5, 3: 5, 4: 24, 21: 29, 5: 34, 20: 48, 6: 65, 19: 66, 7: 88, 18: 114, 8: 132,
   17: 144, 9: 188, 10: 197, 16: 221, 15: 234, 14: 238, 12: 260, 11: 278, 13: 294
}
max sum xs (9*5=45) 45 sum max ys (5*5=25) 25
min for both x & y is 0 (zero)
"""
import math
import commands.show.list_ms_history as lh  # lh.get_ms_asc_history_as_list


def extract_x_y_from_dozen_intval(intval):
  dozendigit = math.floor((intval-1)/10) + 1
  colweight = intval % 10
  colweight = colweight if colweight > 0 else 10
  x, y = colweight, dozendigit
  return x, y


def trans_dozens_to_points(dozens):
  xs_n_ys = list(map(lambda e: extract_x_y_from_dozen_intval(e), dozens))
  return xs_n_ys


def calc_dist_as_dxdysum_dx_dy_to_refpoint(point, refpoint):
  x, y = point[0], point[1]
  rx, ry = refpoint[0], refpoint[1]
  dx = x - rx
  dy = y - ry
  dist_sum = dx + dy
  return dist_sum, dx, dy


def calc_distance_xs_ys_sums_metric_f_cardgame(dozens):
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
  min_x, min_y = min(xs), min(ys)
  xdistances = [x - min_x for x in xs]
  ydistances = [y - min_y for y in ys]
  dist_sum_xs_ys_tuple = sum(xdistances), sum(ydistances)
  return dist_sum_xs_ys_tuple


class MetricDistanceXsYsSummer:

  def __init__(self, dozens):
    self.ord_dozens = sorted(dozens)
    self.distsum_xs_ys_tuple = None
    self.process()

  def process(self):
    self.distsum_xs_ys_tuple = calc_distance_xs_ys_sums_metric_f_cardgame(self.ord_dozens)

  def __str__(self):
    outstr = f"MetricDistanceXsYsSummer cardgame={self.ord_dozens} sum_x_y={self.distsum_xs_ys_tuple}"
    return outstr


def update_histograms(distsum_xs_ys, histogram_x, histogram_y):
  xs_sum = distsum_xs_ys[0]
  ys_sum = distsum_xs_ys[1]
  if xs_sum in histogram_x:
    histogram_x[xs_sum] += 1
  else:
    histogram_x[xs_sum] = 1
  if ys_sum in histogram_y:
    histogram_y[ys_sum] += 1
  else:
    histogram_y[ys_sum] = 1


def list_dist_xysum_metric_thru_ms_history():
  # t1
  dozens = (4, 12, 23, 33, 45, 51)
  summer = MetricDistanceXsYsSummer(dozens)
  print(summer)
  # t2
  dozens = (10, 38, 11, 23, 45, 52)
  summer = MetricDistanceXsYsSummer(dozens)
  print(summer)
  ms_asc_history_list = lh.get_ms_asc_history_as_list()
  histogram_x, histogram_y = {}, {}
  for i, dozens in enumerate(ms_asc_history_list):
    nconc = i + 1
    summer = MetricDistanceXsYsSummer(dozens)
    distsum_xs_ys = summer.distsum_xs_ys_tuple
    update_histograms(distsum_xs_ys, histogram_x, histogram_y)
    scrmsg = f"nconc={nconc} | dist_xs_ys={distsum_xs_ys} | {dozens}"
    print(scrmsg)
  histogram_x = dict(sorted(histogram_x.items(), key=lambda e: e[1]))
  histogram_y = dict(sorted(histogram_y.items(), key=lambda e: e[1]))
  print('histogram_x', histogram_x)
  print('histogram_y', histogram_y)
  print('max sum xs (9*5=45)', 9*5, 'sum max ys (5*5=25)', 5*5)


def adhoc_test2():
  """
  """
  dozens = (1, 4, 12, 23, 45, 51)
  rx, ry = extract_x_y_from_dozen_intval(dozens[0])
  for dozen in dozens[1:]:
    x, y = extract_x_y_from_dozen_intval(dozen)
    point = x, y
    refpoint = rx, ry
    dist_sum, dx, dy = calc_dist_as_dxdysum_dx_dy_to_refpoint(point, refpoint)
    print('ref dz', dozens[0], 'dz', dozen, 'distsum', dist_sum, 'dx', dx, 'dy', dy)
  dozens = sorted((10, 38, 11, 23, 45, 52))
  metric_tuple = calc_distance_xs_ys_sums_metric_f_cardgame(dozens)
  print(dozens, 'metric_tuple', metric_tuple)


def adhoc_test():
  pass


if __name__ == '__main__':
  """
  adhoc_test()
  """
  list_dist_xysum_metric_thru_ms_history()
