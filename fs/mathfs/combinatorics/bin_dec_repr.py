#!/usr/bin/env python3
"""

"""
import math, time, sys  # for timing purposes
from cardprint import pprint

class IntPacker(object):
  """
  This class helps read and write integers (from 0 up to 2 ** nOfBytes - 1)
    from and to binary files.

  The orginal purpose was to keep lgi_b1idx's numbers.  Each lgi_b1idx, as it's known,
    represents a jogo-combination.

  """
  def __init__(self, nOfBytes):
    self.n_of_bytes = nOfBytes
    self.maxInt   = 2 ** (nOfBytes*8) - 1
    self.offset    = 0 # offset is a byte index, readIndex, also an index, is offset * 3
    self.readIndex = 0 # readIndex is incremented 1 at each read()
    self.number   = None
    self.byteList = None
    self.file_obj  = None

  def set_number(self, number):
    if number > self.maxInt:
      raise ValueError, 'number %d is greater than maxInt %d.' %(number, self.maxInt)
    self.number   = number
    #print 'self.pack_to_bytes()', self.number
    self.pack_to_bytes()

  def set_byte_list(self, byte_list):
    if len(byte_list) > self.n_of_bytes:
      raise ValueError, 'byteList %s has more than %d (nOfBytes)' %(byte_list, self.n_of_bytes)
    self.byteList = byte_list
    self.unpack_from_bytes()

  def pack_to_bytes(self):
    if not self.number:
      raise ValueError, 'self.number is missing.'
    self.byteList = pack_byte_int(self.number, self.n_of_bytes)
    #print 'pack_to_bytes(self):', self.byteList

  def unpack_from_bytes(self):
    if not self.byteList:
      errmsg = 'self.byteList is missing.'
      raise ValueError(errmsg)
    self.number = unpack_byte_int(self.byteList, self.n_of_bytes)

  def set_file_obj(self, file_obj, read_mode=False):
    if read_mode:
      self.read_mode  = True
      self.write_mode = False
    else:
      self.read_mode  = False
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
  '''
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

  '''
  if number < 0:
    errmsg = 'Only unsigned int numbers are allowed.'
    raise ValueError(errmsg)
  max_unsigned_int_here = 2 ** (n_of_bytes * 8) - 1
  if number > max_unsigned_int_here:
    errmsg = 'number is greater than max_unsigned_int_here.'
    raise ValueError(errmsg)
  #mask = get_mask(nOfBytes)
  bytes = [0] * n_of_bytes; mask = 255
  for i in range(n_of_bytes):
    chunk = number & mask
    mask = mask << 8 # from 11111111 to 1111111100000000 and so
    shift_left = 8*i
    chunk = chunk >> shift_left
    bytes[i] = chr(chunk)
  return bytes


def unpack_byte_int(byteList, nOfBytes):
  if len(byteList) > nOfBytes:
    errmsg = 'number is greater than maxUnsignedIntHere.'
    raise ValueError(errmsg)
  c, out_number = 0, 0
  for i in range(len(byteList)):
    sub_number = ord(byteList[i])
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




def minNOfBits(n):
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

def packJogoToBinaryDecRepr(dezenas, nOfBits):
  n = len(jogo)
  #nOfBits = log2(
  stuff = 0
  for dezena in dezenas:
    n -= 1
    nc = nOfBits * n
    # print 'nc', nc, 'dezn', dezena, 'n',n
    # shift-left nc bits :: eg. 1 << 5 = 32
    # or 1 << 5 = 1 * 2**5
    # the inverse is 32 >> 5 = 1 or 32 / (2**5) = 1
    trunk = dezena << nc 
    stuff = stuff | trunk
  #print jogo,
  #print stuff
  return stuff

