from dataclasses import dataclass, field

@dataclass
class Command:
  msg: str
  uid: str

  def execute(self, repo):
    pass


class InsertManyCommand(Command):
  def execute(self, repo):
    print('InsertMany')

class SummaryCommand(Command):
  def execute(self, repo):
    print('summary')

# no need to inherit from Command
class HelpCommand:
  def execute(self, repo = None):
    print('Help')
