import os
import json

class configManager:
  def __init__(self,path):
    self.dir_path = path
    if os.path.isfile(f'{self.dir_path}/creds.json'):
      with open(f'{self.dir_path}/creds.json','r') as json_file:
        self.configs = json.load(json_file)
      if "configs" not in self.configs:
        self.set("configs",{})
    else:
      with open(f'{self.dir_path}/creds.json','w') as json_file:
        self.configs = {"region" : "west", "configs" : {}}
        json.dump(self.configs, json_file, indent=4, sort_keys=True)
  def set(self,key,data):
    self.configs[key] = data
    with open(f'{self.dir_path}/creds.json','w') as json_file:
      json.dump(self.configs, json_file, indent=4, sort_keys=True)
  def get(self,key):
    if key in self.configs:
      return self.configs[key]
    return None