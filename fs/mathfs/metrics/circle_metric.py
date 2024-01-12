#!/usr/bin/env python3
"""
fs/mathfs/metrics/circle_metric.py
  Implements the abstract circle metric

1) nconsecutives => when draw dozens are consecutive (eg (1, 2): 2 is consecutive of 1 and viceversa, also (1, 60) is also consecutive as modulo 60)

2) n_immed_repeat => when a dozen draw also happened in the previous conc

3) repeat_depth_commasep => the number of concs down history until a dozen happened (this method is related to histogram, though not it)

4) immg_rad_n_cnt_commasep
 => an immaginary circle is abstracted here, the 2D-tuple is composed of the circle's radius and center rounded-off integers; the radius is multiplied by 100 before being rounded-off to integer
Example: (200, 23) 200 is the radius and 23 is the dozen that centers it
the algorithm centers rows and then columns finding the integer middle; the radius is the avg of the squared x, y distances of each dozen to its integer middle, where x is row and y is column

Updates:

1) resto6 & resto10 is derived from rowpatt and colpatt, rethink them (maybe change them to resto5 & resto12)

2) histogram_json should become histogram_commasep_str

"""

class Jogo:

  def __init__(self, points):
    self.points = points
    self.calculate_center_n_radius()
    self._mid_x = (10 + 1) / 2
    self._mid_y = (6 + 1) / 2

  @property
  def card_mid_x(self):
    return self._mid_x

  @property
  def card_mid_y(self):
    return self._mid_y

  @property
  def mid_x(self):
    return self._mid_x

  @property
  def mid_y(self):
    return self._mid_y

  def calculate_center_n_radius(self):




def adhoctest():
  pass


def process():
  pass


if __name__ == '__main__':
  adhoctest()
  process()
