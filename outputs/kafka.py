from __future__ import annotations

import json
import time
from typing import Any

from outputs.base import OutputStrategy


class KafkaOutputStrategy(OutputStrategy):
    def __init__(self, bootstrap_servers: str, topic: str) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self._producer = None

    def _get_producer(self):
        if self._producer is not None:
            return self._producer

        # Lazy import: so console mode doesn't require Kafka deps.
        from confluent_kafka import Producer  # type: ignore

        self._producer = Producer({"bootstrap.servers": self.bootstrap_servers})
        return self._producer

    def emit(self, message: str) -> None:
        payload: dict[str, Any] = {"ts": int(time.time()), "message": message}
        producer = self._get_producer()
        producer.produce(self.topic, json.dumps(payload, ensure_ascii=False).encode("utf-8"))
        producer.poll(0)

