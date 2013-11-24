#!/usr/bin/env python
import wx

TRAY_TOOLTIP = 'System Tray Demo'
TRAY_ICON = 'icon.png'

class TaskBarIcon(wx.TaskBarIcon):
	Money=0
	def __init__(self):
		super(TaskBarIcon, self).__init__()
		self.set_icon(TRAY_ICON)

	def set_icon(self, path):
		icon = wx.IconFromBitmap(wx.Bitmap(path))
		tt="Won $"+str(self.Money)+" so far!"
		self.SetIcon(icon, tt)
		
	def update(self, money):
		self.Money=money
		self.set_icon(TRAY_ICON)

app = wx.PySimpleApp()
icon=TaskBarIcon()

def main():
	app.MainLoop()

def update(money):
	icon.update(money)

def registerOnClick(function):
	icon.Bind(wx.EVT_TASKBAR_LEFT_DOWN, function)
