"""1단계 담당 전원(SET GET DEL EXISTS), 3단계 담당 1번(EXPIRE TTL PERSIST): 키 명령 모듈이다."""

from lwredis.commands import NIL, find, number, take
from lwredis.store import Store


def cmd_set(store: Store, args: list[str]) -> str:
    """SET key value: 키에 값을 저장한다."""
    key, value = take(args, 2)
    store.set(key, value)
    return "OK"


def cmd_get(store: Store, args: list[str]) -> str:
    """GET key: 키의 값을 돌려준다."""
    [key] = take(args, 1)
    value = find(store, key, str)
    return NIL if value is None else value


def cmd_del(store: Store, args: list[str]) -> str:
    """DEL key: 키를 지운다. 지웠으면 1, 없던 키면 0을 돌려준다."""
    [key] = take(args, 1)
    return str(int(store.delete(key)))


def cmd_exists(store: Store, args: list[str]) -> str:
    """EXISTS key: 키가 있는지 알려 준다. 있으면 1, 없으면 0을 돌려준다."""
    [key] = take(args, 1)
    return str(int(store.exists(key)))


def cmd_expire(store: Store, args: list[str]) -> str:
    """EXPIRE key seconds: 키가 지정한 초 뒤에 사라지도록 정한다. 정했으면 1, 없는 키면 0을 돌려준다."""
    key, seconds = take(args, 2)
    seconds = number(seconds, int)
    if not store.exists(key):
        return "0"
    store.expiry.expire(key, seconds)
    return "1"


def cmd_ttl(store: Store, args: list[str]) -> str:
    """TTL key: 키가 사라질 때까지 남은 초를 알려 준다. 없는 키면 -2, 만료 시각이 없는 키면 -1을 돌려준다."""
    [key] = take(args, 1)
    if not store.exists(key):
        return "-2"
    ttl = store.expiry.ttl(key)
    return "-1" if ttl is None else str(round(ttl))


def cmd_persist(store: Store, args: list[str]) -> str:
    """PERSIST key: 키의 만료 시각을 없앤다. 없앴으면 1, 없앨 시각이 없었으면 0을 돌려준다."""
    [key] = take(args, 1)
    return str(int(store.exists(key) and store.expiry.persist(key)))
