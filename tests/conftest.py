import pytest
from django.core.cache import cache
from rest_framework.test import APIClient

from tests.users.factories import UserFactory
from users.api.tokens import generate_user_tokens
from users.models import User


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def other_user():
    return UserFactory()


@pytest.fixture
def make_auth_client():
    def _make(user: User) -> APIClient:
        client = APIClient()
        tokens = generate_user_tokens(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        return client

    return _make


@pytest.fixture
def auth_client(user):
    client = APIClient()

    tokens = generate_user_tokens(user)
    access = tokens["access"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    return client


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
    yield
    cache.clear()
