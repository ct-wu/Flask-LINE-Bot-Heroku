from . import command

class CommandFactory:
  @staticmethod
  def generate(msg, uid):
    if msg.startswith("/"):
      if msg == '/sum':
        return command.SummaryCommand(msg, uid)

      return command.HelpCommand()
    elif msg.count(' ') > 0:
      return command.InsertManyCommand(msg, uid)
    
    return command.HelpCommand()
