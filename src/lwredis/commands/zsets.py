"""2단계 담당 3번: 정렬 집합 명령 모듈이다."""

from lwredis.store import Store


def cmd_zadd(store: Store, args: list[str]) -> str:
    """ZADD key score member: 정렬 집합에 멤버를 점수와 함께 넣는다."""
    raise NotImplementedError


def cmd_zscore(store: Store, args: list[str]) -> str:
    """ZSCORE key member: 멤버의 점수를 돌려준다."""
    raise NotImplementedError


def cmd_zrank(store: Store, args: list[str]) -> str:
    """ZRANK key member: 멤버의 순위를 돌려준다."""
    raise NotImplementedError


def cmd_zrange(store: Store, args: list[str]) -> str:
    """ZRANGE key start stop: 순위 범위의 멤버를 낮은 점수부터 돌려준다."""
    raise NotImplementedError


def cmd_zrem(store: Store, args: list[str]) -> str:
    """ZREM key member: 정렬 집합에서 멤버를 지운다."""
    raise NotImplementedError
