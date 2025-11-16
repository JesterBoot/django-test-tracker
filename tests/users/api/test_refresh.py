from http import HTTPStatus

import pytest
from django.urls import reverse

from users.api.tokens import generate_user_tokens


MIN_ACCESS_TOKEN_LENGTH = 10


@pytest.mark.django_db
def test_refresh_success(api_client, user):
    refresh = generate_user_tokens(user)["refresh"]

    url = reverse("auth-refresh")
    payload = {"refresh": refresh}

    response = api_client.post(url, payload, format="json")

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "access" in data
    assert len(data["access"]) > MIN_ACCESS_TOKEN_LENGTH


def test_refresh_missing_token(api_client):
    url = reverse("auth-refresh")
    response = api_client.post(url, {}, format="json")
    assert response.status_code == HTTPStatus.BAD_REQUEST
