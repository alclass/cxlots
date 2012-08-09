#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
'''
import os
print os.getcwd() 
relpath = os.path.dirname(__file__)
abspath = os.path.abspath(relpath)
print abspath 
