"""serve로 띄운 서버에 접속해 명령을 보내고, 함수 결과를 서버에 캐시하는 클라이언트 모듈이다."""

import functools
import json
import socket
import threading
from collections.abc import Callable
from urllib.parse import quote, unquote

from lwredis.commands import NIL
from lwredis.dispatch import ERROR_PREFIX
from lwredis.errors import CommandError


def _pack(value: object) -> str:
    """값을 공백이 없는 글자 한 덩어리로 바꾼다. 서버가 줄을 공백으로 나누기 때문에 필요하다."""
    return quote(json.dumps(value, sort_keys=True), safe="")


def _unpack(text: str) -> object:
    """_pack으로 바꾼 글자를 원래 값으로 되돌린다."""
    return json.loads(unquote(text))


class Client:
    """서버와의 접속 하나이다. 만들 때 한 번 접속하고, 이후의 명령과 캐시가 모두 이 접속을 함께 쓴다."""

    def __init__(self, host: str = "127.0.0.1", port: int = 6380) -> None:
        """host와 port의 서버에 접속한다."""
        self.conn = socket.create_connection((host, port))
        self.reader = self.conn.makefile("r", encoding="utf-8")
        self.lock = threading.Lock()  # 여러 스레드가 한 접속을 쓸 때 요청과 응답이 섞이지 않게 한다

    def command(self, line: str) -> str:
        """명령 한 줄을 보내고 응답 한 줄을 돌려준다. 에러 응답이면 CommandError를 일으킨다."""
        return self.commands(line)[0]

    def commands(self, *lines: str) -> list[str]:
        """명령 여러 줄을 한꺼번에 보내고 응답을 순서대로 돌려준다. 서버까지 한 번만 오가므로 한 줄씩 보내는 것보다 빠르다."""
        with self.lock:
            self.conn.sendall("".join(line + "\n" for line in lines).encode())
            responses = [self.reader.readline() for _ in lines]
        if not all(responses):
            raise ConnectionError("server closed the connection")
        responses = [response.rstrip("\n") for response in responses]
        for response in responses:
            if response.startswith(ERROR_PREFIX):
                raise CommandError(response.removeprefix(ERROR_PREFIX))
        return responses

    def cache(self, ttl: int | None = None) -> Callable[[Callable], Callable]:
        """함수의 결과를 서버에 저장하고, 같은 인자로 다시 부르면 함수를 실행하지 않고 저장된 값을 돌려주는 데코레이터를 만든다.

        ttl은 저장한 값이 사라지기까지의 초이고 None이면 사라지지 않는다.
        인자와 결과는 JSON으로 바꿀 수 있는 값(숫자, 문자열, 리스트, dict, True/False, None)이어야 한다.
        """

        def decorator(function: Callable) -> Callable:
            name = f"{function.__module__}.{function.__qualname__}"

            def key(*args: object, **kwargs: object) -> str:
                """이 인자로 부른 결과가 서버에 저장되는 키를 돌려준다."""
                return f"{name}:{_pack([args, kwargs])}"

            @functools.wraps(function)
            def wrapper(*args: object, **kwargs: object) -> object:
                stored_at = key(*args, **kwargs)
                found = self.command(f"GET {stored_at}")
                if found != NIL:
                    return _unpack(found)
                value = function(*args, **kwargs)
                writes = [f"SET {stored_at} {_pack(value)}"]
                if ttl is not None:
                    writes.append(f"EXPIRE {stored_at} {ttl}")
                self.commands(*writes)
                return value

            wrapper.key = key
            return wrapper

        return decorator

    def close(self) -> None:
        """접속을 닫는다."""
        self.reader.close()
        self.conn.close()
