from http import HTTPStatus
from uuid import uuid4

import pytest
from django.urls import reverse

from tests.users.factories import UserFactory
from users.selectors.user_list_selectors import select_users
from users.selectors.user_selectors import get_user_by_id
from users.services.user_logout import blacklist_refresh_token


@pytest.mark.django_db
def test_user_select_view_filters_and_limits(auth_client, user):
    matched = UserFactory(email="match@example.com")
    UserFactory(email="other@example.com")

    url = reverse("auth-users-select")
    response = auth_client.get(url, {"q": "match", "limit": "1"})
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == str(matched.id)

    response2 = auth_client.get(url, {"limit": "bad"})
    assert response2.status_code == HTTPStatus.OK
    expected_count = 2
    assert len(response2.json()) == expected_count


@pytest.mark.django_db
def test_select_users_helper_and_get_user_by_id(user):
    another = UserFactory(email="foo@example.com")
    results = list(select_users(q=None, limit=5, exclude_user_id=user.id))
    assert another in results
    assert user not in results

    assert get_user_by_id(user.id) == user
    assert get_user_by_id(another.id) == another
    assert get_user_by_id(uuid4()) is None


@pytest.mark.django_db
def test_user_str(user):
    assert str(user) == user.email


def test_blacklist_refresh_token_handles_invalid(monkeypatch):
    class FakeRefreshToken:
        def __init__(self, raw):
            from rest_framework_simplejwt.exceptions import TokenError  # noqa

            raise TokenError("bad token")

    monkeypatch.setattr("users.services.user_logout.RefreshToken", FakeRefreshToken)
    # Should not raise
    blacklist_refresh_token({"refresh": "broken"})
