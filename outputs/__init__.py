from .base import OutputStrategy
from .console import ConsoleOutputStrategy
from .kafka import KafkaOutputStrategy

__all__ = [
    "OutputStrategy",
    "ConsoleOutputStrategy",
    "KafkaOutputStrategy",
]

