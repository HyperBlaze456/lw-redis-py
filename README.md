# lw-redis-py

파이썬으로 만드는 Redis 일부 클론이다.

## 실행

이 프로젝트는 [uv](https://docs.astral.sh/uv/)로 관리하고 파이썬 3.15를 쓴다.

```
uv sync                          # 파이썬 3.15, 가상 환경, 개발 도구를 한 번에 준비
uv run python -m lwredis         # 입력 루프
uv run pytest                    # 테스트
uv run python -m bench.measure   # 성능 그래프
```

- `uv sync`는 `.python-version`에 적힌 파이썬을 내려받고 `.venv/`를 만든 뒤 `uv.lock`에 적힌 버전 그대로 설치한다.
- `uv run`은 실행 전에 환경을 `uv.lock`에 맞추므로, `.venv`를 직접 켜거나 `pip`을 쓸 필요가 없다.
- 라이브러리를 추가할 때는 `uv add 이름`을, 개발 도구를 추가할 때는 `uv add --dev 이름`을 쓴다. 이때 바뀌는 `pyproject.toml`과 `uv.lock`은 함께 커밋한다.
- `uv sync`가 파이썬 3.15를 찾지 못하면 uv가 오래된 것이다. `uv self update`로 올린 뒤 다시 실행한다.

코드는 `src/lwredis/`에 있다.
`uv sync`는 이 폴더를 가리키는 연결만 설치하므로, 코드를 고친 뒤에 다시 설치할 필요가 없다.

지금은 모든 함수가 `NotImplementedError`를 일으킨다.
테스트 파일에는 무엇을 작성할지에 대한 설명만 있다.
그래서 누군가 테스트를 쓰기 전까지 `pytest`는 테스트 0개를 보고한다.

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
  test_*.py            작성할 검증의 설명
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
- 응답 문자열의 형식은 아직 정하지 않았다. 예를 들어 없는 키에 `GET`을 하면 무엇을 돌려줄지 정해야 한다.
