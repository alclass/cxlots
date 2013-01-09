# -*- coding: utf-8 -*-
'''

This functionality in this package-signal __init__.py module, previously was put in localpythonpath.py

Some source code modules have been commented: 

#import localpythonpath
#localpythonpath.setlocalpythonpath()

# New importing code:
import __init__
__init__.setlocalpythonpath()


This module is imported, from package to package across the application, 
 being copied to all folder packages, 
 to find and set the Application's Root Python Path

Restriction: a calling module cannot be at a depth more than 4 folders away from the application's root,
ie, the longest "distance" is: appsdir/folder1/folder12/folder13/folder14/

This code allows application to be run if it's moved to a different absolute directory path.
'''
import os, sys

# print 'at __init__.py'

def add_path_if_not_already_added(relpath):
  if relpath not in sys.path:
    sys.path.insert(0, relpath)
  try:
    import appspythonpath  # importing will run sys.path globally on localpythonpath module
    appspythonpath.set_appspythonpath()
    return
  except ImportError:
    error_msg = "Could not find appspythonpath.setappspythonpath() to set the application's root folder. This error should only happen during software development, never in use.  Please, contact development team."
    raise ImportError, error_msg

def setlocalpythonpath():
  for relpath in ['.', '..', '../..', '../../..', '../../../..']:
    filepath = relpath + '/' + 'appspythonpath.py'
    if os.path.isfile(filepath):
      # found local_settings.py, add, if it's not already there, its path to sys.path
      add_path_if_not_already_added(relpath)
      return

# setlocalpythonpath()
