from uuid import UUID

from users.models import User
from users.services.dto.me import MeResponseDTO


def get_user_by_email(email: str) -> User | None:
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None


def get_user_by_id(user_id: UUID) -> User | None:
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


def get_user_me_dto(user: User) -> MeResponseDTO:
    return MeResponseDTO(
        user_id=str(user.id),
        email=user.email,
    )
