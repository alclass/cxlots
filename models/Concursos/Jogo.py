#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 04/12/2011

@author: friend
'''

class Jogo(object):

  def __init__(self, dezenas):
    self.dezenas = dezenas

  def dezena(self, index):
    return self.dezenas[index]

  def as_tuple(self):
    return tuple(self.dezenas)

  def as_list(self):
    return list(self.dezenas)

  def set_til_r(self, til_r):
    self.til_r = til_r
    self.til_r.calculate_slot_values(self.dezenas)

if __name__ == '__main__':
  pass
