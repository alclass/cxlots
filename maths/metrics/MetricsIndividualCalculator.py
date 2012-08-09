#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
  This module contains 'business' classes: Jogos and Til
'''
import sys

import localpythonpath
localpythonpath.setlocalpythonpath()

import funcsForMetrics as ffMetrics
from models.Jogo import JogoSlider

somaNList = [1, 3, 7, 15]

def calc_iguaisComOAnterior(jogo):
  '''
  jogo must implement get_dezenas()
  '''
  jogo_anterior = jogo.get_previous()
  if jogo_anterior == None:
    return 0
  return ffMetrics.getNOfCoincidences(jogo_anterior, jogo)
  
def calc_coincsComNAnteriores(jogo, nDeAnteriores):
  '''
  jogo must implement get_dezenas()
  coincsComNAnteriores() call nDeAnteriores times iguaisComOAnterior 
  '''
  nDeCoincsComAnteriores = 0
  for backward_i in range(nDeAnteriores):
    nDeCoincsComAnteriores += calc_iguaisComOAnterior(jogo)
    jogo = jogo.get_previous()
    if jogo == None:
      break
      backward_i # does nothing here, just for "Eclipse"
  return nDeCoincsComAnteriores 

def calc_coincsComOs3Anteriores(jogo):
  return calc_coincsComNAnteriores(jogo, 3)

def calc_maxDeIguais(jogo):
  maxDeIguais = 0; distAo1o = 0; maxDeIguaisOcorrencia = 1; iguaisMediaComPassado = 0.0
  for nDoConc_to_compare in range(jogo.nDoConc - 1, 0, -1):
    jogo_to_compare = jogo.get_jogo_by_nDoConc(nDoConc_to_compare)
    nDeCoincsComAnteriores = ffMetrics.getNOfCoincidences(jogo, jogo_to_compare)
    iguaisMediaComPassado += nDeCoincsComAnteriores 
    if nDeCoincsComAnteriores > maxDeIguais:
      maxDeIguais = nDeCoincsComAnteriores
      distAo1o = jogo.nDoConc - nDoConc_to_compare
      maxDeIguaisOcorrencia = 1      
    elif nDeCoincsComAnteriores == maxDeIguais:
      maxDeIguaisOcorrencia += 1
  if jogo.nDoConc > 1:            
    iguaisMediaComPassado = iguaisMediaComPassado / (jogo.nDoConc - 1.0)
  return maxDeIguais, distAo1o, maxDeIguaisOcorrencia, iguaisMediaComPassado  

f_remainder_pattern = lambda x, modulo : x % modulo
def calc_remainder_pattern(jogo, modulo):
  print 'modulo', modulo
  modulo_repeated_for_map_function = [modulo]*len(jogo.get_dezenas())
  remainderpatternlist = map(f_remainder_pattern, jogo.get_dezenas(), modulo_repeated_for_map_function)
  remainderpatternstr = ''.join(remainderpatternlist)
  return remainderpatternstr 
    
def calc_rem2pattern(jogo):    
  return calc_remainder_pattern(jogo, 2)

def calc_rem3pattern(jogo):    
  return calc_remainder_pattern(jogo, 3)

def calc_rem5pattern(jogo):    
  return calc_remainder_pattern(jogo, 5)

def calc_rem6pattern(jogo):    
  return calc_remainder_pattern(jogo, 6)


def adhoc_test():
  print 'f_remainder_pattern(4,2)', f_remainder_pattern(4,2)
  jogo = JogoSlider().get_last_jogo()
  n_iguaisComOAnterior     = calc_iguaisComOAnterior(jogo)
  print 'n_iguaisComOAnterior', n_iguaisComOAnterior
  print jogo
  print jogo.get_previous()

  n_coincsComOs3Anteriores = calc_coincsComOs3Anteriores(jogo)
  print 'n_coincsComOs3Anteriores', n_coincsComOs3Anteriores

  n_coincsComNAnteriores   =   calc_coincsComNAnteriores(jogo, nDeAnteriores=7)
  print 'n_coincsCom 7 Anteriores', n_coincsComNAnteriores

#  n_maxDeIguais, distAo1o, maxDeIguaisOcorrencia, iguaisMediaComPassado = calc_maxDeIguais(jogo)
#  print 'n_maxDeIguais, distAo1o, maxDeIguaisOcorrencia', n_maxDeIguais, distAo1o, maxDeIguaisOcorrencia, iguaisMediaComPassado
#  print jogo
#  print jogo.get_jogo_by_nDoConc(jogo.nDoConc - distAo1o)
    
  pattern = calc_rem2pattern(jogo)    
  print 'calc_rem2pattern(jogo)', pattern
  pattern = calc_rem3pattern(jogo)    
  print 'calc_rem3pattern(jogo)', pattern
  pattern = calc_rem5pattern(jogo)    
  print 'calc_rem5pattern(jogo)', pattern
  pattern = calc_rem6pattern(jogo)    
  print 'calc_rem6pattern(jogo)', pattern


def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()

if __name__ == '__main__':
  look_for_adhoctest_arg()
