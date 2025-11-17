from http import HTTPStatus

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_login_success(api_client, user):
    url = reverse("auth-login")
    payload = {
        "email": user.email,
        "password": "password123",
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["email"] == user.email
    assert "tokens" in data
    assert "access" in data["tokens"]
    assert "refresh" in data["tokens"]


@pytest.mark.django_db
def test_login_throttle(api_client):
    url = reverse("auth-login")
    payload = {"email": "a@b.com", "password": "wrong"}

    for _ in range(5):
        response = api_client.post(url, payload, format="json")
        assert response.status_code in (200, 400, 401)

    blocked = api_client.post(url, payload, format="json")
    assert blocked.status_code == HTTPStatus.TOO_MANY_REQUESTS
