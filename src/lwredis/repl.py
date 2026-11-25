"""1단계 담당 전원: 표준 입력으로 명령을 받는 입력 루프 모듈이다."""

import sys

from lwredis.aof import AOF, DEFAULT_PATH
from lwredis.store import Store


def main() -> None:
    """표준 입력에서 한 줄씩 읽어 execute에 넘기고 응답을 출력하는 입력 루프이다. 시작할 때 로그 파일을 재실행해 지난 내용을 되살린다."""
    store, aof = Store(), AOF(DEFAULT_PATH)
    aof.replay(store)
    for line in sys.stdin:
        if line.strip():
            print(aof.run(store, line))
