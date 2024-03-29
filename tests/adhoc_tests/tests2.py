#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
a=1
import StatClasses
import CLClasses
#import pprint
import IndicesCombiner as ic
#import actions
import takeOut11
import LgiCombiner as lgicomb

def testRefactoredPackUnpack():
  jogo = [1,2,3,4,5,6]
  shouldBeHex = 0x420c4146
  nDeDezenasNoVolante = 60
  nOfBits = takeOut11.min_n_of_bits(nDeDezenasNoVolante)
  print 'nDeDezenasNoVolante', nDeDezenasNoVolante, 'nOfBits', nOfBits
  stuff = takeOut11.pack_jogo_to_binary_dec_repr(jogo, nOfBits)
  print jogo, 'stuff', stuff
  print 'shouldBeHex',  shouldBeHex # 0x820c8186

  jogoUnpacked = takeOut11.unpack_jogo_from_binary_dec_repr(stuff, len(jogo), nOfBits)
  print 'jogoUnpacked', jogoUnpacked

def testBinStr():
  #binStr='1000010000011000100000101000110'
  binStr='1000010000011000100000101'
  #binStr='1000010000011000100'
  soma = 0; exp = 0
  for i in range(len(binStr)):
    index = len(binStr) - 1 - exp
    digit = int(binStr[index])
    parcel = 2**exp * digit
    soma += parcel
    # print digit, parcel, soma
    exp += 1
  print soma, '>> hex', hex(soma)
  binVal = int(binStr)
  r = binVal & 3
  print binVal, ' :: binVal & 3 = ', r


def testJogoObjBinDecRepr():
  jogo = [1,2,3,4,5,6]
  jogoObj = Jogo(jogo, 'MS')
  binDec = jogoObj.getBinDecRepr()
  print jogoObj, 'binDec', binDec
  jogoObj = Jogo(binDec, 'MS')
  print 'inv', jogoObj, 'binDec', binDec
  print '='*40
  jogo = range(1,16,1)
  jogoObj = Jogo(jogo, 'LF')
  binDec = jogoObj.getBinDecRepr()
  print jogoObj, 'binDec', binDec
  jogoObj = Jogo(binDec, 'LF')
  print 'inv', jogoObj, 'binDec', binDec

def testPartialJogos():
  '''
  testPartialJogos()
  testJogoObjBinDecRepr()
  std2letter = 'LF'
  updateBase(std2letter)
  jogosObj = getJogosObj(std2letter)
  jogosfs = jogosObj.getJogos()
  pprint.printJogos(jogosfs)
  '''
  jObj = CLClasses.getJogosObj('LF')
  print 'jObj.standard2LetterName', jObj.standard2LetterName
  print jObj.getHistG()
  partial = PartialJogos('LF')
  print 'partial.standard2...',partial.standard2LetterName
  partial.setAteConcurso(100)
  print partial.getHistG()

def testJogosObj__Str__():
  for loteria in CLClasses.standardNames:
    bObj = CLClasses.Base(loteria)
    print bObj

def testStatClassPrintAttributes():
  jogosObj = CLClasses.getJogosObj('LF')
  stat     = StatClasses.Stat(jogosObj)
  stat.printAttributes()

tmpMinusOne = lambda x : x - 1
def filterMinusOne(jogo):
  newJogo = map(tmpMinusOne, jogo)
  return newJogo
  
def testLgiOf():
  jogo = [10, 8, 7, 5, 3, 2]
  print 'jogo', jogo
  lgiObj = lgicomb.LgiCombiner(ic.iCmb(60, 6) - 1, -1, jogo)
  lgi = lgiObj.get_lgi()
  print 'lgi_b1idx', lgi
  jogo = filterMinusOne(jogo)
  print 'jogo', jogo
  lgiObj = lgicomb.LgiCombiner(ic.iCmb(60, 6) - 1, -1, jogo)
  lgi = lgiObj.get_lgi()
  print 'lgi_b1idx', lgi

def testLgiInJogoClass():
  jogosObj = CLClasses.getJogosObj('LF')
  jogo = jogosObj.getLastJogo()
  print 'jogo', jogo
  jogoObj = CLClasses.ShapeAreaCircleCalculator(jogo, 'LF')
  lgi = jogoObj.get_lgi()

if __name__ == '__main__':
  pass
  testLgiInJogoClass()
  '''
  testLgiOf()
  testJogosObj__Str__()
  testStatClassPrintAttributes()
  testRefactoredPackUnpack()
  testBinStr()
  '''