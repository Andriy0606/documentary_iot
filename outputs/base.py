from __future__ import annotations

from abc import ABC, abstractmethod


class OutputStrategy(ABC):
    @abstractmethod
    def emit(self, message: str) -> None:
        raise NotImplementedError

