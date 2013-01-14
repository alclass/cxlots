#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Dict2(dict):
  def add1_or_set1_to_key(self, k):
    if self.has_key(k):
      self[k]+=1
    else:
      self[k]=1


if __name__ == '__main__':
  pass
