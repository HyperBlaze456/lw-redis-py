"""3단계 담당 2번. 대상: commands.lists.
작성할 검증: `deque`와 결과 비교, `LRANGE k 0 -1`과 빈 리스트 POP.
"""

from collections import deque

from lwredis.dispatch import execute
from lwredis.store import Store


def test_matches_deque(rng):
    store, expected = Store(), deque()
    for i in range(2_000):
        op = rng.choice(["LPUSH", "RPUSH", "LPOP", "RPOP"])
        if op == "LPUSH":
            expected.appendleft(str(i))
            assert execute(store, f"LPUSH k {i}") == str(len(expected))
        elif op == "RPUSH":
            expected.append(str(i))
            assert execute(store, f"RPUSH k {i}") == str(len(expected))
        elif op == "LPOP":
            assert execute(store, "LPOP k") == (expected.popleft() if expected else "(nil)")
        else:
            assert execute(store, "RPOP k") == (expected.pop() if expected else "(nil)")
        assert execute(store, "LRANGE k 0 -1") == (" ".join(expected) or "(empty)")


def test_lpop_missing_key():
    assert execute(Store(), "LPOP nothing") == "(nil)"
