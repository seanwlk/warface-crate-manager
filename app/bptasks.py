import tkinter as tk
from tkinter import ttk
from app.utils.verticalscrollframe import VerticalScrolledFrame

class _bpTasksWindow:
  def __init__(self, app):
    self.app = app
  def show(self):
    self.window = tk.Tk()
    self.window.title("Battlepass tasks")
    self.window.resizable(True, True)
    self.window.geometry("790x575")
    missionList = VerticalScrolledFrame(self.window)
    missionList.pack(fill="x", expand=True)
    tasks = self.app.accountManager.get("https://$baseurl$/minigames/battlepass/task/all")
    tableFrame = tk.Frame(missionList)
    tableFrame.pack(fill="x", expand=True)
    tk.Label(tableFrame, text="Task").grid(row=0, column=0, sticky=tk.W)
    tk.Label(tableFrame, text="Rewards").grid(row=0, column=1, sticky=tk.W)
    tk.Label(tableFrame, text="Status").grid(row=0, column=2, sticky=tk.W)
    hr = tk.Frame(tableFrame, height=1, width=750, bg="black")
    hr.grid(row=0, columnspan=3, sticky=tk.S)
    for index, task in enumerate(tasks['data']):
      index+=1
      taskFrame = tk.Frame(tableFrame, borderwidth=0, relief=tk.GROOVE, highlightthickness=0, highlightcolor="light grey")
      taskFrame.grid(row=index, column=0, sticky=tk.W)
      tk.Label(taskFrame,text=f"{task['title']}").grid(row=0, sticky=tk.W)
      tk.Label(taskFrame,text="Progress: {progress}/{target_count}".format(**task)).grid(row=1, sticky=tk.W)
      hr = tk.Frame(tableFrame, height=1, width=730, bg="black")
      hr.grid(row=index, columnspan=3, sticky=tk.S)

      rewardFrame = tk.Frame(tableFrame, borderwidth=0, relief=tk.GROOVE, highlightthickness=0, highlightcolor="light grey")
      rewardFrame.grid(row=index, column=1, sticky=tk.W)
      tk.Label(rewardFrame,text=f"{self._showRewards(task['rewards'])}",justify=tk.LEFT).grid(row=0, rowspan=2, column=1, sticky=tk.W)

      statusFrame = tk.Frame(tableFrame, borderwidth=0, relief=tk.GROOVE, highlightthickness=0, highlightcolor="light grey")
      statusFrame.grid(row=index, column=2, sticky=tk.W)
      if task['is_complete']:
        tk.Label(statusFrame, text="\u2713", fg="green", font=("Arial", 18)).grid(row=0, rowspan=2, column=0, sticky=tk.E)
    missionList.pack(side=tk.LEFT, fill=tk.BOTH)
  def _showRewards(self,rewards):
    data = []
    for r in rewards:
      if r['reward']['type'] == "game_item":
        if 'permanent' in r['reward']['item'].values() or 'permanent' in r['reward']['item']:
          data.append(r['title']+ " - Permanent")
        elif 'consumable' in r['reward']['item'].values() or 'consumable' in r['reward']['item']:
          data.append(r['title']+ " - Amount: {}".format(r['reward']['item']['count']))
        else:
          data.append(r['title']+ " - {0} {1}".format(r['reward']['item']['duration'],r['reward']['item']['duration_type']))
      elif r['reward']['type'] == "currency":
        if r['reward']['currency'] == "soft":
          data.append(str(r['reward']['count']) + ' Currency')
        elif r['reward']['currency'] == "hard":
          data.append(str(r['reward']['count']) + ' Rare Tokens')
      else:
        data.append(r['title']) # Will this even happen ?
    return "\n".join(data)
