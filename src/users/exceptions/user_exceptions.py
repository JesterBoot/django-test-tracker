class UserAlreadyExistsError(Exception):
    """Пользователь с таким email уже существует."""

    pass


class InvalidCredentialsError(Exception):
    """Переданы неверные email или пароль."""

    pass
