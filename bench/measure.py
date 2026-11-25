"""4단계 담당 3번: 자료구조 성능을 재고 그래프를 그리는 모듈이다.

`python -m bench.measure`로 실행하고 그래프 네 장을 `bench/graphs/`에 저장한다.
"""

import os
import random
import time

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from lwredis.lru import LRU
from lwredis.structures.hashtable import HashTable
from lwredis.structures.linkedlist import DoublyLinkedList
from lwredis.structures.skiplist import SkipListSet
from lwredis.structures.sorted_array import SortedArraySet

SIZES = (1_000, 10_000, 100_000)
GRAPH_DIR = "bench/graphs"


def _seconds(action) -> float:
    """action을 한 번 실행하는 데 걸린 초를 돌려준다."""
    start = time.perf_counter()
    action()
    return time.perf_counter() - start


def _plot(name: str, title: str, sizes, series: dict[str, list[float]]) -> None:
    """series마다 선 하나를 로그 축으로 그려 GRAPH_DIR/name.png로 저장한다."""
    os.makedirs(GRAPH_DIR, exist_ok=True)
    plt.figure()
    for label, times in series.items():
        plt.plot(sizes, times, marker="o", label=label)
        print(f"{name} {label}: " + ", ".join(f"{n}={t:.3g}s" for n, t in zip(sizes, times)))
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("n")
    plt.ylabel("seconds")
    plt.title(title)
    plt.legend()
    plt.savefig(os.path.join(GRAPH_DIR, f"{name}.png"))
    plt.close()


def bench_lookup(sizes: tuple[int, ...] = SIZES) -> None:
    """키 조회 시간을 해시 테이블과 리스트 순차 탐색으로 나누어 재고 그래프로 그린다."""
    table_times, list_times = [], []
    for n in sizes:
        table = HashTable()
        for i in range(n):
            table.set(i, i)
        pairs = [(i, i) for i in range(n)]
        keys = [random.randrange(n) for _ in range(100)]
        table_times.append(_seconds(lambda: [table.get(k) for k in keys]) / 100)
        list_times.append(_seconds(lambda: [next(v for k, v in pairs if k == key) for key in keys]) / 100)
    _plot("lookup", "Lookup time per key", sizes, {"HashTable": table_times, "list scan": list_times})


def bench_push_front(sizes: tuple[int, ...] = SIZES) -> None:
    """앞쪽 삽입 시간을 이중 연결 리스트와 내장 list.insert(0, x)로 나누어 재고 그래프로 그린다."""
    linked_times, list_times = [], []
    for n in sizes:
        linked = DoublyLinkedList()
        plain = []
        linked_times.append(_seconds(lambda: [linked.push_front(i) for i in range(n)]))
        list_times.append(_seconds(lambda: [plain.insert(0, i) for i in range(n)]))
    _plot("push_front", "Total time for n front inserts", sizes, {"DoublyLinkedList": linked_times, "list.insert(0, x)": list_times})


def bench_evict(sizes: tuple[int, ...] = SIZES) -> None:
    """축출 1회 시간을 해시 + 연결 리스트 LRU와 사용 시각을 적어 두고 전체 탐색하는 방식으로 나누어 재고 그래프로 그린다."""
    lru_times, scan_times = [], []
    for n in sizes:
        lru = LRU(n)
        last_used = {}
        for i in range(n):
            lru.touch(i)
            last_used[i] = i
        lru_times.append(_seconds(lambda: [lru.evict() for _ in range(100)]) / 100)
        scan_times.append(_seconds(lambda: [last_used.pop(min(last_used, key=last_used.get)) for _ in range(100)]) / 100)
    _plot("evict", "Time per eviction", sizes, {"LRU (hash + linked list)": lru_times, "full scan": scan_times})


def bench_insert(sizes: tuple[int, ...] = SIZES) -> None:
    """삽입 시간을 스킵 리스트와 정렬 배열로 나누어 재고 그래프로 그린다."""
    skip_times, array_times = [], []
    for n in sizes:
        scores = [random.random() for _ in range(n)]
        skip, array = SkipListSet(), SortedArraySet()
        skip_times.append(_seconds(lambda: [skip.add(f"m{i}", s) for i, s in enumerate(scores)]))
        array_times.append(_seconds(lambda: [array.add(f"m{i}", s) for i, s in enumerate(scores)]))
    _plot("insert", "Total time to add n members", sizes, {"SkipListSet": skip_times, "SortedArraySet": array_times})


def main() -> None:
    """네 가지 측정을 차례로 실행해 그래프를 GRAPH_DIR에 저장한다."""
    bench_lookup()
    bench_push_front()
    bench_evict()
    bench_insert()
    print(f"graphs saved in {GRAPH_DIR}")


if __name__ == "__main__":
    main()
