from abc import ABC, abstractmethod

from micro_task import MicroTask


class AbstractScheduler(ABC):

    @abstractmethod
    def add(self, micro_task: MicroTask) -> None:
        raise NotImplementedError

    @abstractmethod
    def start(self) -> None:
        pass
