from abc import ABC
from dataclasses import dataclass


@dataclass(slots=True)
class AbstractCommand(ABC):
    pass
