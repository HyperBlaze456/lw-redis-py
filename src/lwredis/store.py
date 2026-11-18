"""1단계 담당 전원, 이후 담당 1번: 모든 키를 보관하는 저장소 모듈이다."""

import time
from collections.abc import Callable


class Store:
    """모든 키가 거치는 저장소이다.

    1단계에서는 내장 dict에 저장하고, 2단계에서 HashTable로 바꾼다.
    3단계의 만료 검사와 4단계의 LRU 접근 기록은 이 클래스의 메서드 안에서 수행한다.
    """

    def __init__(
        self, now: Callable[[], float] = time.time, max_keys: int | None = None
    ) -> None:
        """now는 현재 시각을 돌려주는 함수이고 테스트에서 바꿔 끼운다. max_keys는 LRU 축출의 키 개수 한도이다."""
        raise NotImplementedError

    def get(self, key: str) -> object | None:
        """키의 값을 돌려주고 없거나 만료되었으면 None을 돌려준다."""
        raise NotImplementedError

    def set(self, key: str, value: object) -> None:
        """키에 값을 저장한다."""
        raise NotImplementedError

    def delete(self, key: str) -> bool:
        """키를 지우고 있던 키였으면 True를 돌려준다."""
        raise NotImplementedError

    def exists(self, key: str) -> bool:
        """키가 존재하면 True를 돌려준다."""
        raise NotImplementedError
