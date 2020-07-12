import tkinter as tk
from tkinter import ttk

class _resourcesWindow:
  def __init__(self, app):
    self.app = app
  def show(self):
    self.window = tk.Tk()
    self.window.title("Resources")
    self.window.resizable(False, False)
    self.window.geometry("225x130")
    resources = self.app.accountManager.crafting.resources()
    level1=resources[0]['amount']
    level2=resources[1]['amount']
    level3=resources[2]['amount']
    level4=resources[3]['amount']
    level5=resources[4]['amount']

    current_res_labels = ttk.Labelframe(self.window, text='Current Resources')
    current_res_labels.grid(row=0, column=0, sticky=tk.W)
    tk.Label(current_res_labels, text=f"Level 1: {level1}").grid(row=0, column=0, sticky=tk.W)
    tk.Label(current_res_labels, text=f"Level 2: {level2}").grid(row=1, column=0, sticky=tk.W)
    tk.Label(current_res_labels, text=f"Level 3: {level3}").grid(row=2, column=0, sticky=tk.W)
    tk.Label(current_res_labels, text=f"Level 4: {level4}").grid(row=3, column=0, sticky=tk.W)
    tk.Label(current_res_labels, text=f"Level 5: {level5}").grid(row=4, column=0, sticky=tk.W)

    tk.Label(self.window).grid(row=0, column=1, sticky=tk.W) #Space

    converted_res = ttk.Labelframe(self.window, text='If all converted')
    converted_res.grid(row=0, column=2, sticky=tk.W)
    tk.Label(converted_res, text=f"Level 1: {level1%50}").grid(row=0, column=0, sticky=tk.W)
    level2 = level2 + int(level1/50)
    tk.Label(converted_res, text=f"Level 2: {level2%50}").grid(row=1, column=0, sticky=tk.W)
    level3 = level3 + int(level2/50)
    tk.Label(converted_res, text=f"Level 3: {level3%35}").grid(row=2, column=0, sticky=tk.W)
    level4 = level4 + int(level3/35)
    tk.Label(converted_res, text=f"Level 4: {level4%25}").grid(row=3, column=0, sticky=tk.W)
    level5 = level5 + int(level4/25)
    tk.Label(converted_res, text=f"Level 5: {level5}").grid(row=4, column=0, sticky=tk.W)