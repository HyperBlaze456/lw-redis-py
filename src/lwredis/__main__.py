"""`python -m lwredis`로 입력 루프를, `python -m lwredis serve [키 개수 한도]`로 TCP 서버를 실행하는 진입점이다."""

import sys

from lwredis.repl import main
from lwredis.server import serve

if __name__ == "__main__":
    if sys.argv[1:2] == ["serve"]:
        serve(max_keys=int(sys.argv[2]) if len(sys.argv) > 2 else None)
    else:
        main()
