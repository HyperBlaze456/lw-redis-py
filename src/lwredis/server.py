"""5단계 담당 전원: TCP 서버 모듈이다."""


def serve(host: str = "127.0.0.1", port: int = 6380) -> None:
    """TCP 접속을 받아 줄마다 execute를 호출하고 모든 접속이 하나의 Store를 공유한다."""
    raise NotImplementedError
