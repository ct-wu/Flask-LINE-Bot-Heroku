from dataclasses import dataclass, field
from typing import Type
from src.dto import Item

from src.repo import Repo

@dataclass
class Command:
  msg: str
  uid: str

  def execute(self, repo_cls: Type[Repo]) -> str:
    pass


class InsertManyCommand(Command):
  def execute(self, repo_cls):
    tokens = [x.strip() for x in self.msg.split(',')]

    data = []
    for token in tokens:
        item, cost = [t(s) for t,s in zip((str,int), token.split())]
        data.append(Item(item, cost))
    
    repo = repo_cls(self.uid)
    success_cnt = repo.insert_many(data)
    return f'成功寫入{success_cnt}筆'

class SummaryCommand(Command):
  def execute(self, repo_cls):
    repo = repo_cls(self.uid)
    summary = repo.aggr_this_month()

    ret = []
    total = 0
    for x in summary:
      ret.append(f'{x.item}：{x.cost}')
      total += x.cost

    ret.append(f'總共：{total}')
    return '\n'.join(ret)


usage = '''使用說明
<項目><空格><金額>
例如：早餐 100
也支援透過半形逗號分隔多筆
例如：早餐 100, 午餐 200

/sum
當月匯總
'''
# no need to inherit from Command
class HelpCommand:
  def execute(self, repo = None):
    return usage
