"""2단계 담당 2번: 이중 연결 리스트 모듈이다."""

from collections.abc import Iterator


class Node:
    """이중 연결 리스트의 노드이다."""

    __slots__ = ("value", "prev", "next")

    def __init__(self, value: object) -> None:
        """값을 담은 노드를 만들고 앞뒤 연결은 비워 둔다."""
        raise NotImplementedError


class DoublyLinkedList:
    """리스트 명령과 LRU의 바탕이 되는 이중 연결 리스트이다."""

    def __init__(self) -> None:
        """빈 리스트를 만든다."""
        raise NotImplementedError

    def push_front(self, value: object) -> Node:
        """앞쪽에 값을 넣고 만든 노드를 돌려준다. LRU가 이 노드를 키→노드 표에 보관한다."""
        raise NotImplementedError

    def push_back(self, value: object) -> Node:
        """뒤쪽에 값을 넣고 만든 노드를 돌려준다. LRU가 이 노드를 키→노드 표에 보관한다."""
        raise NotImplementedError

    def pop_front(self) -> object:
        """앞쪽 값을 빼서 돌려준다."""
        raise NotImplementedError

    def pop_back(self) -> object:
        """뒤쪽 값을 빼서 돌려준다."""
        raise NotImplementedError

    def remove(self, node: Node) -> None:
        """노드 하나를 O(1)에 떼어 낸다."""
        raise NotImplementedError

    def __len__(self) -> int:
        """리스트에 든 값의 개수를 돌려준다."""
        raise NotImplementedError

    def __iter__(self) -> Iterator[object]:
        """앞쪽부터 뒤쪽 순서로 값을 하나씩 돌려준다."""
        raise NotImplementedError
