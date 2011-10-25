#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime #,  sys
import BeautifulSoup as bf


def columnMapping():
  # html name versus sql name
  htmlColumns = '''
  
  '''


htmlDataFile = 'mega.htm'
text = open(htmlDataFile).read()
bsObj = bf.BeautifulSoup(text)



