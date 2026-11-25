"""1단계 담당 전원, 이후 담당 1번: 모든 키를 보관하는 저장소 모듈이다."""

import time
from collections.abc import Callable

from lwredis.expiry import Expiry
from lwredis.lru import LRU
from lwredis.structures.hashtable import HashTable


class Store:
    """모든 키가 거치는 저장소이다.

    값은 HashTable에 저장한다.
    3단계의 만료 검사와 4단계의 LRU 접근 기록은 이 클래스의 메서드 안에서 수행한다.
    """

    def __init__(
        self, now: Callable[[], float] = time.time, max_keys: int | None = None
    ) -> None:
        """now는 현재 시각을 돌려주는 함수이고 테스트에서 바꿔 끼운다. max_keys는 LRU 축출의 키 개수 한도이다."""
        self.data = HashTable()  # 키 → 값 (문자열, 리스트, 정렬 집합)
        self.expiry = Expiry(now)
        self.lru = None if max_keys is None else LRU(max_keys)

    def get(self, key: str) -> object | None:
        """키의 값을 돌려주고 없거나 만료되었으면 None을 돌려준다."""
        if self.expiry.is_expired(key):
            self.delete(key)
        value = self.data.get(key)
        if value is not None:
            self._touch(key)
        return value

    def set(self, key: str, value: object) -> None:
        """키에 값을 저장한다. 키에 걸려 있던 만료 시각은 없어진다."""
        self.data.set(key, value)
        self.expiry.remove(key)
        self._touch(key)

    def delete(self, key: str) -> bool:
        """키를 지우고 있던 키였으면 True를 돌려준다."""
        expired = self.expiry.is_expired(key)
        self.expiry.remove(key)
        if self.lru is not None:
            self.lru.remove(key)
        return self.data.delete(key) and not expired

    def exists(self, key: str) -> bool:
        """키가 존재하면 True를 돌려준다."""
        return self.get(key) is not None

    def _touch(self, key: str) -> None:
        """키를 방금 쓴 것으로 기록하고, 키 개수가 한도를 넘으면 가장 오래 쓰지 않은 키를 지운다."""
        if self.lru is None:
            return
        self.lru.touch(key)
        if len(self.lru) > self.lru.capacity:
            self.delete(self.lru.evict())
