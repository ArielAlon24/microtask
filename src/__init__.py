from typing import Generator, TypeVar
from .commands import AbstractCommand

T = TypeVar("T")

Future = Generator[AbstractCommand, None, T]
