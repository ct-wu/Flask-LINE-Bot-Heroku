from collections import OrderedDict
from typing import List
import unittest
from src.command import InsertManyCommand, SummaryCommand
from src.dto import Item

from src.repo import Repo

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class MockRepo(metaclass=Singleton):
  def __init__(self, uid = 'faker'):
    self.db = OrderedDict()

  def insert_many(self, data: List[Item]) -> int:
    base_id = max(self.db.keys() or [0])
    for i, x in enumerate(data, start=1):
      self.db[base_id + i] = {'item': x.item, 'cost': x.cost, 'dt': 'fake_datetime'}

    return len(data)
  
  def aggr_this_month(self) -> List[Item]:
    ret = []
    for v in self.db.values():
      ret.append(Item(v['item'], v['cost']))

    return ret
    
class TestCommand(unittest.TestCase):
  def setUp(self):
    self.uid = 'faker'

  def tearDown(self):
    MockRepo().db = OrderedDict()

  def test_insert_many(self):
    mock_db = MockRepo().db

    cmd = InsertManyCommand('abc 100', self.uid)
    ret = cmd.execute(MockRepo)
    self.assertEqual(ret, '成功寫入1筆')
    self.assertDictEqual(mock_db, {1: {'item': 'abc', 'cost': 100, 'dt': 'fake_datetime'}})
    
    cmd = InsertManyCommand('def 100, ghi 200', self.uid)
    ret = cmd.execute(MockRepo)
    self.assertEqual(ret, '成功寫入2筆')
    self.assertDictEqual(mock_db, {
      1: {'item': 'abc', 'cost': 100, 'dt': 'fake_datetime'},
      2: {'item': 'def', 'cost': 100, 'dt': 'fake_datetime'},
      3: {'item': 'ghi', 'cost': 200, 'dt': 'fake_datetime'},
      })
  
  def test_summary(self):
    cmd = InsertManyCommand('def 100, ghi 200', self.uid)
    cmd.execute(MockRepo)

    cmd = SummaryCommand('/sum', self.uid)
    ret = cmd.execute(MockRepo)
    self.assertEqual(ret, 'def：100\nghi：200\n總共：300')