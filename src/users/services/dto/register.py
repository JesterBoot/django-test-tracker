from typing import TypedDict

from users.services.dto.tokens import TokenPairDTO


class RegisterUserDTO(TypedDict):
    email: str
    password: str


class RegisterUserResponseDTO(TypedDict):
    user_id: str
    email: str
    tokens: TokenPairDTO
