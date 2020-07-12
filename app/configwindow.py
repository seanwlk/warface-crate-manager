import tkinter as tk
from tkinter import ttk

class _ConfigWindow:
  def __init__(self, app):
    self.app = app
  def _boolToInt(self,v):
    return 1 if v else 0
  def show(self):
    self.window = tk.Tk()
    self.window.title("Config")
    self.window.resizable(False, False)
    self.window.geometry("250x170")
    self.v_autoCrateOpen = tk.IntVar(master=self.window)
    self.v_checkTaskCompletion = tk.IntVar(master=self.window)
    self.v_freeCrateOpen = tk.IntVar(master=self.window)
    self.v_notifications = tk.IntVar(master=self.window)
    
    if "autoCrateOpen" in self.app.configs.get("configs"):
      self.v_autoCrateOpen.set(self._boolToInt(self.app.configs.get("configs")['autoCrateOpen']))
    else:
      self.v_autoCrateOpen.set(0)
    if "checkTaskCompletion" in self.app.configs.get("configs"):
      self.v_checkTaskCompletion.set(self._boolToInt(self.app.configs.get("configs")['checkTaskCompletion']))
    else:
      self.v_autoCrateOpen.set(0)
    if "freeCrateOpen" in self.app.configs.get("configs"):
      self.v_freeCrateOpen.set(self._boolToInt(self.app.configs.get("configs")['freeCrateOpen']))
    else:
      self.v_autoCrateOpen.set(0)
    if "notifications" in self.app.configs.get("configs"):
      self.v_notifications.set(self._boolToInt(self.app.configs.get("configs")['notifications']))
    else:
      self.v_notifications.set(0)

    confFrame = ttk.Labelframe(self.window, text='Configuration panel')
    confFrame.grid(row=0,columnspan=6,sticky=tk.W)

    tk.Label(confFrame, text="Auto open crates").grid(row=0,column=0,sticky = tk.W)
    _autoCrateOpenSelector = tk.Frame(confFrame)
    _autoCrateOpenSelector.grid(row=0, column=1,sticky = tk.E)
    tk.Radiobutton(_autoCrateOpenSelector, text="On", variable=self.v_autoCrateOpen, value=1).grid(row=0,column=0,sticky = tk.W)
    tk.Radiobutton(_autoCrateOpenSelector, text="Off", variable=self.v_autoCrateOpen, value=0).grid(row=0,column=1,sticky = tk.W)

    tk.Label(confFrame, text="Check task completion").grid(row=1,column=0,sticky = tk.W)
    _checkTaskCompletionSelector = tk.Frame(confFrame)
    _checkTaskCompletionSelector.grid(row=1, column=1,sticky = tk.E)
    tk.Radiobutton(_checkTaskCompletionSelector, text="On", variable=self.v_checkTaskCompletion, value=1).grid(row=0,column=0,sticky = tk.W)
    tk.Radiobutton(_checkTaskCompletionSelector, text="Off", variable=self.v_checkTaskCompletion, value=0).grid(row=0,column=1,sticky = tk.W)

    tk.Label(confFrame, text="Gorgona free crate opener").grid(row=2,column=0,sticky = tk.W)
    _freeCrateOpenSelector = tk.Frame(confFrame)
    _freeCrateOpenSelector.grid(row=2, column=1,sticky = tk.E)
    tk.Radiobutton(_freeCrateOpenSelector, text="On", variable=self.v_freeCrateOpen, value=1).grid(row=0,column=0,sticky = tk.W)
    tk.Radiobutton(_freeCrateOpenSelector, text="Off", variable=self.v_freeCrateOpen, value=0).grid(row=0,column=1,sticky = tk.W)

    tk.Label(confFrame, text="Notifications").grid(row=3,column=0,sticky = tk.W)
    _notificationsSelector = tk.Frame(confFrame)
    _notificationsSelector.grid(row=3, column=1,sticky = tk.E)
    tk.Radiobutton(_notificationsSelector, text="On", variable=self.v_notifications, value=1).grid(row=0,column=0,sticky = tk.W)
    tk.Radiobutton(_notificationsSelector, text="Off", variable=self.v_notifications, value=0).grid(row=0,column=1,sticky = tk.W)

    tk.Label(self.window).grid(row=1,column=0,sticky = tk.W)
    tk.Button(self.window, bd =2,text='Save',command=self.saveConf).grid(row=2,column=0,columnspan=6,sticky = tk.S)
    self.window.bind('<Return>',self.saveConf)
  def saveConf(self,*args):
    cfg = {
      "autoCrateOpen" : True if self.v_autoCrateOpen.get() == 1 else False,
      "checkTaskCompletion" : True if self.v_checkTaskCompletion.get() == 1 else False,
      "freeCrateOpen" : True if self.v_freeCrateOpen.get() == 1 else False,
      "notifications" : True if self.v_notifications.get() == 1 else False
    }
    self.app.configs.set("configs",cfg)
    self.window.destroy()