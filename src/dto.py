import datetime
from dataclasses import dataclass, field

@dataclass
class Item:
    item: str
    cost: int
    dt: datetime.datetime = field(init=False)

    def __post_init__(self):
        self.dt = datetime.datetime.now()
