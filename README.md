# microtask

A dumb way to create asynchronous tasks in Python.

## How microtask works?

microtask takes each function decorated with a scheduler and edits it runtime - it adds yield statements one after each line. For example the function

```python
@scheduler
def test() -> Future[int]:
    a = 10
    a += 2
    return 12
```

will turn into
```python
def test() -> Generator[Future]:
    a = 10
    # '_Empty' is used as a placeholder for an empty yield as None can also count as a return value
    yield _Empty
    a += 2
    yield _Empty
    yield 12  # A return statement turns into a yield.
```

The scheduler (currently, only a simple RoundRobin scheduler is available) runs an event loop, starting with an initial microtask passed as an argument. The scheduler can decide which function to advance by calling `next` on the corresponding generator created by the decorated function.

Also, some commands are available for controlling the execution:

- `sleep` - Stop the execution of the micro task in a non blocking way.
- `wait` - Acts like the `await` keyword, waits until the `Future` object passed to it completes.



