#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

a=1
import funcsForBinDecRepr as binDec
'''
#import Numeric as N
import numpy # as N
import array

import numpy # from numpy import *
from scipy.io import write_array
from scipy.io import read_array
from pylab import load           # warning, the load() function of numpy will be shadowed
from pylab import save
'''

def m1():
  data = numpy.zeros((3,3))
  #write_array("myfile.txt", data)
  #data = read_array(file("myfile.txt"))
  numpy.savetxt('myfile.txt', data)
  rd = numpy.loadtxt("myfile.txt")
  print 'rd', rd

#import scipy # from scipy.io.numpyio import fwrite, fread
def m2():
  data = numpy.zeros((3,3), int)
  print 'data', data
  #write:
  fd = open('myfile.dat', 'wb')
  scipy.io.numpyio.fwrite(fd, data.size, data)
  fd.close()
  #read:
  fd = open('myfile.dat', 'rb')
  datatype = 'i'
  size = 9
  shape = (3,3)
  read_data = scipy.io.numpyio.fread(fd, size, datatype)
  read_data = data.reshape(shape)
  print 'read_data', read_data

import random
def rand():
  n = random.randint(0,9)
  print 'n', n
  return n

def m3():
  fd = open('myfile.dat', 'wb')
  for i in range(10):
    n = rand()
    scipy.io.numpyio.fwrite(fd, 1, n)
  fd.close()
  #read:
  fd = open('myfile.dat', 'rb')
  read_data = scipy.io.numpyio.fread(fd, 1, 'i')
  print 'read_data', read_data

  read_data = scipy.io.numpyio.fread(fd, 1, 'i')
  print 'read_data', read_data

mask = [0]*4
mask[0] = 2**8 - 1 # ie, 255
for i in range(1,4):
  mask[i] = mask[i-1] << 8 

maxInt = 2**16 - 1
import IndicesCombiner
c25to15 = IndicesCombiner.comb(25,15)

def m4():
  randomLgis = []
  tmpfile = "tmp.bin"
  fileobj = open(tmpfile, 'wb')
  nOfBytes = 3
  
  for i in range(5):
    lgi = random.randint(0,c25to15)
    randomLgis.append(lgi)
    print 'lgi', lgi
    bytes = binDec.packByteInt(lgi, nOfBytes)
    for byte in bytes:
      #print 'byte', byte
      fileobj.write(chr(byte))
  print
  fileobj.close()

  # getting them back
  print 'getting them back'
  fileobj = open(tmpfile, 'rb')
  allbytes = fileobj.read(); c=0; composed = 0
  bytes = []; i=0
  for byte in allbytes:
    bytes.append(byte)
    if len(bytes) == 3:
      outNumber = unpackByteInt(bytes, nOfBytes)
      print 'outNumber', outNumber
      print 'lgi', randomLgis[i]
      i+=1
      bytes = []
  print

def m5():
  i=0
  while 1:
    i+=1
    p=22*i
    if p % 8 == 0:
      d = p / 8
      print 'found i=', i,'p =',p, 'd =', d
      break

import math
def m6():
  # math.e
  # log 2 x = log e x / log e 2
  r = math.log(c25to15) / math.log(2)
  print 'log 2 (c25to15 =', c25to15, ') =', r

def m7():
  ip = binDec.IntPacker(3)
  fileobj = open('tmp.bin', 'wb')
  ip.setFileObj(fileobj) # readMode is defaulted to False
  for i in range(5):
    lgi = random.randint(0,c25to15)
    print i, 'lgi', lgi
    ip.setNumber(lgi)
    ip.write()

  fileobj.close()
  fileobj = open('tmp.bin', 'rb')
  ip.setFileObj(fileobj, True) # readMode now
  for i in range(5):
    number = ip.read()
    print i,'number', number
  number = ip.read()
  print i,'number', number
  number = ip.read()
  print i,'number', number


if __name__ == "__main__":
  m7()
