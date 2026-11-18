"""3단계 담당 2번: 리스트 명령 모듈이다."""

from lwredis.store import Store


def cmd_lpush(store: Store, args: list[str]) -> str:
    """LPUSH key value [value ...]: 리스트의 앞쪽에 값을 넣는다."""
    raise NotImplementedError


def cmd_rpush(store: Store, args: list[str]) -> str:
    """RPUSH key value [value ...]: 리스트의 뒤쪽에 값을 넣는다."""
    raise NotImplementedError


def cmd_lpop(store: Store, args: list[str]) -> str:
    """LPOP key: 리스트의 앞쪽 값을 빼서 돌려준다."""
    raise NotImplementedError


def cmd_rpop(store: Store, args: list[str]) -> str:
    """RPOP key: 리스트의 뒤쪽 값을 빼서 돌려준다."""
    raise NotImplementedError


def cmd_llen(store: Store, args: list[str]) -> str:
    """LLEN key: 리스트의 길이를 돌려준다."""
    raise NotImplementedError


def cmd_lrange(store: Store, args: list[str]) -> str:
    """LRANGE key start stop: 리스트의 지정한 범위의 값을 돌려준다."""
    raise NotImplementedError
