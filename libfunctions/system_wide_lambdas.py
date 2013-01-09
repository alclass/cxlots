#!/usr/bin/env python
# -*- coding: utf-8 -*-

zfill2              = lambda digit : str(digit).zfill(2)
extract_1st_element = lambda x : x[0]

toInt  = lambda x : int(x)
toStr  = lambda x : str(x)

minusOne = lambda x : x - 1
plusOne  = lambda x : x + 1

greater_than     = lambda value, quant : value >  quant  # para filtro passa-alta 
less_than        = lambda value, quant : value <  quant  # para filtro passa-baixa
greater_or_equal = lambda value, quant : value >= quant  # para filtro passa-alta inclusivo 
less_or_equal    = lambda value, quant : value <= quant  # para filtro passa-baixa inclusivo
is_equal         = lambda value, quant : value == quant  # para filtro passa-igual

greater_than_zero = lambda x : x >  0 # para filtro passa acima de zero 
is_nonzero        = lambda x : x != 0 # para filtro não-passa zero 

is_odd      = lambda x          : x % 2  # when even, 0 (which is also False) returns; when odd, 1 (which is True) returns :: they are used in a filter()
remainder_n = lambda x, divisor : x % divisor

if __name__ == '__main__':
  pass
