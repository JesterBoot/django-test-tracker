from http import HTTPStatus

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_register_success(api_client):
    url = reverse("auth-register")
    payload = {
        "email": "new@example.com",
        "password": "123456",
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert "user_id" in data
    assert data["email"] == "new@example.com"
    assert "tokens" in data
    assert "access" in data["tokens"]
    assert "refresh" in data["tokens"]
