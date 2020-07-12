import tkinter as tk
import datetime

class _cratesWindow:
  def __init__(self, app):
    self.app = app
  def show(self):
    self.window = tk.Tk()
    self.window.title("Crates")
    self.window.resizable(False, False)
    self.window.geometry("250x200")
    crates = self.app.accountManager.crafting.crates()
    tk.Label(self.window).grid(row=0, column=1, sticky=tk.W)
    tk.Label(self.window, text="Type").grid(row=0, column=1, sticky =tk.N)
    tk.Label(self.window, text="Status").grid(row=0, column=2, sticky=tk.N)
    for index,crate in enumerate(crates):
      square_icon = tk.Canvas(self.window, width=15, height=15)
      square_icon.grid(row=index+1, column=0, sticky=tk.W)
      if crate['type'] == "platinum":
        square_icon.create_rectangle(0, 0, 15, 15, fill="black")
      elif crate['type'] == "gold":
        square_icon.create_rectangle(0, 0, 15, 15, fill="yellow")
      elif crate['type'] == "silver":
        square_icon.create_rectangle(0, 0, 15, 15, fill="silver")
      elif crate['type'] == "common":
        square_icon.create_rectangle(0, 0, 15, 15, fill="white")
      tk.Label(self.window, text="{}".format(crate['type'].capitalize())).grid(row=index+1, column=1, sticky=tk.W)
      tk.Label(self.window, text=f"{self._crateState(crate)}").grid(row=index+1, column=2, sticky=tk.W)
  def _crateDate(self,endedAt):
    if endedAt > 0:
      return f"Opens in {datetime.timedelta(seconds=endedAt)}"
    else:
      return "Crate Open"
  def _crateState(self,crate):
    if crate['state'] == "new":
      return "New"
    return self._crateDate(crate['ended_at'])
