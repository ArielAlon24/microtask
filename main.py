from src.commands import sleep, wait
from src.schedulers import RoundRobin
from src import Future

scheduler = RoundRobin(quantum=0.001)


@scheduler
def loop(message: str) -> Future[str]:
    for _ in range(10):
        yield sleep(0.1)
        print(message)
    return f"Result: {message}"


@scheduler
def main() -> Future[None]:
    future1 = loop("foo")
    future2 = loop("bar")

    a = yield wait(future1)
    print(f"future1 is: {a}")

    b = yield wait(future2)
    print(f"future2 is: {b}")


if __name__ == "__main__":
    scheduler.start(main)
