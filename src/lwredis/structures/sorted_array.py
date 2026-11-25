"""2단계 담당 3번: 정렬 배열 기반 정렬 집합 모듈이다."""

from bisect import bisect_left, insort

from lwredis.structures.hashtable import HashTable


class SortedArraySet:
    """정렬 배열과 이진 탐색으로 만든 정렬 집합이다. 순서는 점수 오름차순이고 같은 점수는 멤버 사전순이다. SkipListSet과 메서드가 같아야 한다."""

    def __init__(self) -> None:
        """빈 정렬 집합을 만든다."""
        self.scores = HashTable()  # 멤버 → 점수
        self.pairs: list[tuple[float, str]] = []  # (점수, 멤버)를 순서대로 둔 배열

    def add(self, member: str, score: float) -> bool:
        """멤버를 점수와 함께 넣고 새 멤버면 True, 점수만 바꿨으면 False를 돌려준다."""
        is_new = not self.remove(member)
        self.scores.set(member, score)
        insort(self.pairs, (score, member))
        return is_new

    def score(self, member: str) -> float | None:
        """멤버의 점수를 돌려주고 없으면 None을 돌려준다."""
        return self.scores.get(member)

    def rank(self, member: str) -> int | None:
        """멤버의 순위(0부터)를 돌려주고 없으면 None을 돌려준다."""
        score = self.scores.get(member)
        if score is None:
            return None
        return bisect_left(self.pairs, (score, member))

    def range(self, start: int, stop: int) -> list[str]:
        """순위 start부터 stop까지(양 끝 포함)의 멤버를 순서대로 돌려준다."""
        return [member for _, member in self.pairs[start : stop + 1]]

    def remove(self, member: str) -> bool:
        """멤버를 지우고 있던 멤버였으면 True를 돌려준다."""
        rank = self.rank(member)
        if rank is None:
            return False
        del self.pairs[rank]
        self.scores.delete(member)
        return True

    def __len__(self) -> int:
        """멤버의 개수를 돌려준다."""
        return len(self.pairs)
