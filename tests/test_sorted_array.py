"""2단계 담당 3번. 대상: structures.sorted_array, commands.zsets.
작성할 검증: 무작위 ZADD 후 ZRANGE 결과가 내장 `sorted` 결과와 일치, 같은 점수는 멤버 사전순.
"""

import pytest

from lwredis.commands import zsets
from lwredis.dispatch import execute
from lwredis.store import Store
from lwredis.structures.skiplist import SkipListSet
from lwredis.structures.sorted_array import SortedArraySet


@pytest.mark.parametrize("kind", [SortedArraySet, SkipListSet])
def test_zrange_matches_sorted(rng, monkeypatch, kind):
    monkeypatch.setattr(zsets, "ZSet", kind)
    store, scores = Store(), {}
    for _ in range(500):
        member, score = f"m{rng.randrange(100)}", rng.randrange(5)
        execute(store, f"ZADD z {score} {member}")
        scores[member] = float(score)
    expected = [m for _, m in sorted((s, m) for m, s in scores.items())]
    assert execute(store, "ZRANGE z 0 -1") == " ".join(expected)
