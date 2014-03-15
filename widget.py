#!/usr/bin/env python
import wx

TRAY_TOOLTIP = 'System Tray Demo'

def create_menu_item(menu, label, func):
	item = wx.MenuItem(menu, -1, label)
	menu.Bind(wx.EVT_MENU, func, id=item.GetId())
	menu.AppendItem(item)
	return item

class TaskBarIcon(wx.TaskBarIcon):
	TRAY_ICON='icon.png'
	Money=0
	def __init__(self):
		super(TaskBarIcon, self).__init__()
		self.set_icon(self.TRAY_ICON)

	def set_icon(self, path):
		icon = wx.IconFromBitmap(wx.Bitmap(path))
		tt="Won $"+str(self.Money)+" so far!"
		self.SetIcon(icon, tt)
		
	def update(self, money):
		self.Money=money
		self.set_icon(self.TRAY_ICON)
		
	def CreatePopupMenu(self):
		menu = wx.Menu()
		menu.AppendSeparator()
		create_menu_item(menu, 'Exit', self.Exit)
		return menu
	
	def Exit(self, anything=None):
		wx.CallAfter(killItWithFire)


class TaskBarFrame(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, style=wx.FRAME_NO_TASKBAR | wx.NO_FULL_REPAINT_ON_RESIZE)
		self.icon_state = False
		self.blink_state = False

		self.tbicon = TaskBarIcon()
		icon = wx.Icon('icon.png', desiredWidth=22, desiredHeight=22)
		self.tbicon.SetIcon(icon, '')
		wx.EVT_TASKBAR_RIGHT_UP(self.tbicon, self.OnTaskBarRightClick)
		self.Show(True) 

	def OnTaskBarRightClick(self, evt):
		self.Close(True)
		wx.GetApp().ProcessIdle()

app = wx.App(False)
#frame = TaskBarFrame(None)
#frame.Show(True)
icon=TaskBarIcon()

def main():
	app.MainLoop()

def killItWithFire():
	icon.Destroy()
	app.Destroy()
	app.ExitMainLoop()

def update(money):
	#print money
	icon.update(money)

def registerOnClick(function):
	icon.Bind(wx.EVT_TASKBAR_LEFT_DOWN, function)
