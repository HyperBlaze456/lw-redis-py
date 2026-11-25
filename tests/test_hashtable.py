"""2단계 담당 1번. 대상: structures.hashtable.
작성할 검증: 무작위 삽입·조회·삭제 1만 번을 내장 `dict`와 나란히 수행해 매번 결과 일치.
"""

from lwredis.structures.hashtable import HashTable


def test_matches_dict(rng):
    table, expected = HashTable(), {}
    for _ in range(10_000):
        key = rng.randrange(500)
        op = rng.choice(["set", "get", "delete"])
        if op == "set":
            value = rng.random()
            table.set(key, value)
            expected[key] = value
        elif op == "get":
            assert table.get(key) == expected.get(key)
        else:
            assert table.delete(key) == (expected.pop(key, None) is not None)
        assert len(table) == len(expected)
    assert sorted(table.items()) == sorted(expected.items())
