"""4단계 담당 1번. 대상: lwredis.aof.
작성할 검증: 명령 수행 후 빈 저장소에 파일을 재실행해 두 저장소의 전체 내용 일치.
"""

from lwredis.aof import AOF
from lwredis.commands import zsets
from lwredis.store import Store
from lwredis.structures.linkedlist import DoublyLinkedList

LINES = [
    "SET a 1",
    "SET b 2",
    "RPUSH l x",
    "LPUSH l y",
    "ZADD z 2 m",
    "ZADD z 1 n",
    "DEL b",
    "GET a",  # 읽기 명령은 기록하지 않는다
    "SET c",  # 잘못된 명령은 기록하지 않는다
]
WRITES = 7


def dump(store):
    """저장소의 모든 키를 비교하기 쉬운 평범한 값으로 바꿔 돌려준다."""
    result = {}
    for key, value in store.data.items():
        if isinstance(value, DoublyLinkedList):
            value = list(value)
        elif isinstance(value, zsets.ZSet):
            value = [(m, value.score(m)) for m in value.range(0, len(value) - 1)]
        result[key] = value
    return result


def test_replay_restores_store(tmp_path):
    aof = AOF(str(tmp_path / "log.aof"))
    original = Store()
    for line in LINES:
        aof.run(original, line)
    restored = Store()
    assert aof.replay(restored) == WRITES
    assert dump(restored) == dump(original)
