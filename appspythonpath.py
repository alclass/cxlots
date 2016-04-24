# -*- coding: utf-8 -*-
# local_settings.py
'''
This module should exist only on the Application's Root Folder
Its purpose is to set the Application's Root absolute directory path to the PYTHON PATH,
so that this path is known everywhere within the application, ie, all modules may import other modules within the application.
'''

import os, sys

def set_appspythonpath():
  root_folder_relpath = os.path.dirname(__file__)
  app_root_abspath = os.path.abspath(root_folder_relpath)
  if app_root_abspath not in sys.path:
    sys.path.insert(0, app_root_abspath)

