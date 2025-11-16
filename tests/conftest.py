import pytest
from rest_framework.test import APIClient

from tests.users.factories import UserFactory
from users.api.tokens import generate_user_tokens


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def auth_client(user):
    client = APIClient()

    tokens = generate_user_tokens(user)
    access = tokens["access"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    return client
