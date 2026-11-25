"""3단계 담당 2번: 리스트 명령 모듈이다."""

from collections.abc import Callable

from lwredis.commands import EMPTY, NIL, bounds, find_or_new, number, take
from lwredis.store import Store
from lwredis.structures.linkedlist import DoublyLinkedList


def _push(
    store: Store, args: list[str], push: Callable[[DoublyLinkedList, str], object]
) -> str:
    """값들을 push로 하나씩 넣고 리스트의 길이를 돌려준다. 리스트가 없으면 새로 만든다."""
    take(args, 2)
    values = find_or_new(store, args[0], DoublyLinkedList, save=True)
    for value in args[1:]:
        push(values, value)
    return str(len(values))


def _pop(
    store: Store, args: list[str], pop: Callable[[DoublyLinkedList], object]
) -> str:
    """pop으로 값 하나를 빼서 돌려준다. 리스트가 비면 키도 지운다."""
    [key] = take(args, 1)
    values = find_or_new(store, key, DoublyLinkedList)
    value = pop(values)
    if len(values) == 0:
        store.delete(key)
    return NIL if value is None else value


def cmd_lpush(store: Store, args: list[str]) -> str:
    """LPUSH key value [value ...]: 리스트의 앞쪽에 값을 넣는다."""
    return _push(store, args, DoublyLinkedList.push_front)


def cmd_rpush(store: Store, args: list[str]) -> str:
    """RPUSH key value [value ...]: 리스트의 뒤쪽에 값을 넣는다."""
    return _push(store, args, DoublyLinkedList.push_back)


def cmd_lpop(store: Store, args: list[str]) -> str:
    """LPOP key: 리스트의 앞쪽 값을 빼서 돌려준다."""
    return _pop(store, args, DoublyLinkedList.pop_front)


def cmd_rpop(store: Store, args: list[str]) -> str:
    """RPOP key: 리스트의 뒤쪽 값을 빼서 돌려준다."""
    return _pop(store, args, DoublyLinkedList.pop_back)


def cmd_llen(store: Store, args: list[str]) -> str:
    """LLEN key: 리스트의 길이를 돌려준다."""
    [key] = take(args, 1)
    return str(len(find_or_new(store, key, DoublyLinkedList)))


def cmd_lrange(store: Store, args: list[str]) -> str:
    """LRANGE key start stop: 리스트의 지정한 범위의 값을 돌려준다."""
    key, start, stop = take(args, 3)
    values = list(find_or_new(store, key, DoublyLinkedList))
    start, stop = bounds(number(start, int), number(stop, int), len(values))
    return " ".join(values[start : stop + 1]) or EMPTY
