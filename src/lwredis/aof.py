"""4단계 담당 1번: 쓰기 명령을 파일에 남기고 다시 실행하는 모듈이다."""

from lwredis.dispatch import ERROR_PREFIX, execute
from lwredis.store import Store

DEFAULT_PATH = "lwredis.aof"  # repl과 server가 쓰는 로그 파일

# 저장소의 내용을 바꾸는 명령이다. 이 명령만 로그에 남긴다.
WRITE_COMMANDS = {
    "SET",
    "DEL",
    "EXPIRE",
    "PERSIST",
    "LPUSH",
    "RPUSH",
    "LPOP",
    "RPOP",
    "ZADD",
    "ZREM",
}


class AOF:
    """쓰기 명령을 파일 끝에 덧붙여 기록하는 로그이다."""

    def __init__(self, path: str) -> None:
        """path는 로그 파일의 경로이다."""
        self.path = path
        self.file = open(path, "a", encoding="utf-8")  # 한 번 열어 두고 계속 쓴다

    def append(self, line: str) -> None:
        """쓰기 명령 한 줄을 파일 끝에 기록한다."""
        self.file.write(line + "\n")
        self.file.flush()

    def replay(self, store: Store) -> int:
        """파일의 명령을 처음부터 store에 다시 실행하고 실행한 줄 수를 돌려준다."""
        with open(self.path, encoding="utf-8") as file:
            lines = file.read().splitlines()
        for line in lines:
            execute(store, line)
        return len(lines)

    def run(self, store: Store, line: str) -> str:
        """명령 한 줄을 실행하고 응답을 돌려준다. 성공한 쓰기 명령이면 파일에 기록한다. repl과 server는 이 메서드로 명령을 실행한다."""
        response = execute(store, line)
        words = line.split()
        if (
            words
            and words[0].upper() in WRITE_COMMANDS
            and not response.startswith(ERROR_PREFIX)
        ):
            self.append(" ".join(words))
        return response
