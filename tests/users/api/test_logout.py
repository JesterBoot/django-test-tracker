from http import HTTPStatus

import pytest
from django.urls import reverse

from users.api.tokens import generate_user_tokens


@pytest.mark.django_db
def test_logout_blacklists_token(auth_client, user):
    tokens = generate_user_tokens(user)
    refresh = tokens["refresh"]

    url = reverse("auth-logout")
    payload = {"refresh": refresh}

    response = auth_client.post(url, payload, format="json")
    assert response.status_code == HTTPStatus.NO_CONTENT

    # refresh теперь невалидный
    refresh_url = reverse("auth-refresh")
    r = auth_client.post(refresh_url, {"refresh": refresh}, format="json")

    assert r.status_code == HTTPStatus.UNAUTHORIZED
    data = r.json()
    assert data["error"] == "invalid_refresh_token"


@pytest.mark.django_db
def test_logout_missing_refresh(auth_client):
    url = reverse("auth-logout")
    response = auth_client.post(url, {}, format="json")
    assert response.status_code == HTTPStatus.BAD_REQUEST
