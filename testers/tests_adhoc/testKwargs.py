#!/usr/bin/env python
#-*-coding:utf8-*-

def funct(*args, **kwargs):
  print args, kwargs

dic = {1:'a',2:'b'}
funct(dic='abc')
