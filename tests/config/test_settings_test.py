from config import settings_test


def test_settings_test_overrides():
    assert (
        settings_test.CACHES["default"]["BACKEND"]
        == "django.core.cache.backends.locmem.LocMemCache"
    )
    assert settings_test.ENV == "test"
    assert settings_test.DEBUG is True
