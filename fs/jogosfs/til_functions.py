#!/usr/bin/env python3
"""
fs/jogosfs/til_functions.py

"""
import fs.mathfs.combinatorics.combinatoric_algorithms as combinatorics


def sum_digits(pattern):
  """
  This function sums a sequence of numbers in a string or
    in an iterator from which int(element) is possible
  From the context of cxlots, its function is to sum up
    the digits in a pattern string

  Example:
  '10221' will sum as follows: 1+0+2+2+1=6
  """
  # in the future, refactor this part to test it for an iterator,
  # instead of str, list or tuple
  if pattern is None or type(pattern) not in [str, list, tuple]:
    return None
  try:
    int_pattern = [int(c) for c in pattern]
    soma = sum(int_pattern)
    return soma
  except ValueError:
    return None
  # errmsg = 'Program flow logical error in function sum_digits() :: pattern = %s ' % str(pattern)
  # raise ValueError(errmsg)


def get_all_possible_til_patterns_for(elemsum=6, n_slots=5):
  """
  The Til Patterns are found with the help of finding first the "Integer Partitions"
    @see module combinations.py

  Once having found the "Integer Partitions", two operations are called, ie:
    1) stuff the patterns with less than patternSize with 0 (zeros)
    2) those patterns that are greater in size than patternSize are filtered out
  The result set corresponds to the wanted Til Patterns

  Example:
  eg1 getTilPatternsFor(elemsum=6, n_slots=2) results in a 7-element array, ie:
  ----------------------------  
  06  60  15  51  24  42  33
  ----------------------------  
  eg1 getTilPatternsFor(elemsum=6, n_slots=5) results in a 210-element array, ie:
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
  """
  if n_slots == 0:
    return []
  if n_slots == 1:
    if elemsum < 10:
      return [str(elemsum)]
    else:
      return []
  subtokens = combinatorics.mount_all_integer_partitions_for(elemsum)
  # [[6], [5, 1], [4, 2], [4, 1, 1], [3, 3], [3, 2, 1], [3, 1, 1, 1],
  # [2, 2, 2], [2, 2, 1, 1], [2, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]
  subtokens = ["".join(map(str, subtoken)) for subtoken in subtokens]
  # ['6', '51', '42', '411', '33', '321', '3111', '222', '2211', '21111', '111111']
  subtokens = combinatorics.fill_right_zeroes_to_eachstr_in_list(subtokens, n_slots)
  # ['60000', '51000', '42000', '41100', '33000', '32100', '31110', '22200', '22110', '21111', '111111']
  subtokens = combinatorics.filter_out_strings_greater_than_size(subtokens, n_slots)
  # in the case n_slots=5, only the last one ('111111') is removed because it takes 6 slots
  subtokens = combinatorics.get_permutations(subtokens)
  # ['00006', '00060', '00600', '06000', '60000', '00015', '00051', '00105', '00150', ..., '12111', '21111']
  return subtokens


def adhoctest():
  res = get_all_possible_til_patterns_for(elemsum=6, n_slots=5)
  print(res)
  print('size', len(res))


if __name__ == '__main__':
  """
  @see the adhoctest module (adhoctest_til_functions.py)
  """
  adhoctest()
