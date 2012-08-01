#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
TilPattern.py
'''
# import numpy, time, sys
import sys

class TilFilter(object):
  '''

    Eg.  1
    
      
  '''

  def __init__(self, jogos):
    self.tilqueue = []
    self.jogos = jogos

  def add_tilpattern(self, tilpattern):
    self.tilqueue.append(tilpattern)

  def add_tilpatterns(self, tilpatterns):
    self.tilqueue += tilpatterns

  def pipeline(self):
    for jogo in self.jogos:
      for tilpattern in self.tilqueue:
        if self.jogo.til(tilpattern.tilnumber, tillpattern.soma) in 
    
  def __str__(self):
    return "'<TilPattern(%d,%d,'%s')>" %(self.tilnumber, self.freqsoma, self.tilpattern)


def adhoc_test():
  print 'adhoc_test()'
  tilpattern = TilPattern(5, 6)
  tilpattern.set_tilpattern('02220')
  print 'tilpattern', tilpattern
  tilpattern2 = TilPattern('a', 6)
  tilpattern2.set_tilpattern('02320')
  print 'tilpattern', tilpattern

if __name__ == '__main__':
  adhoc_test()