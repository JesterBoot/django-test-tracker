import pytest

from users.exceptions.user_exceptions import InvalidCredentialsError, UserAlreadyExistsError
from users.models import User
from users.services.user_services import authenticate_user, register_user


@pytest.mark.django_db
def test_register_user_duplicate():
    User.objects.create_user(email="x@example.com", password="123")

    with pytest.raises(UserAlreadyExistsError):
        register_user({"email": "x@example.com", "password": "123"})


@pytest.mark.django_db
def test_authenticate_user_wrong_password(user):
    with pytest.raises(InvalidCredentialsError):
        authenticate_user({"email": user.email, "password": "WRONGPASS"})


@pytest.mark.django_db
def test_authenticate_user_not_found():
    with pytest.raises(InvalidCredentialsError):
        authenticate_user({"email": "missing@example.com", "password": "123"})
