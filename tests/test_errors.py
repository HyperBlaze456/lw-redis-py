"""5단계 담당 전원. 대상: 전 명령.
작성할 검증: 인자 부족, 리스트 키에 GET, 숫자 자리에 문자 → 죽지 않고 에러 응답.
"""

import pytest

from lwredis.dispatch import execute
from lwredis.store import Store


@pytest.mark.parametrize(
    "line",
    ["SET a", "GET", "GET l", "LPUSH s x", "ZADD z x m", "EXPIRE s x", "LRANGE l 0 x", "NOPE", ""],
)
def test_error_response(line):
    store = Store()
    execute(store, "RPUSH l 1")
    execute(store, "SET s 1")
    assert execute(store, line).startswith("ERR ")
