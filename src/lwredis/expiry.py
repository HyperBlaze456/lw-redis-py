"""3단계 담당 1번: 키의 만료 시각을 관리하는 모듈이다."""

import time
from collections.abc import Callable

from lwredis.structures.hashtable import HashTable


class Expiry:
    """키별 만료 시각표이다."""

    def __init__(self, now: Callable[[], float] = time.time) -> None:
        """now는 현재 시각을 돌려주는 함수이고 테스트에서 바꿔 끼운다."""
        self.now = now
        self.deadlines = HashTable()  # 키 → 만료 시각

    def expire(self, key: str, seconds: float) -> None:
        """키가 지금부터 seconds초 뒤에 만료되도록 기록한다."""
        self.deadlines.set(key, self.now() + seconds)

    def ttl(self, key: str) -> float | None:
        """키가 만료될 때까지 남은 초를 돌려주고 만료 시각이 없으면 None을 돌려준다."""
        deadline = self.deadlines.get(key)
        return None if deadline is None else deadline - self.now()

    def persist(self, key: str) -> bool:
        """키의 만료 시각을 없애고 있던 시각이었으면 True를 돌려준다."""
        return self.deadlines.delete(key)

    def is_expired(self, key: str) -> bool:
        """키의 만료 시각이 지났으면 True를 돌려준다."""
        ttl = self.ttl(key)
        return ttl is not None and ttl <= 0

    def remove(self, key: str) -> None:
        """키의 만료 기록을 지운다."""
        self.deadlines.delete(key)
