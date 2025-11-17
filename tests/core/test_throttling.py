from types import SimpleNamespace

from core.throttling import RefreshTokenRateThrottle


class DummyView:
    pass


def test_refresh_throttle_returns_none_on_token_error(monkeypatch):
    throttle = RefreshTokenRateThrottle()

    class FakeRefreshToken:
        def __init__(self, value):
            raise Exception("fake_exception")

    monkeypatch.setattr("core.throttling.RefreshToken", FakeRefreshToken)

    request = SimpleNamespace(data={"refresh": "bad"})
    assert throttle.get_cache_key(request, DummyView()) is None
