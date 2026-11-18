"""4단계 담당 3번: 자료구조 성능을 재고 그래프를 그리는 모듈이다.

`python -m bench.measure`로 실행하고 그래프 네 장을 `bench/graphs/`에 저장한다.
"""

SIZES = (1_000, 10_000, 100_000)
GRAPH_DIR = "bench/graphs"


def bench_lookup(sizes: tuple[int, ...] = SIZES) -> None:
    """키 조회 시간을 해시 테이블과 리스트 순차 탐색으로 나누어 재고 그래프로 그린다."""
    raise NotImplementedError


def bench_push_front(sizes: tuple[int, ...] = SIZES) -> None:
    """앞쪽 삽입 시간을 이중 연결 리스트와 내장 list.insert(0, x)로 나누어 재고 그래프로 그린다."""
    raise NotImplementedError


def bench_evict(sizes: tuple[int, ...] = SIZES) -> None:
    """축출 1회 시간을 해시 + 연결 리스트 LRU와 사용 시각을 적어 두고 전체 탐색하는 방식으로 나누어 재고 그래프로 그린다."""
    raise NotImplementedError


def bench_insert(sizes: tuple[int, ...] = SIZES) -> None:
    """삽입 시간을 스킵 리스트와 정렬 배열로 나누어 재고 그래프로 그린다."""
    raise NotImplementedError


def main() -> None:
    """네 가지 측정을 차례로 실행해 그래프를 GRAPH_DIR에 저장한다."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
