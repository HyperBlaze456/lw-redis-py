"""1단계 담당 전원(SET GET DEL EXISTS), 3단계 담당 1번(EXPIRE TTL PERSIST): 키 명령 모듈이다."""

from lwredis.store import Store


def cmd_set(store: Store, args: list[str]) -> str:
    """SET key value: 키에 값을 저장한다."""
    raise NotImplementedError


def cmd_get(store: Store, args: list[str]) -> str:
    """GET key: 키의 값을 돌려준다."""
    raise NotImplementedError


def cmd_del(store: Store, args: list[str]) -> str:
    """DEL key: 키를 지운다."""
    raise NotImplementedError


def cmd_exists(store: Store, args: list[str]) -> str:
    """EXISTS key: 키가 있는지 알려 준다."""
    raise NotImplementedError


def cmd_expire(store: Store, args: list[str]) -> str:
    """EXPIRE key seconds: 키가 지정한 초 뒤에 사라지도록 정한다."""
    raise NotImplementedError


def cmd_ttl(store: Store, args: list[str]) -> str:
    """TTL key: 키가 사라질 때까지 남은 초를 알려 준다."""
    raise NotImplementedError


def cmd_persist(store: Store, args: list[str]) -> str:
    """PERSIST key: 키의 만료 시각을 없앤다."""
    raise NotImplementedError
