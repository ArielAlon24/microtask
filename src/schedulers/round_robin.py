import time

from commands import AbstractCommand
import commands

from .abstract_scheduler import AbstractScheduler
from micro_task import MicroTask, _Empty

from dataclasses import dataclass, field
from typing import List


@dataclass(slots=True)
class Task:
    micro_task: MicroTask
    command: AbstractCommand | None = field(default=None)


class RoundRobin(AbstractScheduler):
    def __init__(self, quantum: float) -> None:
        self.quantum = quantum
        self.tasks = []
        self.index = -1

    def add(self, micro_task: MicroTask) -> None:
        return self.tasks.append(Task(micro_task))

    def start(self) -> None:
        while len(self.tasks) != 0:
            task = self.get_next_task()

            start_time = time.perf_counter()

            while time.perf_counter() - start_time < self.quantum:
                try:
                    result = next(task.micro_task)

                    if isinstance(result, AbstractCommand):
                        task.command = result
                        break

                    elif result != _Empty:
                        raise StopIteration

                except StopIteration:
                    self.tasks.remove(task)
                    break

                current_time = time.perf_counter()

    def get_next_task(self) -> Task:
        while True:
            self.index = (self.index + 1) % len(self.tasks)
            task = self.tasks[self.index]

            if task.command is None:
                return task

            if isinstance(task.command, commands.Sleep):
                if task.command.is_done():
                    return task

    def handle_command(self, command: AbstractCommand) -> None:
        if isinstance(command, commands.Sleep):
            pass
