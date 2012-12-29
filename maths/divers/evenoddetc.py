#!/usr/bin/env python
# -*- coding: utf-8 -*-

def evenOddTrip(n, counter=1):
  '''
  This recursive function implements a "trip" algorithm, ie, every n > 1 will "trip" towards 1
  
  if n is even, n is divided by 2, the result feeds back to this algorithm
  if n is odd, n is multiplied by 3 and added by 1, again, result goes back to the algorithm

  Examples:

  Recurse(10)
    10 , 5 , 16 , 8 , 4 , 2 , 1 , It took  7 iterations
  Recurse(11)
    11 , 34 , 17 , 52 , 26 , 13 , 40 , 20 , 10 , 5 , 16 , 8 , 4 , 2 , 1 , It took  15 iterations
  Recurse(15)
    15 , 46 , 23 , 70 , 35 , 106 , 53 , 160 , 80 , 40 , 20 , 10 , 5 , 16 , 8 , 4 , 2 , 1 , It took  18 iterations
  Recurse(32)
    32 , 16 , 8 , 4 , 2 , 1 , It took  6 iterations
  '''
  print n, ',',
  if n == 1:    # halt !
    return counter
  if n % 2 == 0: # ie, n is even
    return evenOddTrip(n/2, counter+1)
  else: # ie, n is odd  
    return evenOddTrip(3*n+1, counter+1)

def evenOddTripStart(n):
  try:
    n = int(n)
  except ValueError:
    return 0
  if n < 1:    
    return 0
  return evenOddTrip(n)

def process():
  numbers = [10, 9, 11, 15, 33, 24, 32]
  for n in numbers:
    print 'Recurse(%d)' %n
    n_iterations = evenOddTripStart(n) 
    print 'It took ', n_iterations, 'iterations'
  
if __name__ == '__main__':
  process()
