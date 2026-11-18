"""2~3단계의 무작위 테스트는 이 rng를 써서 실패가 재현되게 한다."""

import random

import pytest

SEED = 20261118


@pytest.fixture
def rng() -> random.Random:
    """고정한 시드로 만든 난수 생성기를 돌려준다."""
    return random.Random(SEED)
