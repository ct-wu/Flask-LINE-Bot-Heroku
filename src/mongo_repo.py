from datetime import datetime
import os
from typing import List

from pymongo import MongoClient
from src.dto import Item
from src.repo import Repo

mongo_client = MongoClient(os.environ.get("MONGODB_URI"))

class MongoRepo(Repo):
  def __init__(self, uid):
    self.db = mongo_client['accounting'][uid]

  def insert_many(self, data: List[Item]) -> int:
    self.db.insert_many([
      {'item': x.item, 'cost': x.cost, 'dt': x.dt} for x in data
      ])
    return len(data)
  
  def aggr_this_month(self) -> List[Item]:
    now = datetime.now()
    first_day = datetime(now.year, now.month, 1, 0, 0, 0)
    last_day = datetime(now.year, now.month + 1, 1, 23, 59, 59)

    ret = self.db.aggregate([
                         {
                           '$match': {
                             'dt': {
                               '$gte': first_day,
                               '$lte': last_day
                             }
                           }
                         },
                         {
                           '$group': {
                             '_id': "$item",
                             'total_cost': {
                               '$sum': "$cost"
                             }
                           }
                         }
                       ])

    summary = [Item(x['_id'], x['total_cost']) for x in ret]
    return summary