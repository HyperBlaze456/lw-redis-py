"""명령 처리 함수를 모아 둔 패키지이다. 세 명령 모듈이 함께 쓰는 응답 문자열과 도구도 여기에 둔다."""

from collections.abc import Callable

from lwredis.errors import CommandError
from lwredis.store import Store

NIL = "(nil)"  # 값이 없을 때의 응답
EMPTY = "(empty)"  # 여러 값을 돌려주는 명령의 결과가 하나도 없을 때의 응답


def take(args: list[str], count: int) -> list[str]:
    """인자를 앞에서 count개 꺼내고 모자라면 CommandError를 일으킨다."""
    if len(args) < count:
        raise CommandError("wrong number of arguments")
    return args[:count]


def number[T: (int, float)](text: str, kind: Callable[[str], T]) -> T:
    """문자열을 kind(int 또는 float)로 바꾸고 숫자가 아니면 CommandError를 일으킨다."""
    try:
        return kind(text)
    except ValueError:
        raise CommandError(f"'{text}' is not a number") from None


def find[T](store: Store, key: str, kind: type[T]) -> T | None:
    """키의 값을 돌려주고 없으면 None을 돌려준다. 값이 kind 타입이 아니면 CommandError를 일으킨다."""
    value = store.get(key)
    if value is not None and not isinstance(value, kind):
        raise CommandError("wrong type of value for this command")
    return value


def find_or_new[T](store: Store, key: str, kind: type[T], save: bool = False) -> T:
    """find와 같지만 키가 없으면 빈 kind를 만들어 돌려준다. save가 참이면 만든 것을 키에 저장한다."""
    value = find(store, key, kind)
    if value is None:
        value = kind()
        if save:
            store.set(key, value)
    return value


def bounds(start: int, stop: int, length: int) -> tuple[int, int]:
    """Redis식 범위를 0부터 세는 (start, stop)으로 바꾼다. 음수는 뒤에서부터 세고(-1이 마지막) 양 끝을 포함한다."""
    if start < 0:
        start = max(start + length, 0)
    if stop < 0:
        stop = max(stop + length, -1)
    return start, min(stop, length - 1)
