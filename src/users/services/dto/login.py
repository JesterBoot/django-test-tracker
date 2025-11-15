from typing import TypedDict

from users.services.dto.tokens import TokenPairDTO


class LoginUserDTO(TypedDict):
    email: str
    password: str


class LoginUserResponseDTO(TypedDict):
    user_id: str
    email: str
    tokens: TokenPairDTO
