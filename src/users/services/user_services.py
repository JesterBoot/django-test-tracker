from django.db import transaction

from users.exceptions.user_exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
)
from users.models import User
from users.selectors.user_selectors import get_user_by_email
from users.services.dto.autenticate import AuthenticateUserDTO
from users.services.dto.register import RegisterUserDTO


@transaction.atomic
def register_user(data: RegisterUserDTO) -> User:
    email = data["email"]
    password = data["password"]

    existing = get_user_by_email(email)
    if existing is not None:
        raise UserAlreadyExistsError(f"User with email '{email}' already exists")

    return User.objects.create_user(email=email, password=password)


def authenticate_user(data: AuthenticateUserDTO) -> User | None:
    user = get_user_by_email(data["email"])
    if user is None:
        raise InvalidCredentialsError("Invalid email or password")

    if not user.check_password(data["password"]):
        raise InvalidCredentialsError("Invalid email or password")

    return user
