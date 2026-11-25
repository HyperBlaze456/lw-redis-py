"""2단계 담당 2번: 이중 연결 리스트 모듈이다."""

from collections.abc import Iterator


class Node:
    """이중 연결 리스트의 노드이다."""

    __slots__ = ("value", "prev", "next")

    def __init__(self, value: object) -> None:
        """값을 담은 노드를 만들고 앞뒤 연결은 비워 둔다."""
        self.value = value
        self.prev: Node | None = None
        self.next: Node | None = None


class DoublyLinkedList:
    """리스트 명령과 LRU의 바탕이 되는 이중 연결 리스트이다."""

    def __init__(self) -> None:
        """빈 리스트를 만든다. head와 tail은 값이 없는 양 끝 표지 노드이고, 실제 값은 그 사이에 놓인다."""
        self.head = Node(None)
        self.tail = Node(None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def _insert_after(self, prev: Node, value: object) -> Node:
        """prev 노드 바로 뒤에 값을 넣고 만든 노드를 돌려준다."""
        node = Node(value)
        node.prev, node.next = prev, prev.next
        prev.next.prev = node
        prev.next = node
        self.size += 1
        return node

    def push_front(self, value: object) -> Node:
        """앞쪽에 값을 넣고 만든 노드를 돌려준다. LRU가 이 노드를 키→노드 표에 보관한다."""
        return self._insert_after(self.head, value)

    def push_back(self, value: object) -> Node:
        """뒤쪽에 값을 넣고 만든 노드를 돌려준다. LRU가 이 노드를 키→노드 표에 보관한다."""
        return self._insert_after(self.tail.prev, value)

    def pop_front(self) -> object:
        """앞쪽 값을 빼서 돌려준다. 비어 있으면 None을 돌려준다."""
        return self._pop(self.head.next)

    def pop_back(self) -> object:
        """뒤쪽 값을 빼서 돌려준다. 비어 있으면 None을 돌려준다."""
        return self._pop(self.tail.prev)

    def _pop(self, node: Node) -> object:
        """노드를 떼어 내고 그 값을 돌려준다. 리스트가 비어 있으면 None을 돌려준다."""
        if self.size == 0:
            return None
        self.remove(node)
        return node.value

    def remove(self, node: Node) -> None:
        """노드 하나를 O(1)에 떼어 낸다."""
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def __len__(self) -> int:
        """리스트에 든 값의 개수를 돌려준다."""
        return self.size

    def __iter__(self) -> Iterator[object]:
        """앞쪽부터 뒤쪽 순서로 값을 하나씩 돌려준다."""
        node = self.head.next
        while node is not self.tail:
            yield node.value
            node = node.next
