import time

from .abstract_scheduler import AbstractScheduler
from micro_thread import MicroThread, _Empty


class RoundRobin(AbstractScheduler):
    def __init__(self, quantum: float) -> None:
        self.quantum = quantum
        self.micro_threads = []

    def add(self, micro_thread: MicroThread) -> None:
        return self.micro_threads.append(micro_thread)

    def run(self) -> None:
        index = 0

        while len(self.micro_threads) != 0:
            micro_thread = self.micro_threads[index]
            start_time = time.perf_counter()
            current_time = time.perf_counter()

            while current_time - start_time < self.quantum:
                try:
                    result = next(micro_thread)
                    if result != _Empty:
                        raise StopIteration
                except StopIteration:
                    self.micro_threads.remove(micro_thread)
                    break

                current_time = time.perf_counter()

            index = (index + 1) % len(self.micro_threads)
            print(index)
