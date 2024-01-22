#!/usr/bin/env python3
"""
fs/mathfs/funcs_for_random.py

#import os
#import shutil
#import time
"""
import random
import sys
PRIMES_TILL_60 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]
alphabet = map(chr, range(65, 65+28))


def random_set(n):
  dezenas_to_combine = []
  for i in range(n):
    go_ahead = False
    while not go_ahead:
      d = random.randint(1,60)
      if d not in dezenas_to_combine:
        dezenas_to_combine.append(d)
        go_ahead = True
  dezenas_to_combine.sort()
  return dezenas_to_combine


def x_random_dezenas():
  #dezenas = [1,2,3,4,5,6,7]
  #dezenas = range(1,16)
  dezenas_to_combine = random_set(20)
  comb6Conv(dezenas_to_combine)


def d60_minus_x_last_jogos(n_of_last_jogos_to_not_consider=2):
  n_of_last_jogo = Sena.getNOfLastJogo(); dezenas_to_strip = []
  for i in range(n_of_last_jogos_to_not_consider):
    nOfJogo = n_of_last_jogo - i
    jogo = Sena.jogosPool.getJogo(nOfJogo)
    dezenas_to_strip += jogo.getDezenas()
  setWithStripped2Jogos = []
  d60=range(1,61)
  for d in d60:
    if d in dezenas_to_strip:
      continue
    setWithStripped2Jogos.append(d)
  return setWithStripped2Jogos

filtroDict = {1:0, 2:0, 3:0, 4:0}; filtroKeys = filtroDict.keys()
filtroKeys.sort()

OneMillion = 10 ** 6
passing = 1; nOfFailPass = 0; nOfPass = 0
def run_combinations(startAt, endAt, nOfLastJogosToNotConsider=2):
  scrmsg = ' [run_combinations()] with the following data:'
  print(scrmsg)
  set_with_stripped2_jogos = d60_minus_x_last_jogos(nOfLastJogosToNotConsider)
  print('Dezenas a combinar: ', set_with_stripped2_jogos)
  tam = len(set_with_stripped2_jogos)
  n_de_comb = comb(tam, 6)
  if endAt is None or endAt < 1:
    endAt = n_de_comb
  scrmsg = 'O número de combinações para %d dezenas é de %d' % (tam, n_de_comb)
  print(scrmsg)
  scrmsg = 'Relatively long processing, some messages will appear.  Please wait.'
  print(scrmsg)
  comb_obj = Comb6IterativeGenerator(set_with_stripped2_jogos, startAt, endAt)
  comb_obj.run()


def run_combinations_with_d60_minus():
  set_with_stripped2_jogos = d60_minus_x_last_jogos()
  c, allDrawns = 0, []
  d60_minus_size = len(set_with_stripped2_jogos);
  for i in range(11):
    hasPassed = False
    while not hasPassed:
      dezenas = []
      while len(dezenas) < 6:
        index = random.randint(1,d60_minus_size)
        d = set_with_stripped2_jogos[index-1]
        if d not in dezenas:
          dezenas.append(d)
      c += 1
      jogo = Sena.ShapeAreaCircleCalculator(-c)
      dezenas.sort()
      jogo.setDezenas(dezenas)
      tuple2 = filters.passThruFilters(jogo)
      hasPassed = tuple2[0]
      if not hasPassed:
        print jogo, filters.getMessageStrFromFilterReturnNumberCode(tuple2[1])
    allDrawns.append(jogo.getDezenas())
  allDrawns.sort()
  print 'Tirados:', len(allDrawns), 'Tentativas totais:', c
  for drawnList in allDrawns:
    tmpF = lambda x: str(x).zfill(2)
    drawnStrList = map(tmpF, drawnList)
    line = ' '.join(drawnStrList)
    print line

def main2():
  #  start_at = 10*OneMillion + 1; end_at = 20*OneMillion
  start_at = 1
  end_at   = 2000
  try:
    start_at = int(sys.argv[1])
    end_at = int(sys.argv[2])
    print(' *** Using start_at =', start_at, 'and end_at =', end_at)
  except ValueError:
    pass
  run_combinations(start_at, end_at)

def main1():
  n_of_combs48a6 = comb(48, 6)
  end_at = n_of_combs48a6
  for i in range(10):
    drawn = random.randint(1,n_of_combs48a6)
    start_at = drawn
    print( ' *** Using start_at =', start_at, 'and end_at =', end_at)
    run_combinations(start_at, end_at)


def test_comb6():
  c=0
  comb = Comb6(comb=[59,50,40,30,20,10])
  c += 1
  print(c, '==>>', comb)
  comb = Comb6(lgi=100)
  c+=1
  print(c, '==>>', comb)
  comb = Comb6(comb=[9,6,5,4,2,0])
  c+=1
  print(c, '==>>', comb)


def adhoc_test():
  #run_combinations_with_d60_minus()
  test_comb6()


if __name__ == '__main__':
  look_up_cli_params_for_tests_or_processing()
