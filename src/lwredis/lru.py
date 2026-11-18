"""4단계 담당 2번: LRU 축출 기록 모듈이다."""


class LRU:
    """HashTable(키→노드)과 DoublyLinkedList로 만든 LRU 기록이다."""

    def __init__(self, capacity: int) -> None:
        """capacity는 기록할 키 개수의 한도이다."""
        raise NotImplementedError

    def touch(self, key: str) -> None:
        """키를 가장 최근에 쓴 것으로 표시하고 없던 키면 새로 등록한다."""
        raise NotImplementedError

    def evict(self) -> str | None:
        """가장 오래 쓰지 않은 키를 빼서 돌려준다."""
        raise NotImplementedError

    def remove(self, key: str) -> None:
        """키의 기록을 지운다."""
        raise NotImplementedError

    def __len__(self) -> int:
        """기록된 키의 개수를 돌려준다."""
        raise NotImplementedError
