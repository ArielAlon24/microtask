import time
from typing import Any, Callable
from commands import AbstractCommand
from yield_injector import inject
from .abstract_scheduler import AbstractScheduler
from micro_task import Function, MicroTask, _Empty, MicroTaskGen, Future


class RoundRobin(AbstractScheduler):
    def __init__(self, quantum: float) -> None:
        self.quantum = quantum
        self.micro_tasks = []
        self.index = -1

    def __call__(self, function: Function) -> Callable[..., Future]:
        generator_creator = inject(function)

        def wrapper(*args: Any, **kwargs: Any) -> Future:
            return self.add(generator_creator(*args, **kwargs))

        return wrapper

    def add(self, generator: MicroTaskGen) -> Future:
        micro_task = MicroTask(generator)
        self.micro_tasks.append(micro_task)
        return micro_task._future

    def start(self, entry: Callable[..., Future]) -> None:
        entry()  # adding the micro_task to the scheduler

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
                        task._future._value = result
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

            if micro_task._command.is_done():
                micro_task._generator.send(micro_task._command.result())
                return micro_task
