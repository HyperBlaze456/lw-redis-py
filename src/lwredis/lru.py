"""4단계 담당 2번: LRU 축출 기록 모듈이다."""

from lwredis.structures.hashtable import HashTable
from lwredis.structures.linkedlist import DoublyLinkedList


class LRU:
    """HashTable(키→노드)과 DoublyLinkedList로 만든 LRU 기록이다."""

    def __init__(self, capacity: int) -> None:
        """capacity는 기록할 키 개수의 한도이다."""
        self.capacity = capacity
        self.nodes = HashTable()  # 키 → order 안의 노드
        self.order = DoublyLinkedList()  # 앞쪽일수록 최근에 쓴 키

    def touch(self, key: str) -> None:
        """키를 가장 최근에 쓴 것으로 표시하고 없던 키면 새로 등록한다."""
        self.remove(key)
        self.nodes.set(key, self.order.push_front(key))

    def evict(self) -> str | None:
        """가장 오래 쓰지 않은 키를 빼서 돌려준다."""
        key = self.order.pop_back()
        self.nodes.delete(key)
        return key

    def remove(self, key: str) -> None:
        """키의 기록을 지운다."""
        node = self.nodes.get(key)
        if node is not None:
            self.order.remove(node)
            self.nodes.delete(key)

    def __len__(self) -> int:
        """기록된 키의 개수를 돌려준다."""
        return len(self.order)
