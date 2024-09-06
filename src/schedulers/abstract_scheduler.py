from abc import ABC, abstractmethod
from typing import Callable

from micro_task import Future, MicroTaskGen


class AbstractScheduler(ABC):

    @abstractmethod
    def add(self, generator: MicroTaskGen) -> Future:
        raise NotImplementedError

    @abstractmethod
    def start(self, entry: Callable[..., Future]) -> None:
        raise NotImplementedError
