#!/usr/bin/env python3
# import time # os, random, sys
import os.path

from paidGamesInput import *


def get_jogos_from_file(filepath=None):
  if filepath is None or not os.path.isfile(filepath):
    errmsg = f'file [{filepath}] does not exist.'
    raise OSError(errmsg)
  lines = open(filepath).readlines()
  line_to_dezenas_obj = LineToDezenas()
  jogos_tuple = []
  for line in lines:
    if line.endswith('\n'):
      line = line.rstrip('\n')
    dezenas = line_to_dezenas_obj.get_dezenas_from_line(line)
    jogos_tuple.append(dezenas)
  return jogos_tuple


class Conferidor(object):

  def __init__(self):
    self.lineToDezenasObj = LineToDezenas()
    self.dezenas = []

  def confere(self):
    line = input('Type Result to check against d1 d2 d3 d4 d5 d6 ==>> ')
    self.dezenas = self.lineToDezenasObj.get_dezenas_from_line(line, sort_them=True)
    jogos_tuple = get_jogos_from_file()
    n_jogos = 0
    for jogo_tuple in jogos_tuple:
      n_acertos = 0
      for dezena in self.dezenas:
        if dezena in jogo_tuple:
          n_acertos += 1
      n_jogos += 1
      scrmsg = f'n_jogos {n_acertos} ACERTOS {self.dezenas} {jogo_tuple}'
      print(scrmsg)
      if n_acertos == 4:
        print(' * QUADRA * ')
      elif n_acertos == 5:
        print(' ** QUINA ** ')
      elif n_acertos == 6:
        print(' *** SENA *** ')
        

def process():
  conferidor = Conferidor()
  conferidor.confere()


if __name__ == '__main__':
  process()
