from http import HTTPStatus

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_me_success(auth_client, user):
    url = reverse("auth-me")

    response = auth_client.get(url)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["email"] == user.email
    assert data["user_id"] == str(user.id)
