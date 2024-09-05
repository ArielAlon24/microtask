import time
from typing import Any
from commands import AbstractCommand
import commands
from .abstract_scheduler import AbstractScheduler
from micro_task import MicroTask, _Empty, MicroTaskGen, Future


class RoundRobin(AbstractScheduler):
    def __init__(self, quantum: float) -> None:
        self.quantum = quantum
        self.micro_tasks = []
        self.index = -1

    def add(self, generator: MicroTaskGen) -> Future:
        micro_task = MicroTask(generator)
        self.micro_tasks.append(micro_task)
        return micro_task._future

    def wait(self, future: Future) -> Any:
        while not future.is_done:
            print("inside")
            self.start()
        return future._value

    def start(self) -> None:
        while len(self.micro_tasks) != 0:
            task = self._select_next_micro_task()
            start_time = time.perf_counter()

            while time.perf_counter() - start_time < self.quantum:
                try:
                    result = next(task._generator)

                    if isinstance(result, AbstractCommand):
                        task._command = result
                        break

                    elif result != _Empty:
                        task._future._value = result  # type: ignore
                        raise StopIteration

                except StopIteration:
                    self.micro_tasks.remove(task)
                    break

    def _select_next_micro_task(self) -> MicroTask:
        while True:
            self.index = (self.index + 1) % len(self.micro_tasks)
            micro_task = self.micro_tasks[self.index]

            if micro_task._command is None:
                return micro_task

            if isinstance(micro_task._command, commands.Sleep):
                if micro_task._command.is_done():
                    return micro_task

            if isinstance(micro_task._command, commands.Wait):
                if micro_task._command.is_done():
                    micro_task._generator.send(micro_task._command.future._value)
                    return micro_task
