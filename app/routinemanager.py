
class routineManager:
  def __init__(self,app,window):
    self.app = app
    self.window = window
    self.taskHistory = {}
  def checkCrates(self):
    if self.app.configs.get("configs")['autoCrateOpen']:
      crates = self.app.accountManager.crafting.crates()
      for crate in crates:
        if crate['state'] == 'new':
          r = self.app.accountManager.crafting.startCrate(crate['id'])
          self.app.consoleLog(f"New {crate['type']} crate available! {r['state']} opening, ID: {crate['id']}")
          self.app.notif.send("New crate",f"You received a {crate['type']} crate")
        elif crate['ended_at'] < 0:
          r = self.app.accountManager.crafting.openCrate(crate['id'])
          self.app.consoleLog(f"{crate['type']} crate opening...\n    Content -> Level: {r['data']['resource']['level']} | Amount: {r['data']['resource']['amount']}")
          self.app.notif.send(f"{crate['type']} crate opened",f"Level: {r['data']['resource']['level']}\nAmount: {r['data']['resource']['amount']}")
    self.window.after(30000,self.checkCrates)
  def checkFreeCrate(self):
    if self.app.configs.get("configs")['freeCrateOpen']:

      wallets = self.app.accountManager.get("https://$baseurl$/minigames/battlepass/wallets")
      if wallets['data']['victory'] >= 5:
        req = self.app.accountManager.post("https://$baseurl$/minigames/battlepass/box/open",data={"id":6,"count":1,"currency":3})
        if len(req['data']) == 0:
          content = "There were no rewards in this crate" # Is this possible?
        else:
          item = req['data'][0]
          if 'permanent' in item['reward']['item'].values() or 'permanent' in item['reward']['item']:
            content = item['title']+ " - Permanent"
          elif 'consumable' in item['reward']['item'].values() or 'consumable' in item['reward']['item']:
            content = item['title']+ " - Amount: {}".format(item['count'])
          elif 'regular' in item['reward']['item'].values() or 'regular' in item['reward']['item']:
            content = item['title']
          else:
            content = item['title']+ " - {0} {1}".format(item['reward']['item']['duration'],item['reward']['item']['duration_type'])
        self.app.consoleLog(f"Free win box opened : {content}")
        self.app.notif.send("Free win box opened",f"Reward: {content}")
      if self.app.hasBattlePass and wallets['data']['victory_vip'] >= 5:
        req = self.app.accountManager.post("https://$baseurl$/minigames/battlepass/box/open",data={"id":5,"count":1,"currency":4})
        if len(req['data']) == 0:
          content = "There were no rewards in this crate" # Is this possible?
        else:
          item = req['data'][0]
          if 'permanent' in item['reward']['item'].values() or 'permanent' in item['reward']['item']:
            content = item['title']+ " - Permanent"
          elif 'consumable' in item['reward']['item'].values() or 'consumable' in item['reward']['item']:
            content = item['title']+ " - Amount: {}".format(item['count'])
          elif 'regular' in item['reward']['item'].values() or 'regular' in item['reward']['item']:
            content = item['title']
          else:
            content = item['title']+ " - {0} {1}".format(item['reward']['item']['duration'],item['reward']['item']['duration_type'])
        self.app.consoleLog(f"VIP win box opened : {content}")
        self.app.notif.send("VIP win box opened",f"Reward: {content}")
    self.window.after(300000,self.checkFreeCrate)
  def checkTasks(self):
    if self.app.configs.get("configs")['checkTaskCompletion']:
      temp = {}
      req = self.app.accountManager.get("https://$baseurl$/minigames/battlepass/task/all")
      for j, task in enumerate(req['data']):
        temp[j] = (task['is_complete'] == False)
        if self.taskHistory == {}:
          continue
        if temp[j] != self.taskHistory[j]:
          self.app.consoleLog(f"Task Completed : {task['title']}")
          self.app.notif.send("Task Completed",f"{task['title']}")
      self.taskHistory = temp
    self.window.after(300000,self.checkTasks)