#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import time # os, random, sys
from paidGamesInput import *

def get_jogos_from_file():
  lines = open('Sat Dec 29 21:56:32 2012.log').readlines()
  lineToDezenasObj = LineToDezenas()
  jogos_tuple = []
  for line in lines:
    if line.endswith('\n'):
      line = line.rstrip('\n')
    dezenas = lineToDezenasObj.get_dezenas_from_line(line)
    jogos_tuple.append(dezenas)
  return jogos_tuple

class Conferidor(object):

  def __init__(self):
    self.lineToDezenasObj = LineToDezenas()

  def confere(self):
    line = raw_input('Type Result to check against d1 d2 d3 d4 d5 d6 ==>> ')
    self.dezenas = self.lineToDezenasObj.get_dezenas_from_line(line,  sortThem=True)
    jogos_tuple = get_jogos_from_file()
    n_jogos = 0
    for jogo_tuple in jogos_tuple:
      n_acertos = 0
      for dezena in self.dezenas:
        if dezena in jogo_tuple:
          n_acertos += 1
      n_jogos += 1
      print n_jogos, '==>>', n_acertos, 'ACERTOS', self.dezenas, jogo_tuple
      if n_acertos == 4:
        print ' * QUADRA * '
      elif n_acertos == 5:
        print ' ** QUINA ** '
      elif n_acertos == 6:
        print ' *** SENA *** '
        
def process():
  conferidor = Conferidor()
  conferidor.confere()

if __name__ == '__main__':
  process()
