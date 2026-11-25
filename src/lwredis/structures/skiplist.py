"""3단계 담당 3번: 스킵 리스트 기반 정렬 집합 모듈이다."""

import random
from collections.abc import Iterator
from itertools import islice

from lwredis.structures.hashtable import HashTable

MAX_LEVEL = 16  # 노드가 가질 수 있는 층 수의 한도


class _Node:
    """스킵 리스트의 노드이다. next[i]는 i층에서 이 노드 다음에 오는 노드이다."""

    __slots__ = ("score", "member", "next")

    def __init__(self, score: float, member: str, level: int) -> None:
        self.score = score
        self.member = member
        self.next: list[_Node | None] = [None] * level


class SkipListSet:
    """정렬 집합의 내부를 교체하는 스킵 리스트 버전이고, 명령은 그대로 둔다."""

    def __init__(self) -> None:
        """빈 정렬 집합을 만든다."""
        self.scores = HashTable()  # 멤버 → 점수
        self.head = _Node(0.0, "", MAX_LEVEL)  # 모든 층의 출발점이 되는 표지 노드

    def _path(self, score: float, member: str) -> list[_Node]:
        """층마다 (score, member) 자리의 바로 앞 노드를 찾아 돌려준다. 맨 위층에서 출발해 오른쪽으로 가다가 넘치기 전에 한 층씩 내려온다."""
        path = [self.head] * MAX_LEVEL
        node = self.head
        for level in reversed(range(MAX_LEVEL)):
            while (after := node.next[level]) is not None and (
                after.score,
                after.member,
            ) < (score, member):
                node = after
            path[level] = node
        return path

    def add(self, member: str, score: float) -> bool:
        """멤버를 점수와 함께 넣고 새 멤버면 True, 점수만 바꿨으면 False를 돌려준다."""
        is_new = not self.remove(member)
        self.scores.set(member, score)
        level = 1
        while level < MAX_LEVEL and random.random() < 0.5:
            level += 1
        node = _Node(score, member, level)
        for index, before in enumerate(self._path(score, member)[:level]):
            node.next[index] = before.next[index]
            before.next[index] = node
        return is_new

    def score(self, member: str) -> float | None:
        """멤버의 점수를 돌려주고 없으면 None을 돌려준다."""
        return self.scores.get(member)

    def _members(self) -> Iterator[str]:
        """맨 아래층을 따라 모든 멤버를 순서대로 돌려준다."""
        node = self.head.next[0]
        while node is not None:
            yield node.member
            node = node.next[0]

    def rank(self, member: str) -> int | None:
        """멤버의 순위(0부터)를 돌려주고 없으면 None을 돌려준다."""
        if member not in self.scores:
            return None
        return next(i for i, found in enumerate(self._members()) if found == member)

    def range(self, start: int, stop: int) -> list[str]:
        """순위 start부터 stop까지(양 끝 포함)의 멤버를 순서대로 돌려준다."""
        return list(islice(self._members(), start, stop + 1))

    def remove(self, member: str) -> bool:
        """멤버를 지우고 있던 멤버였으면 True를 돌려준다."""
        score = self.scores.get(member)
        if score is None:
            return False
        path = self._path(score, member)
        node = path[0].next[0]
        for index in range(len(node.next)):
            path[index].next[index] = node.next[index]
        self.scores.delete(member)
        return True

    def __len__(self) -> int:
        """멤버의 개수를 돌려준다."""
        return len(self.scores)
