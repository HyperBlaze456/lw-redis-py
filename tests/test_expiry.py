"""3단계 담당 1번. 대상: lwredis.expiry, store.
작성할 검증: 현재 시각 함수를 바꿔 끼우고, 시각을 11초 뒤로 돌려 `EXPIRE a 10`한 키가 사라졌는지 확인.
"""

from lwredis.dispatch import execute
from lwredis.store import Store


def test_expire_removes_key():
    clock = [1000.0]
    store = Store(now=lambda: clock[0])
    execute(store, "SET a 1")
    assert execute(store, "EXPIRE a 10") == "1"
    assert execute(store, "TTL a") == "10"
    clock[0] += 11
    assert execute(store, "GET a") == "(nil)"
    assert execute(store, "TTL a") == "-2"


def test_persist_keeps_key():
    clock = [1000.0]
    store = Store(now=lambda: clock[0])
    execute(store, "SET a 1")
    execute(store, "EXPIRE a 10")
    assert execute(store, "PERSIST a") == "1"
    clock[0] += 11
    assert execute(store, "GET a") == "1"
