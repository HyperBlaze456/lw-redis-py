"""2단계 담당 2번. 대상: structures.linkedlist.
작성할 검증: 무작위 양끝 삽입·삭제 1만 번을 `collections.deque`와 비교.
"""

from collections import deque

from lwredis.structures.linkedlist import DoublyLinkedList


def test_matches_deque(rng):
    linked, expected = DoublyLinkedList(), deque()
    for i in range(10_000):
        op = rng.choice(["push_front", "push_back", "pop_front", "pop_back"])
        if op == "push_front":
            linked.push_front(i)
            expected.appendleft(i)
        elif op == "push_back":
            linked.push_back(i)
            expected.append(i)
        elif op == "pop_front":
            assert linked.pop_front() == (expected.popleft() if expected else None)
        else:
            assert linked.pop_back() == (expected.pop() if expected else None)
        assert list(linked) == list(expected)
