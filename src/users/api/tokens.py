from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.services.dto.tokens import TokenPairDTO


def generate_user_tokens(user: User) -> TokenPairDTO:
    refresh = RefreshToken.for_user(user)

    return TokenPairDTO(
        access=str(refresh.access_token),
        refresh=str(refresh),
    )
