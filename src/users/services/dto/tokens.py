from typing import TypedDict


class TokenPairDTO(TypedDict):
    access: str
    refresh: str


class RefreshTokenDTO(TypedDict):
    refresh: str


class RefreshTokenResponseDTO(TypedDict):
    access: str
