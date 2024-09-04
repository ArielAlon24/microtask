import commands
from schedulers import RoundRobin
from yield_injector import inject as microtask


scheduler = RoundRobin(0.001)


@microtask
def loop(message: str):
    yield commands.sleep(10)
    while True:
        print(message)


scheduler.add(loop("foo"))
scheduler.add(loop("bar"))

scheduler.start()
