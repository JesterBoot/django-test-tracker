from typing import TypedDict


class AuthenticateUserDTO(TypedDict):
    email: str
    password: str
