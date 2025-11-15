from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from users.services.dto.logout_dto import LogoutDTO


def blacklist_refresh_token(data: LogoutDTO) -> None:
    """
    Помещает refresh-токен в blacklist, делая его недействительным.
    """
    try:
        token = RefreshToken(data["refresh"])  # type: ignore[arg-type]
        token.blacklist()
    except TokenError:
        # Уже недействителен
        pass
