#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
volante_functions.py
"""
# import time  # for timing purposes
DEFAULT_FILENAME = 'jogosfs-bet-mantidos.txt'


def return_int_range_or_default_or_raise_ValueError(int_range, DEFAULT_INT_RANGE):
  """
  # type: (tuple, tuple) -> tuple
  This function returns the DEFAULT_INT_RANGE is int_range is None, if it's not a 2-tuple and if elements of the 2-tuple are not int
  But, it will raise ValueError is the first element is greater than the second. (There is a unittest for all these cases.)

  IMPORTANT: one thing may change in the future: if elements of the 2-tuple are not int, there may be a raising
    (but I hope I do update this __doc__ and the unittest if this change comes to happen.)

  Args:
    int_range: tuple
    DEFAULT_INT_RANGE: tuple

  Returns:
    object: tuple

  """
  if int_range is None or len(int_range) != 2:
    return DEFAULT_INT_RANGE
  try:
    least_n = int(int_range[0])
    greatest_n = int(int_range[1])
  except ValueError:
    return DEFAULT_INT_RANGE
  if least_n > greatest_n:
    errmsg = 'least_n (=%d) > greatest_n (=%d) ' %(least_n, greatest_n)
    raise ValueError(errmsg)
  return int_range


def find_standard2_letter_name_in_filename(apostas_filename):
  """
  Apostas filename are standardized
  yyyy-mm-dd-s2LN-apostas.txt[.n]
  where n, if exists, is a int number equal or greater than one
  Eg.
  2009-10-04-ms-apostas.txt.3
  """
  pp = apostas_filename.split('-')
  standard2_letter_name = pp[3]
  standard2_letter_name = standard2_letter_name.upper()
  return standard2_letter_name

def record_new_bet_file(bin_dec_repr_jogos, file_out=None):
  if file_out is None:
    file_out = DEFAULT_FILENAME
  mantem_file = open(file_out, 'w')
  n_of_excluded = 0
  for bin_dec_repr_jogo in bin_dec_repr_jogos:
    jogo_line = JogoLine(None,None,bin_dec_repr_jogo)
    line = jogo_line.getLine() + '\n'
    mantem_file.write(line)
  mantem_file.close()

def queue_tasks(file_in='jogosfs-bet.txt'):
  bin_dec_repr_jogos_dict = chargeBetFileIntoBinDecReprDict(file_in)
  bin_dec_repr_jogos = filter11OutImpl2(bin_dec_repr_jogos_dict)
  # save some memory if possible
  del bin_dec_repr_jogos_dict
  record_new_bet_file(bin_dec_repr_jogos)

def generate_sample_bet(quant):
  print 'generate_sample_bet()'
  jogosBetFile = open('jogosfs-bet.txt')
  jogosSampleBetFile = open('sample-jogosfs-bet.txt','w')
  line = jogosBetFile.readline(); nOfLines = 0
  while line and nOfLines < quant:
    nOfLines += 1
    jogosSampleBetFile.write(line)
  jogosSampleBetFile.close()


def sweep_coincidences_in_jogos_consecutives(jogos):
  """
  Run thru jogosfs, calculating consecutive coincidences
  """
  acum, coinc_min, coinc_max = 0, 25, 0
  for i in range(1,len(jogos)):
    jogo = jogos[i]
    jogo_previous = jogos[i-1]
    nOfCoinc = getNOfCoincidences(jogo, jogo_previous)
    print pprint(jogo), 'nOfCoinc', nOfCoinc
    acum += nOfCoinc
    if nOfCoinc < coinc_min:
      coinc_min = nOfCoinc
    if nOfCoinc > coinc_max:
      coinc_max = nOfCoinc
  average = acum / (0.0 + len(jogos) - 1)
  print 'average', average
  print 'min coinc', coinc_min
  print 'max coinc', coinc_max
  import comb as co
  averageInt = int(average) + 1
  nOfCombsWithAverage = co.iCmb(15, averageInt)
  print 'nOfCombsWithAverage', nOfCombsWithAverage

def initializeSetJogoCoincWithJogoDict(nOfJogos):
  '''
  Just initializes list elems with an empty dict
  This is a coupled method, ie, an extension of another method for zeroing the dict
  '''
  for i in range(nOfJogos):
    jogosCoincWithJogos[i]={}

def setJogoCoincWithJogo(i, j, nOfCoincs):
  '''
  Double set two coincident jogosfs, one with the other
  '''
  dictOfCoincs = jogosCoincWithJogos[i]
  dictOfCoincs[j]=nOfCoincs
  dictOfCoincs = jogosCoincWithJogos[j]
  dictOfCoincs[i]=nOfCoincs

coincDict = {}
def setCoincs(jogos):
  '''
  Test-like routine
  '''
  for i in range(len(jogos)-1):
    for j in range(i+1,len(jogos)):
      jogoA = jogos[i]
      jogoB = jogos[j]
      nOfCoincs = 0
      for dezena in jogoA:
        if dezena in jogoB:
          nOfCoincs += 1
      setJogoCoincWithJogo(i, j, nOfCoincs)
      try:
        coincDict[nOfCoincs]+=1
      except KeyError:
        coincDict[nOfCoincs]=1

      #if coincs >= 11:
        #print i, j, 'coincs', coincs

coincWithPreviousDict = {}; setJogoCoincWithPrevious = []
def checkCoincsWithPrevious(jogos):
  '''
  Check consecutive jogosfs for coincidences in a set of jogosfs
  '''
  nOfJogos = len(jogos)
  setJogoCoincWithPrevious = [0]*nOfJogos
  for i in range(len(jogos)-1):
    jogoA = jogos[i]
    jogoB = jogos[i+1]
    nOfCoincs = 0
    for dezena in jogoA:
      if dezena in jogoB:
        nOfCoincs += 1
    setJogoCoincWithPrevious[i]=nOfCoincs
    try:
      coincWithPreviousDict[nOfCoincs]+=1
    except KeyError:
      coincWithPreviousDict[nOfCoincs]=1


if __name__ == '__main__':
  pass
  '''
  testMinNOfBits()
  # testPackAndUnpack()
  fileIn='sample-jogosfs-bet.txt'
  print 'queue_tasks()'
  #queue_tasks(fileIn)
  queue_tasks()
  #generate_sample_bet(100)
  '''