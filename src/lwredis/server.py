"""5단계 담당 전원: TCP 서버 모듈이다."""

import asyncio

from lwredis.aof import AOF, DEFAULT_PATH
from lwredis.store import Store

MAX_LINE = 16 * 1024 * 1024  # 명령 한 줄의 최대 크기(바이트)이다. 넘으면 그 접속을 끊는다.


def serve(
    host: str = "127.0.0.1",
    port: int = 6380,
    aof_path: str = DEFAULT_PATH,
    max_keys: int | None = None,
) -> None:
    """TCP 접속을 받아 줄마다 execute를 호출하고 모든 접속이 하나의 Store를 공유한다. 시작할 때 로그 파일을 재실행해 지난 내용을 되살린다.

    max_keys를 주면 키 개수가 그 한도를 넘을 때 가장 오래 쓰지 않은 키부터 지운다.
    """
    store, aof = Store(max_keys=max_keys), AOF(aof_path)
    aof.replay(store)

    async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """접속 하나를 맡아, 받은 줄마다 명령을 실행하고 응답 한 줄을 돌려보낸다."""
        async for raw in reader:
            writer.write((aof.run(store, raw.decode()) + "\n").encode())
            await writer.drain()
        writer.close()

    async def main() -> None:
        async with await asyncio.start_server(
            handle, host, port, limit=MAX_LINE
        ) as server:
            await server.serve_forever()

    asyncio.run(main())