def unpackJogoFromBinaryDecRepr(binaryDecRepr, nDeDezenasSorteadas, nOfBits, maskSortOrReverse=0):
  '''
  The unpack is done in reverse order,
  if order is important, reverse parameter should be passed in as True
  '''
  #print 'binaryDecRepr, nDeDezenasSorteadas, nOfBits'
  #print binaryDecRepr, nDeDezenasSorteadas, nOfBits
  jogo = [-1] * nDeDezenasSorteadas
  # if nOfBits is 5, onesForAndOp should be binary 11111
  # if nOfBits is 3, onesForAndOp should be binary 111, and so on
  onesForAndOp = 2 ** nOfBits - 1
  # parse it backwardly
  for i in range(nDeDezenasSorteadas-1,-1,-1):
    # 31 in binary, is 11111
    # with an AND operation (&), we're throwing everything away except the right-most 5-bits
    # the packing was done in trunks of 5 bits each

    dezena = binaryDecRepr & onesForAndOp
    #print dezena,
    jogo[i] = int(dezena)
    # shift-right 5 bits to get the next 5 bits to the left as loop goes round
    binaryDecRepr = binaryDecRepr >> nOfBits
    #print binaryDecRepr,
  # a first reverse is necess
  return returnJogoTreatingTheOrderOrReverseMask(jogo, maskSortOrReverse)

def returnJogoTreatingTheOrderOrReverseMask(jogo, maskSortOrReverse):
  '''
  maskInOrderAndReverse should be binaries 11 (=3 dec), 10 (=2 dec) or 01 (=1 dec)
  reverse is both a sort() and a reverse()
  '''
  if type(maskSortOrReverse) <> int:
    return jogo
  if maskSortOrReverse not in [0, 1, 2]:
    return jogo
  putInOrder = maskSortOrReverse >> 1 & 1
  reverse    = maskSortOrReverse & 1
  #print 'putInOrder', putInOrder, 'reverse', reverse, 'maskSortOrReverse'
  #print 'jogo', jogo
  if putInOrder:
    jogo.sort()
  if reverse:
    jogo.sort()
    jogo.reverse()
  return jogo

def chargeBetFileIntoBinDecReprDict(fileIn='jogosfs-bet.txt'):
  nOfLines  = 0
  jogosBetFile = open(fileIn)
  print 'Counting lines and charging jogosfs into dict, please wait.'
  line = jogosBetFile.readline(); binDecReprJogosDict = {}
  while line:
    nOfLines += 1
    if nOfLines % 100000 == 0:
      print nOfLines, ' ... ',
    jogoLine = JogoLine(line)
    binDecRepr = jogoLine.getBinDecRepr()
    # all binDecReprJogos receive, initially, 1
    binDecReprJogosDict[binDecRepr] = 1
    line = jogosBetFile.readline()
  print 'nOfLines', nOfLines
  print 'len(binDecReprJogosDict)', len(binDecReprJogosDict)
  jogosBetFile.close()
  return binDecReprJogosDict

def filter11Out(binDecReprJogosDict):
  '''
  Enter dict
  Goes out list
  '''
  binDecReprJogos = binDecReprJogosDict.keys()
  # save some memory if possible
  del binDecReprJogosDict
  print 'start sort binDecReprJogos', time.ctime()
  binDecReprJogos.sort()
  print 'finish sort binDecReprJogos', time.ctime()
  nOfExcluded = 0; i=0
  dynSize = len(binDecReprJogos)
  while i < dynSize - 1:
    binDecReprJogoI = binDecReprJogos[i]
    #if binDecReprJogosDict[binDecReprJogoI] == 0:
      #continue
    jogoLineI = JogoLine(None,None,binDecReprJogoI)
    for j  in range(i+1, dynSize):
      binDecReprJogoJ = binDecReprJogos[j]
      #if binDecReprJogosDict[binDecReprJogoJ] == 0:
        #continue
      jogoLineJ = JogoLine(None,None,binDecReprJogoJ)
      r = has11OrMoreCoincs(jogoLineI.jogo, jogoLineJ.jogo)
      if r:
        del binDecReprJogos[i]
        #binDecReprJogosDict[binDecReprJogoJ] = 0
        nOfExcluded+=1
        #print 0,
        i-=1
        break
      else:
        pass
        #print 1,
      if nOfExcluded % 10000 == 0:
        print 'excl', nOfExcluded,
    dynSize = len(binDecReprJogos)
    i+=1
  print 'nOfExcluded', nOfExcluded
  return binDecReprJogos


