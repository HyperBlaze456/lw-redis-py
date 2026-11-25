"""4단계 담당 2번. 대상: lwredis.lru.
작성할 검증: 한도 3에서 a b c 저장 → a 조회 → d 저장 시 b만 사라짐.
"""

from lwredis.dispatch import execute
from lwredis.store import Store


def test_evicts_least_recently_used():
    store = Store(max_keys=3)
    for key in "abc":
        execute(store, f"SET {key} 1")
    execute(store, "GET a")
    execute(store, "SET d 1")
    assert [execute(store, f"EXISTS {k}") for k in "abcd"] == ["1", "0", "1", "1"]
