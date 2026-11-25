"""2단계 담당 1번: 해시 테이블 모듈이다."""

from collections.abc import Hashable, Iterator


class HashTable:
    """모든 키 저장에 쓰고, 만료 시각표, LRU의 키→노드, 정렬 집합의 멤버→점수에 재사용한다."""

    def __init__(self) -> None:
        """빈 해시 테이블을 만든다."""
        self.buckets: list[list[tuple[Hashable, object]]] = [[] for _ in range(8)]
        self.size = 0

    def _bucket(self, key: Hashable) -> list[tuple[Hashable, object]]:
        """키의 해시값으로 고른 칸을 돌려준다. 같은 칸에 걸린 키들은 한 리스트에 함께 들어 있다."""
        return self.buckets[hash(key) % len(self.buckets)]

    def get(self, key: Hashable, default: object = None) -> object:
        """키의 값을 돌려주고 없으면 default를 돌려준다."""
        for stored_key, value in self._bucket(key):
            if stored_key == key:
                return value
        return default

    def set(self, key: Hashable, value: object) -> None:
        """키에 값을 저장하고 이미 있으면 값을 바꾼다."""
        bucket = self._bucket(key)
        for index, (stored_key, _) in enumerate(bucket):
            if stored_key == key:
                bucket[index] = (key, value)
                return
        bucket.append((key, value))
        self.size += 1
        if self.size > len(self.buckets):
            self._grow()

    def _grow(self) -> None:
        """칸 수를 두 배로 늘리고 모든 쌍을 새 칸에 다시 넣는다."""
        pairs = list(self.items())
        self.buckets = [[] for _ in range(len(self.buckets) * 2)]
        for key, value in pairs:
            self._bucket(key).append((key, value))

    def delete(self, key: Hashable) -> bool:
        """키를 지우고 있던 키였으면 True를 돌려준다."""
        bucket = self._bucket(key)
        for index, (stored_key, _) in enumerate(bucket):
            if stored_key == key:
                del bucket[index]
                self.size -= 1
                return True
        return False

    def __contains__(self, key: Hashable) -> bool:
        """키가 들어 있으면 True를 돌려준다."""
        return any(stored_key == key for stored_key, _ in self._bucket(key))

    def __len__(self) -> int:
        """저장된 키의 개수를 돌려준다."""
        return self.size

    def items(self) -> Iterator[tuple[Hashable, object]]:
        """저장된 (키, 값) 쌍을 하나씩 돌려준다."""
        for bucket in self.buckets:
            yield from bucket
