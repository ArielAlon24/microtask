from typing import Any
import commands
from schedulers import RoundRobin
from yield_injector import inject as microtask

scheduler = RoundRobin(0.001)


@microtask
def loop(message: str):
    yield commands.sleep(1)
    for _ in range(100):
        print(message)
    return f"boom {message}"


@microtask
def main() -> None:
    future = scheduler.add(loop("foo"))

    a = scheduler.wait(future)
    print(a)


if __name__ == "__main__":
    scheduler.add(main())
    scheduler.start()
