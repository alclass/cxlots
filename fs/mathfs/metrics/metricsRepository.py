#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import sys
import unittest
'''
Created on 15/11/2011
@author: friend


'''
def cleanUpRepeatsAndPutInOrder(numbers):
  if type(numbers) not in [list, tuple]:
    raise TypeError, 'numbers must be a list or tuple as passed-in parameters to cleanUpRepeatsAndPutInOrder()'
  numbers = numbers.sort()
  index = 0
  while 1:
    number = numbers[index]
    if index >= len(numbers) - 1:
      break
    nextNumber = numbers[index + 1]
    if number == nextNumber:
      del numbers[index+1]
      continue
    index += 1
  return numbers


def iguais_com_o_anterior(concurso, concursoAnterior, DO_REPEAT_CLEAN_UP=False):
  '''
  Metric 1 iguais_com_os_n_anteriores
  
  Steps:
    1st) check type conformity
    2nd) do a DO_REPEAT_CLEAN_UP if "it's asked" via passed-in param DO_REPEAT_CLEAN_UP
    3rd) count equals and return it 
  '''
  if type(concurso) not in [list, tuple]:
    raise TypeError, 'concurso and must be a list or tuple as passed-in parameters to iguaisComOAnterior()'
  if type(concursoAnterior) not in [list, tuple]:
    raise TypeError, 'concursoAnterior must be a list or tuple as passed-in parameters to iguaisComOAnterior()'
  if DO_REPEAT_CLEAN_UP:
    concurso = cleanUpRepeatsAndPutInOrder(concurso)
    concursoAnterior = cleanUpRepeatsAndPutInOrder(concursoAnterior)
  nDeIguais = 0
  for dezena in concurso:
    if dezena in concursoAnterior:
      nDeIguais += 1
  return nDeIguais

def iguais_com_os_n_anteriores(concurso, concursosAnteriores, n_anteriores):
  '''

  Metric 1 iguais_com_os_n_anteriores

  n_anteriores > 1
  Steps:
    1st) check type conformity
    2nd) check size of concursosAnteriores that must be equal to nAnteriores
    3rd) reduce problem to its elements, ie loop through concursosAnteriores and invoke iguaisComOAnterior  
  '''
  if type(concursosAnteriores) not in [list, tuple]:
    raise TypeError, 'concursosAnteriores and must be a list or tuple as passed-in parameters to iguaisComOsNAnteriores()'
  if len(concursosAnteriores) != n_anteriores:
    raise IndexError, 'concursosAnteriores has a size = %d which is different from nAnteriores' %(len(concursosAnteriores), nAnteriores)
  for concursoAnterior in concursosAnteriores:
    iguais_com_os_n_aAnteriores(concurso, concursoAnterior)    


def consecutive_metrics(concurso, concursos):
  '''
  Metric 2 consecutive
  '''
  pass
    

def parParImparImpar_digit_metric(concurso, concursos):
  '''
  Metric 3 parParImparImpar digit-digit metric consecutive
  '''
  pass

def n_impares_metric(concurso, concursos):
  '''
  Metric 4 Remainders
  '''
  pass

def remainder_n_pattern(concurso, concursos, n):
  '''

  Metric 4 Remainders

  Notice:
    Remainder 2 is n_impares_metric
    Remainder 6 is close to line_pattern
    Remainder 10 is close to column_pattern
  '''
  pass

def soma_metric(concurso, concursos):
  '''

  Metric 5 Somas
  
  '''
  pass

def soma_com_os_n_anteriores(concurso, concursos, n):
  '''

  Metric 5 Somas
  
  '''
  pass

def avg_metric(concurso, concursos):
  '''

  Metric 5 Somas (actually, avg is, in the Megasena example, just soma by 6)
  
  '''
  pass

def std_metric(concurso, concursos):
  '''

  Metric 6 Desvios
  
  '''
  pass

def column_pattern(concurso, concursos):
  '''
  Metric 4 Remainders
  '''
  pass

def column_drawing(concurso, concursos):
  '''
  Metric 4 Remainders (aggregate)
  '''
  pass

def line_pattern(concurso, concursos):
  '''
  Metric 4 Remainders (aggregate)
  '''
  pass

def line_drawing(concurso, concursos):
  '''
  Metric 4 Remainders (aggregate)
  '''
  pass

def ocorrenciasDeCadaDezena(concurso, concursos):
  '''
  Metric 7 Frequencies
  '''
  pass

