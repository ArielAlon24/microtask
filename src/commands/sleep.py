import time
from .abstract_command import AbstractCommand
from dataclasses import dataclass, field


@dataclass
class Sleep(AbstractCommand[None]):
    duration: float
    start_time: float = field(default_factory=time.perf_counter)

    def is_done(self) -> bool:
        return time.perf_counter() - self.start_time >= self.duration

    def result(self) -> None:
        return None
