#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/bin_dec_repr.py
"""
import math, time, sys  # for timing purposes
# from cardprint import pprint


class IntPacker(object):
  """
  This class helps read and write integers (from 0 up to 2 ** nOfBytes - 1)
    from and to binary files.

  The original purpose was to keep lgi_b1idx's numbers.  Each lgi_b1idx, as it's known,
    represents a combination-set.

  This original purpose (keeping the lgi's) is no longer necessary
    because the bijective functions (from and to) sets to lgi and viceversa are already available.
  """
  def __init__(self, n_of_bytes):
    self.n_of_bytes = n_of_bytes
    self.maxInt = 2 ** (n_of_bytes * 8) - 1
    self.offset = 0  # offset is a byte index, readIndex, also an index, is offset * 3
    self.readIndex = 0  # readIndex is incremented 1 at each read()
    self.read_mode = False
    self.write_mode = False
    self.number = None
    self.byteList = None
    self.file_obj = None

  def set_number(self, number):
    if number > self.maxInt:
      errmsg = 'number %d is greater than maxInt %d.' % (number, self.maxInt)
      raise ValueError(errmsg)
    self.number = number
    #print 'self.pack_to_bytes()', self.number
    self.pack_to_bytes()

  def set_byte_list(self, byte_list):
    if len(byte_list) > self.n_of_bytes:
      errmsg = 'byteList %s has more than %d (nOfBytes)' % (byte_list, self.n_of_bytes)
      raise ValueError(errmsg)
    self.byteList = byte_list
    self.unpack_from_bytes()

  def pack_to_bytes(self):
    if not self.number:
      scrmsg = f'number={self.number} is missing.'
      raise ValueError(scrmsg)
    self.byteList = pack_byte_int(self.number, self.n_of_bytes)
    #print 'pack_to_bytes(self):', self.byteList

  def unpack_from_bytes(self):
    if not self.byteList:
      errmsg = f'byteList {self.byteList} is missing.'
      raise ValueError(errmsg)
    self.number = unpack_byte_int(self.byteList, self.n_of_bytes)

  def set_file_obj(self, file_obj, read_mode=False):
    if read_mode:
      self.read_mode = True
      self.write_mode = False
    else:
      self.read_mode = False
      self.write_mode = True
    self.file_obj = file_obj

  def write(self, number=None):
    if self.read_mode:
      errmsg = 'cannot write in read mode.'
      raise TypeError(errmsg)
    if number is not None:
      self.set_number(number)
    if not self.byteList:
      errmsg = 'byteList has not been set.'
      raise TypeError(errmsg)
    for byte in self.byteList:
      self.file_obj.write(byte)

  def first(self):
    self.offset = 0
    self.file_obj.seek(self.offset)
    self.read()

  def read(self):
    if self.write_mode:
      errmsg = 'cannot read in write mode.'
      raise TypeError(errmsg)
    if not self.file_obj:
      errmsg = 'fileObj has not been set.'
      raise TypeError(errmsg)
    self.byteList = []
    chrs = self.file_obj.read(self.n_of_bytes) # read nOfBytes bytes
    if not chrs:
      return None
    self.offset += self.n_of_bytes
    self.readIndex += 1
    for ch in chrs:
      self.byteList.append(ch)
      #print self.byteList,
    self.unpack_from_bytes()
    return self.number

  def next(self):
    return self.read()

  def close(self):
    self.file_obj.close()


def get_n_of_bytes_for_packer(n_of_combs):
  exponent = math.log(n_of_combs) / math.log(2)
  exp_int = int(exponent)
  if exponent > exp_int:
    exp_int+=1
  n_of_bytes = exp_int / 8
  if exp_int > 8*n_of_bytes:
    n_of_bytes += 1
  return n_of_bytes


def pack_byte_int(number, n_of_bytes):
  """
  The purpose and this method (and the next, for unpacking)
    is to allow the formation of
    an array of bytes that represent a non-negative integer in
    the range from 0 to 2**(nOfBytes*8) - 1

  Eg. to keep lgi_b1idx's for LF, which has its max int c25to15 = 3268760 (minus 1),
    one needs 22 bits.

    Here follows some calculations:
    log2(3268760) = 21.6403120243
    2 ** 21 = 2097152
    2 ** 22 = 4194304, so 22 bits will suffice

  Because writing happens byte to byte, each having 8 bits,
    3 bytes (24 bits) will be used (2 bits will be wasted)

    (a maximizing scheme could be implemented...)
  """
  if number < 0:
    errmsg = 'Only unsigned int numbers are allowed.'
    raise ValueError(errmsg)
  max_unsigned_int_here = 2 ** (n_of_bytes * 8) - 1
  if number > max_unsigned_int_here:
    errmsg = 'number is greater than max_unsigned_int_here.'
    raise ValueError(errmsg)
  #mask = get_mask(nOfBytes)
  bytes = [0] * n_of_bytes
  mask = 255
  for i in range(n_of_bytes):
    chunk = number & mask
    mask = mask << 8 # from 11111111 to 1111111100000000 and so
    shift_left = 8*i
    chunk = chunk >> shift_left
    bytes[i] = chr(chunk)
  return bytes


def unpack_byte_int(byte_list, n_of_bytes):
  if len(byte_list) > n_of_bytes:
    errmsg = 'number is greater than maxUnsignedIntHere.'
    raise ValueError(errmsg)
  c, out_number = 0, 0
  for i in range(len(byte_list)):
    sub_number = ord(byte_list[i])
    shift_left = 8*i
    sub_number= sub_number<< shift_left
    out_number += sub_number
  return out_number


def get_mask(n_of_bytes):
  """
  This function is not used anymore, left here for reference purposes
  """
  mask = [0] * n_of_bytes
  mask[0] = 255 # ie 2**8 - 1
  for i in range(1, n_of_bytes):
    mask[i] = mask[i-1] << 8


def min_n_of_bits(n):
  #t = math.log(n) * 1 / log(2)
  if n < 0:
    return None
  if n == 0:
    return 0
  if n == 1 or n == 2: # here, it can only be 1 or 2
    return 1
  n = n - 1
  c = 0
  while n > 0:
    n = n >> 1
    c += 1
  return c


def pack_jogo_to_binary_dec_repr(dezenas, n_of_bits):
  n = len(dezenas)
  #nOfBits = log2(
  stuff = 0
  for dezena in dezenas:
    n -= 1
    nc = n_of_bits * n
    # print 'nc', nc, 'dezn', dezena, 'n',n
    # shift-left nc bits :: eg. 1 << 5 = 32
    # or 1 << 5 = 1 * 2**5
    # the inverse is 32 >> 5 = 1 or 32 / (2**5) = 1
    trunk = dezena << nc 
    stuff = stuff | trunk
  #print jogo,
  #print stuff
  return stuff


def unpack_jogo_from_binary_dec_repr(binary_dec_repr, n_de_dezenas_sorteadas, n_of_bits, mask_sort_or_reverse=0):
  """
  The unpack is done in reverse order,
  if order is important, reverse parameter should be passed in as True
  """
  #print 'binaryDecRepr, nDeDezenasSorteadas, nOfBits'
  #print binaryDecRepr, nDeDezenasSorteadas, nOfBits
  jogo = [-1] * n_de_dezenas_sorteadas
  # if nOfBits is 5, ones_for_and_op should be binary 11111
  # if nOfBits is 3, ones_for_and_op should be binary 111, and so on
  ones_for_and_op = 2 ** n_of_bits - 1
  # parse it backwardly
  for i in range(n_de_dezenas_sorteadas - 1, -1, -1):
    # 31 in binary, is 11111
    # with an AND operation (&), we're throwing everything away except the right-most 5-bits
    # the packing was done in trunks of 5 bits each
    dezena = binary_dec_repr & ones_for_and_op
    #print dezena,
    jogo[i] = int(dezena)
    # shift-right 5 bits to get the next 5 bits to the left as loop goes round
    binary_dec_repr = binary_dec_repr >> n_of_bits
    #print binaryDecRepr,
  # a first reverse is necess
  return return_jogo_treating_the_order_or_reverse_mask(jogo, mask_sort_or_reverse)


def return_jogo_treating_the_order_or_reverse_mask(jogo, mask_sort_or_reverse):
  """
  maskInOrderAndReverse should be binaries 11 (=3 dec), 10 (=2 dec) or 01 (=1 dec)
  reverse is both a sort() and a reverse()
  """
  if type(mask_sort_or_reverse) != int:
    return jogo
  if mask_sort_or_reverse not in [0, 1, 2]:
    return jogo
  put_in_order = mask_sort_or_reverse >> 1 & 1
  reverse = mask_sort_or_reverse & 1
  #print 'put_in_order', put_in_order, 'reverse', reverse, 'maskSortOrReverse'
  #print 'jogo', jogo
  if put_in_order:
    jogo.sort()
  if reverse:
    jogo.sort()
    jogo.reverse()
  return jogo

def charge_bet_file_into_bin_dec_repr_dict(fileIn='jogosfs-bet.txt'):
  nOfLines  = 0
  jogosBetFile = open(fileIn)
  print('Counting lines and charging jogosfs into dict, please wait.')
  line = jogosBetFile.readline()
  bin_dec_repr_jogos_dict = {}
  while line:
    nOfLines += 1
    if nOfLines % 100000 == 0:
      print(nOfLines, ' ... ',)
    jogo_line = JogoLine(line)
    binDecRepr = jogo_line.getBinDecRepr()
    # all binDecReprJogos receive, initially, 1
    bin_dec_repr_jogos_dict[binDecRepr] = 1
    line = jogosBetFile.readline()
  print 'nOfLines', nOfLines
  print 'len(bin_dec_repr_jogos_dict)', len(bin_dec_repr_jogos_dict)
  jogosBetFile.close()
  return bin_dec_repr_jogos_dict


def filter11_out(bin_dec_repr_jogos_dict):
  """
  Enter dict
  Goes out list
  """
  bin_dec_repr_jogos = bin_dec_repr_jogos_dict.keys()
  # save some memory if possible
  del bin_dec_repr_jogos_dict
  print('start sort bin_dec_repr_jogos', time.ctime())
  bin_dec_repr_jogos.sort()
  print('finish sort bin_dec_repr_jogos', time.ctime())
  n_of_excluded = 0; i=0
  dyn_size = len(bin_dec_repr_jogos)
  while i < dyn_size - 1:
    bin_dec_repr_jogo_i = bin_dec_repr_jogos[i]
    #if binDecReprJogosDict[bin_dec_repr_jogo_i] == 0:
      #continue
    jogo_line_i = JogoLine(None, None, bin_dec_repr_jogo_i)
    for j  in range(i+1, dyn_size):
      bin_dec_repr_jogo_j = bin_dec_repr_jogos[j]
      #if binDecReprJogosDict[bin_dec_repr_jogo_j] == 0:
        #continue
      jogo_line_j = JogoLine(None,None,bin_dec_repr_jogo_j)
      r = has11OrMoreCoincs(jogo_line_i.jogo, jogo_line_j.jogo)
      if r:
        del bin_dec_repr_jogos[i]
        #binDecReprJogosDict[bin_dec_repr_jogo_j] = 0
        n_of_excluded+=1
        #print 0,
        i-=1
        break
      else:
        pass
        #print 1,
      if n_of_excluded % 10000 == 0:
        print('excl', n_of_excluded,)
    dyn_size = len(bin_dec_repr_jogos)
    i+=1
  print('n_of_excluded', n_of_excluded)
  return bin_dec_repr_jogos


def record_new_bet_file(bin_dec_repr_jogos, file_out='jogosfs-bet-mantidos.txt'):
  mantem_file = open(file_out, 'w')
  for binDecReprJogo in bin_dec_repr_jogos:
    jogo_line = JogoLine(None, None, binDecReprJogo)
    line = jogo_line.getLine() + '\n'
    mantem_file.write(line)
  mantem_file.close()


def queue_tasks(file_in='jogosfs-bet.txt'):
  bin_dec_repr_jogos_dict = charge_bet_file_into_bin_dec_repr_dict(file_in)
  bin_dec_repr_jogos = filter11OutImpl2(bin_dec_repr_jogos_dict)
  # save some memory if possible
  del bin_dec_repr_jogos_dict
  record_new_bet_file(bin_dec_repr_jogos)


def generate_sample_bet(quant):
  print('generate_sample_bet()')
  jogos_bet_file = open('jogosfs-bet.txt')
  jogos_sample_bet_file = open('sample-jogosfs-bet.txt','w')
  line = jogos_bet_file.readline()
  n_of_lines = 0
  while line and n_of_lines < quant:
    n_of_lines += 1
    jogos_sample_bet_file.write(line)
  jogos_sample_bet_file.close()


def testMinNOfBits():
  n = 25; expect = 5
  r = min_n_of_bits(n)
  print 'min_n_of_bits(',n,') ==>>', r
  assert(r == expect)
  # =====================================
  n = 60; expect = 6
  r = min_n_of_bits(n)
  print 'min_n_of_bits(',n,') ==>>', r
  assert(r == expect)
  # =====================================
  n = 1024; expect = 10
  r = min_n_of_bits(n)
  print 'min_n_of_bits(',n,') ==>>', r
  assert(r == expect)
  # =====================================
  n = 1; expect = 1
  r = min_n_of_bits(n)
  print 'min_n_of_bits(',n,') ==>>', r
  assert(r == expect)
  # =====================================
  n = 0; expect = 0
  r = min_n_of_bits(n)
  print 'min_n_of_bits(',n,') ==>>', r
  assert(r == expect)
  # =====================================
  n = -1; expect = None
  r = min_n_of_bits(n)
  print 'min_n_of_bits(',n,') ==>>', r
  assert(r == expect)
  # =====================================


def sweep_coincidences_in_jogos_consecutives(jogos):
  """
  Run thru jogosfs, calculating consecutive coincidences
  """
  acum, coinc_min, coinc_max = 0, 0, 0
  for i in range(1,len(jogos)):
    jogo = jogos[i]
    jogo_previous = jogos[i-1]
    n_of_coinc = getNOfCoincidences(jogo, jogo_previous)
    print(pprint(jogo), 'n_of_coinc', n_of_coinc)
    acum += n_of_coinc
    if n_of_coinc < coinc_min:
      coinc_min = n_of_coinc
    if n_of_coinc > coinc_max:
      coinc_max = n_of_coinc
  average = acum / (0.0 + len(jogos) - 1)
  print('average', average)
  print('min coinc', coinc_min)
  print('max coinc', coinc_max)
  average_int = int(average) + 1
  n_of_combs_with_average = co.iCmb(15, average_int)
  print('n_of_combs_with_average', n_of_combs_with_average)


def initialize_set_jogo_coinc_with_jogo_dict(n_of_jogos):
  """
  Just initializes list elems with an empty dict
  This is a coupled method, ie, an extension of another method for zeroing the dict
  """
  for i in range(n_of_jogos):
    jogosCoincWithJogos[i]={}


def set_jogo_coinc_with_jogo(i, j, n_of_coincs):
  """
  Double set two coincident jogosfs, one with the other
  """
  dict_of_coincs = jogosCoincWithJogos[i]
  dict_of_coincs[j] = n_of_coincs
  dict_of_coincs = jogosCoincWithJogos[j]
  dict_of_coincs[i] = n_of_coincs

coincDict = {}
def set_coincs(jogos):
  """
  Test-like routine
  """
  for i in range(len(jogos)-1):
    for j in range(i+1,len(jogos)):
      jogo_a = jogos[i]
      jogo_b = jogos[j]
      n_of_coincs = 0
      for dezena in jogo_a:
        if dezena in jogo_b:
          n_of_coincs += 1
      set_jogo_coinc_with_jogo(i, j, n_of_coincs)
      try:
        coincDict[n_of_coincs] += 1
      except KeyError:
        coincDict[n_of_coincs] = 1

coincWithPreviousDict = {}; setJogoCoincWithPrevious = []

def check_coincs_with_previous(jogos):
  """
  Check consecutive jogosfs for coincidences in a set of jogosfs
  """
  n_of_jogos = len(jogos)
  set_jogo_coinc_with_previous = [0] * n_of_jogos
  for i in range(len(jogos)-1):
    jogo_a = jogos[i]
    jogo_b = jogos[i+1]
    n_of_coincs = 0
    for dezena in jogo_a:
      if dezena in jogo_b:
        n_of_coincs += 1
    set_jogo_coinc_with_previous[i]=n_of_coincs
    try:
      coincWithPreviousDict[n_of_coincs]+=1
    except KeyError:
      coincWithPreviousDict[n_of_coincs]=1


def adhoctest():
  pass


if __name__ == '__main__':
  adhoctest()