def recordNewBetFile(binDecReprJogos, fileOut='jogosfs-bet-mantidos.txt'):
  mantemFile = open(fileOut,'w')
  nOfExcluded = 0
  for binDecReprJogo in binDecReprJogos:
    jogoLine = JogoLine(None,None,binDecReprJogo)
    line = jogoLine.getLine() + '\n'
    mantemFile.write(line)
  mantemFile.close()

def queueTasks(fileIn='jogosfs-bet.txt'):
  binDecReprJogosDict = chargeBetFileIntoBinDecReprDict(fileIn)
  binDecReprJogos = filter11OutImpl2(binDecReprJogosDict)
  # save some memory if possible
  del binDecReprJogosDict
  recordNewBetFile(binDecReprJogos)

def generateSampleBet(quant):
  print 'generate_sample_bet()'
  jogosBetFile = open('jogosfs-bet.txt')
  jogosSampleBetFile = open('sample-jogosfs-bet.txt','w')
  line = jogosBetFile.readline(); nOfLines = 0
  while line and nOfLines < quant:
    nOfLines += 1
    jogosSampleBetFile.write(line)
  jogosSampleBetFile.close()

'''
def testPackAndUnpack():
  jogosObj = LFClasses.getJogosObj()
  jogo = jogosObj.getJogos()[0]
  stuff = packJogoToBinaryDecRepr(jogo)
  dezenas = unpackJogoFromBinaryDecRepr(stuff)
  print dezenas
  jogo = jogosObj.getJogos()[-1]
  stuff = packJogoToBinaryDecRepr(jogo)
  dezenas = unpackJogoFromBinaryDecRepr(stuff)
  print dezenas  
'''
def testMinNOfBits():
  n = 25; expect = 5
  r = minNOfBits(n)
  print 'minNOfBits(',n,') ==>>', r
  assert(r == expect)
  # =====================================
  n = 60; expect = 6
  r = minNOfBits(n)
  print 'minNOfBits(',n,') ==>>', r
  assert(r == expect)
  # =====================================
  n = 1024; expect = 10
  r = minNOfBits(n)
  print 'minNOfBits(',n,') ==>>', r
  assert(r == expect)
  # =====================================
  n = 1; expect = 1
  r = minNOfBits(n)
  print 'minNOfBits(',n,') ==>>', r
  assert(r == expect)
  # =====================================
  n = 0; expect = 0
  r = minNOfBits(n)
  print 'minNOfBits(',n,') ==>>', r
  assert(r == expect)
  # =====================================
  n = -1; expect = None
  r = minNOfBits(n)
  print 'minNOfBits(',n,') ==>>', r
  assert(r == expect)
  # =====================================


#import csv, os, pickle

'''# establish where data file is located
dataDir = '..' + os.sep + 'Dados'
csvFile='D_LOTFAC.csv'
csvPath=os.path.join(dataDir, csvFile)

def readDataIntoTable2():
***
  Main routine to read jogosfs data from the csv file
***
  pReader = csv.reader(open(csvPath), dialect='excel', delimiter=';', quotechar='|')
  rowCount = 0; fields=None; table = []
  for row in pReader:

'''

def sweepCoincidencesInJogosConsecutives(jogos):
  '''
  Run thru jogosfs, calculating consecutive coincidences
  '''
  acum = 0; coincMin = 25; coincMax = 0
  for i in range(1,len(jogos)):
    jogo = jogos[i]
    jogoPrevious = jogos[i-1]
    nOfCoinc = getNOfCoincidences(jogo, jogoPrevious)
    print pprint(jogo), 'nOfCoinc', nOfCoinc
    acum += nOfCoinc
    if nOfCoinc < coincMin:
      coincMin = nOfCoinc
    if nOfCoinc > coincMax:
      coincMax = nOfCoinc
  average = acum / (0.0 + len(jogos) - 1)
  print 'average', average
  print 'min coinc', coincMin
  print 'max coinc', coincMax
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

def adhoc_test():
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

import unittest
class MyTest(unittest.TestCase):

  def test_1(self):
    pass

def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()
    elif arg.startswith('-u'):
      # unittest complains if argument is available, so remove it from sys.argv
      del sys.argv[1]
      unittest.main()


if __name__ == '__main__':
  look_for_adhoctest_arg()
