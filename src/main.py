import commands
from schedulers import RoundRobin

scheduler = RoundRobin(quantum=0.001)


@scheduler
def loop(message: str):
    for _ in range(10):
        yield commands.sleep(0.1)
        print(message)
    return f"Result: {message}"


@scheduler
def main():
    future1 = loop("foo")
    future2 = loop("bar")

    b = yield commands.wait(future2)
    print(f"future2 is: {b}")

    a = yield commands.wait(future1)
    print(f"future1 is: {a}")


if __name__ == "__main__":
    scheduler.start(main)
