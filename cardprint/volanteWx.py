#!/usr/bin/env python
#-*-coding:utf8-*-
'''
wx01
'''
#import os, sys
import wx

class MyFrame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, None, -1, "My Frame", size=(300,300))
    panel = wx.Panel(self, -1)
    panel.Bind(wx.EVT_MOTION, self.OnMove)