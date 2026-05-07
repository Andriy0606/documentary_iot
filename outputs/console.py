from __future__ import annotations

from outputs.base import OutputStrategy


class ConsoleOutputStrategy(OutputStrategy):
    def emit(self, message: str) -> None:
        print(message)

