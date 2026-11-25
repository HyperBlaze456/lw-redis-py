"""3단계 담당 3번. 대상: structures.skiplist.
작성할 검증: 같은 무작위 명령 1만 개를 정렬 배열 버전과 스킵 리스트 버전에 넣어 응답 전부 일치.
"""

from lwredis.structures.skiplist import SkipListSet
from lwredis.structures.sorted_array import SortedArraySet


def test_matches_sorted_array(rng):
    skip, array = SkipListSet(), SortedArraySet()
    for _ in range(10_000):
        member = f"m{rng.randrange(200)}"
        op = rng.choice(["add", "score", "rank", "remove", "range"])
        if op == "add":
            score = float(rng.randrange(20))
            assert skip.add(member, score) == array.add(member, score)
        elif op == "score":
            assert skip.score(member) == array.score(member)
        elif op == "rank":
            assert skip.rank(member) == array.rank(member)
        elif op == "remove":
            assert skip.remove(member) == array.remove(member)
        else:
            start = rng.randrange(50)
            stop = start + rng.randrange(50)
            assert skip.range(start, stop) == array.range(start, stop)
        assert len(skip) == len(array)
