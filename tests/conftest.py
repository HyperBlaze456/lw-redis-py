"""여러 테스트가 함께 쓰는 준비물이다. 2~3단계의 무작위 테스트는 rng를 써서 실패가 재현되게 한다."""

import random
import socket
import threading
import time

import pytest

from lwredis.server import serve

SEED = 20261118


@pytest.fixture
def rng() -> random.Random:
    """고정한 시드로 만든 난수 생성기를 돌려준다."""
    return random.Random(SEED)


@pytest.fixture
def server_port(tmp_path) -> int:
    """비어 있는 포트에 서버를 띄우고, 접속을 받기 시작하면 그 포트 번호를 돌려준다."""
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    args = ("127.0.0.1", port, str(tmp_path / "log.aof"))
    threading.Thread(target=serve, args=args, daemon=True).start()
    for _ in range(500):
        try:
            socket.create_connection(("127.0.0.1", port)).close()
            return port
        except OSError:
            time.sleep(0.01)
    raise TimeoutError("server did not start")
