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
