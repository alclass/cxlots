#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import __init__
__init__.setlocalpythonpath()

import maths.combinatorics.algorithmsForCombinatorics as combinatorics


def sumDigits(pattern):
  '''
  This function sums a sequence of numbers in a string or an iterator from which int(element) is possible
  From the context of cxlots, its function is to sum up the digits in a pattern string
  Eg
  '10221' will sum as follows: 1+0+2+2+1=6
  '''
  if pattern == None:
    return None
  # in the future, refactor this part to test for an iterator, instead of str, list or tuple
  if type(pattern) not in [str, list, tuple]:
    return None
  soma = 0
  for c in pattern:
    try:
      soma += int(c)
    except ValueError:
      return None
  return soma


def getTilPatternsFor(patternSize=10, patternSoma=6):
  '''
  The Til Patterns are found with the help of finding first the "Integer Partitions"
  Once having found the "Integer Partitions", two operations are called, ie:
  1) stuff the patterns with less than patternSize with 0 (zeros)
  2) those patterns that are greater in size than patternSize are filtered out
  The result set corresponds to the wanted Til Patterns
  
  Eg.
  eg1 getTilPatternsFor(patternSize=2, patternSoma=3) results in a 7-element array, ie:
  ----------------------------  
  06  60  15  51  24  42  33
  ----------------------------  
  
  eg1 getTilPatternsFor(patternSize=5, patternSoma=6) results in a 210-element array, ie:
  ----------------------------  
  00006 00060 00600 06000 60000 00015 00051 00105 00150 00501 00510 01005 01050 01500 05001
  05010 05100 10005 10050 10500 15000 50001 50010 50100 51000 00024 00042 00204 00240 00402
  00420 02004 02040 02400 04002 04020 04200 20004 20040 20400 24000 40002 40020 40200 42000
  00114 00141 00411 01014 01041 01104 01140 01401 01410 04011 04101 04110 10014 10041 10104
  10140 10401 10410 11004 11040 11400 14001 14010 14100 40011 40101 40110 41001 41010 41100
  00033 00303 00330 03003 03030 03300 30003 30030 30300 33000 00123 00132 00213 00231 00312
  00321 01023 01032 01203 01230 01302 01320 02013 02031 02103 02130 02301 02310 03012 03021
  03102 03120 03201 03210 10023 10032 10203 10230 10302 10320 12003 12030 12300 13002 13020
  13200 20013 20031 20103 20130 20301 20310 21003 21030 21300 23001 23010 23100 30012 30021
  30102 30120 30201 30210 31002 31020 31200 32001 32010 32100 01113 01131 01311 03111 10113
  10131 10311 11013 11031 11103 11130 11301 11310 13011 13101 13110 30111 31011 31101 31110
  00222 02022 02202 02220 20022 20202 20220 22002 22020 22200 01122 01212 01221 02112 02121
  02211 10122 10212 10221 11022 11202 11220 12012 12021 12102 12120 12201 12210 20112 20121
  20211 21012 21021 21102 21120 21201 21210 22011 22101 22110 11112 11121 11211 12111 21111
  ----------------------------  
  
  '''
  subtokens = combinatorics.geraSumComponents(6)
  subtokens = combinatorics.sumComponentsToListOfStrs(subtokens)
  subtokens = combinatorics.stuffStrWithZeros(subtokens, patternSize)
  subtokens = combinatorics.filterOutStringsGreaterThanSize(subtokens, patternSize)
  return combinatorics.getPermutations(subtokens)


import unittest
class Test(unittest.TestCase):
  def test_sumDigits(self):
    expected = 6 # eg 1+0+2+2+1=6
    for pattern in ['10221', '11112', '600000000', '111111','0000000000000051']:
      self.assertEqual(sumDigits(pattern), expected)
    for pattern in ['310221', '911112', '1600000000', '9111111','30000000000000051', '0']:
      # expected is still the same above, ie 6
      self.assertNotEqual(sumDigits(pattern), expected)
    for pattern in ['a10221', 'string', 1.23, ['blah','blah'],'-1','+0']:
      self.assertIsNone(sumDigits(pattern))

def adhoc_test():
  patternSize=4; patternSoma=6
  tilpatterns = getTilPatternsFor(patternSize, patternSoma)
  print 'tilpatterns', tilpatterns
  print 'size', len(tilpatterns) 
  patternSize=10; patternSoma=6
  tilpatterns = getTilPatternsFor(patternSize, patternSoma)
  # print 'tilpatterns', tilpatterns
  print 'size', len(tilpatterns) 

def look_for_adhoctest_arg():
  for arg in sys.argv:
    if arg.startswith('-t'):
      adhoc_test()
    elif arg.startswith('-u'):
      # unittest complains if arguments are not the ones expected by itself
      del sys.argv[1:]
      unittest.main()

if __name__ == '__main__':
  look_for_adhoctest_arg()
