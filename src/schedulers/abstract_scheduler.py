from abc import ABC, abstractmethod

from micro_task import Future, MicroTaskGen


class AbstractScheduler(ABC):

    @abstractmethod
    def add(self, generator: MicroTaskGen) -> Future:
        raise NotImplementedError

    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError
