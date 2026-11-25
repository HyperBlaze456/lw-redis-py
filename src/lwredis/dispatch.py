"""1단계 담당 전원, 5단계 에러 처리: 명령 이름으로 처리 함수를 찾아 실행하는 모듈이다."""

from collections.abc import Callable

from lwredis.commands import keys, lists, zsets
from lwredis.errors import CommandError
from lwredis.store import Store

type Handler = Callable[[Store, list[str]], str]

ERROR_PREFIX = "ERR "  # 모든 에러 응답의 앞부분

COMMANDS: dict[str, Handler] = {
    "SET": keys.cmd_set,
    "GET": keys.cmd_get,
    "DEL": keys.cmd_del,
    "EXISTS": keys.cmd_exists,
    "EXPIRE": keys.cmd_expire,
    "TTL": keys.cmd_ttl,
    "PERSIST": keys.cmd_persist,
    "LPUSH": lists.cmd_lpush,
    "RPUSH": lists.cmd_rpush,
    "LPOP": lists.cmd_lpop,
    "RPOP": lists.cmd_rpop,
    "LLEN": lists.cmd_llen,
    "LRANGE": lists.cmd_lrange,
    "ZADD": zsets.cmd_zadd,
    "ZSCORE": zsets.cmd_zscore,
    "ZRANK": zsets.cmd_zrank,
    "ZRANGE": zsets.cmd_zrange,
    "ZREM": zsets.cmd_zrem,
}


def execute(store: Store, line: str) -> str:
    """명령 한 줄을 받아 COMMANDS에서 처리 함수를 찾아 실행하고 응답 문자열을 돌려준다. 없는 명령과 CommandError는 에러 응답으로 바꾼다."""
    words = line.split()
    if not words:
        return ERROR_PREFIX + "empty command"
    handler = COMMANDS.get(words[0].upper())
    if handler is None:
        return ERROR_PREFIX + f"unknown command '{words[0]}'"
    try:
        return handler(store, words[1:])
    except CommandError as error:
        return ERROR_PREFIX + str(error)
