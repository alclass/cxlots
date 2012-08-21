# -*- coding: utf-8 -*-
'''
This module is imported, from package to package across the application, being copied to all folder packages, to find and set the Application's Root Python Path

Restriction: a calling module cannot be at a depth more than 4 folders away from the application's root,
ie, the longest "distance" is: appsdir/folder1/folder12/folder13/folder14/

This code allows application to be run if it's moved to a different absolute directory path.
'''
import sys

def setlocalpythonpath():
  for relpath in ['.', '..', '../..', '../../..', '../../../..']:
    try:
      if relpath not in sys.path:
        sys.path.insert(0, relpath)
      import appspythonpath  # importing will run sys.path globally on localpythonpath module
      appspythonpath.set_appspythonpath()
      return
    except ImportError:
      # print 'ImportError:', relpath
      pass
  error_msg = "Could not find appspythonpath.setappspythonpath() to set the application's root folder. This error should only happen during software development, never in use.  Please, contact development team."
  raise ImportError, error_msg

