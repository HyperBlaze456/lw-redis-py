"""2단계 담당 1번: 해시 테이블 모듈이다."""

from collections.abc import Hashable, Iterator


class HashTable:
    """모든 키 저장에 쓰고, 만료 시각표, LRU의 키→노드, 정렬 집합의 멤버→점수에 재사용한다."""

    def __init__(self) -> None:
        """빈 해시 테이블을 만든다."""
        raise NotImplementedError

    def get(self, key: Hashable, default: object = None) -> object:
        """키의 값을 돌려주고 없으면 default를 돌려준다."""
        raise NotImplementedError

    def set(self, key: Hashable, value: object) -> None:
        """키에 값을 저장하고 이미 있으면 값을 바꾼다."""
        raise NotImplementedError

    def delete(self, key: Hashable) -> bool:
        """키를 지우고 있던 키였으면 True를 돌려준다."""
        raise NotImplementedError

    def __contains__(self, key: Hashable) -> bool:
        """키가 들어 있으면 True를 돌려준다."""
        raise NotImplementedError

    def __len__(self) -> int:
        """저장된 키의 개수를 돌려준다."""
        raise NotImplementedError

    def items(self) -> Iterator[tuple[Hashable, object]]:
        """저장된 (키, 값) 쌍을 하나씩 돌려준다."""
        raise NotImplementedError
