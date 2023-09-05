import unittest

from src.factory import CommandFactory
from src.command import HelpCommand, InsertManyCommand, SummaryCommand

class TestCommandFactory(unittest.TestCase):
  def setUp(self):
    self.uid = 'faker'

  def test_insert_many(self):
    msg = 'item 100'
    self.assertTrue(isinstance(CommandFactory.generate(msg, self.uid), InsertManyCommand))

    msg = 'item 100, item2 200'
    self.assertTrue(isinstance(CommandFactory.generate(msg, self.uid), InsertManyCommand))

    msg = 'invaliditem100'
    self.assertTrue(isinstance(CommandFactory.generate(msg, self.uid), HelpCommand))

  def test_summary(self):
    msg = '/sum'
    self.assertTrue(isinstance(CommandFactory.generate(msg, self.uid), SummaryCommand))
    
    msg = '/summary'
    self.assertTrue(isinstance(CommandFactory.generate(msg, self.uid), HelpCommand))