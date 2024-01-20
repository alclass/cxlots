#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
TilPattern.py
'''
# import numpy, time, sys
import sys

from Til import TilR

class TilFilter(object):
  '''
    This class implements a filtering-in set operation, ie, jogosfs with a certain patterns will be filtered in
      those not having those patterns will be filtered out.

    Eg.  Suppose the following til_r queue
      TilR(5,6) with '00321'
      TilR(5,6) with '02121'
      TilR(5,6) with '01122'

    Only jogosfs with those slots_values will be filtered in.

    Remind also that the til_r(n_slots, n_elements) can be computed from the jogo instance against database.
  '''

  def __init__(self, jogos):
    self.til_r_queue = []
    self.jogos = jogos
    self.jogos_filtered_in = []

  def add_til_r(self, til_r):
    self.til_r_queue.append(til_r)

  def pipeline(self):
    for jogo in self.jogos:
      for til_r in self.til_r_queue:
        jogo_til_r = jogo.get_til_r(til_r.n_slots, til_r.n_elements)
        if jogo_til_r.slots_values == til_r.slots_values:
          self.jogos_filtered_in.append(jogo)
    
  def __str__(self):
    outstr = ''
    for til_r in self.til_r_queue:
      outstr += "<TilR(%d,%d)='%s')>\n" %(self.n_slots, self.n_elements, self.slots_values)
    return outstr

def get_sample_jogos():
  jogo = Jogo()


def adhoc_test():
  jogos = get_sample_jogos()
  tilfilter = TilFilter(jogos)
  print 'list_dist_xysum_metric_thry_ms_history()'
  #1
  til_r = TilR(5, 6)
  til_r.set_slots_values('02220')
  tilfilter.add_til_r(til_r)
  #2
  til_r = TilR(5, 6)
  til_r.set_slots_values('01320')
  tilfilter.add_til_r(til_r)
  #3
  til_r = TilR(5, 6)
  til_r.set_slots_values('01311')
  tilfilter.add_til_r(til_r)


if __name__ == '__main__':
  adhoc_test()