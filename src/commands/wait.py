from .abstract_command import AbstractCommand
from dataclasses import dataclass, field
from micro_task import Future


@dataclass
class Wait(AbstractCommand):
    future: Future

    def is_done(self) -> bool:
        return self.future.is_done
