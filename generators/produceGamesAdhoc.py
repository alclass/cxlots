#!/usr/bin/env python
# -*- coding: utf-8 -*-
# local_settings.py
'''
Created on 28/12/2012

@author: friend
'''

import localpythonpath
localpythonpath.setlocalpythonpath()
from models.ConcursoHTML import *
from models.ConcursoSlider import *

import random
def get_tuple():
  t=[]
  while len(t) < 6:
    d = random.randint(1,60)
    if d not in t:
      t.append(d)
  return t

def check(all_jogos_as_dezenas, random_dezenas):
  for dezenas in all_jogos_as_dezenas:
    acertos = 0
    for dezena in dezenas:
      if dezena in random_dezenas:
        acertos += 1
      if acertos > 3:
        return False
  return True

zfill2 = lambda s : str(s).zfill(2) 
def dezenas_to_str(dezenas):
  dezenas.sort()
  dezenas = map(zfill2, dezenas)
  dezenas = ' '.join(dezenas)
  return dezenas

def write_to_file(all_random_dezenas):
  n_done = 0
  for dezenas in all_random_dezenas:
    dezenas_str = dezenas_to_str(dezenas)
    outfile.write(dezenas_str + '\n')
    n_done +=1
    print n_done, dezenas_str

def produce():
  slider = ConcursoHTML()
  last_concurso = slider.get_last_concurso()
  last_nDoConc = last_concurso.nDoConc 
  # print 'last_nDoConc', last_nDoConc
  all_jogos_as_dezenas = []
  print 'Reading database'
  for i in range(1, last_nDoConc+1):
    concurso = slider.get_concurso_by_nDoConc(i)
    dezenas = concurso.get_dezenas()
    # print i, # dezenas
    if i%250 == 0:
      print i, 'done'
    all_jogos_as_dezenas.append(dezenas)
  #print 'concurso nº', nDoConc, concurso
  print 'Starting process of random generation'
  n_done = 0
  all_random_dezenas = []
  while n_done < 360:
    random_dezenas = get_tuple()
    result = check(all_jogos_as_dezenas, random_dezenas)
    #print random_dezenas, result
    if result:
      n_done += 1
      all_random_dezenas.append(random_dezenas)
      print n_done, random_dezenas
  while len(all_random_dezenas) > 120:
    i = random.randint(1, len(all_random_dezenas)-1)
    print 'deleting', i, all_random_dezenas[i] 
    del all_random_dezenas[i]
  write_to_file(all_random_dezenas)

outfile = open('megasena_results.log', 'w')
produce()
outfile.close()