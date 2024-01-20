#!/usr/bin/env python3
"""
fs/mathfs/combinatorics/adhoctests_combinatoric_algorithms.py
  Contains "adhoc test functions" to combinatoric_algorithms.py in the same folder (package)

Main functions here:
  -- permute(arrayN)
  -- geraSumComponents(soma, parcel=-1, acc=[])
     Generates Integer Partitions
     (look for further explanation on the comments at the beginning of the function below)
  -- getTilPatternsFor(patternSize=10, patternSoma=6)
     Uses geraSumComponents(patternSoma) then it stuffs zeroes
     and filters out larger strings than patternSize
"""
import fs.mathfs.combinatorics.combinatoric_algorithms as ca  # .RCombiner


def adhoc_test1():
  """
    geraSumComponents(soma, parcel=-1, acc=[])
  """
  n = 3
  rc = ca.RCombiner(n)
  scrmsg = f"""adhoctest for geraSumComponents(soma, parcel=-1, acc=[])
  rc = ca.RCombiner({n}) => output {rc}"""
  print(scrmsg)
  n = 4
  rc = ca.RCombiner(n)
  scrmsg = f"""adhoctest for geraSumComponents(soma, parcel=-1, acc=[])
  rc = ca.RCombiner({n}) => output {rc}"""
  print(scrmsg)


def adhoc_test2():
  """
    getTilPatternsFor
  """
  res = ca.get_TilPatternsFor()


def adhoc_test3():
  """
  random_permutation(perm)
  """
  res = ca.random_permutation()
  print(res)


def adhoc_test4():
  #def test_generate_integer_partitions():
  """
  5 R: [[5], [4, 1], [3, 2], [3, 1, 1], [2, 2, 1], [2, 1, 1, 1], [1, 1, 1, 1, 1]]
  """
  for soma in range(5,6):
    acc = generate_integer_partitions(soma, soma, [])
    # check it up
    for elem in acc:
      calc_soma = sum(elem)
      if soma != calc_soma:
        scrmsg = f'soma {soma} != sum(elem) = {calc_soma}'
        print(scrmsg)
    scrmsg = f"soma {R} {acc}"
    print(scrmsg)

  
def adhoc_tests_show():
  scrmsg = '''
    combinatoric_algorithms.py -t <n>
      Where <n> is
    1 for test1: testAdHocRCombiner()
    2 for test2: testAdHocRandomPermutation()
    3 for test3: testAdHocPermuteN(arrayN=range[3])
    4 for test4: test_generate_integer_partitions()
  '''
  print(scrmsg)


def adhoc_test():
  try:
    if sys.argv[2]=='showtests':
      return adhoc_tests_show()
    n_test = int(sys.argv[2])
    print( 'Executing test', n_test)
    funcname = 'list_dist_xysum_metric_thry_ms_history%d()' %n_test
    exec(funcname)
    return
  except (IndexError, ValueError):
    pass
  adhoc_test1()


def process():
  adhoc_test1()


if __name__ == '__main__':
  """
  """
  process()
