# lw-redis-py

파이썬으로 만드는 Redis 일부 클론이다.

## 실행

이 프로젝트는 [uv](https://docs.astral.sh/uv/)로 관리하고 파이썬 3.15를 쓴다.

```
uv sync                          # 파이썬 3.15, 가상 환경, 개발 도구를 한 번에 준비
uv run python -m lwredis         # 입력 루프
uv run python -m lwredis serve   # TCP 서버 (127.0.0.1:6380, `nc 127.0.0.1 6380`으로 접속)
uv run python -m lwredis serve 1000   # 키를 1000개까지만 두는 서버 (넘으면 가장 오래 쓰지 않은 키부터 지운다)
uv run pytest                    # 테스트
uv run python -m bench.measure   # 성능 그래프
```

- `uv sync`는 `.python-version`에 적힌 파이썬을 내려받고 `.venv/`를 만든 뒤 `uv.lock`에 적힌 버전 그대로 설치한다.
- `uv run`은 실행 전에 환경을 `uv.lock`에 맞추므로, `.venv`를 직접 켜거나 `pip`을 쓸 필요가 없다.
- 라이브러리를 추가할 때는 `uv add 이름`을, 개발 도구를 추가할 때는 `uv add --dev 이름`을 쓴다. 이때 바뀌는 `pyproject.toml`과 `uv.lock`은 함께 커밋한다.
- `uv sync`가 파이썬 3.15를 찾지 못하면 uv가 오래된 것이다. `uv self update`로 올린 뒤 다시 실행한다.

코드는 `src/lwredis/`에 있다.
`uv sync`는 이 폴더를 가리키는 연결만 설치하므로, 코드를 고친 뒤에 다시 설치할 필요가 없다.

입력 루프와 서버는 성공한 쓰기 명령을 실행한 폴더의 `lwredis.aof`에 기록하고, 다음에 시작할 때 이 파일을 재실행해 내용을 되살린다.

## 명령이 처리되는 순서

1. `repl.main` 또는 `server.serve`가 한 줄을 읽어 `AOF.run`에 넘긴다.
2. `AOF.run`이 `dispatch.execute`를 부르고, 성공한 쓰기 명령이면 파일에 한 줄을 남긴다.
3. `execute`가 줄을 공백으로 나누고, 첫 단어로 `COMMANDS`에서 처리 함수를 찾아 부른다.
4. `commands/`의 처리 함수가 인자를 검사하고 `Store`에서 값을 꺼내거나 저장한다.
5. `Store`가 만료 검사(`Expiry`)와 접근 기록(`LRU`)을 거쳐 `HashTable`을 읽고 쓴다.
6. 처리 함수가 응답 문자열을 돌려주고, `CommandError`가 나면 `execute`가 에러 응답으로 바꾼다.

## 응답 형식

| 경우 | 응답 |
|---|---|
| `SET` 성공 | `OK` |
| 값 하나 (`GET`, `LPOP`, `RPOP`, `ZSCORE`, `ZRANK`) | 값 그대로, 없으면 `(nil)` |
| 했는지 여부 (`DEL`, `EXISTS`, `EXPIRE`, `PERSIST`, `ZADD`, `ZREM`) | `1` 또는 `0` |
| 길이 (`LPUSH`, `RPUSH`, `LLEN`) | 숫자 |
| 여러 값 (`LRANGE`, `ZRANGE`) | 공백으로 이어 붙인 한 줄, 하나도 없으면 `(empty)` |
| `TTL` | 남은 초, 만료 시각이 없으면 `-1`, 없는 키면 `-2` |
| 에러 | `ERR `로 시작하는 한 줄 |

인자가 모자라면 에러이고, 남는 인자는 무시한다.

## 파이썬 코드에서 쓰기

서버를 먼저 띄운 뒤, 파이썬 코드에서 `Client`로 한 번 접속하고 그 접속을 계속 쓴다.

```python
from lwredis.client import Client

client = Client()                 # 127.0.0.1:6380에 접속한다

@client.cache(ttl=60)             # 결과를 서버에 60초 동안 저장한다
def find_user(user_id):
    return {"id": user_id, "name": load_name(user_id)}

find_user(7)                      # 함수를 실행하고 결과를 서버에 저장한다
find_user(7)                      # 함수를 실행하지 않고 서버에 저장된 값을 돌려준다
client.command("LPUSH jobs a")    # 명령을 직접 보낼 수도 있다
```

- `ttl`은 저장한 값이 사라지기까지의 초이다. 생략하면 사라지지 않는다.
- 키 개수 한도는 데코레이터가 아니라 서버를 띄울 때 정한다(`serve 1000`). 서버가 모든 키를 하나의 LRU 기록으로 관리하기 때문이다.
- 인자와 결과는 JSON으로 바꿀 수 있는 값(숫자, 문자열, 리스트, dict, True/False, None)이어야 한다.
- 저장되는 키는 `find_user.key(7)`로 확인할 수 있다. `client.command(f"DEL {find_user.key(7)}")`로 저장된 값 하나를 지운다.

## 구조

```
pyproject.toml         패키지 정보, 개발 도구 목록, pytest 설정
uv.lock                설치할 버전을 고정한 잠금 파일 (손으로 고치지 않는다)
.python-version        사용할 파이썬 버전 (3.15)
src/
  lwredis/
    __main__.py        python -m lwredis 진입점
    repl.py            표준 입력 루프
    errors.py          CommandError 예외
    store.py           모든 키를 보관하는 저장소
    dispatch.py        명령 이름으로 처리 함수를 찾아 실행
    expiry.py          키 만료 시각표
    lru.py             LRU 축출 기록
    aof.py             쓰기 명령 로그와 재실행
    server.py          TCP 서버
    client.py          서버에 접속하는 클라이언트와 캐시 데코레이터
    commands/
      keys.py          SET GET DEL EXISTS EXPIRE TTL PERSIST
      lists.py         LPUSH RPUSH LPOP RPOP LLEN LRANGE
      zsets.py         ZADD ZSCORE ZRANK ZRANGE ZREM
    structures/
      hashtable.py     해시 테이블
      linkedlist.py    이중 연결 리스트
      sorted_array.py  정렬 배열 기반 정렬 집합
      skiplist.py      스킵 리스트 기반 정렬 집합
bench/
  measure.py           성능 측정과 그래프
tests/
  conftest.py          고정 시드 rng
  test_*.py            단계별 검증
```

아래 표의 구현 파일은 `bench/measure`를 빼고 모두 `src/lwredis/` 아래에 있다.

## 단계별 작업

| 순서 | 담당 | 구현 파일 | 테스트 파일 |
|---|---|---|---|
| 1 | 전원 | dispatch, repl, store, commands/keys | tests/test_dispatch.py |
| 2 | 1번 | structures/hashtable | tests/test_hashtable.py |
| 2 | 2번 | structures/linkedlist | tests/test_linkedlist.py |
| 2 | 3번 | structures/sorted_array, commands/zsets | tests/test_sorted_array.py |
| 3 | 1번 | expiry, commands/keys | tests/test_expiry.py |
| 3 | 2번 | commands/lists | tests/test_list_commands.py |
| 3 | 3번 | structures/skiplist | tests/test_skiplist.py |
| 4 | 1번 | aof | tests/test_aof.py |
| 4 | 2번 | lru | tests/test_lru.py |
| 4 | 3번 | bench/measure | 없음 |
| 5 | 전원 | errors, dispatch | tests/test_errors.py |
| 5 | 전원 | server | tests/test_server.py |

## 합의할 것

- `structures/`의 메서드 이름은 제안이다. 세 사람이 2단계 전에 확정한다.
- `execute`는 저장소를 첫 인자로 받는다. AOF 테스트에서 저장소 두 개를 나란히 돌리기 위해서이다.
- 응답 문자열의 형식은 위의 "응답 형식" 표대로 구현했다. 바꾸려면 `commands/__init__.py`의 `NIL`, `EMPTY`와 `dispatch.py`의 `ERROR_PREFIX`를 고친다.
