
from typing import Type
from src.factory import CommandFactory
from src.repo import Repo


class Service:
  def __init__(self, repo_cls: Type[Repo]) -> None:
    self.repo_cls = repo_cls

  def handle_msg(self, msg: str, uid: str) -> str:
    try:
      cmd = CommandFactory.generate(msg, uid)
      return cmd.execute(self.repo_cls)
    except Exception as e:
      return f'Error: {e}'