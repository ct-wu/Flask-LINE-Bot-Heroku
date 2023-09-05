from abc import ABC, abstractmethod
from typing import List

from src.dto import Item

class Repo(ABC):
  def __init__(self, uid):
    self.uid = uid

  @abstractmethod
  def insert_many(self, data: List[Item]) -> int:
    pass

  @abstractmethod
  def aggr_this_month(self) -> List[Item]:
    pass