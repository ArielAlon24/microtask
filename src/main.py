from schedulers.round_robin import RoundRobin
from yield_injector import inject


@inject
def loop(message: str):
    while True:
        print(message)


scheduler = RoundRobin(1)
scheduler.add(loop("foo"))
scheduler.add(loop("bar"))

scheduler.run()
