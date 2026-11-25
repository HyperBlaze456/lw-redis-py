"""2단계 담당 3번: 정렬 집합 명령 모듈이다."""

from lwredis.commands import EMPTY, NIL, bounds, find_or_new, number, take
from lwredis.store import Store
from lwredis.structures.skiplist import SkipListSet

ZSet = SkipListSet  # 정렬 집합의 내부 구현이다. SortedArraySet으로 바꿔도 명령은 그대로 동작한다.


def cmd_zadd(store: Store, args: list[str]) -> str:
    """ZADD key score member: 정렬 집합에 멤버를 점수와 함께 넣는다. 새 멤버면 1, 점수만 바꿨으면 0을 돌려준다."""
    key, score, member = take(args, 3)
    score = number(score, float)
    return str(int(find_or_new(store, key, ZSet, save=True).add(member, score)))


def cmd_zscore(store: Store, args: list[str]) -> str:
    """ZSCORE key member: 멤버의 점수를 돌려준다."""
    key, member = take(args, 2)
    score = find_or_new(store, key, ZSet).score(member)
    return NIL if score is None else str(score)


def cmd_zrank(store: Store, args: list[str]) -> str:
    """ZRANK key member: 멤버의 순위를 돌려준다."""
    key, member = take(args, 2)
    rank = find_or_new(store, key, ZSet).rank(member)
    return NIL if rank is None else str(rank)


def cmd_zrange(store: Store, args: list[str]) -> str:
    """ZRANGE key start stop: 순위 범위의 멤버를 낮은 점수부터 돌려준다."""
    key, start, stop = take(args, 3)
    zset = find_or_new(store, key, ZSet)
    start, stop = bounds(number(start, int), number(stop, int), len(zset))
    return " ".join(zset.range(start, stop)) or EMPTY


def cmd_zrem(store: Store, args: list[str]) -> str:
    """ZREM key member: 정렬 집합에서 멤버를 지운다. 지웠으면 1, 없던 멤버면 0을 돌려준다."""
    key, member = take(args, 2)
    zset = find_or_new(store, key, ZSet)
    removed = zset.remove(member)
    if removed and len(zset) == 0:
        store.delete(key)
    return str(int(removed))
