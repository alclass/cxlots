#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import sys

import localpythonpath
localpythonpath.setlocalpythonpath()
from GeradorIter import Gerador 
from lib.jogos_functions import has_game_equal_or_more_than_n_acertos
from models.ReadConcursosHistory import read_concursos_history


def filtra_dentro_jogos_com_menos_que_3_iguais():
  jogos_history = read_concursos_history()
  gerador = Gerador()   # print len(gerador)
  for jogo_as_dezenas in gerador:
    index = gerador.iterator.at_index
    if has_game_equal_or_more_than_n_acertos(jogo_as_dezenas, jogos_history, cant_have_n_acertos = 4):
      # print '[OUT]', index, gerador.iterator #convert_intlist_to_spaced_zfillstr(jogo_as_dezenas)
      continue
    print gerador.iterator
    
def process():
  filtra_dentro_jogos_com_menos_que_3_iguais()

if __name__ == '__main__':
  process()
