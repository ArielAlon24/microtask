from abc import ABC, abstractmethod

from micro_thread import MicroThread


class AbstractScheduler(ABC):

    @abstractmethod
    def add(self, micro_thread: MicroThread) -> None:
        raise NotImplementedError

    @abstractmethod
    def run(self) -> None:
        pass
