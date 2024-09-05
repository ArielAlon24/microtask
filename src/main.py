from typing import Any
import commands
from schedulers import RoundRobin
from yield_injector import inject as microtask

scheduler = RoundRobin(quantum=0.001)


@microtask
def loop(message: str):
    for _ in range(10):
        yield commands.sleep(0.1)
        print(message)
    return f"Result: {message}"


@microtask
def main():
    future1 = scheduler.add(loop("foo"))
    future2 = scheduler.add(loop("bar"))

    b = yield commands.wait(future2)
    print(f"future2 is: {b}")

    a = yield commands.wait(future1)
    print(f"future1 is: {a}")


if __name__ == "__main__":
    scheduler.add(main())
    scheduler.start()
