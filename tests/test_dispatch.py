"""1단계 담당 전원. 대상: lwredis.dispatch.
작성할 검증: `SET a 1` → OK, `GET a` → 1, `DEL a` 후 `GET a` → 없음, 없는 명령 → 에러.
"""