def posAnteriorDeOcorrenciaDeCadaDezena(concurso, concursos):
  '''
  Metric 8 spike-depths
  Results in the tuple-spike, example
  1, 7, 12, 13, 25, 31
  Suppose:
    when d1 = 1  last occurred = 10 games ago
    when d2 = 7  last occurred = 7 games ago
    when d3 = 12 last occurred = 1 game ago
    when d4 = 13 last occurred = 10 games ago
    when d5 = 25 last occurred = 5 games ago
    when d6 = 31 last occurred = 15 games ago
  Thus, results may be implemented:
  1) a simple result is:
    10,7,1,10,5,15 
  2) a combined-index-like result is:
    desc-order it: 15,10,10,7,5,1 
    apply the dot product indicated: 15*6+10*5+10*4+7*3+5*2+1*1 (this will collide a lot)
  3) generate a TilR-like pattern (a 2nd computation level)
  Suppose TilR5DistDepth for last occurred distances are:
    depth 15 is slot 4
    depth 10 is slot 3
    same
    depth 7 is slot 1
    depth 5 is slot 1
    depth 1 is slot 5
  Then, result here is 543311  (this is a relative index result, not absolute)
  '''
  pass

def iguaisMediaComPassado(concurso, concursos):
  pass

def maxDeIguais(concurso, concursos):
  pass

def maxDeIguaisDistAo1oAnterior(concurso, concursos):
  pass

def maxDeIguaisOcorrencia(concurso, concursos):
  pass

def histograma_de_coincidentes(concurso, concursos):
  '''
  Example:
  Suppose the following game:
  1, 7, 12, 13, 25, 31
  
  Looking back at history, the following coincides histogram may be calculated:
    coincides[6] = n_of_games_that_have_6_coincides (ie, equal games)
    coincides[5] = n_of_games_that_have_5_coincides (ie, quina in common)
    coincides[4] = n_of_games_that_have_4_coincides (ie, quadra in common)
    coincides[3] = n_of_games_that_have_3_coincides (ie, terno in common)
    coincides[2] = n_of_games_that_have_2_coincides (ie, duo in common)
    coincides[1] = n_of_games_that_have_1_coincides (ie, one dozen in common)
    coincides[0] = n_of_games_that_have_0_coincides (ie, nothing in common)

  This might be, for example:
  { 6:0, 5:1, 4:37, 3:345; 2:569; 1:980; 0:the remainder complete the history}
  Or ( 0, 1, 37, 345, 569, 980, remainder )
  
  How to use this metric?
  
  In games generation, a filter might be set with limiting ranges for each n-coincide value.
  For example:
    filter_coinc_6, from 0 to 0 :: meaning there should not be any full equals
    filter_coinc_5, from 0 to 2 :: meaning: accept at most 2 quina games in history
    filter_coinc_4, from 30 to 40 :: meaning: filter out those in history that have either less than 30 quadra games or more than 40 quadra games
    filter_coinc_3, from 300 to 400 :: meaning: filter out those in history that have either less than 300 terno-games or more than 400 terno-games
    filter_coinc_2, from 500 to 600 :: meaning: filter out those in history that have either less than 500 duo-games or more than 600 duo-games
    filter_coinc_1, from 1000 to 1200 :: meaning: filter out those in history that have either less than 1000 one-in-common-games or more than 1200 one-in-common-games
    filter_coinc_0, from remainder1 to remainder2 :: meaning: filter out those in history that have either less than remainder1 one-in-common-games or more than remainder2 one-in-common-games 
  
  '''
  pass

def til_n_pattern(concurso, concursos, tiln):
  '''
  Metric 7 Frequencies
  '''
  pass

def tilr_n_pattern(concurso, concursos, tilrn):
  '''
  Metric 7 Frequencies
  '''
  pass

def pathway(concurso, concursos):
  '''
  Metric 8 Geometry
  '''
  pass

def allpaths(concurso, concursos):
  '''
  Metric 8 Geometry
  '''
  pass

def binDecReprSomaDe1s(concurso, concursos):
  '''
  Metric 9 Sequential Index Mapping
  '''
  pass

def lgiDist(concurso, concursos):
  '''
  Metric 9 Sequential Index Mapping
  '''
  pass

def depth_up_and_down_for_soma_backwards_n_concursos(concurso, concursos, n_backwards):
  '''
  Metric 10 up and down variation
  
  Example:
  Suppose n_backwards = 5, this means we'll look up 5 previous concursos
  Suppose that we have as soma for the current game: 200
  And:
  210 up
  220 up
  205 down
  205 equal
  206 up
  This may be represented by: 22012 ie
  2 = up
  1 = equal
  0 = down
  '''
  pass

def depth_up_and_down_for_std_backwards_n_concursos(concurso, concursos, n_backwards):
  '''
  Metric 10 up and down variation (for desvios)
  
  See commentary for the same metrics, as for soma
  '''
  pass
