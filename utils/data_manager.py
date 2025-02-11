import json
import os

from config import DATA_FOLDER

class DataManager:
    def __init__(self, filename):
        self.filename = os.path.join(DATA_FOLDER, filename)
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.filename):
            self.data = {}
            self.save_data()
        else:
            with open(self.filename, "r") as f:
                self.data = json.load(f)

    def save_data(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)

    def get_all(self):
        return self.data

    def get_by_id(self, id):
        return self.data.get(str(id))

    def create(self, item):
      self.data.update(item)
      self.save_data()
      return list(item.keys())
    
    def create_post(self, id, item):
        new_dat = self.data[str(id)]
        new_dat.update({len(new_dat) + 1 : item})
        self.data[str(id)] = new_dat
        self.save_data()
        return True

    def update(self, id, item):
        if str(id) in self.data:
          self.data[str(id)] = item
          self.save_data()
          return True
        return False

    def delete(self, id):
        if str(id) in self.data:
          del self.data[str(id)]
          self.save_data()
          return True
        return False

    def delete_post(self, user_id, post_id):
      if str(user_id) in self.data and str(post_id) in self.data[str(user_id)]:
        del self.data[str(user_id)][str(post_id)]
        self.save_data()
        return True
      return False
    
    def update_post(self, user_id, post_id, post_data):
        user_id = str(user_id)
        post_id = str(post_id)
        if user_id in self.data and post_id in self.data[user_id]:
            self.data[user_id][post_id] = post_data
            self.save_data()
            return True
        return False