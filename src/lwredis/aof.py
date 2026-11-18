"""4단계 담당 1번: 쓰기 명령을 파일에 남기고 다시 실행하는 모듈이다."""

from lwredis.store import Store


class AOF:
    """쓰기 명령을 파일 끝에 덧붙여 기록하는 로그이다."""

    def __init__(self, path: str) -> None:
        """path는 로그 파일의 경로이다."""
        raise NotImplementedError

    def append(self, line: str) -> None:
        """쓰기 명령 한 줄을 파일 끝에 기록한다."""
        raise NotImplementedError

    def replay(self, store: Store) -> int:
        """파일의 명령을 처음부터 store에 다시 실행하고 실행한 줄 수를 돌려준다."""
        raise NotImplementedError
