"""대상: lwredis.client.
검증: 캐시 데코레이터를 붙인 함수를 같은 인자로 다시 부르면 함수가 실행되지 않고, 다른 접속도 같은 값을 받는다.
"""

import pytest

from lwredis.client import Client
from lwredis.errors import CommandError


def make_square(client, calls, ttl=None):
    """실행될 때마다 calls에 인자를 적는 함수를 만들어 client의 캐시를 붙인다."""

    @client.cache(ttl=ttl)
    def square(n):
        calls.append(n)
        return {"n": n, "squared": n * n}

    return square


def test_cached_result_is_shared(server_port):
    first, second, calls = Client(port=server_port), Client(port=server_port), []
    square = make_square(first, calls)
    assert square(4) == {"n": 4, "squared": 16}
    assert square(4) == {"n": 4, "squared": 16}
    assert make_square(second, calls)(4) == {"n": 4, "squared": 16}
    assert square(5) == {"n": 5, "squared": 25}
    assert calls == [4, 5]


def test_ttl_is_set_on_the_key(server_port):
    client = Client(port=server_port)
    square = make_square(client, [], ttl=60)
    square(4)
    assert 0 < int(client.command(f"TTL {square.key(4)}")) <= 60
    assert client.command(f"TTL {make_square(client, []).key(9)}") == "-2"


def test_error_response_raises(server_port):
    with pytest.raises(CommandError):
        Client(port=server_port).command("NOPE")
