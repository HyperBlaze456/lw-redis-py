"""5단계 담당 전원. 대상: lwredis.server.
작성할 검증: 두 접속을 열어 한쪽에서 쓴 값을 다른 쪽에서 조회 (수동 확인은 `nc` 두 개).
"""

import socket


def test_two_connections_share_store(server_port):
    address = ("127.0.0.1", server_port)
    with socket.create_connection(address) as first, socket.create_connection(address) as second:
        reader1, reader2 = first.makefile("r"), second.makefile("r")
        first.sendall(b"SET a 1\n")
        assert reader1.readline().strip() == "OK"
        second.sendall(b"GET a\n")
        assert reader2.readline().strip() == "1"
